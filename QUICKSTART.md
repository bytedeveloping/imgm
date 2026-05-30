# imgm Quick Start Guide

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run imgm:**
   ```bash
   python imgm.py --help
   ```

## First Run Examples

### Example 1: Basic Filter
```bash
python imgm.py photo.png --brightness 1.5 --contrast 1.2 -o output.png
```

### Example 2: Using Presets
```bash
# See available presets
python imgm.py --list-presets

# Apply Instagram preset
python imgm.py photo.png --preset instagram -o photo_instagram.png
```

### Example 3: Batch Processing
```bash
# Process entire folder (creates processed_images folder)
python imgm.py photos/ --preset noir --batch --output-folder processed_images/

# With more threads for faster processing
python imgm.py photos/ --blur 2 --batch --threads 8
```

### Example 4: Format Conversion
```bash
# Convert PNG to JPEG
python imgm.py photo.png --convert jpg

# Convert entire folder
python imgm.py photos/ --convert webp --batch
```

### Example 5: GUI Mode
```bash
# Launch interactive GUI
python imgm.py --gui
```

## Folder Structure

```
imgm/
├── imgm.py              ← Main CLI tool (run this)
├── processor.py         ← Image processing engine
├── filters.py           ← All filter implementations
├── presets.py           ← Preset definitions
├── plugins_system.py    ← Plugin loader
├── gui.py               ← Tkinter GUI interface
├── plugins/             ← Custom filter plugins go here
├── requirements.txt     ← Python dependencies
├── setup.py             ← Installation script
└── README.md            ← Full documentation
```

## Key Features at a Glance

| Feature | Example |
|---------|---------|
| Single filter | `imgm.py photo.png --blur 5` |
| Multiple filters | `imgm.py photo.png --brightness 1.2 --contrast 1.1` |
| Presets | `imgm.py photo.png --preset instagram` |
| Batch | `imgm.py photos/ --batch --threads 4` |
| Format | `imgm.py photo.png --convert jpg` |
| GUI | `imgm.py --gui` |

## Next Steps

1. **Explore filters:**
   ```bash
   python imgm.py photo.png --greyscale
   python imgm.py photo.png --invert
   python imgm.py photo.png --resize 800 600
   ```

2. **Try presets:**
   ```bash
   python imgm.py photo.png --preset vintage -o vintage.png
   python imgm.py photo.png --preset noir -o noir.png
   ```

3. **Create custom presets** by editing `presets.py`

4. **Create plugins** by adding Python files to the `plugins/` folder

## Help & Support

```bash
# Full help
python imgm.py --help

# List all presets
python imgm.py --list-presets

# List all plugins
python imgm.py --list-plugins

# Verbose output
python imgm.py photo.png --brightness 1.5 -v
```

---

**That's it! You're ready to process images like a pro.** 🚀
