# imgm - Professional Image Processing CLI Tool

A modern, professional-grade image processing command-line tool built with Python. **imgm** brings the power of ImageMagick, GIMP, and Photoshop to your terminal.

## Features

### 🎛️ Core Architecture
- **CLI Parser** - Powerful argparse-based command interface
- **Processing Engine** - Fast image manipulation with Pillow
- **Filter Pipeline** - Chain multiple effects together
- **Batch Processing** - Process entire folders
- **Format Conversion** - Convert between any image format
- **Safe File Handling** - No destructive overwrites, proper error handling

### ✨ Built-in Filters
- **Greyscale** - Convert to black & white
- **Opacity** - Adjust transparency (0.0-1.0)
- **Blur** - Gaussian blur with adjustable radius
- **Resize** - High-quality LANCZOS resampling
- **Rotate** - Rotate images without cropping
- **Invert** - Invert RGB while preserving alpha
- **Brightness** - Adjust image brightness (0.0-2.0)
- **Contrast** - Adjust image contrast (0.0-2.0)

### ⭐ Advanced Features
1. **Multithreading** - Process multiple images in parallel (`--threads N`)
2. **Progress Bars** - Visual feedback with tqdm
3. **Colorized Output** - Rich, color-coded terminal output
4. **Preset System** - Pre-built filter combinations for common effects
5. **Plugin Architecture** - Extend with custom filters
6. **GUI Mode** - Simple Tkinter interface for visual editing

## Installation

### From source
```bash
cd imgm
pip install -r requirements.txt
pip install -e .
```

Or simply run:
```bash
python imgm.py --help
```

## Usage

### Basic Single File Processing

```bash
# Increase brightness
python imgm.py photo.png --brightness 1.5

# Add blur
python imgm.py photo.png --blur 5 --output photo_blurred.png

# Greyscale
python imgm.py photo.png --greyscale

# Multiple filters at once
python imgm.py photo.png --brightness 1.2 --contrast 1.3 --blur 2
```

### Using Presets

```bash
# Instagram-style filter
python imgm.py photo.png --preset instagram

# Film noir effect
python imgm.py photo.png --preset noir

# Vintage look
python imgm.py photo.png --preset vintage

# List all presets
python imgm.py --list-presets
```

### Batch Processing

```bash
# Process entire folder with 4 threads
python imgm.py photos/ --brightness 1.1 --batch

# Process with custom thread count
python imgm.py photos/ --blur 3 --batch --threads 8

# Save to different folder
python imgm.py photos/ --preset vivid --batch --output-folder processed/
```

### Format Conversion

```bash
# Convert PNG to JPEG
python imgm.py photo.png --convert jpg --output photo.jpg

# Convert entire folder to WebP
python imgm.py photos/ --convert webp --batch
```

### GUI Mode

```bash
# Launch interactive GUI
python imgm.py --gui
```

The GUI provides:
- File picker for loading images
- Real-time preview
- Interactive sliders for brightness, contrast, blur
- Preset buttons
- Save functionality

### Advanced Examples

```bash
# Resize + apply Instagram preset
python imgm.py photo.png --resize 1920 1080 --preset instagram

# Create noir thumbnail
python imgm.py photo.png --resize 200 200 --preset noir --output thumb.png

# Batch: Greyscale + high contrast
python imgm.py old_photos/ --greyscale --contrast 1.5 --batch

# Process with custom output folder
python imgm.py photos/ --preset bright --batch --output-folder brightened/
```

## Available Presets

| Preset | Effect |
|--------|--------|
| `instagram` | Bright, high-contrast with slight blur |
| `noir` | Black & white, high contrast, darker |
| `vintage` | Slightly desaturated, soft appearance |
| `bright` | Increased brightness and contrast |
| `dark` | Darker with enhanced contrast |
| `vivid` | Enhanced colors and brightness |

## Plugin System

Create custom filters and load them automatically on startup.

### Persistent Plugin Registration with --load

The `--load` flag **registers** a plugin to auto-load on every startup by saving it to `plugins.json`:

```bash
# Register a plugin (saved to plugins.json)
python imgm.py --load ./my_custom_filter.py

# Now the plugin auto-loads on every startup - no need to specify it again
python imgm.py photo.png --brightness 1.2
```

### How It Works

1. **First run:**
   ```bash
   imgm --load ./custom_pixelate.py
   ```
   - Validates the plugin
   - Saves the path to `plugins.json`
   - Returns to prompt

2. **Subsequent runs:**
   ```bash
   imgm photo.png
   ```
   - Automatically loads plugins listed in `plugins.json`
   - Your registered plugins are ready to use
   - No need to specify `--load` again

### Creating a Plugin

Create `my_custom_filter.py` or `plugins/my_filter.py`:

```python
"""My custom image filter."""
from PIL import Image

def apply_filter(img, **kwargs):
    """Apply custom filter to image.
    
    Args:
        img: PIL Image object (RGBA mode)
        **kwargs: Optional parameters
    
    Returns:
        Modified PIL Image object
    """
    # Your filter logic here
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Process the image
    # ... your code ...
    
    return img

# Optional: Plugin metadata
plugin_info = {
    'name': 'My Filter',
    'version': '1.0',
    'description': 'My custom image filter',
    'author': 'Your Name',
}
```

### Plugin Locations

**Option 1: Registered Plugins (Persistent)**
```bash
# Register once
imgm --load /path/to/my_filter.py

# Auto-loads on every startup
imgm photo.png
```

**Option 2: Folder Plugins (No Registration)**
```bash
# Drop file in plugins/ folder
cp my_filter.py plugins/

# Auto-discovered on startup
imgm --list-plugins
```

### View All Plugins

