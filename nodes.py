import json
import os
import random

# ── NSFW config ──
_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(_DIR, "config.json"), "r") as _f:
        _NSFW_ENABLED = json.load(_f).get("nsfw", False)
except (FileNotFoundError, json.JSONDecodeError):
    _NSFW_ENABLED = False

# ──────────────────────────────────────────────
# Identity preservation phrase (appended when
# character reference image is being used)
# ──────────────────────────────────────────────
IDENTITY_LOCK_PROMPT = (
    "Maintain exact likeness, identical facial structure, bone structure, "
    "eye shape, eye color, nose, lips, jawline, skin tone, breast size "
    "and shape, body proportions, and all identifying marks from the "
    "character reference"
)

# ──────────────────────────────────────────────
# "as in reference" default for all dropdowns
# ──────────────────────────────────────────────
_REF = "as in reference"
_RND = "random"


def _resolve_random(value, options):
    """If value is 'random', pick a random concrete option (skip ref/random/custom)."""
    if value != _RND:
        return value
    concrete = [v for v in options if v not in (_REF, _RND, "custom")]
    return random.choice(concrete) if concrete else _REF


# ──────────────────────────────────────────────
# Lighting presets with rich prose expansions
# ──────────────────────────────────────────────
LIGHTING_EXPANSIONS = {
    _REF: "",
    _RND: "",
    "ring light": "even ring light illumination with circular catchlights in the eyes and minimal shadows",
    "softbox beauty": "professional softbox beauty lighting with soft wrap-around illumination and flattering skin tones",
    "natural window light": "soft natural light streaming through a window, creating gentle gradients from light to shadow",
    "golden hour": "warm golden hour sunlight with long shadows and rich amber tones",
    "blue hour": "cool blue hour twilight with deep indigo sky and soft diffused ambient light",
    "neon/artificial": "vibrant neon and artificial light casting colorful reflections and electric atmosphere",
    "direct flash": "direct on-camera flash with harsh shadows and high contrast pop",
    "overcast soft": "soft overcast daylight creating even, shadowless illumination with gentle tonal gradations",
    "backlit sun flare": "backlit sun flare with the subject haloed in warm luminous light and lens flare",
    "LED strip ambient": "colorful LED strip ambient light casting soft gradients of color across the scene",
    "screen/monitor glow": "cool screen glow illuminating the face with soft bluish-white light in a dim room",
    "harsh midday sun": "harsh midday sun with strong overhead shadows and high contrast",
    "studio rim light": "dramatic studio rim light separating the subject from the background with a luminous edge",
    "dramatic side light": "strong directional side light carving deep shadows and bright highlights",
    "candlelight": "warm flickering candlelight casting intimate orange glow and dancing soft shadows",
    "custom": "",
}

# ──────────────────────────────────────────────
# IG-focused scene/location types
# ──────────────────────────────────────────────
SCENE_TYPES = [
    _REF,
    _RND,
    "bedroom",
    "bathroom",
    "living room",
    "kitchen",
    "hotel room",
    "urban street",
    "cafe",
    "bar/club",
    "rooftop",
    "beach",
    "pool",
    "park",
    "gym",
    "studio",
    "balcony",
    "car",
    "stairwell",
    "hallway/corridor",
]

# ──────────────────────────────────────────────
# IG-focused shot types / framing
# ──────────────────────────────────────────────
SHOT_TYPES = [
    _REF,
    _RND,
    "extreme close-up",
    "close-up face",
    "headshot",
    "upper body portrait",
    "chest-up portrait",
    "waist-up portrait",
    "three-quarter portrait",
    "cowboy shot",
    "full body",
    "wide full-body",
    "selfie arm-length",
    "environmental portrait",
    "candid mid-shot",
    "from-behind candid",
    "silhouette framing",
]

# ──────────────────────────────────────────────
# IG-focused camera angles
# ──────────────────────────────────────────────
CAMERA_ANGLES = [
    _REF,
    _RND,
    "eye level",
    "slightly low angle",
    "slightly high angle",
    "3/4 angle",
    "profile angle",
    "mirror selfie angle",
    "phone camera angle",
    "dutch angle",
    "low-angle hero shot",
    "overhead selfie angle",
    "from below",
    "rear 3/4 angle",
]

