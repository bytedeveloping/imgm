"""
Example Custom Plugin: Pixelate Effect

This demonstrates how to create a plugin that can be loaded with --load flag.

Usage:
  imgm photo.png --load ./custom_pixelate.py

The plugin will automatically be loaded at startup if the --load flag is used.
"""

from PIL import Image


def apply_filter(img, pixel_size=10):
    """
    Apply pixelate/mosaic effect to image.
    
    Args:
        img: PIL Image object
        pixel_size: Size of pixels (default: 10)
    
    Returns:
        Modified PIL Image object
    """
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Resize down then up to create pixelate effect
    small = img.resize(
        (img.width // pixel_size, img.height // pixel_size),
        Image.Resampling.LANCZOS
    )
    pixelated = small.resize(img.size, Image.Resampling.NEAREST)
    
    return pixelated


# Plugin metadata
plugin_info = {
    'name': 'Pixelate',
    'version': '1.0',
    'description': 'Apply pixelate/mosaic effect to images',
    'author': 'Custom Plugin',
}
