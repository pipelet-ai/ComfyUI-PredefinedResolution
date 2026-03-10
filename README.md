# ComfyUI-PredefinedResolution

A ComfyUI custom node that automatically snaps input dimensions to predefined resolutions and aspect ratios.

## Features

- **Automatic Ratio Detection**: Analyzes input width/height and snaps to the closest standard aspect ratio (21:9, 16:9, 1:1, 9:16, 9:21)
- **Predefined Output Resolutions**: Choose from 720p, 1080p, 2K, or 4K output resolutions
- **Custom Resolution Support**: Define your own resolution presets for each aspect ratio
- **Ratio Outputs**: Returns both width/height and height/width ratios for downstream nodes

## Installation

1. Clone this repository into your ComfyUI custom_nodes folder:
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/pipelet-ai/ComfyUI-PredefinedResolution.git
```

2. Restart ComfyUI

## Usage

### Inputs

**Required:**
- `width` (INT): Input image width (64-8192)
- `height` (INT): Input image height (64-8192)
- `output_resolution`: Select from "720p", "1080p", "2K", "4K", or "Custom"
- `target_ratio`: Target aspect ratio (21:9, 16:9, 1:1, 9:16, 9:21)

**Optional:**
- `width_height_scale` (FLOAT): Override the calculated ratio with a manual value (0.0 = use calculated ratio)
- `custom_21_9` (STRING): Custom resolution for 21:9 ratio (format: "width,height", e.g., "2560,1080")
- `custom_16_9` (STRING): Custom resolution for 16:9 ratio (default: "1920,1080")
- `custom_1_1` (STRING): Custom resolution for 1:1 ratio (default: "1080,1080")
- `custom_9_16` (STRING): Custom resolution for 9:16 ratio (default: "608,1080")
- `custom_9_21` (STRING): Custom resolution for 9:21 ratio (default: "464,1080")

### Outputs

- `width` (INT): Output width
- `height` (INT): Output height
- `width_height_ratio` (FLOAT): Width divided by height
- `height_width_ratio` (FLOAT): Height divided by width

### Example

**Input:** 720 x 800 (from an uploaded image)
- Detected ratio: Closest to 1:1
- Output resolution: 1080p
- **Output:** 1080 x 1080, ratio: 1.0, 1.0

**Input:** 1920 x 800
- Detected ratio: Closest to 21:9
- Output resolution: 2K
- **Output:** 4608 x 2048, ratio: 2.25, 0.44

## How It Works

1. The node calculates the aspect ratio from input width/height (or uses the optional `width_height_scale` if provided)
2. It finds the closest matching standard aspect ratio (21:9, 16:9, 1:1, 9:16, 9:21)
3. Based on the selected output resolution preset, it calculates the appropriate dimensions
4. Returns the final width, height, and both ratio values

## License

See LICENSE file for details.
