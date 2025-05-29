import numpy as np
from tqdm import tqdm
from PIL import ImageFont
import math
from utils import fill_text_to_width
from .base import FontBase

class SimpleFont(FontBase):
    BASE_FONT_SIZE = 29

    def init(self, cfg: dict):
        self.cfg = cfg
        self.dpi = cfg.get('dpi', 200)
        self.base_font_size = cfg.get('base_size', self.BASE_FONT_SIZE)
        # Scale the font size even more aggressively for high DPI screens.
        # Using a cubic scaling factor means 400 DPI will produce roughly
        # eight times the font size compared to 200 DPI.
        self.FONT_SIZE = self.base_font_size * (self.dpi / 200) ** 3
 
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
        # Allow fonts to grow more when DPI is high. The cubic scaling
        # keeps step proportional to the font size increase at higher DPI.
        step = 6 * (self.dpi / 200) ** 3
        if font_size > self.FONT_SIZE + step:
            font_size = self.FONT_SIZE + step
        elif font_size > self.FONT_SIZE:
            font_size = self.FONT_SIZE
        elif font_size > self.FONT_SIZE - step / 2:
            font_size = self.FONT_SIZE - step / 2
        else:
            font_size = self.FONT_SIZE - step

        ygain = int(font_size * 1.15)

        fnt = ImageFont.truetype('fonts/TimesNewRoman.ttf', int(font_size))
        processed = fill_text_to_width(text, fnt, width)
        lines = len(processed.split("\n"))

        while lines * ygain > height and font_size > 10:
            font_size -= 1
            ygain = int(font_size * 1.15)
            fnt = ImageFont.truetype('fonts/TimesNewRoman.ttf', int(font_size))
            processed = fill_text_to_width(text, fnt, width)
            lines = len(processed.split("\n"))

        return "TimesNewRoman.ttf", int(font_size), int(ygain)
                