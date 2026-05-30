#!/usr/bin/env python3
"""imgm - Professional Image Processing CLI Tool."""

import argparse
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from rich.console import Console
from rich.table import Table

import processor
from presets import list_presets, get_preset
from plugins_system import (
    load_plugins, list_plugins, load_plugin_from_path, 
    load_registered_plugins, register_plugin, unregister_plugin, 
    load_plugins_config
)
import gui


console = Console()

# ============================================================================
# IMGM_CONFIG: Global configuration for flags and arguments
# ============================================================================
IMGM_CONFIG = {
    'flags': {
        'gui': {'help': 'Launch GUI mode', 'action': 'store_true'},
        'batch': {'help': 'Process entire folder', 'action': 'store_true'},
        'greyscale': {'help': 'Convert to greyscale', 'action': 'store_true'},
        'invert': {'help': 'Invert colors', 'action': 'store_true'},
        'list-presets': {'help': 'List available presets', 'action': 'store_true'},
        'list-plugins': {'help': 'List available plugins', 'action': 'store_true'},
        'verbose': {'help': 'Verbose output', 'action': 'store_true'},
    },
    'arguments': {
        'input': {'nargs': '?', 'help': 'Input image or folder'},
        'output': {'help': 'Output file path'},
        'output-folder': {'help': 'Output folder for batch processing'},
        'brightness': {'type': float, 'help': 'Brightness adjustment (0.0-2.0)'},
        'contrast': {'type': float, 'help': 'Contrast adjustment (0.0-2.0)'},
        'blur': {'type': float, 'help': 'Blur radius'},
        'resize': {'type': int, 'nargs': 2, 'metavar': ('WIDTH', 'HEIGHT'), 'help': 'Resize image'},
        'rotate': {'type': float, 'help': 'Rotate image (degrees)'},
        'opacity': {'type': float, 'help': 'Opacity adjustment (0.0-1.0)'},
        'preset': {'help': 'Apply preset filter set'},
        'convert': {'help': 'Convert image format (png, jpg, gif, etc.)'},
        'threads': {'type': int, 'default': 4, 'help': 'Number of threads for batch processing'},
        'load': {'help': 'Load external plugin from file path'},
    }
}
# ============================================================================


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="imgm - Professional Image Processing CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  imgm photo.png --brightness 1.5 --contrast 1.2
  imgm photo.png --preset instagram --output photo_ig.png
  imgm folder/ --blur 2 --batch
  imgm photo.jpg --convert png
  imgm photo.png --load ./custom_filter.py
  imgm --gui
        """
    )
    
    # Input
    parser.add_argument('input', nargs='?', help='Input image or folder')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-of', '--output-folder', help='Output folder for batch processing')
    
    # Filters
    parser.add_argument('--brightness', type=float, help='Brightness adjustment (0.0-2.0)')
    parser.add_argument('--contrast', type=float, help='Contrast adjustment (0.0-2.0)')
    parser.add_argument('--blur', type=float, help='Blur radius')
    parser.add_argument('--resize', type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'), help='Resize image')
    parser.add_argument('--rotate', type=float, help='Rotate image (degrees)')
    parser.add_argument('--opacity', type=float, help='Opacity adjustment (0.0-1.0)')
    parser.add_argument('--greyscale', action='store_true', help='Convert to greyscale')
    parser.add_argument('--invert', action='store_true', help='Invert colors')
    
    # Presets & Plugins
    parser.add_argument('--preset', help='Apply preset filter set')
    parser.add_argument('--list-presets', action='store_true', help='List available presets')
    parser.add_argument('--list-plugins', action='store_true', help='List available plugins')
    parser.add_argument('--load', help='Load external plugin from file path')
    
    # Conversion
    parser.add_argument('--convert', help='Convert image format (png, jpg, gif, etc.)')
    
    # Batch processing
    parser.add_argument('--batch', action='store_true', help='Process entire folder')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads for batch processing')
    
    # GUI
    parser.add_argument('--gui', action='store_true', help='Launch GUI mode')
    
    # Verbose
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    return parser.parse_args()


def build_filter_dict(args):
    """Build filter dictionary from arguments."""
    filters = {}
    
    if args.brightness is not None:
        filters['brightness'] = args.brightness
    if args.contrast is not None:
        filters['contrast'] = args.contrast
    if args.blur is not None:
        filters['blur'] = args.blur
    if args.resize is not None:
        filters['resize'] = tuple(args.resize)
    if args.rotate is not None:
        filters['rotate'] = args.rotate
    if args.opacity is not None:
        filters['opacity'] = args.opacity
    if args.greyscale:
        filters['greyscale'] = True
    if args.invert:
        filters['invert'] = True
    
    return filters


def list_presets_cmd():
    """List available presets."""
    presets = list_presets()
    
    table = Table(title="Available Presets")
    table.add_column("Preset", style="cyan")
    table.add_column("Description", style="magenta")
    
    descriptions = {
        "instagram": "Bright, high-contrast with slight blur",
        "noir": "Black & white, high contrast, darker",
        "vintage": "Slightly desaturated, soft",
        "bright": "Increased brightness and contrast",
        "dark": "Darker with enhanced contrast",
        "vivid": "Enhanced colors and brightness",
    }
    
    for preset in presets:
        table.add_row(preset, descriptions.get(preset, "Custom preset"))
    
    console.print(table)


def list_plugins_cmd():
    """List available plugins."""
    plugins = list_plugins()
    
    if not plugins:
        console.print("[yellow]No plugins found in plugins/ folder[/yellow]")
    else:
        table = Table(title="Available Plugins (plugins/ folder)")
        table.add_column("Plugin", style="cyan")
        
        for plugin in plugins:
            table.add_row(plugin)
        
        console.print(table)
    
    # Also show registered plugins
    config = load_plugins_config()
    if config['plugins']:
        table = Table(title="Registered Plugins (auto-load from plugins.json)")
        table.add_column("Plugin Path", style="magenta")
        
        for plugin_path in config['plugins']:
            table.add_row(plugin_path)
        
        console.print(table)
    else:
        console.print("[yellow]No registered plugins[/yellow]")


def process_single_file(args, filters):
    """Process a single file."""
    input_path = args.input
    output_path = args.output or processor.get_output_filename(input_path, output_format=args.convert)
    
    console.print(f"[cyan]Processing:[/cyan] {input_path}")
    
    if args.convert:
        success = processor.convert_format(input_path, output_path, args.convert)
    else:
        success = processor.process_image(
            input_path, output_path, filters, 
            preset=args.preset,
            format_hint=args.convert
        )
    
    if success:
        console.print(f"[green]✓ Success:[/green] {output_path}")
    else:
        console.print(f"[red]✗ Failed:[/red] {input_path}")


def process_batch_threaded(image_files, filters, args):
    """Process images using multithreading."""
    max_workers = args.threads
    output_folder = args.output_folder or Path(args.input).parent
    
    def process_file(filepath):
        input_file = Path(filepath)
        if args.convert:
            output_filename = input_file.stem + '.' + args.convert.lower()
        else:
            output_filename = input_file.name
        output_path = Path(output_folder) / output_filename
        return processor.process_image(
            filepath, str(output_path), filters,
            preset=args.preset,
            format_hint=args.convert
        ), filepath
    
    successful = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, f): f for f in image_files}
        
        with tqdm(total=len(image_files), desc="Processing images", unit="img") as pbar:
            for future in as_completed(futures):
                success, filepath = future.result()
                if success:
                    successful += 1
                pbar.update(1)
    
    return successful, len(image_files)


def process_batch_folder(args, filters):
    """Process entire folder."""
    folder_path = args.input
    output_folder = args.output_folder or folder_path
    
    # Get all valid images
    folder = Path(folder_path)
    image_files = [
        str(f) for f in folder.iterdir()
        if f.suffix.lower() in processor.VALID_EXTENSIONS
    ]
    
    if not image_files:
        console.print(f"[yellow]No images found in {folder_path}[/yellow]")
        return
    
    console.print(f"[cyan]Found {len(image_files)} image(s)[/cyan]")
    
    # Use multithreading for batch
    if args.threads > 1:
        successful, total = process_batch_threaded(image_files, filters, args)
    else:
        successful = 0
        with tqdm(total=len(image_files), desc="Processing", unit="img") as pbar:
            for filepath in image_files:
                input_file = Path(filepath)
                if args.convert:
                    output_filename = input_file.stem + '.' + args.convert.lower()
                else:
                    output_filename = input_file.name
                output_path = Path(output_folder) / output_filename
                if processor.process_image(str(filepath), str(output_path), filters, args.preset, args.convert):
                    successful += 1
                pbar.update(1)
        total = len(image_files)
    
    console.print(f"[green]✓ Processed {successful}/{total} images[/green]")


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # GUI mode
    if args.gui:
        gui.launch_gui()
        return
    
    # List presets
    if args.list_presets:
        list_presets_cmd()
        return
    
    # List plugins
    if args.list_plugins:
        list_plugins_cmd()
        return
    
    # Load plugins
    if args.load:
        console.print(f"[cyan]Registering plugin: {args.load}[/cyan]")
        if not register_plugin(args.load):
            return 1
        console.print(f"[green]✓ Plugin will auto-load on next startup[/green]")
        return 0
    
    # Load registered plugins from plugins.json
    console.print("[cyan]Loading registered plugins...[/cyan]")
    registered_plugins = load_registered_plugins()
    
    if args.verbose:
        console.print("[cyan]Loading plugins from plugins/ folder...[/cyan]")
        folder_plugins = load_plugins()
        if folder_plugins:
            console.print(f"[green]Loaded {len(folder_plugins)} plugin(s) from folder[/green]")
    
    # Require input for processing
    if not args.input:
        console.print("[red]Error: Input image or folder required[/red]")
        return 1
    
    # Build filter dictionary
    filters = build_filter_dict(args)
    
    # Validate preset
    if args.preset and not get_preset(args.preset):
        console.print(f"[yellow]Warning: Unknown preset '{args.preset}'[/yellow]")
    
    # Process
    input_path = Path(args.input)
    
    if input_path.is_dir() or args.batch:
        process_batch_folder(args, filters)
    elif input_path.is_file():
        process_single_file(args, filters)
    else:
        console.print(f"[red]Error: Path not found: {args.input}[/red]")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
