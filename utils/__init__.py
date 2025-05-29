import os
from .textwrap_local import fw_fill, fw_wrap
from .ocr_model import OCRModel
from .layout_model import LayoutAnalyzer
from .gui import create_gradio_app
from PIL import ImageFont

import yaml

__all__ = ["fw_fill", "fw_wrap", "OCRModel", "LayoutAnalyzer", "fill_text_to_width"]


def _text_width(font: ImageFont.FreeTypeFont, text: str) -> int:
    """Return the pixel width of ``text`` for the given font."""
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]


def fill_text_to_width(text: str, font: ImageFont.FreeTypeFont, width: int) -> str:
    """Wrap ``text`` so that each line fits within ``width`` pixels."""
    wrapped_lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current_line = ""
        for word in words:
            candidate = word if current_line == "" else current_line + " " + word
            if _text_width(font, candidate) <= width:
                current_line = candidate
            else:
                if current_line:
                    wrapped_lines.append(current_line)
                # if a single word is too long, break it character by character
                if _text_width(font, word) <= width:
                    current_line = word
                else:
                    tmp = ""
                    for ch in word:
                        if _text_width(font, tmp + ch) <= width:
                            tmp += ch
                        else:
                            wrapped_lines.append(tmp)
                            tmp = ch
                    current_line = tmp
        wrapped_lines.append(current_line)
    return "\n".join(wrapped_lines)

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