# ──────────────────────────────────────────────
# Lenses
# ──────────────────────────────────────────────
LENSES = [
    _REF,
    _RND,
    "24mm wide",
    "35mm",
    "50mm",
    "85mm portrait",
    "105mm",
    "135mm",
    "iPhone front camera",
    "iPhone rear camera",
]

# ──────────────────────────────────────────────
# Depth of field
# ──────────────────────────────────────────────
DEPTH_OF_FIELD = [
    _REF,
    _RND,
    "razor thin f/1.4",
    "shallow f/2.0",
    "shallow f/2.8",
    "moderate f/4",
    "standard f/5.6",
    "sharp f/8",
]

# ──────────────────────────────────────────────
# IG-focused photo styles / vibes
# ──────────────────────────────────────────────
PHOTO_STYLES = [
    _REF,
    _RND,
    "phone candid",
    "mirror selfie",
    "editorial",
    "lifestyle",
    "fashion",
    "cinematic",
    "film grain",
    "flash photography",
    "golden hour aesthetic",
    "neon night",
    "studio clean",
    "vintage retro",
    "street style",
    "paparazzi",
    "documentary candid",
]

# ──────────────────────────────────────────────
# IG-focused poses
# ──────────────────────────────────────────────
POSES = [
    _REF,
    _RND,
    "standing",
    "standing hand on hip",
    "standing both hands on hips",
    "standing arms crossed",
    "standing hands in pockets",
    "standing contrapposto",
    "standing one leg bent",
    "walking",
    "walking mid-step turn",
    "sitting",
    "sitting cross-legged",
    "sitting one knee up",
    "sitting on edge",
    "sitting couch lounge",
    "sitting on floor",
    "sitting on stairs",
    "leaning against wall",
    "leaning on railing",
    "leaning in doorway",
    "leaning on table",
    "crouching",
    "squatting",
    "kneeling",
    "reclining on sofa",
    "lying on side",
    "lying on back",
    "lying on stomach elbows up",
    "over the shoulder look",
    "back to camera",
    "three-quarter turn",
    "profile",
    "head tilt",
    "looking away",
    "hair flip",
    "touching hair",
    "tucking hair behind ear",
    "hand on chest",
    "chin on hand",
    "fingers near lips",
    "adjusting collar",
    "adjusting jacket",
    "mirror selfie pose",
    "holding phone",
    "texting",
    "holding coffee",
    "peace sign",
    "laughing candid",
    "serious editorial",
    "twirl",
    "dance step",
    "small jump",
    "stretch overhead",
    "yoga warrior pose",
]

# ──────────────────────────────────────────────
# Hairstyles
# ──────────────────────────────────────────────
HAIR_COLORS = [
    "as in reference",
    _RND,
    "ash blonde",
    "auburn",
    "black",
    "bleach blonde",
    "blue",
    "brunette",
    "caramel",
    "chestnut",
    "copper",
    "dark brown",
    "dirty blonde",
    "ginger",
    "golden blonde",
    "gray",
    "green",
    "honey blonde",
    "jet black",
    "lavender",
    "light brown",
    "medium brown",
    "ombre",
    "pastel pink",
    "pink",
    "platinum blonde",
    "red",
    "silver",
    "strawberry blonde",
    "two-tone",
    "white",
]

HAIRSTYLES = [
    "as in reference",
    _RND,
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
]

# ──────────────────────────────────────────────
# Color grading
# ──────────────────────────────────────────────
COLOR_GRADINGS = [
    _REF,
    _RND,
    "natural",
    "warm golden",
    "cool blue",
    "cinematic teal-orange",
    "muted desaturated",
    "vibrant",
    "film noir",
    "vintage kodak",
    "fuji velvia",
    "faded film",
    "high contrast",
    "pastel soft",
]

LIGHTING_SETUPS = list(LIGHTING_EXPANSIONS.keys())

# ──────────────────────────────────────────────
# NSFW expansion dicts (optional — loaded from
# nsfw_pack if present, empty dicts otherwise)
# ──────────────────────────────────────────────
try:
    from .nsfw_pack.nsfw_data import (
        NSFW_POSE_EXPANSIONS,
        NSFW_ACTION_EXPANSIONS,
        NSFW_GROUP_ACTION_EXPANSIONS,
    )
