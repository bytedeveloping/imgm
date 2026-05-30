"""Presets for imgm."""

PRESETS = {
    "instagram": {
        "brightness": 1.2,
        "contrast": 1.3,
        "blur": 1,
    },
    "noir": {
        "greyscale": True,
        "contrast": 1.5,
        "brightness": 0.8,
    },
    "vintage": {
        "brightness": 1.1,
        "contrast": 0.9,
        "blur": 0.5,
    },
    "bright": {
        "brightness": 1.5,
        "contrast": 1.1,
    },
    "dark": {
        "brightness": 0.6,
        "contrast": 1.3,
    },
    "vivid": {
        "contrast": 1.5,
        "brightness": 1.1,
    },
}


def get_preset(name):
    """Get preset by name."""
    return PRESETS.get(name, None)


def list_presets():
    """List all available presets."""
    return list(PRESETS.keys())
