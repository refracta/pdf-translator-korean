import numpy as np
from tqdm import tqdm
from .base import FontBase

class NanumFont(FontBase):
    FONT_SIZE = 29

    def init(self, cfg: dict):
        self.cfg = cfg

    def get_all_fonts(self, layout):
        for i, line in tqdm(enumerate(layout)):
            if line.type in ["text", "list", "title"]:
                image = line.image
                family, size, ygain = self.get_font_info(image, line.line_cnt)
                line.font = {"family": family, "size": size, "ygain": ygain}
        return layout

    def get_font_info(self, image: np.ndarray, line_cnt: int = 1):
        if image.ndim == 3:
            height, width, _ = image.shape
        else:
            height, width = image.shape

        if not line_cnt or line_cnt <= 0:
            line_cnt = 1

        font_size = height / line_cnt
        print(f"width: {width}, height: {height}, fs: {font_size}")
        if font_size > 46:
            font_size = self.FONT_SIZE + 6
            ygain = 40
        elif font_size > 31:
            font_size = self.FONT_SIZE
            ygain = 33
        elif font_size > 28.5:
            font_size = self.FONT_SIZE - 3
            ygain = 30
        else:
            font_size = self.FONT_SIZE - 6
            ygain = 22

        return 'NanumMyeongjo.ttf', font_size, ygain
