"""
VLM Prompt Refiner node for KPPB.
One-shot VLM compose: the vision model sees reference images + scene settings
and writes a complete Klein 9B generation prompt in a single call.
Direct HTTP calls to Ollama REST API — no external custom node dependencies.
"""

import json
import base64
import io
import re
import urllib.request
import urllib.error
import numpy as np
from PIL import Image as PILImage

from .nodes import IDENTITY_LOCK_PROMPT


# ──────────────────────────────────────────────
# Ollama API helpers
# ──────────────────────────────────────────────

# Browser-like User-Agent — required for RunPod/Cloudflare proxied endpoints
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

def _tensor_to_base64(image_tensor):
    """Convert a single ComfyUI IMAGE frame [H, W, C] float32 0-1 to base64 PNG."""
    img_np = (image_tensor.cpu().numpy() * 255).clip(0, 255).astype(np.uint8)
    pil_img = PILImage.fromarray(img_np)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def _strip_think_blocks(text):
    """Remove <think>...</think> blocks from Qwen3 reasoning output."""
    return re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL).strip()


def _extract_from_thinking(thinking):
    """When the model dumps everything into thinking and produces no content,
    try to extract the last composed prompt from the thinking field.
    Looks for the last substantial quoted string (likely the final draft)."""
    # Find all quoted strings longer than 50 chars (skip short fragments)
    quotes = re.findall(r'"([^"]{50,})"', thinking)
    if quotes:
        # Return the last one — the model's final draft
        result = quotes[-1].strip()
        # Clean up degeneration artifacts (repeated words)
        result = re.sub(r'\b(\w+)( \1){3,}\b', r'\1', result)
        return result
    return ""


def _ollama_chat(url, model, messages, temperature=0.3,
                 seed=-1, think=False, label="", format=None):
    """Send a chat completion request to Ollama and return the response text."""
    endpoint = f"{url.rstrip('/')}/api/chat"

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": think,
        "options": {
            "temperature": temperature,
            "num_predict": -1,
            "repeat_penalty": 1.3,
        },
    }
    if format is not None:
        payload["format"] = format
    if seed >= 0:
        payload["options"]["seed"] = seed

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": _UA},
        method="POST",
    )

    tag = f"[KPPB:{label}]" if label else "[KPPB]"

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))

            # ── Token stats ──
            prompt_tokens = result.get("prompt_eval_count", "N/A")
            eval_tokens = result.get("eval_count", "N/A")
            done_reason = result.get("done_reason", "N/A")
            total_dur = result.get("total_duration", 0)
            dur_sec = total_dur / 1e9 if total_dur else 0
            print(f"{tag} ── Ollama stats ──")
            print(f"{tag}   think={think}, done_reason={done_reason}")
            print(f"{tag}   prompt_tokens={prompt_tokens}, eval_tokens={eval_tokens}")
            print(f"{tag}   duration={dur_sec:.1f}s")

            # ── Thinking content (separate field in Ollama for Qwen3) ──
            thinking = result.get("message", {}).get("thinking", "")
            if thinking:
                print(f"{tag} ── THINKING ({len(thinking)} chars) ──")
                print(f"{tag} {thinking}")
                print(f"{tag} ── END THINKING ──")

            # ── Response content ──
            raw_content = result["message"]["content"]
            print(f"{tag} ── RAW CONTENT ({len(raw_content)} chars) ──")
            print(f"{tag} {raw_content}")
            print(f"{tag} ── END RAW CONTENT ──")

            # Strip any inline <think> blocks that end up in content
            content = _strip_think_blocks(raw_content).strip()
            if content != raw_content.strip():
                print(f"{tag} (stripped inline think blocks, {len(content)} chars remaining)")

            # ── Fallback: extract from thinking if content is empty ──
            if not content and thinking:
                extracted = _extract_from_thinking(thinking)
                if extracted:
                    print(f"{tag} ── Content empty, extracted {len(extracted)} chars from thinking ──")
                    print(f"{tag} {extracted[:300]}")
                    return extracted

            return content
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if e.code == 524:
            raise RuntimeError(
                f"Cloudflare timeout (HTTP 524) from {url}.\n"
                f"The model '{model}' is likely too large for the GPU and "
                f"Ollama is offloading to CPU, causing slow inference.\n"
                f"Try a smaller quantization (e.g. q4_K_M instead of q8_0)."
            ) from e
        if "not found" in body.lower() or e.code == 404:
            raise RuntimeError(
                f"Model '{model}' not found in Ollama.\n"
                f"Pull it first:  ollama pull {model}"
            ) from e
        raise RuntimeError(f"Ollama HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise ConnectionError(
            f"Cannot connect to Ollama at {url}. "
            f"Make sure Ollama is running ('ollama serve').\n"
            f"Error: {e}"
        ) from e
    except KeyError as e:
        raise RuntimeError(
            f"Unexpected Ollama response format: {result}"
        ) from e


