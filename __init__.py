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

# ── Optional NSFW module ──
# Delete the nsfw_pack/ folder to remove all NSFW nodes.
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
    pass
