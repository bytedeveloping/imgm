"""Image processing engine for imgm."""
import os
from pathlib import Path
from PIL import Image
from rich.console import Console
import filters
from presets import get_preset


console = Console()

VALID_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff'}
FORMAT_MAP = {
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.png': 'PNG',
    '.gif': 'GIF',
    '.bmp': 'BMP',
    '.webp': 'WEBP',
    '.tiff': 'TIFF',
}


def load_image(filepath):
    """Load image safely."""
    try:
        img = Image.open(filepath)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        return img
    except Exception as e:
        console.print(f"[red]Error loading {filepath}: {e}[/red]")
        return None


def save_image(img, output_path, format_hint=None):
    """Save image safely."""
    try:
        # Determine format
        ext = Path(output_path).suffix.lower()
        output_format = format_hint or FORMAT_MAP.get(ext, 'PNG')
        
        # Handle JPEG (no transparency)
        if output_format == 'JPEG' and img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        
        img.save(output_path, output_format)
        return True
    except Exception as e:
        console.print(f"[red]Error saving {output_path}: {e}[/red]")
        return False


def apply_filters(img, filter_dict):
    """Apply a chain of filters."""
    try:
        for filter_name, value in filter_dict.items():
            if filter_name == 'greyscale' and value:
                img = filters.greyscale(img)
            elif filter_name == 'opacity':
                img = filters.opacity(img, value)
            elif filter_name == 'blur':
                img = filters.blur(img, value)
            elif filter_name == 'resize':
                if isinstance(value, tuple) and len(value) == 2:
                    img = filters.resize(img, value[0], value[1])
            elif filter_name == 'rotate':
                img = filters.rotate(img, value)
            elif filter_name == 'invert' and value:
                img = filters.invert(img)
            elif filter_name == 'brightness':
                img = filters.brightness(img, value)
            elif filter_name == 'contrast':
                img = filters.contrast(img, value)
        return img
    except Exception as e:
        console.print(f"[red]Error applying filters: {e}[/red]")
        return None


def process_image(input_path, output_path, filter_dict, preset=None, format_hint=None):
    """Process a single image."""
    try:
        img = load_image(input_path)
        if img is None:
            return False
        
        # Apply preset if provided
        if preset:
            preset_dict = get_preset(preset)
            if preset_dict:
                filter_dict = {**preset_dict, **filter_dict}
        
        img = apply_filters(img, filter_dict)
        if img is None:
            return False
        
        return save_image(img, output_path, format_hint)
    except Exception as e:
        console.print(f"[red]Error processing {input_path}: {e}[/red]")
        return False


def process_folder(folder_path, filter_dict, preset=None, output_folder=None, format_hint=None):
    """Process all images in a folder."""
    try:
        folder = Path(folder_path)
        if not folder.is_dir():
            console.print(f"[red]Folder not found: {folder_path}[/red]")
            return 0
        
        output_folder = output_folder or folder_path
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        
        count = 0
        for file in folder.iterdir():
            if file.suffix.lower() in VALID_EXTENSIONS:
                output_file = Path(output_folder) / file.name
                if process_image(str(file), str(output_file), filter_dict, preset, format_hint):
                    count += 1
        
        return count
    except Exception as e:
        console.print(f"[red]Error processing folder: {e}[/red]")
        return 0


def convert_format(input_path, output_path, output_format):
    """Convert image format."""
    try:
        img = load_image(input_path)
        if img is None:
            return False
        
        # Map format string to PIL format
        format_map = {
            'jpeg': 'JPEG', 'jpg': 'JPEG',
            'png': 'PNG', 'gif': 'GIF',
            'bmp': 'BMP', 'webp': 'WEBP',
            'tiff': 'TIFF',
        }
        
        pil_format = format_map.get(output_format.lower(), 'PNG')
        return save_image(img, output_path, pil_format)
    except Exception as e:
        console.print(f"[red]Error converting format: {e}[/red]")
        return False


def get_output_filename(input_path, output_format=None, suffix='processed'):
    """Generate output filename."""
    path = Path(input_path)
    if output_format:
        return path.stem + f'_{suffix}.' + output_format.lower()
    return path.stem + f'_{suffix}' + path.suffix
