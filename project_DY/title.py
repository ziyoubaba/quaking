# -*- coding:utf-8 -*-

class TitleHandler:
    def __init__(self):
        self.width = 32

    # 1
    def calc_text_width(self, text):
        return self.width * len(text)

