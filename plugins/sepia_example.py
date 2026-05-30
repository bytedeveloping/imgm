"""
Example Plugin: Sepia Effect

This is an example plugin that demonstrates how to create custom filters.
To use plugins, place Python files in the plugins/ folder and they will
be automatically loaded.

Usage:
  imgm photo.png --plugin sepia
"""

from PIL import Image


def apply_filter(img, strength=1.0):
    """
    Apply sepia effect to image.
    
    Args:
        img: PIL Image object
        strength: Intensity of sepia effect (0.0 to 1.0)
    
    Returns:
        Modified PIL Image object
    """
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Convert to RGBA for sepia processing
    data = img.getdata()
    new_data = []
    
    for item in data:
        r, g, b = item[0], item[1], item[2]
        a = item[3] if len(item) == 4 else 255
        
        # Sepia formula
        tr = int(0.393 * r + 0.769 * g + 0.189 * b)
        tg = int(0.349 * r + 0.686 * g + 0.168 * b)
        tb = int(0.272 * r + 0.534 * g + 0.131 * b)
        
        # Clamp values
        tr = min(255, int(tr * strength + r * (1 - strength)))
        tg = min(255, int(tg * strength + g * (1 - strength)))
        tb = min(255, int(tb * strength + b * (1 - strength)))
        
        new_data.append((tr, tg, tb, a))
    
    result = Image.new('RGBA', img.size)
    result.putdata(new_data)
    return result


# Plugin metadata
plugin_info = {
    'name': 'Sepia',
    'version': '1.0',
    'description': 'Apply vintage sepia tone effect',
    'author': 'imgm',
}
