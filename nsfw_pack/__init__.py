"""
Optional NSFW module for KPPB.

Delete this entire nsfw_pack/ folder to remove all NSFW content.
The core prompt builder will continue to work with SFW content only.
"""

from .nsfw_data import (
    NSFW_POSE_EXPANSIONS,
    NSFW_ACTION_EXPANSIONS,
    NSFW_GROUP_ACTION_EXPANSIONS,
)
from .nsfw_list_nodes import (
    KPPBNSFWActionList,
    KPPBNSFWGroupActionList,
    KPPBNSFWPoseList,
)

__all__ = [
    "NSFW_POSE_EXPANSIONS",
    "NSFW_ACTION_EXPANSIONS",
    "NSFW_GROUP_ACTION_EXPANSIONS",
    "KPPBNSFWActionList",
    "KPPBNSFWGroupActionList",
    "KPPBNSFWPoseList",
]