except ImportError:
    NSFW_POSE_EXPANSIONS = {}
    NSFW_ACTION_EXPANSIONS = {}
    NSFW_GROUP_ACTION_EXPANSIONS = {}


# ══════════════════════════════════════════════
# MAIN PROMPT BUILDER
# ══════════════════════════════════════════════
class KPPBPromptBuilder:
    """IG-focused photorealistic prompt builder for FLUX.2 Klein 9B."""

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "subject": ("STRING", {"multiline": True, "default": ""}),
                "pose": (POSES, {"default": _REF}),
                "action": ("STRING", {"multiline": True, "default": ""}),
                "scene_type": (SCENE_TYPES, {"default": _REF}),
                "shot_type": (SHOT_TYPES, {"default": _REF}),
                "camera_angle": (CAMERA_ANGLES, {"default": _REF}),
                "lighting_setup": (LIGHTING_SETUPS, {"default": _REF}),
                "photo_style": (PHOTO_STYLES, {"default": _REF}),
                "lens": (LENSES, {"default": _REF}),
                "depth_of_field": (DEPTH_OF_FIELD, {"default": _REF}),
                "color_grading": (COLOR_GRADINGS, {"default": _REF}),
                "hairstyle": (HAIRSTYLES, {"default": "as in reference"}),
                "hair_color": (HAIR_COLORS, {"default": "as in reference"}),
                "preserve_identity": ("BOOLEAN", {"default": True,
                                                  "tooltip": "Append identity lock phrase for character reference consistency"}),
            },
            "optional": {
                "outfit": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "edit_instructions": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "environment": ("STRING", {"multiline": True, "default": ""}),
                "lighting_custom": ("STRING", {"default": ""}),
                "mood": ("STRING", {"default": ""}),
                "extra_details": ("STRING", {"multiline": True, "default": ""}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
            },
        }
        if _NSFW_ENABLED:
            inputs["optional"]["expose_breasts"] = ("BOOLEAN", {"default": False,
                "tooltip": "ON: clothing adjusted to reveal breasts. OFF: nipples always concealed by fabric, hands, or hair"})
            inputs["optional"]["remove_bra"] = ("BOOLEAN", {"default": False,
                "tooltip": "No bra under clothing"})
            inputs["optional"]["remove_panties"] = ("BOOLEAN", {"default": False,
                "tooltip": "No panties/underwear — only visible if pose or camera angle reveals it"})
        return inputs

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt", "prompt_json")
    FUNCTION = "build_prompt"
    CATEGORY = "conditioning/klein"

    def build_prompt(
        self,
        subject,
        pose,
        scene_type,
        shot_type,
        camera_angle,
        lighting_setup,
        photo_style,
        lens,
        depth_of_field,
        color_grading,
        action="",
        hairstyle="as in reference",
        hair_color="as in reference",
        preserve_identity=True,
        outfit="",
        edit_instructions="",
        environment="",
        lighting_custom="",
        mood="",
        extra_details="",
        negative_prompt="",
        expose_breasts=False,
        remove_bra=False,
        remove_panties=False,
    ):
        # ── Resolve "random" selections ──
        pose = _resolve_random(pose, POSES)
        scene_type = _resolve_random(scene_type, SCENE_TYPES)
        shot_type = _resolve_random(shot_type, SHOT_TYPES)
        camera_angle = _resolve_random(camera_angle, CAMERA_ANGLES)
        lighting_setup = _resolve_random(lighting_setup, LIGHTING_SETUPS)
        photo_style = _resolve_random(photo_style, PHOTO_STYLES)
        lens = _resolve_random(lens, LENSES)
        depth_of_field = _resolve_random(depth_of_field, DEPTH_OF_FIELD)
        color_grading = _resolve_random(color_grading, COLOR_GRADINGS)
        hairstyle = _resolve_random(hairstyle, HAIRSTYLES)
        hair_color = _resolve_random(hair_color, HAIR_COLORS)

        _is_ref = lambda v: v == _REF
        _expand = lambda v: NSFW_POSE_EXPANSIONS.get(v, NSFW_ACTION_EXPANSIONS.get(v, NSFW_GROUP_ACTION_EXPANSIONS.get(v, v)))
        sentences = []

        # 1. Opening: style + generic subject (identity comes from ReferenceLatent, not text)
        subj_label = subject.strip() if subject.strip() else "the character from the reference image"
        opener = ""
        if not _is_ref(photo_style):
            style_label = photo_style.capitalize()
            opener = f"{style_label} photo of {subj_label}"
        else:
            opener = f"Photo of {subj_label}"

        # Append pose (expand NSFW shorthand → explicit)
        if not _is_ref(pose):
            opener += f", {_expand(pose)}"

        sentences.append(opener)

        # 2. Action (expand NSFW shorthand → explicit)
        if action and action.strip():
            sentences.append(_expand(action.strip()).rstrip("."))

        # 3. Hair (color + style, only if changed from reference)
        hair_parts = []
        if hair_color and not _is_ref(hair_color):
            hair_parts.append(hair_color)
        if hairstyle and not _is_ref(hairstyle):
            hair_parts.append(f"{hairstyle} hair")
        if hair_parts:
            sentences.append(" ".join(hair_parts).capitalize())

        # 3. Outfit (from Outfit Composer or manual)
        if outfit and outfit.strip():
            sentences.append(outfit.strip().rstrip("."))

        # 3b. Exposure control (after outfit) — only when NSFW mode is on
        if _NSFW_ENABLED:
            exposure = []
            if expose_breasts:
                exposure.append("clothing adjusted to expose breasts")
                if remove_bra:
                    exposure.append("no bra")
            else:
                exposure.append("nipples fully concealed by clothing, fabric, hands, or hair")
                exposure.append("breasts fully covered by outfit")
            if remove_panties:
                exposure.append("not wearing panties")
            else:
                exposure.append("underwear or lingerie covering intimate areas")
            sentences.append(", ".join(exposure).capitalize())

        # 4. Environment / scene
        if environment and environment.strip():
            env = environment.strip()
            lower = env.lower()
            preps = ("in ", "at ", "on ", "near ", "by ", "inside ", "outside ",
                     "under ", "above ", "along ", "within ")
            if not any(lower.startswith(p) for p in preps):
                sentences.append(f"In {env}")
            else:
                sentences.append(env[0].upper() + env[1:])
        elif not _is_ref(scene_type):
            article = "an" if scene_type[0].lower() in "aeiou" else "a"
            sentences.append(f"In {article} {scene_type} setting")

        # 5. Extra details
        if extra_details and extra_details.strip():
            d = extra_details.strip().rstrip(".")
            sentences.append(d[0].upper() + d[1:] if d else d)

        # 6. Lighting (most impactful for Klein 9B)
        lighting_prose = LIGHTING_EXPANSIONS.get(lighting_setup, "") if not _is_ref(lighting_setup) else ""
        if lighting_custom and lighting_custom.strip():
            if lighting_prose:
                lighting_prose = f"{lighting_prose}, {lighting_custom.strip()}"
            else:
                lighting_prose = lighting_custom.strip()
        if lighting_prose:
            sentences.append(lighting_prose[0].upper() + lighting_prose[1:])

        # 7. Technical: shot type, angle, lens, DoF — only include overridden fields
        tech_parts = []
        if not _is_ref(shot_type):
            tech_parts.append(shot_type.capitalize())
        if not _is_ref(camera_angle):
            tech_parts.append(camera_angle)
        if not _is_ref(lens):
            tech_parts.append(f"{lens} lens")
        if not _is_ref(depth_of_field):
            dof_words = depth_of_field.split()
            dof_desc = dof_words[0]
            dof_fstop = dof_words[-1]
            tech_parts.append(f"{dof_desc} depth of field at {dof_fstop}")
        if tech_parts:
            sentences.append(", ".join(tech_parts))

        # 8. Mood + color grading
        tail = []
        if mood and mood.strip():
            m = mood.strip()
            tail.append(f"{m[0].upper() + m[1:]} mood")
        if not _is_ref(color_grading) and color_grading != "natural":
            cg = color_grading[0].upper() + color_grading[1:]
            tail.append(f"{cg} color grading")
        if tail:
            sentences.append(". ".join(tail))

        # 8. Edit instructions (from Image Edit Composer)
        if edit_instructions and edit_instructions.strip():
            sentences.append(edit_instructions.strip().rstrip("."))

        # 9. Identity preservation (for character reference workflows)
        if preserve_identity:
            sentences.append(IDENTITY_LOCK_PROMPT)

        # Auto-inject negative prompt terms
        neg_parts = []
        if negative_prompt and negative_prompt.strip():
            neg_parts.append(negative_prompt.strip())
        # Always-on quality negatives
        neg_parts.append("saggy breasts, torpedo breasts, droopy breasts, pendulous breasts, tubular breasts, uneven breasts, deflated breasts")
        neg_parts.append("extra fingers, extra hands, extra limbs, missing fingers, fused fingers, mutated hands, deformed hands, phantom limb, floating hand, disembodied hand, extra arms, bad anatomy, malformed limbs, wrong number of fingers, six fingers, disfigured, ugly, blurry, watermark, text, logo, signature")
        # Exposure-based negatives
        if _NSFW_ENABLED:
            if not expose_breasts:
                neg_parts.append("exposed nipples, bare breasts, lifted shirt, shirt pulled up, topless, areola visible")
            if not remove_panties:
                neg_parts.append("exposed genitals, no underwear, pantyless, bottomless")
        negative_prompt = ", ".join(neg_parts)

        # Assemble
        positive = ". ".join(sentences)
        positive = positive.replace("..", ".").replace(". .", ".").strip()
        if positive and not positive.endswith("."):
            positive += "."

        # JSON output
        _v = lambda v: "" if _is_ref(v) else v
        prompt_data = {
            "subject": subject,
            "pose": _v(pose),
            "action": action,
            "hairstyle": _v(hairstyle),
            "hair_color": _v(hair_color),
            "scene_type": _v(scene_type),
            "outfit": outfit,
            "edit_instructions": edit_instructions,
            "environment": environment,
            "lighting_setup": _v(lighting_setup),
            "lighting_custom": lighting_custom,
            "shot_type": _v(shot_type),
            "camera_angle": _v(camera_angle),
            "lens": _v(lens),
            "depth_of_field": _v(depth_of_field),
            "photo_style": _v(photo_style),
            "mood": mood,
            "color_grading": _v(color_grading),
            "extra_details": extra_details,
            "exposure": ", ".join(exposure).lower() if _NSFW_ENABLED else "",
            "preserve_identity": preserve_identity,
            "negative_prompt": negative_prompt,
        }
        prompt_json = json.dumps(prompt_data, indent=2)

        return (positive, negative_prompt, prompt_json)


