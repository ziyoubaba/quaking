from OpenGL import GL
from OpenGL.GL import shaders
import freetype
import numpy as np
import os, glm

FONT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "SourceHanSerifSC-VF.ttf")

class CharacterSlot:
    def __init__(self, texture, glyph):
        self.texture = texture
        self.textureSize = (glyph.bitmap.width, glyph.bitmap.rows)

        if isinstance(glyph, freetype.GlyphSlot):
            self.bearing = (glyph.bitmap_left, glyph.bitmap_top)
            self.advance = glyph.advance.x
        elif isinstance(glyph, freetype.BitmapGlyph):
            self.bearing = (glyph.left, glyph.top)
            self.advance = None
        else:
            raise RuntimeError('unknown glyph type')

class EngineText():
    vertex_shader = """
        #version 330 core
        layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
        out vec2 TexCoords;

        uniform mat4 projection;

        void main()
        {
            gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
            TexCoords = vertex.zw;
        }
       """

    fragment_shader = """
        #version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform sampler2D text;
        uniform vec3 textColor;

        void main()
        {    
            vec4 sampled = vec4(1.0, 1.0, 1.0, texture(text, TexCoords).r);
            color = vec4(textColor, 1.0) * sampled;
        }
        """

    def __init__(self, fontfile=FONT):
        self.fontfile = fontfile
        self.shaderProgram = None
        self.Characters = dict()
        self.VBO = None
        self.VAO = None
        self.initliaze()

    def _get_rendering_buffer(self, xpos, ypos, w, h, zfix=0.0):
        return np.asarray([
            xpos, ypos - h, 0, 0,
            xpos, ypos, 0, 1,
            xpos + w, ypos, 1, 1,
            xpos, ypos - h, 0, 0,
            xpos + w, ypos, 1, 1,
            xpos + w, ypos - h, 1, 0
        ], np.float32)

    def init_shader_coop(self, projection):
        GL.glUniformMatrix4fv(self.shader_projection, 1, GL.GL_FALSE, glm.value_ptr(projection))

    def initliaze(self):
        #compiling shaders
        vertexshader = shaders.compileShader(self.vertex_shader, GL.GL_VERTEX_SHADER)
        fragmentshader = shaders.compileShader(self.fragment_shader, GL.GL_FRAGMENT_SHADER)
        #creating shaderProgram
        self.shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)
        GL.glUseProgram(self.shaderProgram)
        #get projection
        #problem
        self.shader_projection = GL.glGetUniformLocation(self.shaderProgram, "projection")
        projection = glm.ortho(0, 640, 640, 0)
        # projection = glm.ortho(0, width, height-1, 0)
        GL.glUniformMatrix4fv(self.shader_projection, 1, GL.GL_FALSE, glm.value_ptr(projection))

        #disable byte-alignment restriction
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)

        face = freetype.Face(self.fontfile)
        face.set_char_size( 48*64 )

        #load first 128 characters of ASCII set
        for i in range(0,128):
            face.load_char(chr(i))
            glyph = face.glyph

            #generate texture
            texture = GL.glGenTextures(1)
            GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RED, glyph.bitmap.width, glyph.bitmap.rows, 0,
                            GL.GL_RED, GL.GL_UNSIGNED_BYTE, glyph.bitmap.buffer)

            #texture options
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

            #now store character for later use
            self.Characters[chr(i)] = CharacterSlot(texture,glyph)

        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

        #configure VAO/VBO for texture quads
        self.VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.VAO)

        self.VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, 6 * 4 * 4, None, GL.GL_DYNAMIC_DRAW)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 4, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

    def text(self, text, x, y, scale, color=(0,0,0,0)):
        face = freetype.Face(self.fontfile)
        face.set_char_size(48 * 64)
        GL.glUniform3f(GL.glGetUniformLocation(self.shaderProgram, "textColor"),
                       color[0] / 255, color[1] / 255, color[2] / 255)

        GL.glActiveTexture(GL.GL_TEXTURE0)

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        GL.glBindVertexArray(self.VAO)
        for c in text:
            ch = self.Characters[c]
            w, h = ch.textureSize
            w = w * scale
            h = h * scale
            vertices = self._get_rendering_buffer(x, y, w, h)

            # render glyph texture over quad
            GL.glBindTexture(GL.GL_TEXTURE_2D, ch.texture)
            # update content of VBO memory
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
            GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            # render quad
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
            # now advance cursors for next glyph (note that advance is number of 1/64 pixels)
            x += (ch.advance >> 6) * scale

        GL.glBindVertexArray(0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
