from OpenGL import GL, GLU
from OpenGL.GL import shaders
import numpy as np
import os
# from quaking.basic.engine.font_v4 import font_data
# from quaking.basic.engine.font_v3 import on_display
# from quaking.basic.engine.font_final import display
from quaking.basic.engine.font_v6 import display

# FONT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "SourceHanSerifSC-VF.ttf")

class EngineText():
    def __init__(self, ):
        pass


    def text(self, text, x, y,  color=(0,0,0,255)):
        # font_data(FONT, 16).glPrint(x, y, text)
        # on_display()
        display(text, pos_x=x, pos_y=y, color=color)