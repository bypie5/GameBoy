import configparser
from pathlib import Path
from typing import Dict, List

CONFIG = configparser.ConfigParser()
CONFIG_PATH: Path = None

def load_config(config_path: Path):
    """Load the .ini file from the specified path, or create a default one if it doesn't exist.

    Args:
        config_path: Path of .ini file to load/create.
    """
    global CONFIG
    global CONFIG_PATH

    CONFIG_PATH = config_path / "config.ini"

    if CONFIG_PATH.is_file():
        CONFIG.read(CONFIG_PATH)
    else:
        CONFIG["Paths"] = {
            "last_rom_dir": CONFIG_PATH.parents[0],
            "boot_rom_dir": "",
            "recent_0": "",
            "recent_1": "",
            "recent_2": "",
            "recent_3": "",
            "recent_4": "",
            "recent_5": "",
            "recent_6": "",
            "recent_7": "",
            "recent_8": "",
            "recent_9": "",
        }

        CONFIG["Colors"] = {
            "Green": "AFCB46 79AA6D 226F5F 082955",
            "Grey":  "E8E8E8 A0A0A0 585858 101010",
        }

        save_config()


def add_recent_path(rom_path: Path):
    """Add a ROM path to the list of recently opened ROMs.

    Args:
        rom_path: Path to add to recents list.
    """
    global CONFIG

    for i in range(8, -1, -1):
        CONFIG["Paths"][f"recent_{i+1}"] = CONFIG["Paths"][f"recent_{i}"]

    CONFIG["Paths"]["recent_0"] = rom_path
    save_config()


def save_config():
    """Save the current config to the .ini file."""
    global CONFIG
    global CONFIG_PATH

    with open(CONFIG_PATH, 'w') as config_file:
            CONFIG.write(config_file)


def get_color_schemes() -> Dict[str, List[int]]:
    """Get a dictionary of each saved color scheme.

    Returns:
        Dictionary connecting color scheme names to their colors.
    """
    global CONFIG

    color_schemes = {}

    for name, colors in CONFIG["Colors"].items():
        color_list = []

        for color_str in colors.split(' '):
            color_list.append(int(color_str[0:2], 16))
            color_list.append(int(color_str[2:4], 16))
            color_list.append(int(color_str[4:6], 16))

        color_schemes[name] = color_list

    return color_schemes


def add_color_scheme(name: str, colors: List[int]):
    """Insert a new color scheme. If a scheme with the same name already exists, it will be updated.

    Args:
        name: Name of color scheme.
        colors: Colors associated with this scheme.
    """
    global CONFIG

    hex_strs = []

    for i in range(0, 4):
        hex_strs.append(f"{colors[i*3]:02x}{colors[i*3 + 1]:02x}{colors[i*3 + 2]:02x}")

    hex_str = " ".join(hex_strs)
    CONFIG["Colors"][name] = hex_str
    save_config()


def delete_color_scheme(name: str):
    """Delete a color scheme from the config.

    Args:
        name: Name of color scheme to delete.
    """
    global CONFIG

    if name in CONFIG["Colors"]:
        CONFIG.remove_option("Colors", name)

    save_config()
