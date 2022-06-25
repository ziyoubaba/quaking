from OpenGL import GL
from PIL import Image

from OpenGL.GL import *

class EngineImage():
    def __init__(self):
        pass

    def image(self, obj_image, x, y, width, height, img_format=GL.GL_RGB):
        """

        :param obj_image:
        :param x:
        :param y:
        :return:
        """
        if isinstance(obj_image, bytes):
            w, h = width, height
            img_bytes = obj_image
        else:
            img_format = GL.GL_RGB if obj_image.mode == "RGB" else GL.GL_RGBA
            w, h = obj_image.size
            img_bytes = obj_image.tobytes()
        # 1 create a texture
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        texture = GL.glGenTextures(1)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, img_format, w, h, 0, img_format,
                        GL.GL_UNSIGNED_BYTE, img_bytes)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f( 0.0, 0.0 ); GL.glVertex3f( x, y, 0 )
        GL.glTexCoord2f( 1.0, 0.0 ); GL.glVertex3f( x+width, y, 0 )
        GL.glTexCoord2f( 1.0, 1.0 ); GL.glVertex3f( x+width, y+height, 0 )
        GL.glTexCoord2f( 0.0, 1.0 ); GL.glVertex3f( x, y+height, 0 )
        GL.glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    def load_image(self, image_file):
        # load the image using Pillow
        obj_image = Image.open(image_file)
        return obj_image
