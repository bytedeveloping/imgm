"""Plugin system for imgm."""
import os
import sys
import json
import importlib.util
from pathlib import Path
from rich.console import Console


console = Console()
PLUGINS_DIR = Path(__file__).parent / 'plugins'
PLUGINS_CONFIG = Path(__file__).parent / 'plugins.json'


def load_plugins():
    """Load all plugins from plugins directory."""
    if not PLUGINS_DIR.exists():
        PLUGINS_DIR.mkdir(exist_ok=True)
        return {}
    
    plugins = {}
    for plugin_file in PLUGINS_DIR.glob('*.py'):
        if plugin_file.name.startswith('_'):
            continue
        
        try:
            spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for filter function
            if hasattr(module, 'apply_filter'):
                plugins[plugin_file.stem] = module.apply_filter
                console.print(f"[green]Loaded plugin:[/green] {plugin_file.stem}")
        except Exception as e:
            console.print(f"[yellow]Failed to load plugin {plugin_file.stem}: {e}[/yellow]")
    
    return plugins


def get_plugin(name, plugins):
    """Get a plugin by name."""
    return plugins.get(name)


def list_plugins():
    """List all available plugins."""
    if not PLUGINS_DIR.exists():
        return []
    return [f.stem for f in PLUGINS_DIR.glob('*.py') if not f.name.startswith('_')]


def load_plugin_from_path(filepath):
    """Load a plugin from a specific file path.
    
    Args:
        filepath: Path to the plugin file
        
    Returns:
        Loaded plugin module or None if failed
    """
    try:
        plugin_path = Path(filepath)
        if not plugin_path.exists():
            console.print(f"[red]Plugin file not found: {filepath}[/red]")
            return None
        
        if not plugin_path.suffix == '.py':
            console.print(f"[red]Plugin must be a .py file: {filepath}[/red]")
            return None
        
        spec = importlib.util.spec_from_file_location(plugin_path.stem, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Check for required function
        if not hasattr(module, 'apply_filter'):
            console.print(f"[red]Plugin missing required 'apply_filter' function: {filepath}[/red]")
            return None
        
        console.print(f"[green]✓ Loaded plugin:[/green] {plugin_path.name}")
        return module
    except Exception as e:
        console.print(f"[red]Failed to load plugin {filepath}: {e}[/red]")
        return None


def load_plugins_config():
    """Load plugins.json configuration.
    
    Returns:
        Dictionary with 'plugins' list or empty dict if file doesn't exist
    """
    if not PLUGINS_CONFIG.exists():
        return {'plugins': []}
    
    try:
        with open(PLUGINS_CONFIG, 'r') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[yellow]Failed to read plugins.json: {e}[/yellow]")
        return {'plugins': []}


def save_plugins_config(config):
    """Save plugins configuration to plugins.json.
    
    Args:
        config: Dictionary with 'plugins' list
    """
    try:
        with open(PLUGINS_CONFIG, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        console.print(f"[red]Failed to save plugins.json: {e}[/red]")


def register_plugin(plugin_path):
    """Register a plugin to auto-load on startup.
    
    Args:
        plugin_path: Path to the plugin file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        plugin_path = str(Path(plugin_path).resolve())
        
        # Validate plugin exists and is valid
        if not load_plugin_from_path(plugin_path):
            return False
        
        config = load_plugins_config()
        
        # Avoid duplicates
        if plugin_path not in config['plugins']:
            config['plugins'].append(plugin_path)
            save_plugins_config(config)
            console.print(f"[green]✓ Registered plugin:[/green] {Path(plugin_path).name}")
        else:
            console.print(f"[yellow]Plugin already registered[/yellow]")
        
        return True
    except Exception as e:
        console.print(f"[red]Failed to register plugin: {e}[/red]")
        return False


def unregister_plugin(plugin_path):
    """Unregister a plugin from auto-loading.
    
    Args:
        plugin_path: Path to the plugin file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        plugin_path = str(Path(plugin_path).resolve())
        config = load_plugins_config()
        
        if plugin_path in config['plugins']:
            config['plugins'].remove(plugin_path)
            save_plugins_config(config)
            console.print(f"[green]✓ Unregistered plugin:[/green] {Path(plugin_path).name}")
            return True
        else:
            console.print(f"[yellow]Plugin not registered[/yellow]")
            return False
    except Exception as e:
        console.print(f"[red]Failed to unregister plugin: {e}[/red]")
        return False


def load_registered_plugins():
    """Load all plugins registered in plugins.json.
    
    Returns:
        Dictionary of loaded plugins
    """
    config = load_plugins_config()
    plugins = {}
    
    for plugin_path in config.get('plugins', []):
        try:
            plugin_path = Path(plugin_path)
            if not plugin_path.exists():
                console.print(f"[yellow]Skipping missing plugin: {plugin_path}[/yellow]")
                continue
            
            spec = importlib.util.spec_from_file_location(plugin_path.stem, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'apply_filter'):
                plugins[plugin_path.stem] = module.apply_filter
                console.print(f"[green]Loaded registered plugin:[/green] {plugin_path.name}")
        except Exception as e:
            console.print(f"[yellow]Failed to load registered plugin {plugin_path}: {e}[/yellow]")
    
    return plugins
