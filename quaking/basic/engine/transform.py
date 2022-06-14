from OpenGL import GL

class EngineTransform():
    def __init__(self):
        pass

    def translate(self, x, y, z=0):
        GL.glTranslatef(x, y, z)

    def rotate(self, degree, x, y, z):
        GL.glRotatef(degree, x, y, z)