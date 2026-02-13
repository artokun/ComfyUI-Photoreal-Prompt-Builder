# ComfyUI Photoreal Prompt Builder

A structured prompt builder for photorealistic image generation with **FLUX Klein 9B** in ComfyUI. Turns dropdown selections into optimized natural-language prompts — no prompt engineering required.

## Features

- **Prompt Builder** — 20+ parameters (pose, scene, lighting, camera, lens, DoF, color grading, etc.) composed into flowing prose optimized for Klein 9B
- **Outfit Composer** — Mix and match tops, bottoms, shoes, lingerie, outerwear, and accessories into natural outfit descriptions
- **Image Edit Composer** — Structured editing instructions (add/remove/replace elements, quick IG effects)
- **VLM Prompt Refiner** — Vision language model integration via Ollama or Claude Code CLI. Sees your reference images and merges character identity with scene settings in a single shot
- **List Nodes** — Boolean-toggle selectors for batch generation via XY Plot Queue (scenes, poses, shots, lighting, outfits, actions, hairstyles, effects, and more)

## Installation

### Git Clone (Recommended)

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/artokun/ComfyUI-Photoreal-Prompt-Builder.git comfyui-klein-photoreal-promptbuilder
```

Restart ComfyUI. No pip dependencies required.

### ComfyUI Manager

Search for **"Photoreal Prompt Builder"** in the ComfyUI Manager install menu.

## Nodes

All nodes appear under **conditioning/klein** in the node menu.

### Prompt Builder (kppb)

The main node. Takes a subject description + structured settings and outputs an optimized positive prompt, negative prompt, and JSON dump of all settings.

**Key inputs:**
| Input | Type | Description |
|---|---|---|
| `subject` | string | Character description (e.g. "blonde woman in her mid 20s") |
| `pose` | dropdown | 53 poses from standing to yoga warrior |
| `scene_type` | dropdown | 17 locations (bedroom, beach, cafe, etc.) |
| `lighting_setup` | dropdown | 15 presets with rich prose expansions |
| `photo_style` | dropdown | 15 styles (phone candid, cinematic, editorial, etc.) |
| `shot_type` | dropdown | 16 framing options (close-up to wide full-body) |
| `camera_angle` | dropdown | 12 angles (eye level, dutch angle, from below, etc.) |
| `lens` | dropdown | 8 options (24mm wide to iPhone cameras) |
| `depth_of_field` | dropdown | 6 aperture settings (f/1.4 to f/8) |
| `color_grading` | dropdown | 12 grades (natural, cinematic teal-orange, film noir, etc.) |
| `hairstyle` | dropdown | 36 styles |
| `hair_color` | dropdown | 27 colors |
| `preserve_identity` | boolean | Append identity lock phrase for character reference consistency |

**Optional inputs:** `outfit` (from Outfit Composer), `edit_instructions` (from Image Edit Composer), `environment`, `lighting_custom`, `mood`, `extra_details`, `negative_prompt`, exposure controls.

### Outfit Composer (kppb)

Compose natural outfit descriptions from categorical selections.

**Inputs:** top, bottom, shoes, lingerie_top, lingerie_bottom, outerwear, 3 accessory slots, extra details.

**Output:** Natural prose like *"Wearing lace bralette, crop top, high-waisted jeans, ankle boots, and choker"*

### Image Edit Composer (kppb)

Build structured edit instructions for inpainting workflows. Supports 3 stacked edit slots + IG quick effects (rain, snow, lens flare, bokeh, neon glow, fog, etc.).

### VLM Prompt Refiner (kppb)

Vision language model integration for AI-assisted prompt composition. The VLM sees your reference images directly and writes the complete generation prompt.

**Modes:**
- **describe & enhance** — Merges character identity from the reference image with your scene settings
- **image edit aware** — Describes the final scene after edits
- **caption only** — Direct image description

**Backends:**
- **Ollama** — Local VLM inference (recommended: Qwen3-VL 32B). Auto-pulls models, auto-unloads from VRAM after inference
- **Claude Code CLI** — Uses Claude as the VLM backend with native image support

**Inputs:** character reference image, optional scene/prop reference images, model settings, temperature, seed.

### List Nodes (kppb)

Boolean-toggle selectors that output `LIST` + `INT` count for XY Plot Queue batch generation:

- Scene List, Pose List, Shot Type List, Camera Angle List
- Lighting List, Outfit List, Hairstyle List
- Action List, Group Action List
- Image Edit List, IG Effect List

## NSFW Module

An optional NSFW expansion module is available as a separate submodule. It adds explicit pose, action, and group action expansions plus corresponding list nodes. See the [NSFW module repo](https://github.com/artokun/ComfyUI-Photoreal-Prompt-Builder-NSFW) for details on what's included.

NSFW content is **disabled by default** and not downloaded during installation.

### Enabling

Edit `config.json` in the node folder:

```json
{
  "nsfw": true
}
```

Restart ComfyUI. The submodule will be fetched automatically and the NSFW nodes will appear in the node menu.

### Disabling

Set the flag back to `false`:

```json
{
  "nsfw": false
}
```

Restart ComfyUI. The NSFW module files will be cleaned up automatically and the nodes will be removed from the menu.

## VLM Setup

### Ollama (Local)

1. Install [Ollama](https://ollama.com)
2. The node auto-pulls models on first use, or manually:
   ```bash
   ollama pull huihui_ai/qwen3-vl-abliterated:32b-instruct-q8_0
   ```
3. Connect the **VLM Prompt Refiner** node with `ollama_url` set to `http://localhost:11434`

### Claude Code CLI

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code):
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
2. Enable `use_claude_code` on the VLM Prompt Refiner node
3. Select model (opus, sonnet, or haiku)

## Tips

- **Lighting is king** for Klein 9B — the lighting preset has the most impact on output quality
- Use `preserve_identity: true` when working with character reference images
- Connect the **Outfit Composer** output to the Prompt Builder's `outfit` input
- Connect the **Image Edit Composer** output to the Prompt Builder's `edit_instructions` input
- Use **List Nodes** with XY Plot Queue for systematic exploration of poses, scenes, lighting, etc.
- Set `unload_model: true` on the VLM Refiner when running Ollama locally to free VRAM for diffusion

## License

[MIT](LICENSE)