def _check_ollama(url):
    """Quick health check — is Ollama running?"""
    try:
        req = urllib.request.Request(f"{url.rstrip('/')}/api/tags", method="GET",
                                     headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return True
    except Exception:
        return False


def _model_exists(url, model):
    """Check if a model is already available locally in Ollama."""
    try:
        endpoint = f"{url.rstrip('/')}/api/tags"
        req = urllib.request.Request(endpoint, method="GET",
                                     headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            local_models = [m.get("name", "") for m in data.get("models", [])]
            for local in local_models:
                if local == model or local == f"{model}:latest":
                    return True
                if ":" not in model and local.split(":")[0] == model:
                    return True
            return False
    except Exception:
        return False


def _pull_model(url, model):
    """Pull a model from Ollama registry. Streams progress to console."""
    import sys
    endpoint = f"{url.rstrip('/')}/api/pull"
    payload = json.dumps({"name": model, "stream": True}).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": _UA},
        method="POST",
    )

    print(f"[KPPB] Model '{model}' not found locally. Pulling from Ollama registry...")
    sys.stdout.flush()

    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            last_status = ""
            for line in resp:
                line = line.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError:
                    continue

                status = chunk.get("status", "")
                if "error" in chunk:
                    raise RuntimeError(
                        f"Ollama pull failed for '{model}': {chunk['error']}"
                    )

                if status != last_status:
                    if "completed" in chunk and "total" in chunk:
                        total = chunk["total"]
                        completed = chunk["completed"]
                        if total > 0:
                            pct = completed / total * 100
                            size_gb = total / 1e9
                            print(f"[KPPB] {status}: {pct:.0f}% of {size_gb:.1f}GB")
                        else:
                            print(f"[KPPB] {status}")
                    else:
                        print(f"[KPPB] {status}")
                    sys.stdout.flush()
                    last_status = status

        print(f"[KPPB] Model '{model}' pulled successfully.")
        sys.stdout.flush()
        return True

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Failed to pull model '{model}' from Ollama.\n"
            f"HTTP {e.code}: {body}\n"
            f"You can try manually: ollama pull {model}"
        ) from e
    except urllib.error.URLError as e:
        raise ConnectionError(
            f"Cannot connect to Ollama at {url} for model pull.\n"
            f"Make sure Ollama is running ('ollama serve').\n"
            f"Error: {e}"
        ) from e


def _unload_model(url, model):
    """Unload model from VRAM by sending keep_alive=0."""
    endpoint = f"{url.rstrip('/')}/api/chat"
    payload = json.dumps({
        "model": model,
        "messages": [],
        "keep_alive": 0,
    }).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": _UA},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp.read()
        print(f"[KPPB] Model '{model}' unloaded from VRAM.")
    except Exception as e:
        print(f"[KPPB] Warning: failed to unload model: {e}")


def _ensure_model(url, model):
    """Check if model exists, pull if not. Called before each inference."""
    if not _check_ollama(url):
        raise ConnectionError(
            f"Ollama is not running at {url}.\n"
            f"Start it with: ollama serve"
        )
    if not _model_exists(url, model):
        _pull_model(url, model)


# ──────────────────────────────────────────────
# VLM system prompt — one-shot compose
# ──────────────────────────────────────────────

VLM_SYSTEM = """\
You write image generation prompts for FLUX Klein 9B. You see reference images \
and receive scene settings as JSON. Output ONLY the prompt — no reasoning, \
no thinking, no explanations, no labels, no markdown.

CRITICAL IDENTITY RULE — NEVER describe the character's physical appearance. \
Do NOT extract or mention face shape, eye color, skin tone, body type, \
height, weight, bust size, or any physical features from the reference image. \
The character's identity is preserved through the reference latent, not text. \
Text descriptions of appearance CONFLICT with the reference and cause drift.

Your prompt MUST begin with:
"[photo_style] photo of the character from the reference image"

Then compose the REST of the prompt using ONLY the settings JSON fields. \
Do NOT describe anything from the reference image — no clothing, no scene, \
no environment, no accessories. ALL of that comes from settings.

EXPOSURE: The JSON contains an "exposure" field with a pre-composed \
sentence. Include this text VERBATIM right after the outfit description. \
Do NOT contradict it or add nudity beyond what it allows.

Write the remaining fields as natural flowing prose in this order:
1. hairstyle and hair_color (if non-empty, override reference hair)
2. pose
3. action — what the subject is actively doing
4. outfit, then the "exposure" field VERBATIM
5. scene_type and environment — FROM SETTINGS ONLY, never from reference
6. extra_details
7. lighting_setup and lighting_custom — be vivid, this matters most for Klein
8. shot_type, camera_angle, lens, depth_of_field
9. mood and color_grading

Skip any field that is empty. Do not skip non-empty fields. \
NEVER repeat or describe the same element twice."""