# ══════════════════════════════════════════════
# OUTFIT COMPOSER
# ══════════════════════════════════════════════

_NONE = "none"

TOPS = [_NONE] + sorted([
    "T-shirt", "Tank top", "Crop top", "Hoodie", "Sweater", "Blouse",
    "Bodysuit", "Bustier", "Corset", "Corset top", "Lace camisole",
    "Satin camisole", "Sheer blouse", "Chiffon blouse", "Mesh top",
    "Fishnet top", "Off-shoulder top", "One-shoulder top", "Halter top",
    "Tube top", "Plunge neckline top", "Deep V-neck top", "Wrap top",
    "Peplum top", "Ribbed knit top", "Turtleneck", "Mock neck top",
    "Sleeveless turtleneck", "Cardigan", "Cropped cardigan", "Bolero shrug",
    "Band t-shirt", "Graphic tee", "Long sleeve top", "Cropped hoodie",
    "Gothic lace top", "Harness top",
])

BOTTOMS = [_NONE] + sorted([
    "Jeans", "Shorts", "Skirt", "Leggings", "Joggers", "Cargo pants",
    "Mini skirt", "Maxi skirt", "Slacks", "Denim skirt", "Micro skirt",
    "Pleated skirt", "Tennis skirt", "Pencil skirt", "Wrap skirt",
    "Asymmetrical skirt", "High-slit skirt", "Leather skirt", "Latex skirt",
    "Plaid skirt", "Denim shorts", "Micro shorts", "High-waisted shorts",
    "Biker shorts", "Hot pants", "Leather pants", "Ripped jeans",
    "Skinny jeans", "High-waisted jeans", "Bell bottoms", "Flare pants",
    "Wide-leg pants", "Palazzo pants", "Track pants", "Sweatpants",
    "Yoga pants", "Fishnet leggings", "Suspender skirt",
])

