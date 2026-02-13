"""
List nodes with boolean toggles for ComfyLab-Pack XY Plot Queue compatibility.
Each outputs RETURN_TYPES = ('LIST', 'INT') for direct connection to dim1/dim2.
"""


def _build_list_from_bools(items, custom_entries="", **kwargs):
    """Collect toggled-on items + custom entries into a list."""
    result = []
    for item in items:
        if kwargs.get(item, False):
            result.append(item)
    if custom_entries and custom_entries.strip():
        for line in custom_entries.strip().split("\n"):
            line = line.strip()
            if line:
                result.append(line)
    return (result, len(result))


def _make_input_types(items):
    """Build INPUT_TYPES dict with a boolean per item + custom multiline."""
    inputs = {"required": {}}
    for item in items:
        inputs["required"][item] = ("BOOLEAN", {"default": False})
    inputs["required"]["custom_entries"] = (
        "STRING", {"multiline": True, "default": ""}
    )
    return inputs


# ══════════════════════════════════════════════
# SCENE LIST
# ══════════════════════════════════════════════

SCENE_ITEMS = sorted([
    "balcony",
    "bar/club",
    "bathroom",
    "beach",
    "bedroom",
    "cafe",
    "car",
    "gym",
    "hallway/corridor",
    "hotel room",
    "kitchen",
    "living room",
    "park",
    "pool",
    "rooftop",
    "stairwell",
    "studio",
    "urban street",
])


class KPPBSceneList:
    """IG scene/location list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = SCENE_ITEMS

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
# POSE LIST
# ══════════════════════════════════════════════

POSE_ITEMS = sorted([
    "adjusting collar",
    "adjusting jacket",
    "arms crossed",
    "back to camera",
    "chin on hand",
    "contrapposto",
    "crouching",
    "dance step",
    "fingers near lips",
    "from-behind candid",
    "hair flip",
    "hand on chest",
    "hand on hip",
    "hands behind head",
    "hands clasped behind back",
    "hands clasped front",
    "hands in pockets",
    "head tilt",
    "holding coffee",
    "holding phone",
    "kneeling",
    "laughing candid",
    "leaning against wall",
    "leaning in doorway",
    "leaning on counter",
    "leaning on railing",
    "leaning on table",
    "looking away",
    "lying on back",
    "lying on side",
    "lying on stomach elbows up",
    "mirror selfie pose",
    "one knee up seated",
    "one leg bent standing",
    "over the shoulder look",
    "peace sign",
    "profile",
    "reclining on sofa",
    "serious editorial",
    "sitting",
    "sitting couch lounge",
    "sitting cross-legged",
    "sitting on edge",
    "sitting on floor",
    "sitting on stairs",
    "small jump",
    "squatting",
    "standing",
    "standing both hands on hips",
    "stretch overhead",
    "texting",
    "three-quarter turn",
    "touching hair",
    "tucking hair behind ear",
    "twirl",
    "walking",
    "walking mid-step turn",
    "weight shifted",
])


class KPPBPoseList:
    """Curated IG pose list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = POSE_ITEMS

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
# SHOT TYPE LIST
# ══════════════════════════════════════════════

SHOT_TYPE_ITEMS = sorted([
    "candid mid-shot",
    "chest-up portrait",
    "close-up face",
    "cowboy shot",
    "environmental portrait",
    "extreme close-up",
    "from-behind candid",
    "full body",
    "headshot",
    "selfie arm-length",
    "silhouette framing",
    "three-quarter portrait",
    "upper body portrait",
    "waist-up portrait",
    "wide full-body",
])