# Caption-only: describe everything as-is
VLM_SYSTEM_CAPTION = """\
You write image generation prompts for FLUX Klein 9B. Describe everything \
visible in the image as one concise paragraph of natural flowing prose. \
Include face, hair, body, clothing, environment, and lighting. \
Output ONLY the prompt — no reasoning, no labels, no markdown."""

# Edit mode: describe final result after edits
VLM_SYSTEM_EDIT = """\
You write image generation prompts for FLUX Klein 9B. You can see reference images \
and receive edit instructions from the user. Output ONLY the prompt — no reasoning, \
no thinking, no explanations, no labels, no markdown.

From the reference image, extract the person's PHYSICAL IDENTITY: face, eyes, \
skin tone, hair, build, distinguishing marks.

Describe the FINAL scene after the requested edits as one concise paragraph. \
Do NOT say "edit" or "change" — describe the result as if it already exists."""


# ──────────────────────────────────────────────
# Prose system prompts (used by Claude Code path)
# ──────────────────────────────────────────────

PROSE_SYSTEM = """\
Respond ONLY with the final prompt text. No reasoning, no thinking, no explanations.

You compose photorealistic prompts for FLUX Klein 9B. You receive reference images \
and the user's DESIRED SETTINGS for the new scene.

NEVER describe the character's physical appearance — no face, eyes, skin, body \
descriptions. Identity is preserved through the reference latent, not text. \
Text descriptions cause identity drift.

Start with "photo of the character from the reference image" then compose \
the scene using ONLY the user's desired settings:
1. Pose and action
2. Outfit
3. Environment/scene
4. Lighting — be specific and vivid
5. Camera/lens/angle if provided

Output ONLY the prompt. No labels, no markdown, no quotes."""

PROSE_SYSTEM_EDIT = """\
Respond ONLY with the final prompt text. No reasoning, no thinking, no explanations.

You compose image-edit prompts for FLUX Klein 9B. You receive reference images \
and EDIT INSTRUCTIONS describing what should change.

Preserve the character's physical identity unless the edit instructions change it. \
Describe the FINAL scene after edits as one concise paragraph. \
Do NOT use words like "edit", "change", "replace" — describe the result directly.

Output ONLY the prompt. No labels, no markdown, no quotes."""

PROSE_SYSTEM_CAPTION = """\
Respond ONLY with the final prompt text. No reasoning, no thinking, no explanations.

Describe Image 1 as one concise paragraph of flowing prose optimized for \
FLUX Klein 9B image generation. Front-load facial and physical details.

Output ONLY the prompt. No labels, no markdown, no quotes."""


# ──────────────────────────────────────────────
# Dataset generation prompt (nanobanana → Qwen 2512 LoRA training)
# ──────────────────────────────────────────────

