"""
NSFW list nodes for XY Plot Queue compatibility.
Optional module — delete the nsfw_pack folder to remove these nodes.
"""

from ..list_nodes import _build_list_from_bools, _make_input_types


# ══════════════════════════════════════════════
# NSFW ACTION LIST (solo)
# ══════════════════════════════════════════════

NSFW_ACTION_ITEMS = sorted([
    "arching back in pleasure",
    "biting finger",
    "biting lip",
    "caressing inner thigh",
    "cupping breasts",
    "dripping wet from shower",
    "finger in mouth",
    "grabbing bedsheets",
    "grinding on pillow",
    "hands between legs",
    "holding vibrator",
    "licking finger",
    "licking lollipop",
    "looking over shoulder seductively",
    "moaning expression",
    "oil dripping on body",
    "peeling off shirt",
    "playing with waistband",
    "pulling down strap",
    "pulling hair back",
    "pulling panties aside",
    "rubbing lotion on legs",
    "running hands through hair",
    "sliding hand down body",
    "slowly undressing",
    "smearing lipstick",
    "spreading legs slowly",
    "squeezing breasts together",
    "stepping out of panties",
    "sucking finger",
    "touching neck sensually",
    "undoing bra clasp",
])


class KPPBNSFWActionList:
    """NSFW solo action list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = NSFW_ACTION_ITEMS

    @classmethod
    def INPUT_TYPES(cls):
        return _make_input_types(cls.ITEMS)

    RETURN_TYPES = ("LIST", "INT")
    RETURN_NAMES = ("list", "count")
    FUNCTION = "build_list"
    CATEGORY = "conditioning/klein"

    def build_list(self, custom_entries="", **kwargs):
        return _build_list_from_bools(self.ITEMS, custom_entries, **kwargs)


# ══════════════════════════════════════════════
# NSFW GROUP ACTION LIST (couples)
# ══════════════════════════════════════════════

NSFW_GROUP_ACTION_ITEMS = sorted([
    "being carried against wall",
    "being fingered",
    "being held down on bed",
    "being kissed on neck from behind",
    "being pinned against wall",
    "bent over receiving from behind",
    "blowjob on knees",
    "cowgirl riding",
    "deep throat",
    "doggy style",
    "face sitting on him",
    "giving handjob",
    "grabbed by hair from behind",
    "grinding on his lap",
    "hand around her throat",
    "hands tied while being taken",
    "him holding her legs up missionary",
    "him pulling her hair during doggy",
    "kissing passionately",
    "legs over his shoulders",
    "legs wrapped around him standing",
    "lying back receiving oral",
    "missionary",
    "on top reverse cowgirl",
    "pressed against glass",
    "prone bone",
    "receiving facial",
    "reverse cowgirl",
    "side by side spooning",
    "sitting on his face",
    "spread eagle for him",
    "standing carry position",
    "straddling his lap face to face",
    "sucking while looking up",
    "undressing each other",
])


class KPPBNSFWGroupActionList:
    """NSFW couples action list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = NSFW_GROUP_ACTION_ITEMS

    @classmethod
    def INPUT_TYPES(cls):
        return _make_input_types(cls.ITEMS)

    RETURN_TYPES = ("LIST", "INT")
    RETURN_NAMES = ("list", "count")
    FUNCTION = "build_list"
    CATEGORY = "conditioning/klein"

    def build_list(self, custom_entries="", **kwargs):
        return _build_list_from_bools(self.ITEMS, custom_entries, **kwargs)


# ══════════════════════════════════════════════
# NSFW POSE LIST
# ══════════════════════════════════════════════

NSFW_POSE_ITEMS = sorted([
    "arched back on all fours",
    "ass up face down",
    "back arched standing",
    "bent over",
    "bent over looking back",
    "chest pressed together arms",
    "hands and knees",
    "kneeling legs apart",
    "kneeling looking up",
    "legs open seated",
    "legs spread lying back",
    "legs up lying back",
    "lying face down hips raised",
    "lying on back knees bent",
    "lying on side leg raised",
    "on elbows and knees",
    "on knees back arched",
    "on knees hands on thighs",
    "one leg up against wall",
    "presenting from behind",
    "reclining legs parted",
    "riding position",
    "sitting legs open",
    "sitting spread eagle",
    "squatting legs apart",
    "standing bent at waist",
    "standing legs apart",
    "straddling",
    "stretching on bed",
    "topless covering with hands",
    "topless hair covering",
])


class KPPBNSFWPoseList:
    """NSFW pose list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = NSFW_POSE_ITEMS

    @classmethod
    def INPUT_TYPES(cls):
        return _make_input_types(cls.ITEMS)

    RETURN_TYPES = ("LIST", "INT")
    RETURN_NAMES = ("list", "count")
    FUNCTION = "build_list"
    CATEGORY = "conditioning/klein"

    def build_list(self, custom_entries="", **kwargs):
        return _build_list_from_bools(self.ITEMS, custom_entries, **kwargs)
