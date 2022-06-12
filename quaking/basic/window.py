import glfw
from OpenGL import GL, GLU


class Window(object):
    def __init__(self, width, height, title: str='', swap_buffer: bool=False, ):
        if not glfw.init():
            raise RuntimeError("glfw init error")
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

    def create_window(self, width, height, title, monitor=None):
        window = glfw.create_window(width, height, title, monitor=monitor, share=None)
        if not window:
            glfw.terminate()
            raise RuntimeError("window created error")
        glfw.make_context_current(window)
        return window

    def set_coor(self, width, height):
        GL.glViewport(0, 0, width, height)
        GL.glLoadIdentity()
        # GLU.gluOrtho2D( 0, width, 0, height)  # 左下角
        # GLU.gluOrtho2D( 0, width, height, 0)  # 左上角
        GL.glOrtho(0, width, height, 0, -1, 1)

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

    def framebuffer_size_callback(self, window, width, height):
        if width and height:
            # print("resized: ", width, height, self.width, self.height)
            # glfw.get_window_frame_size()
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
        print("window iconify: ", iconified)
        if iconified:
            # The window was iconified
            pass
        else:
            # The window was restored
            pass