PROSE_SYSTEM_DATASET = """\
You generate structured JSON for a character LoRA training dataset pipeline.

You receive a reference image of the subject and scene parameters as JSON.
A separate image generation model (nanobanana / Gemini) will use the "prompt" \
field to generate a photorealistic training image. The "caption" field becomes \
the .txt caption paired with that image for LoRA training.

─── OUTPUT FORMAT ───
Respond with ONLY a JSON object. No reasoning, no markdown, no code fences.

{
  "prompt": "<scene description for image generation>",
  "caption": "<LoRA training caption>"
}

─── PROMPT FIELD RULES ───
Write a pure SCENE DESCRIPTION — NOT an instruction. The image generator \
receives this as a text prompt alongside the reference image.

DO: "A photorealistic photo of the woman from the reference, standing..."
DON'T: "Generate a photorealistic photo..." (causes the model to reason \
about the task instead of generating)

CRITICAL IDENTITY RULES:
- NEVER describe the subject's eye color, face shape, skin tone, hair color \
(unless settings explicitly override hair). Describing physical features \
causes the generator to OVERRIDE the reference and invent new features.
- The reference image is the SOLE source of identity. Your text describes \
only the SCENE, not the PERSON.

Structure the prompt as one flowing paragraph:
1. Opening: "A photorealistic photo of the woman from the reference"
2. Pose/action from settings
3. Outfit from settings
4. Environment/scene — be specific with atmosphere
5. Lighting — vivid and cinematic, this drives realism
6. Camera framing, lens, depth of field
7. Mood and color grading
8. Closing (include VERBATIM): "Maintain identical facial structure, bone \
structure, exact eye color, eye shape, nose, lips, jawline, skin tone, \
body type, body proportions, breast size and shape, and all identifying \
marks from the reference."

─── CAPTION FIELD RULES ───
A 1-3 sentence natural-language caption for the .txt file:
- Start with: [trigger]
- Describe ONLY what varies: pose, outfit, lighting, background, expression, \
camera framing, mood
- NEVER describe permanent physical features (face, eyes, skin, body type) — \
the model learns these from images tied to the trigger word
- Use clear flowing prose, concise and focused

─── EXAMPLE OUTPUT ───
{
  "prompt": "A photorealistic photo of the woman from the reference, \
standing with one hand on hip wearing a white oversized t-shirt and \
denim shorts. Set in a cozy cafe with warm wood tones and soft ambient \
lighting. Golden hour sunlight streams through a large window casting \
warm amber tones and gentle shadows across the scene. Waist-up portrait \
framed at 85mm with shallow depth of field softly blurring the background. \
Casual relaxed mood with natural warm color grading. Maintain identical \
facial structure, bone structure, exact eye color, eye shape, nose, lips, \
jawline, skin tone, body type, body proportions, breast size and shape, \
and all identifying marks from the reference.",
  "caption": "[trigger], standing with one hand on hip wearing a white \
oversized t-shirt and denim shorts, golden hour sunlight streaming through \
a cafe window, warm amber tones, waist-up portrait shot at 85mm with \
shallow depth of field."
}"""


# ──────────────────────────────────────────────
# Claude Code helper
# ──────────────────────────────────────────────

CLAUDE_MODELS = [
    "opus",
    "sonnet",
    "haiku",
]


def _find_claude():
    """Find claude binary, checking common install locations beyond PATH.
    Works on macOS, Linux, and Windows."""
    import os
    import shutil
    import sys
    from pathlib import Path

    # Try PATH first (handles most cases where PATH is complete)
    found = shutil.which("claude")
    if found:
        return found

    home = Path.home()
    is_win = sys.platform == "win32"

    if is_win:
        # Windows: npm global installs to %APPDATA%\npm
        appdata = os.environ.get("APPDATA", "")
        localappdata = os.environ.get("LOCALAPPDATA", "")
        candidates = []
        if appdata:
            candidates.append(Path(appdata) / "npm" / "claude.cmd")
        if localappdata:
            candidates.append(Path(localappdata) / "Programs" / "claude" / "claude.exe")
            candidates.append(Path(localappdata) / "fnm_multishells" / "claude.cmd")
        candidates.append(home / ".local" / "bin" / "claude.cmd")
        candidates.append(home / ".local" / "bin" / "claude.exe")
    else:
        # macOS / Linux
        candidates = [
            home / ".local" / "bin" / "claude",
            home / ".npm-global" / "bin" / "claude",
            Path("/usr/local/bin/claude"),
            Path("/opt/homebrew/bin/claude"),
        ]

    for path in candidates:
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
    return None


def _claude_code_available():
    """Check if Claude Code CLI is installed."""
    return _find_claude() is not None


