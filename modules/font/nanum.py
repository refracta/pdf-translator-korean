import numpy as np
from tqdm import tqdm
from PIL import ImageFont
import math
from utils import fw_fill, average_char_width
from .base import FontBase

class NanumFont(FontBase):
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

        ygain = int(font_size * 1.15)

        fnt = ImageFont.truetype('fonts/NanumMyeongjo.ttf', int(font_size))
        char_w = average_char_width(fnt)
        max_width_chars = max(1, math.ceil(width / char_w))
        processed = fw_fill(text, width=max_width_chars)
        lines = len(processed.split("\n"))

        while lines * ygain > height and font_size > 10:
            font_size -= 1
            ygain = int(font_size * 1.15)
            fnt = ImageFont.truetype('fonts/NanumMyeongjo.ttf', int(font_size))
            char_w = average_char_width(fnt)
            max_width_chars = max(1, math.ceil(width / char_w))
            processed = fw_fill(text, width=max_width_chars)
            lines = len(processed.split("\n"))

        return "NanumMyeongjo.ttf", int(font_size), int(ygain)
