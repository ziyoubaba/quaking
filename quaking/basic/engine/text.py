from OpenGL import GL, GLU
from OpenGL.GL import shaders
import freetype
import numpy as np
import os, glm
from quaking.basic.engine.font import FontData

FONT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "SourceHanSerifSC-VF.ttf")
fontdata = FontData()

class EngineText():
    def __init__(self, ):
        pass

    def text_v1(self, text, x, y, scale, color=(0,0,0,0)):
        # face = freetype.Face(self.fontfile)
        # face.set_char_size(48 * 64)
        # GL.glUniform3f(GL.glGetUniformLocation(self.shaderProgram, "textColor"),
        #                color[0] / 255, color[1] / 255, color[2] / 255)
        #
        # GL.glActiveTexture(GL.GL_TEXTURE0)
        #
        # GL.glEnable(GL.GL_BLEND)
        # GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        #
        # GL.glBindVertexArray(self.VAO)
        # for c in text:
        #     ch = self.Characters[c]
        #     w, h = ch.textureSize
        #     w = w * scale
        #     h = h * scale
        #     vertices = self._get_rendering_buffer(x, y, w, h)
        #
        #     # render glyph texture over quad
        #     GL.glBindTexture(GL.GL_TEXTURE_2D, ch.texture)
        #     # update content of VBO memory
        #     GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        #     GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
        #     GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        #     # render quad
        #     GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        #     # now advance cursors for next glyph (note that advance is number of 1/64 pixels)
        #     x += (ch.advance >> 6) * scale
        #
        # GL.glBindVertexArray(0)
        # GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        pass

    def text(self, text, x, y,  color=(0,0,0,0)):
        fontdata.glPrint(x, y, text)
