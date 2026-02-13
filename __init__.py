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


def _fetch_nsfw():
    """Initialize and fetch the nsfw_pack submodule."""
    try:
        subprocess.run(
            ["git", "submodule", "update", "--init", "--", "nsfw_pack"],
            cwd=_DIR, capture_output=True, timeout=60,
        )
        print("[KPPB] NSFW module fetched successfully.")
    except Exception as e:
        print(f"[KPPB] Warning: failed to fetch NSFW submodule: {e}")


def _clean_nsfw():
    """Deinit the nsfw_pack submodule and clean the directory."""
    try:
        subprocess.run(
            ["git", "submodule", "deinit", "-f", "--", "nsfw_pack"],
            cwd=_DIR, capture_output=True, timeout=30,
        )
        # Remove the working tree but keep the .git/modules entry
        # so re-enabling is fast (just re-init)
        import shutil
        if os.path.isdir(_NSFW_DIR):
            for item in os.listdir(_NSFW_DIR):
                path = os.path.join(_NSFW_DIR, item)
                if item == ".git":
                    continue
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
        print("[KPPB] NSFW module cleaned up.")
    except Exception as e:
        print(f"[KPPB] Warning: failed to clean NSFW submodule: {e}")


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
from .vlm_nodes import KPPBVLMRefiner

NODE_CLASS_MAPPINGS = {
    "KPPBPromptBuilder": KPPBPromptBuilder,
    "KPPBOutfitComposer": KPPBOutfitComposer,
    "KPPBImageEditComposer": KPPBImageEditComposer,
    "KPPBVLMRefiner": KPPBVLMRefiner,
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
    "KPPBVLMRefiner": "VLM Prompt Refiner (kppb)",
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