LINGERIE_TOPS = [_NONE] + sorted([
    "Bralette", "Lace bralette", "Satin bra", "Push-up bra",
    "Balconette bra", "Plunge bra", "Strapless bra", "Triangle bra",
    "Sheer bra", "Lace bra", "Longline bra", "Cage bra", "Harness bra",
    "Lace bustier", "Lingerie corset", "Overbust corset",
    "Babydoll top", "Teddy lingerie",
])

LINGERIE_BOTTOMS = [_NONE] + sorted([
    "Lace panties", "Thong", "G-string", "Bikini briefs",
    "Cheeky briefs", "High-waisted panties", "Satin panties",
    "Sheer panties", "Strappy panties", "Garter belt",
    "Suspender belt", "Thigh garters", "Stockings",
    "Fishnet stockings", "Thigh-highs", "Hold-up stockings",
    "Bodystocking", "Sheer tights", "Fishnet tights",
])

OUTERWEAR = [_NONE] + sorted([
    "Trench coat", "Wool coat", "Long coat", "Peacoat", "Puffer jacket",
    "Parka", "Bomber jacket", "Denim jacket", "Leather jacket",
    "Moto jacket", "Blazer", "Oversized blazer", "Cardigan",
    "Long cardigan", "Cropped jacket", "Zip hoodie", "Windbreaker",
    "Faux fur coat", "Cape", "Poncho", "Kimono", "Shawl",
    "Wrap coat", "Duster coat", "Belted coat", "Suit jacket",
    "Satin robe",
])