```bash
# Shows both registered (persistent) and folder plugins
imgm --list-plugins
```

### plugins.json

Stores registered plugin paths:

```json
{
  "plugins": [
    "/absolute/path/to/pixelate.py",
    "/absolute/path/to/custom_sepia.py"
  ]
}
```

- Created automatically when you use `--load`
- Stores absolute paths to registered plugins
- Updated on startup
- Can be edited or deleted to reset

## IMGM_CONFIG

The `IMGM_CONFIG` dictionary in `imgm.py` defines all CLI flags and arguments. It's organized as:

```python
IMGM_CONFIG = {
    'flags': {
        'gui': {'help': '...', 'action': 'store_true'},
        'batch': {...},
        # ... more flags
    },
    'arguments': {
        'input': {'nargs': '?', 'help': '...'},
        'output': {...},
        'load': {'help': 'Load external plugin from file path'},
        # ... more arguments
    }
}
```

This centralized configuration makes it easy to:
- Add new CLI flags and arguments
- Maintain consistent help text
- Modify argument types and defaults

## Command Reference

```
positional arguments:
  input                 Input image or folder

optional arguments:
  -o, --output OUTPUT              Output file path
  -of, --output-folder FOLDER      Output folder for batch processing

Filters:
  --brightness FACTOR              Brightness (0.0-2.0)
  --contrast FACTOR                Contrast (0.0-2.0)
  --blur RADIUS                    Blur radius (pixels)
  --resize WIDTH HEIGHT            Resize to dimensions
  --rotate DEGREES                 Rotate (degrees)
  --opacity LEVEL                  Opacity (0.0-1.0)
  --greyscale                      Convert to greyscale
  --invert                         Invert colors

Presets & Plugins:
  --preset NAME                    Apply preset
  --list-presets                   List all presets
  --list-plugins                   List plugins
  --load PATH                      Load external plugin from file path

Conversion:
  --convert FORMAT                 Convert format (png, jpg, gif, etc.)

Batch:
  --batch                          Process entire folder
  --threads N                      Number of threads (default: 4)

GUI:
  --gui                            Launch GUI mode

Other:
  -v, --verbose                    Verbose output
  -h, --help                       Show this help message
```

## Performance

### Multithreading Benchmarks
- Single file: ~200-500ms
- 100 images (single-threaded): ~30-50s
- 100 images (4 threads): ~12-15s
- 100 images (8 threads): ~8-10s

Performance depends on:
- Image resolution
- Filter complexity
- System CPU cores
- Disk I/O speed

### Tips
- Use `--threads 4` for most systems
- Increase for high-core CPUs
- Reduce for low-memory systems
- Process to SSD for faster I/O

## File Safety

imgm never overwrites input files:
- Single files: Saves as `{name}_processed.{ext}`
- Batch mode: Saves to separate folder
- Use `-o` / `-of` to specify output location
- Supports safe format conversion

## Architecture

```
imgm/
├── imgm.py              # Main CLI entry point
├── processor.py         # Core image processing engine
├── filters.py           # Filter implementations
├── presets.py           # Preset definitions
├── plugins_system.py    # Plugin loader
├── gui.py               # Tkinter GUI
├── plugins/             # User plugins folder
├── requirements.txt     # Dependencies
└── setup.py             # Installation script
```

## Requirements

- Python 3.8+
- Pillow (Image processing)
- tqdm (Progress bars)
- rich (Colorized output)
- colorama (Cross-platform colors)
- tkinter (GUI - usually included with Python)

## License

MIT License - Free for personal and commercial use

---

**Built with ❤️ for image enthusiasts, photographers, designers, and developers.**
<p align="center">

  <!-- Stars -->
  <a href="https://github.com/bytedeveloping/imgm/stargazers">
    <img src="https://img.shields.io/github/stars/bytedeveloping/imgm?style=for-the-badge" />
  </a>

  <!-- Forks -->
  <a href="https://github.com/bytedeveloping/imgm/network/members">
    <img src="https://img.shields.io/github/forks/bytedeveloping/imgm?style=for-the-badge" />
  </a>

  <!-- Watchers -->
  <a href="https://github.com/bytedeveloping/imgm/watchers">
    <img src="https://img.shields.io/github/watchers/bytedeveloping/imgm?style=for-the-badge" />
  </a>

  <!-- Issues -->
  <a href="https://github.com/bytedeveloping/imgm/issues">
    <img src="https://img.shields.io/github/issues/bytedeveloping/imgm?style=for-the-badge" />
  </a>

  <!-- Pull Requests -->
  <a href="https://github.com/bytedeveloping/imgm/pulls">
    <img src="https://img.shields.io/github/issues-pr/bytedeveloping/imgm?style=for-the-badge" />
  </a>

  <!-- License -->
  <a href="https://github.com/bytedeveloping/imgm/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/bytedeveloping/imgm?style=for-the-badge" />
  </a>

  <!-- Last Commit -->
  <a href="https://github.com/bytedeveloping/imgm/commits/main">
    <img src="https://img.shields.io/github/last-commit/bytedeveloping/imgm?style=for-the-badge" />
  </a>

  <!-- Repo Size -->
  <a href="https://github.com/bytedeveloping/imgm">
    <img src="https://img.shields.io/github/repo-size/bytedeveloping/imgm?style=for-the-badge" />
  </a>

  <!-- Commit Activity -->
  <a href="https://github.com/bytedeveloping/imgm/commits">
    <img src="https://img.shields.io/github/commit-activity/y/bytedeveloping/imgm?style=for-the-badge" />
  </a>

  <!-- Contributors -->
  <a href="https://github.com/bytedeveloping/imgm/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/bytedeveloping/imgm?style=for-the-badge" />
  </a>

</p>