def _claude_code_chat(system_prompt, user_prompt, model="sonnet", images_b64=None):
    """Call Claude Code CLI. Supports text and image inputs. Returns response text."""
    import os
    import subprocess
    import tempfile

    claude_path = _find_claude()
    if not claude_path:
        raise RuntimeError(
            "Claude Code CLI not found. Install it or disable 'use_claude_code'.\n"
            "Install: npm install -g @anthropic-ai/claude-code"
        )

    # If images provided, save as temp files and reference in prompt
    temp_files = []
    image_prompt_parts = []
    if images_b64:
        for i, img_b64 in enumerate(images_b64):
            labels = ["CHARACTER REFERENCE", "SCENE REFERENCE", "PROP/PRODUCT REFERENCE"]
            label = labels[i] if i < len(labels) else f"IMAGE {i+1}"
            tf = tempfile.NamedTemporaryFile(suffix=".png", delete=False, prefix=f"kppb_img{i}_")
            tf.write(base64.b64decode(img_b64))
            tf.close()
            temp_files.append(tf.name)
            image_prompt_parts.append(f"[Image {i+1} ({label}): {tf.name}]")

    full_prompt = ""
    if image_prompt_parts:
        full_prompt += "\n".join(image_prompt_parts) + "\n\n"
    full_prompt += user_prompt

    cmd = [
        claude_path,
        "-p", full_prompt,
        "--append-system-prompt", system_prompt,
        "--model", model,
        "--output-format", "text",
        "--max-turns", "1",
        "--dangerously-skip-permissions",
    ]

    print(f"[KPPB:CLAUDE] Calling Claude Code CLI (model={model}, images={len(images_b64 or [])})...")
    print(f"[KPPB:CLAUDE] Prompt: {full_prompt[:400]}...")

    # Clean env: remove CLAUDECODE to avoid nested-session block,
    # and ensure PATH includes common binary locations
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            stdin=subprocess.DEVNULL,
            env=env,
        )

        if result.returncode != 0:
            stderr = result.stderr.strip()
            print(f"[KPPB:CLAUDE] CLI error (code {result.returncode}): {stderr[:500]}")
            raise RuntimeError(f"Claude Code CLI failed: {stderr[:300]}")

        content = result.stdout.strip()
        print(f"[KPPB:CLAUDE] ── RESPONSE ({len(content)} chars) ──")
        print(f"[KPPB:CLAUDE] {content[:500]}")
        print(f"[KPPB:CLAUDE] ── END RESPONSE ──")
        return content

    except subprocess.TimeoutExpired:
        raise RuntimeError("Claude Code CLI timed out after 300s")
    except FileNotFoundError:
        raise RuntimeError("Claude Code CLI not found on PATH")
    finally:
        for tf in temp_files:
            try:
                os.unlink(tf)
            except OSError:
                pass


# ──────────────────────────────────────────────
# Dataset JSON parser
# ──────────────────────────────────────────────

def _parse_dataset_json(text, trigger_word="ohwx"):
    """Parse structured dataset output (JSON or delimiter fallback).
    Returns (gen_prompt, caption) or (None, None) if parsing fails."""
    text = text.strip()

    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()

    # Try JSON first
    try:
        data = json.loads(text)
        gen_prompt = data.get("prompt", "").strip()
        caption = data.get("caption", "").strip()
        if gen_prompt:
            caption = caption.replace("[trigger]", trigger_word)
            if not gen_prompt.endswith("."):
                gen_prompt += "."
            if caption and not caption.endswith("."):
                caption += "."
            return (gen_prompt, caption)
    except (json.JSONDecodeError, TypeError, AttributeError):
        pass

    # Fallback: try ---CAPTION--- delimiter (backwards compat)
    if "---CAPTION---" in text:
        parts = text.split("---CAPTION---", 1)
        gen_prompt = parts[0].strip()
        caption = parts[1].strip()
        caption = caption.replace("[trigger]", trigger_word)
        if gen_prompt and not gen_prompt.endswith("."):
            gen_prompt += "."
        if caption and not caption.endswith("."):
            caption += "."
        return (gen_prompt, caption)

    return (None, None)


# ──────────────────────────────────────────────
# Filename helper
# ──────────────────────────────────────────────

def _make_filename_prefix(prompt_json="", mode=""):
    """Build a descriptive filename prefix from scene settings JSON."""
    parts = []
    if prompt_json and prompt_json.strip():
        try:
            data = json.loads(prompt_json)
        except (json.JSONDecodeError, TypeError):
            data = {}
        # Pick the most descriptive fields
        for key in ("shot_type", "pose", "scene_type", "lighting_setup", "photo_style"):
            val = data.get(key, "")
            if val and val != "as in reference":
                parts.append(val)
    if not parts:
        parts.append(mode.replace(" ", "_") if mode else "img")
    # Sanitize: lowercase, replace spaces/slashes with underscores, strip non-alnum
    slug = "_".join(parts)
    slug = re.sub(r"[^a-z0-9]+", "_", slug.lower()).strip("_")
    # Truncate to reasonable length
    if len(slug) > 80:
        slug = slug[:80].rstrip("_")
    return slug


# ──────────────────────────────────────────────
# Modes
# ──────────────────────────────────────────────

REFINER_MODES = [
    "describe & enhance",
    "image edit aware",
    "caption only",
    "dataset generation",
]