SHOES = [_NONE] + sorted([
    "Sneakers", "Boots", "Heels", "Platform shoes", "Sandals", "Flats",
    "Strappy heels", "Stilettos", "Pumps", "Wedges", "Ankle boots",
    "Knee-high boots", "Thigh-high boots", "Combat boots",
    "Platform heels", "Heeled boots", "Strappy sandals",
    "Gladiator sandals", "Mules", "Slides", "Ballet flats",
    "Cowboy boots", "Pointed-toe heels", "Clear heels",
    "Lace-up heels", "Thigh-high heeled boots", "Barefoot",
])

ACCESSORIES = [_NONE] + sorted([
    "Belt", "Chain belt", "Sunglasses", "Eyeglasses", "Beanie",
    "Baseball cap", "Handbag", "Backpack", "Headphones", "Watch",
    "Choker", "Leather choker", "Spiked choker", "Body harness",
    "Leather harness", "Necklace", "Pendant necklace",
    "Layered necklace", "Chain necklace", "Earrings", "Hoop earrings",
    "Stud earrings", "Bangles", "Rings", "Stacked rings",
    "Nose ring", "Septum ring", "Body chain", "Waist chain",
    "Scarf", "Silk scarf", "Necktie", "Bow tie", "Bracelets",
    "Anklet", "Clutch bag", "Tote bag",
])


