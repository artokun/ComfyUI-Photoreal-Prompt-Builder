import json
import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
_NSFW_DIR = os.path.join(_DIR, "nsfw_pack")
_CONFIG_PATH = os.path.join(_DIR, "config.json")


def _load_config():
    """Load config.json, return defaults if missing or malformed."""
    try:
        with open(_CONFIG_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"nsfw": False}


def _nsfw_populated():
    """Check if nsfw_pack/ has Python files (not just .git metadata)."""
    if not os.path.isdir(_NSFW_DIR):
        return False
    return any(f.endswith(".py") for f in os.listdir(_NSFW_DIR))


_NSFW_REPO = "https://github.com/artokun/ComfyUI-Photoreal-Prompt-Builder-NSFW.git"


def _is_git_repo():
    """Check if the node pack was installed as a git repo (clone) vs zip."""
    return os.path.isdir(os.path.join(_DIR, ".git"))


def _fetch_nsfw():
    """Fetch the nsfw_pack module. Uses git submodule if available,
    otherwise falls back to a direct clone (for zip/tarball installs)."""
    try:
        if _is_git_repo():
            # Git clone install — use submodule
            subprocess.run(
                ["git", "submodule", "update", "--init", "--", "nsfw_pack"],
                cwd=_DIR, capture_output=True, timeout=60,
            )
        else:
            # Zip/tarball install (ComfyUI Manager) — direct clone into nsfw_pack/
            import shutil
            if os.path.isdir(_NSFW_DIR):
                shutil.rmtree(_NSFW_DIR)
            subprocess.run(
                ["git", "clone", _NSFW_REPO, "nsfw_pack"],
                cwd=_DIR, capture_output=True, timeout=60,
            )
        if _nsfw_populated():
            print("[KPPB] NSFW module fetched successfully.")
        else:
            print("[KPPB] Warning: NSFW fetch completed but no Python files found.")
    except Exception as e:
        print(f"[KPPB] Warning: failed to fetch NSFW module: {e}")


def _clean_nsfw():
    """Remove nsfw_pack contents. Handles both git submodule and direct clone."""
    try:
        import shutil
        if _is_git_repo():
            subprocess.run(
                ["git", "submodule", "deinit", "-f", "--", "nsfw_pack"],
                cwd=_DIR, capture_output=True, timeout=30,
            )
        if os.path.isdir(_NSFW_DIR):
            shutil.rmtree(_NSFW_DIR)
            os.makedirs(_NSFW_DIR, exist_ok=True)
        print("[KPPB] NSFW module cleaned up.")
    except Exception as e:
        print(f"[KPPB] Warning: failed to clean NSFW module: {e}")


# ── Config-driven NSFW submodule management ──
_config = _load_config()
_nsfw_enabled = _config.get("nsfw", False)

if _nsfw_enabled and not _nsfw_populated():
    print("[KPPB] NSFW enabled in config.json but module not found. Fetching...")
    _fetch_nsfw()
elif not _nsfw_enabled and _nsfw_populated():
    print("[KPPB] NSFW disabled in config.json. Cleaning up module...")
    _clean_nsfw()

# ── Core node imports ──
from .nodes import KPPBPromptBuilder, KPPBOutfitComposer, KPPBImageEditComposer
from .list_nodes import (
    KPPBSceneList,
    KPPBPoseList,
    KPPBShotTypeList,
    KPPBCameraAngleList,
    KPPBLightingList,
    KPPBOutfitList,
    KPPBImageEditList,
    KPPBIGEffectList,
    KPPBHairstyleList,
    KPPBActionList,
    KPPBGroupActionList,
)
try:
    from .vlm_nodes import KPPBVLMRefiner
    _vlm_available = True
except ImportError:
    _vlm_available = False
    print("[KPPB] Warning: VLM Refiner unavailable (missing numpy/Pillow).")

NODE_CLASS_MAPPINGS = {
    "KPPBPromptBuilder": KPPBPromptBuilder,
    "KPPBOutfitComposer": KPPBOutfitComposer,
    "KPPBImageEditComposer": KPPBImageEditComposer,
    "KPPBSceneList": KPPBSceneList,
    "KPPBPoseList": KPPBPoseList,
    "KPPBShotTypeList": KPPBShotTypeList,
    "KPPBCameraAngleList": KPPBCameraAngleList,
    "KPPBLightingList": KPPBLightingList,
    "KPPBOutfitList": KPPBOutfitList,
    "KPPBImageEditList": KPPBImageEditList,
    "KPPBIGEffectList": KPPBIGEffectList,
    "KPPBHairstyleList": KPPBHairstyleList,
    "KPPBActionList": KPPBActionList,
    "KPPBGroupActionList": KPPBGroupActionList,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KPPBPromptBuilder": "Prompt Builder (kppb)",
    "KPPBOutfitComposer": "Outfit Composer (kppb)",
    "KPPBImageEditComposer": "Image Edit Composer (kppb)",
    "KPPBSceneList": "Scene List (kppb)",
    "KPPBPoseList": "Pose List (kppb)",
    "KPPBShotTypeList": "Shot Type List (kppb)",
    "KPPBCameraAngleList": "Camera Angle List (kppb)",
    "KPPBLightingList": "Lighting List (kppb)",
    "KPPBOutfitList": "Outfit List (kppb)",
    "KPPBImageEditList": "Image Edit List (kppb)",
    "KPPBIGEffectList": "IG Effect List (kppb)",
    "KPPBHairstyleList": "Hairstyle List (kppb)",
    "KPPBActionList": "Action List (kppb)",
    "KPPBGroupActionList": "Group Action List (kppb)",
}

# ── Optional VLM module (requires numpy + Pillow) ──
if _vlm_available:
    NODE_CLASS_MAPPINGS["KPPBVLMRefiner"] = KPPBVLMRefiner
    NODE_DISPLAY_NAME_MAPPINGS["KPPBVLMRefiner"] = "VLM Prompt Refiner (kppb)"

# ── Optional NSFW module (loaded only when enabled + populated) ──
if _nsfw_enabled:
    try:
        from .nsfw_pack import (
            KPPBNSFWActionList,
            KPPBNSFWGroupActionList,
            KPPBNSFWPoseList,
        )

        NODE_CLASS_MAPPINGS.update({
            "KPPBNSFWActionList": KPPBNSFWActionList,
            "KPPBNSFWGroupActionList": KPPBNSFWGroupActionList,
            "KPPBNSFWPoseList": KPPBNSFWPoseList,
        })

        NODE_DISPLAY_NAME_MAPPINGS.update({
            "KPPBNSFWActionList": "NSFW Action List (kppb)",
            "KPPBNSFWGroupActionList": "NSFW Group Action List (kppb)",
            "KPPBNSFWPoseList": "NSFW Pose List (kppb)",
        })
    except ImportError:
        print("[KPPB] Warning: NSFW enabled but module failed to load.")
