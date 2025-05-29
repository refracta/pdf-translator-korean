import os
from .textwrap_local import fw_fill, fw_wrap
from .ocr_model import OCRModel
from .layout_model import LayoutAnalyzer
from .gui import create_gradio_app
from PIL import ImageFont

import yaml

__all__ = ["fw_fill", "fw_wrap", "OCRModel", "LayoutAnalyzer", "average_char_width"]


def average_char_width(font: ImageFont.FreeTypeFont) -> float:
    """Return an estimated average character width for the given font.

    The bounding boxes returned by PIL tend to overestimate individual
    character width. To compensate, measure a longer sample string and
    divide by the number of characters.
    """

    try:
        sample = "가나다라마바사아자차"  # 10 Hangul characters
        bbox = font.getbbox(sample)
        width = bbox[2] - bbox[0]
        if width > 0:
            return width / len(sample)
    except Exception:
        pass

    # Fallback to ASCII if Hangul is unavailable
    sample = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    bbox = font.getbbox(sample)
    return (bbox[2] - bbox[0]) / len(sample)

def load_config(base_config_path, override_config_path):
    with open(base_config_path, 'r') as base_file:
        base_config = yaml.safe_load(base_file)
    
    final_config = base_config

    if os.path.exists(override_config_path):
        with open(override_config_path, 'r') as override_file:
            override_config = yaml.safe_load(override_file)
            final_config = update(base_config, override_config)
    
    # Update the base config with the override config
    # This recursively updates nested dictionaries
    def update(d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = update(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    return final_config


def draw_text(draw, processed_text, current_fnt, font_size, width, ygain):
    """Draw text on an image without justifying spaces."""

    y = 0
    for line in processed_text.split("\n"):
        draw.text((0, y), line, font=current_fnt, fill="black")
        y += ygain