# ══════════════════════════════════════════════
# VLM PROMPT REFINER NODE
# ══════════════════════════════════════════════

class KPPBVLMRefiner:
    """One-shot VLM prompt composer for Klein 9B. The VLM sees the reference
    images directly and composes a complete generation prompt by merging
    the character's physical identity with the user's scene settings."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character_ref": ("IMAGE", {"tooltip": "Character reference image — identity/likeness is extracted from this"}),
                "ollama_url": ("STRING", {"default": "http://localhost:11434"}),
                "model": ("STRING", {"default": "huihui_ai/qwen3-vl-abliterated:32b-instruct-q8_0"}),
                "mode": (REFINER_MODES, {"default": "describe & enhance"}),
            },
            "optional": {
                "scene_ref": ("IMAGE", {"tooltip": "Additional reference for scene, pose, lighting, or outfit"}),
                "prop_ref": ("IMAGE", {"tooltip": "Product/prop reference — handbag, sunglasses, sponsored item, etc."}),
                "positive_prompt": ("STRING", {"default": "", "forceInput": True,
                                               "tooltip": "Connect from Prompt Builder's positive_prompt — used as fallback if VLM returns empty"}),
                "prompt_json": ("STRING", {"default": "", "forceInput": True,
                                           "tooltip": "Connect from Prompt Builder's prompt_json output"}),
                "edit_prompt": ("STRING", {"default": "", "forceInput": True,
                                           "tooltip": "Connect from Image Edit Composer's edit_prompt output"}),
                "system_prompt": ("STRING", {"multiline": True, "default": "",
                                             "placeholder": "Override Claude Code system prompt (leave empty for auto)"}),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 2.0, "step": 0.05,
                                          "tooltip": "Lower = more focused, higher = more creative"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647,
                                 "tooltip": "-1 for random, or set for reproducible output"}),
                "preserve_identity": ("BOOLEAN", {"default": True,
                                                  "tooltip": "Append identity lock phrase to reinforce likeness preservation for the diffusion model"}),
                "unload_model": ("BOOLEAN", {"default": True,
                                             "tooltip": "Unload Ollama LLM from VRAM after inference. Turn ON for localhost (frees VRAM for Klein). Turn OFF for remote/RunPod (avoids slow reload between iterations)"}),
                "use_claude_code": ("BOOLEAN", {"default": False,
                                                "tooltip": "Use Claude Code CLI instead of Ollama — does both stages in one shot with images"}),
                "claude_model": (CLAUDE_MODELS, {"default": "opus",
                                                  "tooltip": "Claude model to use (sonnet recommended for speed/quality balance)"}),
                "trigger_word": ("STRING", {"default": "ohwx",
                                            "tooltip": "Trigger word for LoRA training captions (dataset generation mode only)"}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("refined_prompt", "image_caption", "filename_prefix")
    FUNCTION = "refine"
    CATEGORY = "conditioning/klein"

    def refine(
        self,
        character_ref,
        ollama_url,
        model,
        mode,
        scene_ref=None,
        prop_ref=None,
        positive_prompt="",
        prompt_json="",
        edit_prompt="",
        system_prompt="",
        preserve_identity=True,
        temperature=0.3,
        seed=-1,
        unload_model=True,
        use_claude_code=False,
        claude_model="opus",
        trigger_word="ohwx",
    ):
        # ── Encode all images to base64 (needed by both paths) ──
        images_b64 = []
        if character_ref.dim() == 4:
            images_b64.append(_tensor_to_base64(character_ref[0]))
        else:
            images_b64.append(_tensor_to_base64(character_ref))

        has_scene = scene_ref is not None
        has_prop = prop_ref is not None

        if has_scene:
            if scene_ref.dim() == 4:
                images_b64.append(_tensor_to_base64(scene_ref[0]))
            else:
                images_b64.append(_tensor_to_base64(scene_ref))

        if has_prop:
            if prop_ref.dim() == 4:
                images_b64.append(_tensor_to_base64(prop_ref[0]))
            else:
                images_b64.append(_tensor_to_base64(prop_ref))

        # ════════════════════════════════════════
        # CLAUDE CODE PATH — one-shot with images
        # ════════════════════════════════════════
        if use_claude_code:
            print(f"[KPPB] ═══ CLAUDE CODE MODE ═══")
            print(f"[KPPB] model={claude_model}, images={len(images_b64)}, mode={mode}")

            # Select system prompt
            if system_prompt and system_prompt.strip():
                claude_sys = system_prompt.strip()
            elif mode == "describe & enhance":
                claude_sys = PROSE_SYSTEM
            elif mode == "image edit aware":
                claude_sys = PROSE_SYSTEM_EDIT
            elif mode == "dataset generation":
                claude_sys = PROSE_SYSTEM_DATASET
            else:
                claude_sys = PROSE_SYSTEM_CAPTION

            # Build user prompt with image labels
            image_labels = []
            image_labels.append("Image 1 is the CHARACTER REFERENCE (identity source).")
            if has_scene:
                image_labels.append(f"Image {len(image_labels)+1} is the SCENE REFERENCE (environment, lighting, pose).")
            if has_prop:
                image_labels.append(f"Image {len(image_labels)+1} is a PROP/PRODUCT REFERENCE (describe it precisely).")

            parts = ["\n".join(image_labels)]

            if mode == "describe & enhance":
                if prompt_json and prompt_json.strip():
                    parts.append(f"DESIRED SETTINGS:\n```json\n{prompt_json.strip()}\n```")
                parts.append(
                    "Analyze the images. Use Image 1 for identity, then merge with "
                    "the settings to write a single optimized prompt as one concise paragraph."
                )
            elif mode == "image edit aware":
                if prompt_json and prompt_json.strip():
                    parts.append(f"SCENE SETTINGS:\n```json\n{prompt_json.strip()}\n```")
                if edit_prompt and edit_prompt.strip():
                    parts.append(f"EDIT INSTRUCTIONS:\n{edit_prompt.strip()}")
                parts.append(
                    "Write a prompt describing the FINAL scene after edits, "
                    "preserving the character's identity from Image 1."
                )
            elif mode == "dataset generation":
                if prompt_json and prompt_json.strip():
                    parts.append(f"SCENE SETTINGS:\n```json\n{prompt_json.strip()}\n```")
                parts.append(f"TRIGGER WORD: {trigger_word}")
                parts.append(
                    "Generate the nanobanana prompt and LoRA training caption. "
                    "Use [trigger] as placeholder in the caption — it will be "
                    "replaced with the trigger word automatically."
                )
            else:
                parts.append(
                    "Describe Image 1 as an optimized Klein 9B generation prompt in one concise paragraph."
                )

            claude_user_msg = "\n\n".join(parts)

            result = _claude_code_chat(
                claude_sys, claude_user_msg,
                model=claude_model,
                images_b64=images_b64,
            )

            # Clean up
            result = _strip_think_blocks(result).strip()
            if result.startswith('"') and result.endswith('"'):
                result = result[1:-1]
            if result.startswith("```"):
                lines = result.split("\n")
                lines = [l for l in lines if not l.strip().startswith("```")]
                result = "\n".join(lines).strip()

            if not result or result.strip() == "":
                if positive_prompt and positive_prompt.strip():
                    result = positive_prompt.strip()
                    print(f"[KPPB] Claude returned empty — passing through positive_prompt")
                else:
                    result = "photorealistic portrait."

            # ── Dataset generation: parse JSON with prompt + caption ──
            if mode == "dataset generation":
                gen_prompt, caption = _parse_dataset_json(result, trigger_word)
                if gen_prompt:
                    fname = _make_filename_prefix(prompt_json, mode)
                    print(f"[KPPB] ═══ DATASET OUTPUT ═══")
                    print(f"[KPPB] Generation prompt ({len(gen_prompt)} chars): {gen_prompt[:300]}")
                    print(f"[KPPB] Training caption ({len(caption)} chars): {caption[:300]}")
                    print(f"[KPPB] Filename prefix: {fname}")
                    return (gen_prompt, caption, fname)

            if result and not result.endswith("."):
                result += "."

            # ── Append identity lock phrase ──
            if preserve_identity:
                result = result.rstrip(". ") + ". " + IDENTITY_LOCK_PROMPT + "."

            fname = _make_filename_prefix(prompt_json, mode)
            print(f"[KPPB] ═══ FINAL OUTPUT ({len(result)} chars) ═══")
            print(f"[KPPB] {result[:500]}")
            # Claude mode returns same for both outputs (no separate caption stage)
            return (result, result, fname)

        # ════════════════════════════════════════
        # OLLAMA PATH — one-shot VLM compose
        # ════════════════════════════════════════
        _ensure_model(ollama_url, model)

        print(f"[KPPB] ═══ VLM ONE-SHOT ═══")
        print(f"[KPPB] mode={mode}, scene={has_scene}, prop={has_prop}, model={model}")

        # ── Select system prompt by mode ──
        is_dataset = mode == "dataset generation"
        if system_prompt and system_prompt.strip():
            sys_prompt = system_prompt.strip()
        elif mode == "describe & enhance":
            sys_prompt = VLM_SYSTEM
        elif mode == "image edit aware":
            sys_prompt = VLM_SYSTEM_EDIT
        elif is_dataset:
            sys_prompt = PROSE_SYSTEM_DATASET
        else:
            sys_prompt = VLM_SYSTEM_CAPTION

        # ── Build user message with settings ──
        parts = []

        # Image context labels
        img_labels = ["Image 1 is the CHARACTER REFERENCE."]
        if has_scene:
            img_labels.append(f"Image {len(img_labels)+1} is a SCENE REFERENCE.")
        if has_prop:
            img_labels.append(f"Image {len(img_labels)+1} is a PROP/PRODUCT REFERENCE.")
        parts.append(" ".join(img_labels))

        if mode == "describe & enhance":
            if prompt_json and prompt_json.strip():
                parts.append(f"SCENE SETTINGS:\n{prompt_json.strip()}")
            elif positive_prompt and positive_prompt.strip():
                parts.append(f"SCENE DESCRIPTION:\n{positive_prompt.strip()}")
            parts.append("Write the Klein 9B prompt now.")

        elif mode == "image edit aware":
            if edit_prompt and edit_prompt.strip():
                parts.append(f"EDIT INSTRUCTIONS:\n{edit_prompt.strip()}")
            if prompt_json and prompt_json.strip():
                parts.append(f"SCENE SETTINGS:\n{prompt_json.strip()}")
            parts.append("Write the Klein 9B prompt describing the final result.")

        elif is_dataset:
            if prompt_json and prompt_json.strip():
                parts.append(f"SCENE SETTINGS:\n{prompt_json.strip()}")
            parts.append(f"TRIGGER WORD: {trigger_word}")
            parts.append(
                "Generate the JSON with prompt and caption fields. "
                "Use [trigger] as placeholder in the caption."
            )

        else:  # caption only
            parts.append("Write the Klein 9B prompt describing this image.")

        user_msg = "/nothink\n\n" + "\n\n".join(parts)
        print(f"[KPPB] User message:\n{user_msg[:400]}...")

        vlm_messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_msg, "images": images_b64},
        ]

        result = _ollama_chat(
            ollama_url, model, vlm_messages,
            temperature=temperature,
            seed=seed,
            think=False,
            label="VLM",
            format="json" if is_dataset else None,
        )

        # ── Unload model from VRAM if requested ──
        if unload_model:
            _unload_model(ollama_url, model)

        # ── Clean up result ──
        result = _strip_think_blocks(result).strip() if result else ""
        if result.startswith('"') and result.endswith('"'):
            result = result[1:-1]
        if result.startswith("```"):
            lines = result.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            result = "\n".join(lines).strip()

        # ── Dataset mode: parse JSON ──
        if is_dataset:
            gen_prompt, caption = _parse_dataset_json(result, trigger_word)
            if gen_prompt:
                fname = _make_filename_prefix(prompt_json, mode)
                print(f"[KPPB] ═══ DATASET OUTPUT ═══")
                print(f"[KPPB] Generation prompt ({len(gen_prompt)} chars): {gen_prompt[:300]}")
                print(f"[KPPB] Training caption ({len(caption)} chars): {caption[:300]}")
                print(f"[KPPB] Filename prefix: {fname}")
                return (gen_prompt, caption, fname)
            # Fallback if JSON parse failed
            print(f"[KPPB] Warning: dataset JSON parse failed, using raw output")

        if result and not result.endswith("."):
            result += "."

        # ── Fallback ──
        if not result or result == ".":
            if positive_prompt and positive_prompt.strip():
                result = positive_prompt.strip()
                print(f"[KPPB] VLM returned empty — passing through positive_prompt ({len(result)} chars)")
            else:
                result = "photorealistic portrait."
                print(f"[KPPB] VLM returned empty — using minimal fallback")

        # ── Append identity lock phrase ──
        if preserve_identity:
            result = result.rstrip(". ") + ". " + IDENTITY_LOCK_PROMPT + "."

        fname = _make_filename_prefix(prompt_json, mode)
        print(f"[KPPB] ═══ FINAL OUTPUT ({len(result)} chars) ═══")
        print(f"[KPPB] {result[:500]}")

        return (result, result, fname)
