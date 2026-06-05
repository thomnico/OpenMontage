"""Nano Banana — Google Gemini 2.5 Flash Image generation & editing.

"Nano Banana" is the nickname for Google's Gemini 2.5 Flash Image model, which
excels at multi-reference identity-consistent image editing (compositing real
faces into illustrated scenes, character consistency, instruction-following
edits). This tool wraps the Gemini generateContent API.

Text-to-image: prompt only.
Image edit / multi-reference: pass one or more local image paths; the model
keeps the identities/objects from the references while applying the prompt.
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


class NanoBanana(BaseTool):
    name = "nano_banana"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "image_generation"
    provider = "google_nano_banana"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []  # GOOGLE_API_KEY checked dynamically
    install_instructions = (
        "Set GOOGLE_API_KEY (or GEMINI_API_KEY) to your Google AI API key.\n"
        "  Get one at https://aistudio.google.com/apikey"
    )
    agent_skills = ["google-imagen"]

    capabilities = [
        "generate_image",
        "image_edit",
        "multi_reference_edit",
        "identity_consistent_edit",
    ]
    supports = {
        "image_edit": True,
        "multiple_reference_images": True,
        "identity_consistency": True,
        "text_to_image": True,
    }
    best_for = [
        "compositing real faces from photos into illustrated scenes",
        "identity-consistent multi-reference editing",
        "instruction-following image edits that preserve who/what is in the references",
    ]
    not_good_for = ["precise long text rendering in-image", "print-resolution output (upscale after)"]

    MODELS = {
        "gemini-2.5-flash-image": "gemini-2.5-flash-image",
        "gemini-3-pro-image": "gemini-3-pro-image",
        "gemini-3.1-flash-image": "gemini-3.1-flash-image",
    }

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "image_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Local reference images for edit / multi-reference mode",
            },
            "image_path": {"type": "string", "description": "Single local reference image"},
            "aspect_ratio": {
                "type": "string",
                "enum": ["1:1", "3:4", "4:3", "9:16", "16:9", "2:3", "3:2"],
                "description": "Output aspect ratio (Gemini imageConfig)",
            },
            "model": {
                "type": "string",
                "enum": list(MODELS.keys()),
                "default": "gemini-2.5-flash-image",
            },
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=200, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "image_path", "image_paths", "model"]
    side_effects = ["writes image file to output_path", "calls Google Gemini API (paid)"]
    user_visible_verification = ["Inspect generated image for identity fidelity and quality"]

    def _get_api_key(self) -> str | None:
        return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE if self._get_api_key() else ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        # Gemini 2.5 Flash Image bills per output image (~$0.039). Flat estimate.
        return 0.04

    def _inline_image(self, path: Path) -> dict[str, Any]:
        mime = mimetypes.guess_type(str(path))[0] or "image/png"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return {"inline_data": {"mime_type": mime, "data": data}}

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(success=False, error="No Google API key found. " + self.install_instructions)

        import requests

        start = time.time()
        model = inputs.get("model", "gemini-2.5-flash-image")
        prompt = inputs["prompt"]

        # Collect reference images (single or multiple)
        refs: list[str] = []
        if inputs.get("image_path"):
            refs.append(inputs["image_path"])
        refs.extend(inputs.get("image_paths") or [])

        parts: list[dict[str, Any]] = [{"text": prompt}]
        for r in refs:
            p = Path(r)
            if not p.exists():
                return ToolResult(success=False, error=f"Reference image not found: {p}")
            parts.append(self._inline_image(p))

        output_path = Path(inputs.get("output_path", "nano_banana_image.png"))
        output_path.parent.mkdir(parents=True, exist_ok=True)

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            f"?key={api_key}"
        )
        payload: dict[str, Any] = {"contents": [{"parts": parts}]}
        if inputs.get("aspect_ratio"):
            payload["generationConfig"] = {
                "imageConfig": {"aspectRatio": inputs["aspect_ratio"]}
            }

        try:
            resp = requests.post(url, json=payload, timeout=180)
            resp.raise_for_status()
            data = resp.json()

            img_b64 = None
            for cand in data.get("candidates", []):
                for part in cand.get("content", {}).get("parts", []):
                    inline = part.get("inline_data") or part.get("inlineData")
                    if inline and inline.get("data"):
                        img_b64 = inline["data"]
                        break
                if img_b64:
                    break
            if not img_b64:
                return ToolResult(success=False, error=f"No image in Gemini response: {str(data)[:400]}")

            output_path.write_bytes(base64.b64decode(img_b64))

        except Exception as e:
            return ToolResult(success=False, error=f"Nano Banana generation failed: {e}")

        return ToolResult(
            success=True,
            data={
                "provider": "google_nano_banana",
                "model": model,
                "prompt": prompt,
                "references": refs,
                "output": str(output_path),
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model=model,
        )
