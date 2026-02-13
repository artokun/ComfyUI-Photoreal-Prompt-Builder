"""
NSFW expansion dictionaries for KPPB.

Short UI labels map to explicit prompt text that FLUX Klein 9B can understand.
This module is optional — if the nsfw_pack folder is deleted, the core prompt
builder still works with SFW content only.
"""

# ──────────────────────────────────────────────
# NSFW pose expansions — short UI label → explicit
# prompt text Klein can understand
# ──────────────────────────────────────────────
NSFW_POSE_EXPANSIONS = {
    "arched back on all fours": "on all fours with back deeply arched, ass raised high, face down",
    "ass up face down": "face pressed down with ass raised high in the air, back arched",
    "back arched standing": "standing with back deeply arched pushing chest forward and ass out",
    "bent over": "bent over at the waist, ass presented, upper body lowered",
    "bent over looking back": "bent over at the waist looking back over shoulder, ass prominently displayed",
    "chest pressed together arms": "arms pressing breasts together, enhancing cleavage",
    "hands and knees": "on hands and knees, back slightly arched",
    "kneeling legs apart": "kneeling with knees spread wide apart",
    "kneeling looking up": "kneeling on the floor looking up with lips slightly parted",
    "legs open seated": "sitting with legs spread wide open",
    "legs spread lying back": "lying on back with legs spread wide open",
    "legs up lying back": "lying on back with both legs raised up in the air",
    "lying face down hips raised": "lying face down with hips and ass raised up off the surface",
    "lying on back knees bent": "lying on back with knees bent and pulled toward chest",
    "lying on side leg raised": "lying on side with top leg raised high, exposing inner thigh",
    "on elbows and knees": "on elbows and knees with ass raised high, face near the ground",
    "on knees back arched": "on knees with back deeply arched, chest pushed forward",
    "on knees hands on thighs": "on knees with hands resting on spread thighs",
    "one leg up against wall": "standing with one leg raised up against wall, exposing inner thigh",
    "presenting from behind": "on all fours with ass raised and presented toward camera, back arched, looking back over shoulder",
    "reclining legs parted": "reclining back with legs parted and relaxed open",
    "riding position": "straddling position with hips thrust forward as if riding",
    "sitting legs open": "sitting with legs spread wide apart",
    "sitting spread eagle": "sitting with legs fully spread eagle, wide open",
    "squatting legs apart": "squatting down with knees spread wide apart",
    "standing bent at waist": "standing and bent forward at the waist, ass pushed back",
    "standing legs apart": "standing with legs spread wide apart",
    "straddling": "straddling with legs on either side, hips lowered",
    "stretching on bed": "stretching body across bed with limbs extended, body elongated",
    "topless covering with hands": "topless with hands cupping and covering bare breasts",
    "topless hair covering": "topless with long hair draped over and partially covering bare breasts",
}

# ──────────────────────────────────────────────
# NSFW solo action expansions
# ──────────────────────────────────────────────
NSFW_ACTION_EXPANSIONS = {
    "arching back in pleasure": "arching back with eyes closed and mouth slightly open in pleasure",
    "biting finger": "biting index finger seductively while looking at camera",
    "biting lip": "biting lower lip seductively",
    "caressing inner thigh": "hand slowly caressing up the inner thigh",
    "cupping breasts": "both hands cupping and squeezing breasts together",
    "dripping wet from shower": "skin glistening wet with water dripping down body fresh from shower",
    "finger in mouth": "finger inserted in mouth, lips wrapped around it suggestively",
    "grabbing bedsheets": "hands gripping and clutching the bedsheets tightly",
    "grinding on pillow": "straddling a pillow and grinding hips against it",
    "hands between legs": "one hand reaching down between spread legs",
    "holding vibrator": "holding a vibrator in hand near body",
    "licking finger": "tongue slowly licking finger tip",
    "licking lollipop": "tongue licking a lollipop suggestively",
    "looking over shoulder seductively": "looking back over bare shoulder with seductive half-lidded eyes",
    "moaning expression": "head tilted back, mouth open, eyes closed in ecstasy",
    "oil dripping on body": "glistening body oil being dripped onto skin, body shining wet",
    "peeling off shirt": "pulling shirt up and off over head, midriff exposed",
    "playing with waistband": "fingers hooked in waistband, tugging it down slightly",
    "pulling down strap": "pulling a bra or top strap down off the shoulder",
    "pulling hair back": "both hands pulling hair back behind head, body stretched and exposed",
    "pulling panties aside": "fingers pulling panties to the side",
    "rubbing lotion on legs": "hands rubbing lotion slowly up along legs and thighs",
    "running hands through hair": "running both hands up through hair sensually with eyes closed",
    "sliding hand down body": "hand sliding slowly down from chest over stomach toward hips",
    "slowly undressing": "in the process of slowly removing clothing, half undressed",
    "smearing lipstick": "lipstick smeared messily across lips",
    "spreading legs slowly": "slowly spreading legs apart wider",
    "squeezing breasts together": "hands squeezing breasts together tightly, deepening cleavage",
    "stepping out of panties": "panties around ankles, one foot stepping out of them",
    "sucking finger": "sucking on finger with lips wrapped around it",
    "touching neck sensually": "hand on neck, head tilted, fingers trailing along throat",
    "undoing bra clasp": "hands behind back undoing bra clasp, bra loosening",
}

