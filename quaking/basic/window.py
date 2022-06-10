
import glfw
from OpenGL import GL

class Window(object):
    def __init__(self, width, height, title:str='', swap_buffer:bool=False,):
        if not glfw.init():
            raise RuntimeError("glfw init error")
        # glfw 配置
        self.swap_buffer = swap_buffer  # 默认开启swap_buffer
        if not self.swap_buffer:
            glfw.window_hint(glfw.DOUBLEBUFFER, glfw.FALSE)
        # 创建窗口
        self.window = self.create_window(width, height, title)
        self.set_coor(width, height)

    def create_window(self, width, height, title,):
        window = glfw.create_window(width, height, title, monitor=None, share=None)
        if not window:
            glfw.terminate()
            raise RuntimeError("window created error")
        glfw.make_context_current(window)
        return window

    def set_coor(self, width, height):
        GL.glViewport(0, 0, width, height)
        GL.glLoadIdentity()
        # GLU.gluOrtho2D( 0, self.width, self.height, 0)
        GL.glOrtho(0, width, height, 0, -10, 10)

    def setPosition(self, screen_x, screen_y):
        glfw.set_window_pos(self.window, screen_x, screen_y)
