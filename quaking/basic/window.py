import glfw, glm
from OpenGL import GL, GLU
from quaking.basic.engine.text import EngineText

class Window(object):
    def __init__(self, width, height, title: str='', swap_buffer: bool=False):
        if not glfw.init():
            raise RuntimeError("glfw init error")
        # glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        # glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        # glfw 配置
        self.swap_buffer = swap_buffer  # 默认开启swap_buffer
        if not self.swap_buffer:
            glfw.window_hint(glfw.DOUBLEBUFFER, glfw.FALSE)
        # 创建窗口
        self.primary_monitor = self.get_primary_monitor()  # 主要窗口
        self.display_width, self.display_height = self.init_display(self.primary_monitor)
        self.focused = True
        if hasattr(self, "full") and self.full:
            self.window = self.create_window(width, height, title, monitor=self.primary_monitor)
        else:
            self.window = self.create_window(width, height, title, )
        # size
        self.width, self.height = glfw.get_window_size(self.window)
        self.pwidth = self.width
        self.pheight = self.height

        self.set_coor(self.width, self.height)
        # position
        self.posx, self.posy = glfw.get_window_pos(self.window)
        self.pposx, self.pposy = self.posx, self.posy
        #
        # Todo glReadPixels
        # self.read_gl_pixels()

    def create_window(self, width, height, title, monitor=None):
        window = glfw.create_window(width, height, title, monitor=monitor, share=None)
        if not window:
            glfw.terminate()
            raise RuntimeError("window created error")
        glfw.make_context_current(window)
        return window

    def set_coor(self, width, height):
        GL.glLoadIdentity()
        # GLU.gluOrtho2D( 0, width-1, 0, height-1)  # 左下角
        projection = GLU.gluOrtho2D( 0, width, height-1, -1)  # 左上角
        # projection = glm.ortho(0, width, height-1, 0)
        # EngineText().init_shader_coop(projection)
        # GL.glUniformMatrix4fv(EngineShader.shader_projection, 1, GL.GL_FALSE, glm.value_ptr(projection))
        # GL.glViewport( 0, width, height, 0 )
        # GL.glOrtho(0, width-1, height-1, 0, 0.0, 1.0)
        # GL.glViewport(0, 0, width-1, height-1)
        """
        projection = glm.ortho(0, 640, 640, 0)
        GL.glUniformMatrix4fv(shader_projection, 1, GL.GL_FALSE, glm.value_ptr(projection))
        """

    def setPosition(self, screen_x, screen_y):
        glfw.set_window_pos(self.window, screen_x, screen_y)

    def get_monitors(self):
        monitors = glfw.get_monitors()
        return monitors

    def get_primary_monitor(self):
        monitor = glfw.get_primary_monitor()
        return monitor

    def get_monitor_mode(self, monitor):
        mode_ = glfw.get_video_mode(monitor)
        return mode_

    def init_display(self, monitor):
        mode_ = self.get_monitor_mode(monitor)
        return mode_.size

    def callback_focused(self, monitor, focused):
        # print("focused: ", focused)
        self.focused = bool(focused)

    def full_screen(self, monitor=None):
        if not hasattr(self, "full"):
            self.full = False
        self.full = not self.full
        if self.window:
            monitor = monitor or self.primary_monitor
            if self.full:
                mode_ = self.get_monitor_mode(monitor)
                glfw.set_window_monitor(self.window, monitor, xpos=0, ypos=0,
                                    width=mode_.size.width, height=mode_.size.height,
                                    refresh_rate=mode_.refresh_rate)
            else:
                glfw.set_window_monitor(self.window, None, xpos=self.pposx, ypos=self.pposy,
                                        width=self.pwidth, height=self.pheight,
                                        refresh_rate=0)

    def size(self, width, height):
        if width != self.width or height != self.height:
            # 尺寸存在变动
            glfw.set_window_size(self.window, width, height)

    def read_gl_pixels(self):
        pixels = GL.glReadPixels(0, 0, self.width, self.height, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        self.pixels_w = self.width
        self.pixels_h = self.height
        self.pixels = pixels
        return pixels

    def draw_gl_pixels(self, pixels, width, height):
        GL.glDrawPixels(width, height, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, pixels)

    def framebuffer_size_callback(self, window, width, height):
        if width and height:
            # print("resized: ", width, height, self.width, self.height)
            self.pwidth = self.width
            self.pheight = self.height
            self.width = width
            self.height = height
            self.set_coor(width, height)
            return True
        else:
            return False

    def window_pos_callback(self, window, posx, posy):
        # print("pos: ", posx, posy, self.posx, self.posy)
        self.pposx, self.pposy = self.posx, self.posy
        self.posx = posx
        self.posy = posy

    def window_iconify_callback(self, window, iconified):
        # 最小化
        # print("window iconify: ", iconified)
        if iconified:
            # The window was iconified
            pass
        else:
            # The window was restored
            pass

    def load_pixels(self):
        pixels = self.read_gl_pixels()

    def pixel(self, pos_x, pos_y, pixel_degree=4):
        """

        :param pos_x:
        :param pos_y:
        :param pixel_degree:
        :return:
        """
        # print(len(self.pixels))
        if hasattr(self, "pixels"):
            index_start = (self.pixels_w * (self.pixels_h-pos_y-1) + pos_x ) * pixel_degree # 左上角
            # index_start = (self.pixels_w *  pos_y + pos_x  ) * pixel_degree   # 左下角
            colors = []
            for i in range(pixel_degree):
                colors.append(self.pixels[index_start + i])
            return colors

