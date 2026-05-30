"""Image filters for imgm."""
from PIL import Image, ImageEnhance, ImageFilter


def greyscale(img):
    """Convert image to greyscale."""
    return img.convert('L').convert('RGBA')


def opacity(img, level):
    """Adjust opacity (0.0 to 1.0)."""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    alpha = img.split()[3]
    alpha = alpha.point(lambda x: int(x * level))
    img.putalpha(alpha)
    return img


def blur(img, radius):
    """Apply Gaussian blur."""
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def resize(img, width, height):
    """Resize image with LANCZOS resampling."""
    return img.resize((width, height), Image.Resampling.LANCZOS)


def rotate(img, angle):
    """Rotate image."""
    return img.rotate(angle, expand=True)


def invert(img):
    """Invert RGB while preserving alpha."""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    r, g, b, a = img.split()
    r = ImageEnhance.Color(Image.new('RGBA', img.size, (255, 0, 0, 255))).enhance(0)
    inverted = Image.new('RGBA', img.size)
    inverted.putalpha(a)
    # Manual invert for RGB
    data = img.getdata()
    new_data = []
    for item in data:
        if len(item) == 4:
            new_data.append((255 - item[0], 255 - item[1], 255 - item[2], item[3]))
    inverted.putdata(new_data)
    return inverted


def brightness(img, factor):
    """Adjust brightness."""
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)


def contrast(img, factor):
    """Adjust contrast."""
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)