# ──────────────────────────────────────────────
# NSFW group action expansions
# ──────────────────────────────────────────────
NSFW_GROUP_ACTION_EXPANSIONS = {
    "being carried against wall": "man holding her up pinned against the wall, her legs wrapped around his waist",
    "being fingered": "his hand between her legs, fingers inside her",
    "being held down on bed": "man holding her wrists down on the bed above her head",
    "being kissed on neck from behind": "man standing behind her kissing and biting her neck, his hands on her hips",
    "being pinned against wall": "man pressing her body against the wall face first from behind",
    "bent over receiving from behind": "bent over with man penetrating her from behind, his hands gripping her hips",
    "blowjob on knees": "on her knees with his erect penis in her mouth, looking up at him",
    "cowgirl riding": "straddling on top of him riding with his penis inside her, her hands on his chest",
    "deep throat": "on her knees with his penis deep in her throat, lips at the base",
    "doggy style": "on all fours with man thrusting into her from behind, his hands on her waist",
    "face sitting on him": "sitting on his face, his mouth between her legs, her thighs around his head",
    "giving handjob": "her hand wrapped around his erect penis, stroking it",
    "grabbed by hair from behind": "man gripping her hair and pulling her head back while behind her",
    "grinding on his lap": "sitting on his lap grinding her hips against him, face to face",
    "hand around her throat": "man's hand gently gripping around her throat while facing her",
    "hands tied while being taken": "hands bound together above her head while man takes her",
    "him holding her legs up missionary": "lying on her back with man holding her legs up and apart while thrusting",
    "him pulling her hair during doggy": "on all fours with man behind her pulling her hair back with one hand",
    "kissing passionately": "deeply kissing with mouths open and tongues touching, bodies pressed together",
    "legs over his shoulders": "lying on back with both legs over his shoulders while he penetrates her",
    "legs wrapped around him standing": "lifted up with legs wrapped around his waist, his hands under her ass, face to face",
    "lying back receiving oral": "lying on her back with legs spread, his face between her thighs licking her",
    "missionary": "lying on her back with man on top between her legs, penetrating her",
    "on top reverse cowgirl": "sitting on top of him facing away, riding reverse cowgirl with his penis inside her",
    "pressed against glass": "breasts and body pressed flat against glass surface from behind",
    "prone bone": "lying flat face down with man lying on top penetrating her from behind",
    "receiving facial": "on her knees with eyes closed, cum on her face",
    "reverse cowgirl": "sitting on top of him facing away from him, riding with his penis inside her",
    "side by side spooning": "lying on her side with man spooning behind her, penetrating from behind",
    "sitting on his face": "squatting over his face, his tongue between her legs",
    "spread eagle for him": "lying on back with legs spread wide open as he positions between them",
    "standing carry position": "man carrying her in the air, her legs wrapped around him, penetrating while standing",
    "straddling his lap face to face": "straddling his lap face to face, his penis inside her, arms around his neck",
    "sucking while looking up": "on her knees sucking his penis while making eye contact looking up",
    "undressing each other": "pulling each other's clothes off, both half undressed",
}