class KPPBShotTypeList:
    """IG shot type / framing list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = SHOT_TYPE_ITEMS

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
# CAMERA ANGLE LIST
# ══════════════════════════════════════════════

CAMERA_ANGLE_ITEMS = sorted([
    "3/4 angle",
    "dutch angle",
    "eye level",
    "from below",
    "low-angle hero shot",
    "mirror selfie angle",
    "overhead selfie angle",
    "phone camera angle",
    "profile angle",
    "rear 3/4 angle",
    "slightly high angle",
    "slightly low angle",
])


class KPPBCameraAngleList:
    """IG camera angle list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = CAMERA_ANGLE_ITEMS

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
# LIGHTING LIST
# ══════════════════════════════════════════════

LIGHTING_ITEMS = sorted([
    "backlit sun flare",
    "blue hour",
    "candlelight",
    "direct flash",
    "dramatic side light",
    "golden hour",
    "harsh midday sun",
    "LED strip ambient",
    "natural window light",
    "neon/artificial",
    "overcast soft",
    "ring light",
    "screen/monitor glow",
    "softbox beauty",
    "studio rim light",
])


class KPPBLightingList:
    """Lighting setup list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = LIGHTING_ITEMS

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
# OUTFIT LIST (tops, bottoms, shoes combos)
# ══════════════════════════════════════════════

OUTFIT_ITEMS = sorted([
    "ankle boots and ripped jeans",
    "blazer and pencil skirt",
    "bodysuit and high-waisted jeans",
    "bomber jacket and biker shorts",
    "bralette and high-waisted shorts",
    "bustier and leather skirt",
    "corset top and mini skirt",
    "crop top and cargo pants",
    "crop top and high-waisted jeans",
    "crop top and mini skirt",
    "denim jacket and sundress",
    "graphic tee and joggers",
    "halter top and palazzo pants",
    "hoodie and leggings",
    "lace camisole and silk skirt",
    "leather jacket and jeans",
    "mesh top and leather pants",
    "off-shoulder top and skirt",
    "oversized blazer and shorts",
    "satin robe",
    "sheer blouse and slacks",
    "sports bra and yoga pants",
    "sundress",
    "sweater and mini skirt",
    "swimsuit",
    "tank top and denim shorts",
    "teddy lingerie",
    "tube top and maxi skirt",
    "turtleneck and leather skirt",
    "wrap dress",
])


class KPPBOutfitList:
    """Pre-composed outfit combination list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = OUTFIT_ITEMS

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
# IMAGE EDIT LIST
# ══════════════════════════════════════════════

IMAGE_EDIT_ITEMS = sorted([
    "Add bokeh background",
    "Add confetti falling",
    "Add fog and haze",
    "Add freckles",
    "Add gentle rain",
    "Add golden dust particles",
    "Add lens flare",
    "Add motion blur",
    "Add neon glow and reflections",
    "Add snow falling",
    "Add sparkles catching the light",
    "Add sunglasses",
    "Add tattoos on the arms",
    "Add wet reflective surfaces",
    "Change background to beach sunset",
    "Change background to city rooftop",
    "Change background to city skyline at night",
    "Change background to coffee shop",
    "Change background to neon-lit alley",
    "Change background to studio backdrop",
    "Change hair to black",
    "Change hair to blonde",
    "Change hair to pink",
    "Change hair to red",
    "Change lighting to golden hour",
    "Change lighting to neon",
    "Change season to autumn",
    "Change season to winter",
    "Change time to nighttime",
    "Change to overcast sky",
    "Remove background distractions",
    "Turn into cinematic film style",
    "Turn into vintage film style",
])


