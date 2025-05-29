import numpy as np
from tqdm import tqdm
from PIL import ImageFont
from utils import fw_fill
from .base import FontBase

class SimpleFont(FontBase):
    FONT_SIZE = 29

    def init(self, cfg: dict):
        self.cfg = cfg
 
    def get_all_fonts(self, layout):
        for _, line in tqdm(enumerate(layout)):
            if line.type in ["text", "list", "title"]:
                family, size, ygain = self.get_font_info(line)
                line.font = {"family": family, "size": size, "ygain": ygain}

        return layout
    
    def get_font_info(self, line) -> tuple[str, int, int]:
        image = line.image
        text = line.translated_text or ""

        if image.ndim == 3:
            height, width, _ = image.shape
        else:
            height, width = image.shape

        line_cnt = line.line_cnt if line.line_cnt and line.line_cnt > 0 else 1

        font_size = height / line_cnt
        if font_size > self.FONT_SIZE + 6:
            font_size = self.FONT_SIZE + 6
        elif font_size > self.FONT_SIZE:
            font_size = self.FONT_SIZE
        elif font_size > self.FONT_SIZE - 3:
            font_size = self.FONT_SIZE - 3
        else:
            font_size = self.FONT_SIZE - 6

        while font_size > 10:
            ygain = int(font_size * 1.15)
            max_width_chars = max(1, int(width / (font_size / 2.4)) - 1)
            processed = fw_fill(text, width=max_width_chars)
            lines = processed.split("\n")

            font = ImageFont.truetype("fonts/TimesNewRoman.ttf", int(font_size))
            max_line_width = 0
            for l in lines:
                bbox = font.getbbox(l)
                line_width = bbox[2] - bbox[0]
                if line_width > max_line_width:
                    max_line_width = line_width

            if len(lines) * ygain <= height and max_line_width <= width:
                break

            font_size -= 1

        ygain = int(font_size * 1.15)
        return "TimesNewRoman.ttf", int(font_size), int(ygain)
                