class KPPBOutfitComposer:
    """Compose outfit descriptions from categorical selections."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "top": (TOPS, {"default": _NONE}),
                "bottom": (BOTTOMS, {"default": _NONE}),
                "shoes": (SHOES, {"default": _NONE}),
            },
            "optional": {
                "lingerie_top": (LINGERIE_TOPS, {"default": _NONE}),
                "lingerie_bottom": (LINGERIE_BOTTOMS, {"default": _NONE}),
                "outerwear": (OUTERWEAR, {"default": _NONE}),
                "accessory_1": (ACCESSORIES, {"default": _NONE}),
                "accessory_2": (ACCESSORIES, {"default": _NONE}),
                "accessory_3": (ACCESSORIES, {"default": _NONE}),
                "extra_outfit_details": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("outfit",)
    FUNCTION = "compose_outfit"
    CATEGORY = "conditioning/klein"

    def compose_outfit(
        self,
        top=_NONE,
        bottom=_NONE,
        shoes=_NONE,
        lingerie_top=_NONE,
        lingerie_bottom=_NONE,
        outerwear=_NONE,
        accessory_1=_NONE,
        accessory_2=_NONE,
        accessory_3=_NONE,
        extra_outfit_details="",
    ):
        pieces = []

        # Gather all non-none selections
        for item in [lingerie_top, lingerie_bottom, top, bottom, outerwear, shoes]:
            if item and item != _NONE:
                pieces.append(item.lower())

        # Accessories
        seen_acc = set()
        for item in [accessory_1, accessory_2, accessory_3]:
            if item and item != _NONE and item.lower() not in seen_acc:
                pieces.append(item.lower())
                seen_acc.add(item.lower())

        if not pieces and not (extra_outfit_details and extra_outfit_details.strip()):
            return ("",)

        # Build natural prose
        if pieces:
            if len(pieces) == 1:
                outfit_str = f"Wearing {pieces[0]}"
            elif len(pieces) == 2:
                outfit_str = f"Wearing {pieces[0]} and {pieces[1]}"
            else:
                outfit_str = f"Wearing {', '.join(pieces[:-1])}, and {pieces[-1]}"
        else:
            outfit_str = ""

        if extra_outfit_details and extra_outfit_details.strip():
            extra = extra_outfit_details.strip()
            if outfit_str:
                outfit_str = f"{outfit_str}. {extra}"
            else:
                outfit_str = extra

        return (outfit_str,)


# ══════════════════════════════════════════════
# IMAGE EDIT COMPOSER
# ══════════════════════════════════════════════

EDIT_TYPES = [
    "add element",
    "remove element",
    "replace element",
    "change style",
    "change environment",
    "change outfit",
    "change hair",
    "change makeup",
    "add effect",
    "custom",
]

IG_QUICK_EFFECTS = {
    "none": "",
    "add rain": "Add gentle rain falling throughout the scene with wet reflective surfaces",
    "add snow": "Add softly falling snow with a cold winter atmosphere",
    "add lens flare": "Add warm lens flare from the light source",
    "add bokeh background": "Add beautiful circular bokeh lights in the background",
    "add golden dust particles": "Add golden dust particles floating in the light",
    "add neon glow": "Add colorful neon glow and reflections across the scene",
    "add fog/haze": "Add atmospheric fog and haze softening the background",
    "add confetti": "Add colorful confetti falling through the air",
    "add sparkles": "Add glittering sparkles catching the light",
    "change to nighttime": "Change the time to nighttime with dark sky and artificial lighting",
    "change to golden hour": "Change the lighting to warm golden hour with long amber shadows",
    "change to overcast": "Change the sky to soft overcast with even diffused lighting",
    "add wet/reflective surfaces": "Add wet reflective surfaces with puddles catching the light",
    "add motion blur": "Add subtle motion blur suggesting movement and energy",
}

IG_QUICK_EFFECT_LIST = list(IG_QUICK_EFFECTS.keys())


def _compose_single_edit(edit_type, target, value, location):
    """Compose a single edit instruction from type + fields."""
    target = target.strip() if target else ""
    value = value.strip() if value else ""
    location = location.strip() if location else ""
    loc_suffix = f" {location}" if location else ""

    if not target and not value:
        return ""

    if edit_type == "add element":
        return f"Add {value}{loc_suffix}" if value else ""
    elif edit_type == "remove element":
        return f"Remove {target}{loc_suffix}" if target else ""
    elif edit_type == "replace element":
        if target and value:
            return f"Replace {target} with {value}{loc_suffix}"
        return ""
    elif edit_type == "change style":
        return f"Turn into {value} style" if value else ""
    elif edit_type == "change environment":
        if target and value:
            return f"Change {target} to {value}"
        elif value:
            return f"Change the environment to {value}"
        return ""
    elif edit_type == "change outfit":
        if target and value:
            return f"Replace {target} with {value}"
        elif value:
            return f"Change the outfit to {value}"
        return ""
    elif edit_type == "change hair":
        return f"Change the hair to {value}" if value else ""
    elif edit_type == "change makeup":
        return f"Change the makeup to {value}" if value else ""
    elif edit_type == "add effect":
        return f"Add {value}{loc_suffix}" if value else ""
    elif edit_type == "custom":
        return value
    return ""


class KPPBImageEditComposer:
    """Compose Klein 9B image editing instructions from structured inputs.
    Supports 3 stacked edit slots + IG quick effects."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Edit slot 1
                "edit_1_type": (EDIT_TYPES, {"default": "replace element"}),
                "edit_1_target": ("STRING", {"default": "", "placeholder": "what to affect (e.g. the jacket)"}),
                "edit_1_value": ("STRING", {"default": "", "placeholder": "desired result (e.g. leather bomber)"}),
                "edit_1_location": ("STRING", {"default": "", "placeholder": "where (optional)"}),
                "preserve_identity": ("BOOLEAN", {"default": True,
                                                  "tooltip": "Append identity lock to prevent face/likeness drift during edits"}),
            },
            "optional": {
                # Edit slot 2
                "edit_2_type": (EDIT_TYPES, {"default": "add element"}),
                "edit_2_target": ("STRING", {"default": ""}),
                "edit_2_value": ("STRING", {"default": ""}),
                "edit_2_location": ("STRING", {"default": ""}),
                # Edit slot 3
                "edit_3_type": (EDIT_TYPES, {"default": "add element"}),
                "edit_3_target": ("STRING", {"default": ""}),
                "edit_3_value": ("STRING", {"default": ""}),
                "edit_3_location": ("STRING", {"default": ""}),
                # Quick effect
                "ig_quick_effect": (IG_QUICK_EFFECT_LIST, {"default": "none"}),
                # Preservation note
                "preserve_note": ("STRING", {"multiline": True, "default": "",
                                             "placeholder": "what to keep unchanged (e.g. keep the pose and expression)"}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("edit_prompt", "edit_json")
    FUNCTION = "compose_edit"
    CATEGORY = "conditioning/klein"

    def compose_edit(
        self,
        edit_1_type,
        edit_1_target,
        edit_1_value,
        edit_1_location,
        preserve_identity=True,
        edit_2_type="add element",
        edit_2_target="",
        edit_2_value="",
        edit_2_location="",
        edit_3_type="add element",
        edit_3_target="",
        edit_3_value="",
        edit_3_location="",
        ig_quick_effect="none",
        preserve_note="",
    ):
        instructions = []

        # Compose each edit slot
        for etype, target, value, loc in [
            (edit_1_type, edit_1_target, edit_1_value, edit_1_location),
            (edit_2_type, edit_2_target, edit_2_value, edit_2_location),
            (edit_3_type, edit_3_target, edit_3_value, edit_3_location),
        ]:
            inst = _compose_single_edit(etype, target, value, loc)
            if inst:
                instructions.append(inst)

        # IG quick effect
        effect_prose = IG_QUICK_EFFECTS.get(ig_quick_effect, "")
        if effect_prose:
            instructions.append(effect_prose)

        # Preservation note
        if preserve_note and preserve_note.strip():
            note = preserve_note.strip()
            lower = note.lower()
            if not any(lower.startswith(p) for p in ("keep ", "preserve ", "maintain ", "don't ", "do not ")):
                instructions.append(f"Keep {note}")
            else:
                instructions.append(note[0].upper() + note[1:])

        # Identity preservation
        if preserve_identity:
            instructions.append(IDENTITY_LOCK_PROMPT)

        edit_prompt = ". ".join(instructions)
        if edit_prompt and not edit_prompt.endswith("."):
            edit_prompt += "."

        # JSON output
        edit_data = {
            "edit_1": {"type": edit_1_type, "target": edit_1_target,
                       "value": edit_1_value, "location": edit_1_location},
            "edit_2": {"type": edit_2_type, "target": edit_2_target,
                       "value": edit_2_value, "location": edit_2_location},
            "edit_3": {"type": edit_3_type, "target": edit_3_target,
                       "value": edit_3_value, "location": edit_3_location},
            "ig_quick_effect": ig_quick_effect,
            "preserve_identity": preserve_identity,
            "preserve_note": preserve_note,
            "composed_prompt": edit_prompt,
        }
        edit_json = json.dumps(edit_data, indent=2)

        return (edit_prompt, edit_json)
