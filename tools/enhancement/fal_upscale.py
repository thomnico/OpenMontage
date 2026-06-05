"""AI image upscaling via fal.ai (cloud, paid).

Provides a network-based alternative to the local Real-ESRGAN `upscale` tool.
Uploads a local image to fal.ai as a base64 data URI, runs a creative/clarity
upscaler, downloads the result. No GPU required on-device — useful for print
resolution (e.g. A3 @300 DPI) when no local GPU is available.

Default model: fal-ai/clarity-upscaler (detail-preserving, good for
illustration/painterly content).
"""

from __future__ import annotations

import base64
import mimetypes
import os
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


class FalUpscale(BaseTool):
    name = "fal_upscale"
    version = "0.1.0"
    tier = ToolTier.ENHANCE
    capability = "enhancement"
    provider = "fal"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.SEEDED
    runtime = ToolRuntime.API

    dependencies = []  # FAL_KEY checked dynamically in get_status()
    install_instructions = (
        "Set FAL_KEY to your fal.ai API key.\n"
        "  Get one at https://fal.ai/dashboard/keys"
    )
    agent_skills = ["bfl-api"]

    capabilities = ["image_upscale", "creative_upscale", "print_resolution"]
    supports = {
        "scale": True,
        "creativity": True,
        "cloud": True,
        "no_gpu_required": True,
    }
    best_for = [
        "print-resolution upscaling (A3/A2 @300 DPI) without a local GPU",
        "detail-preserving enlargement of illustrations and painterly images",
        "cloud upscaling when local Real-ESRGAN is unavailable",
    ]
    not_good_for = ["offline use", "video upscaling"]

    # fal.ai upscaler endpoints. clarity-upscaler is the detail-preserving default.
    MODELS = {
        "clarity-upscaler": "fal-ai/clarity-upscaler",
        "esrgan": "fal-ai/esrgan",
    }

    input_schema = {
        "type": "object",
        "required": ["input_path"],
        "properties": {
            "input_path": {"type": "string", "description": "Local source image path"},
            "output_path": {"type": "string"},
            "scale": {
                "type": "integer",
                "enum": [2, 4],
                "default": 2,
                "description": "Upscale factor",
            },
            "model": {
                "type": "string",
                "enum": list(MODELS.keys()),
                "default": "clarity-upscaler",
            },
            "creativity": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
                "default": 0.35,
                "description": "How much new detail the model may invent "
                "(clarity-upscaler only). Lower = faithful, higher = more invented detail.",
            },
            "prompt": {
                "type": "string",
                "default": "",
                "description": "Optional guidance prompt for clarity-upscaler",
            },
            "timeout_seconds": {
                "type": "integer",
                "default": 900,
                "description": "Max total wait for the async queue job to finish",
            },
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=500, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["input_path", "scale", "model", "creativity", "prompt"]
    side_effects = ["uploads image to fal.ai", "writes upscaled file to output_path", "calls fal.ai API (paid)"]
    user_visible_verification = [
        "Compare upscaled output with original for added detail and artifacts",
        "Verify faces and text remain faithful at high creativity values",
    ]

    # ------------------------------------------------------------------
    # Status / cost
    # ------------------------------------------------------------------

    def _get_api_key(self) -> str | None:
        return os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_API_KEY")

    def get_status(self) -> ToolStatus:
        if self._get_api_key():
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        # clarity-upscaler bills roughly per megapixel of output; a single
        # A3-scale run is a few cents. Use a conservative flat estimate.
        return 0.05

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def _to_data_uri(self, path: Path) -> str:
        mime = mimetypes.guess_type(str(path))[0] or "image/png"
        b64 = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{b64}"

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(
                success=False,
                error="No fal.ai API key found. " + self.install_instructions,
            )

        input_path = Path(inputs["input_path"])
        if not input_path.exists():
            return ToolResult(success=False, error=f"Input not found: {input_path}")

        import requests

        start = time.time()
        model_key = inputs.get("model", "clarity-upscaler")
        endpoint = self.MODELS.get(model_key, self.MODELS["clarity-upscaler"])
        scale = inputs.get("scale", 2)

        default_output = str(input_path.with_stem(f"{input_path.stem}_upscaled"))
        output_path = Path(inputs.get("output_path", default_output))
        output_path.parent.mkdir(parents=True, exist_ok=True)

        payload: dict[str, Any] = {
            "image_url": self._to_data_uri(input_path),
            "upscale_factor": scale,
        }
        if model_key == "clarity-upscaler":
            payload["creativity"] = inputs.get("creativity", 0.35)
            if inputs.get("prompt"):
                payload["prompt"] = inputs["prompt"]

        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        }
        # Upscalers can take minutes — use the fal.ai async queue, not the
        # synchronous fal.run endpoint (which times out around 5 min).
        deadline = start + inputs.get("timeout_seconds", 900)

        try:
            submit = requests.post(
                f"https://queue.fal.run/{endpoint}",
                headers=headers, json=payload, timeout=60,
            )
            submit.raise_for_status()
            job = submit.json()
            status_url = job.get("status_url")
            response_url = job.get("response_url")
            if not status_url or not response_url:
                return ToolResult(success=False, error=f"No queue URLs in fal response: {job}")

            # Poll until completed or deadline
            while True:
                if time.time() > deadline:
                    return ToolResult(success=False, error="FAL upscale timed out waiting in queue")
                st = requests.get(status_url, headers=headers, timeout=30)
                st.raise_for_status()
                status = st.json().get("status")
                if status == "COMPLETED":
                    break
                if status in ("FAILED", "ERROR", "CANCELLED"):
                    return ToolResult(success=False, error=f"FAL job {status}: {st.json()}")
                time.sleep(3)

            result = requests.get(response_url, headers=headers, timeout=60)
            result.raise_for_status()
            data = result.json()

            # fal upscalers return either {"image": {"url": ...}} or {"images": [{"url": ...}]}
            image_url = None
            if isinstance(data.get("image"), dict):
                image_url = data["image"].get("url")
            elif data.get("images"):
                image_url = data["images"][0].get("url")
            if not image_url:
                return ToolResult(success=False, error=f"No image in fal response: {data}")

            image_response = requests.get(image_url, timeout=120)
            image_response.raise_for_status()
            output_path.write_bytes(image_response.content)

        except Exception as e:
            return ToolResult(success=False, error=f"FAL upscale failed: {e}")

        return ToolResult(
            success=True,
            data={
                "provider": "fal",
                "model": endpoint,
                "input": str(input_path),
                "output": str(output_path),
                "scale": scale,
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model=endpoint,
        )