class KPPBImageEditList:
    """Pre-composed image edit instructions with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = IMAGE_EDIT_ITEMS

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
# HAIRSTYLE LIST
# ══════════════════════════════════════════════

HAIRSTYLE_ITEMS = sorted([
    "beach waves",
    "blunt bob",
    "box braids",
    "braided crown",
    "braided ponytail",
    "bun",
    "buzz cut",
    "cornrows",
    "curtain bangs",
    "double buns",
    "dutch braids",
    "fishtail braid",
    "french braid",
    "half up half down",
    "high ponytail",
    "hollywood waves",
    "layered",
    "long straight",
    "loose curls",
    "low bun",
    "low ponytail",
    "messy bun",
    "messy waves",
    "middle part straight",
    "pixie cut",
    "shag",
    "side part",
    "side swept",
    "slicked back",
    "space buns",
    "textured bob",
    "tight curls",
    "top knot",
    "wet look",
    "wolf cut",
])


class KPPBHairstyleList:
    """Hairstyle list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = HAIRSTYLE_ITEMS

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
# IG QUICK EFFECTS LIST
# ══════════════════════════════════════════════

IG_EFFECT_ITEMS = sorted([
    "Add beautiful circular bokeh lights in the background",
    "Add atmospheric fog and haze softening the background",
    "Add colorful confetti falling through the air",
    "Add colorful neon glow and reflections across the scene",
    "Add gentle rain falling throughout the scene with wet reflective surfaces",
    "Add glittering sparkles catching the light",
    "Add golden dust particles floating in the light",
    "Add softly falling snow with a cold winter atmosphere",
    "Add subtle motion blur suggesting movement and energy",
    "Add warm lens flare from the light source",
    "Add wet reflective surfaces with puddles catching the light",
    "Change the lighting to warm golden hour with long amber shadows",
    "Change the sky to soft overcast with even diffused lighting",
    "Change the time to nighttime with dark sky and artificial lighting",
])


class KPPBIGEffectList:
    """IG atmospheric effect list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = IG_EFFECT_ITEMS

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
# ACTION LIST (SFW)
# ══════════════════════════════════════════════

ACTION_ITEMS = sorted([
    "adjusting earring",
    "adjusting sunglasses",
    "applying lipstick",
    "blowing a kiss",
    "brushing hair",
    "checking phone",
    "drinking coffee",
    "drinking wine",
    "eating",
    "fixing hair in mirror",
    "holding bouquet",
    "holding shopping bags",
    "laughing at phone",
    "licking lips",
    "listening to music with earbuds",
    "looking in mirror",
    "opening gift box",
    "playing with necklace",
    "pouring drink",
    "putting on jacket",
    "putting on shoes",
    "reading book",
    "removing jacket",
    "scrolling phone on couch",
    "sipping through straw",
    "stretching after waking",
    "taking selfie",
    "tying shoelaces",
    "typing on laptop",
    "winking",
    "writing in journal",
    "zipping up dress",
])


class KPPBActionList:
    """SFW action list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = ACTION_ITEMS

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
# GROUP ACTION LIST (SFW)
# ══════════════════════════════════════════════

GROUP_ACTION_ITEMS = sorted([
    "arm around friend laughing",
    "cheers-ing drinks together",
    "dancing together at party",
    "feeding each other food",
    "group hug",
    "group selfie",
    "having brunch with friends",
    "having coffee with friend",
    "holding hands walking",
    "hugging friend",
    "karaoke with friends",
    "leaning on friend's shoulder",
    "linking arms walking",
    "piggyback ride",
    "playful pushing friend",
    "posing back to back",
    "sharing earbuds listening to music",
    "sharing umbrella",
    "shopping together",
    "sitting on boyfriend's lap",
    "slow dancing",
    "toasting champagne",
    "walking arm in arm",
    "whispering in ear",
])


class KPPBGroupActionList:
    """SFW group/couples action list with boolean toggles. Outputs LIST for XY Plot."""

    ITEMS = GROUP_ACTION_ITEMS

    @classmethod
    def INPUT_TYPES(cls):
        return _make_input_types(cls.ITEMS)

    RETURN_TYPES = ("LIST", "INT")
    RETURN_NAMES = ("list", "count")
    FUNCTION = "build_list"
    CATEGORY = "conditioning/klein"

    def build_list(self, custom_entries="", **kwargs):
        return _build_list_from_bools(self.ITEMS, custom_entries, **kwargs)


