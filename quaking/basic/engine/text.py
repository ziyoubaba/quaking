from OpenGL import GL, GLU
from OpenGL.GL import shaders
import numpy as np
import os
# from quaking.basic.engine.font_v4 import font_data
# from quaking.basic.engine.font_v3 import on_display
# from quaking.basic.engine.font_final import display
from quaking.basic.engine.font_v6 import display

class EngineText():
    def __init__(self, ):
        pass


    def text(self, text, x, y, size=16 ,color=(0,0,0,255)):
        display(text, pos_x=x, pos_y=y, size=size, color=color)