import glfw
from quaking.basic import Basic
from quaking.environment import Environment
from quaking.color import ColorSetting
from quaking.mouse import Mouse
from quaking.keyboard import Keyboard
from quaking.shape import Shape2D, ShapeAttributes
from quaking.transform import Transform
from quaking.image import Image


class Quaking(Basic, Environment, ColorSetting, Mouse, Keyboard, Shape2D, ShapeAttributes, Transform, Image):
    def __init__(self, width: int = 100, height: int = 100, title: str = '', swap_buffer: bool = False):
        Basic.__init__(self, width, height, title=title, swap_buffer=swap_buffer)
        Environment.__init__(self, self)
        ColorSetting.__init__(self, self)
        Mouse.__init__(self, self)
        Keyboard.__init__(self, self)
        Shape2D.__init__(self, self)
        ShapeAttributes.__init__(self, self)
        Transform.__init__(self, self)
        Image.__init__(self, self)
        # 注册事件
        self.regiet_events()

    def regiet_events(self):
        # glfw.set_window_size_callback(self.obj_window.window, self.framebuffer_size_callback)
        glfw.set_framebuffer_size_callback(self.obj_window.window, self.framebuffer_size_callback)  #
        # glfw.set_window_maximize_callback(self.obj_window.window, self.framebuffer_size_callback)  #
        # glfw.set_window_iconify_callback(self.obj_window.window, self.obj_window.window_iconify_callback)  #
        glfw.set_window_pos_callback(self.obj_window.window, self.obj_window.window_pos_callback)  #
        # Mouse
        glfw.set_cursor_pos_callback(self.obj_window.window, self.mouse_position_callback)  # 鼠标移动事件
        glfw.set_mouse_button_callback(self.obj_window.window, self.mouse_button_callback)  # 鼠标点击事件
        glfw.set_scroll_callback(self.obj_window.window, self.mouse_scroll_callback)  # 鼠标滚动事件
        # Keyboard
        glfw.set_key_callback(self.obj_window.window, self.key_callback)  # 键盘按钮事件
        glfw.set_char_callback(self.obj_window.window, self.char_callback)  # 键盘按钮事件
        # window focused
        glfw.set_window_focus_callback(self.obj_window.window, self.obj_window.callback_focused)  # 键盘按钮事件

    def framebuffer_size_callback(self, *args, **kwargs):
        # 设置尺寸和坐标系
        status = self.obj_window.framebuffer_size_callback(*args, **kwargs)
        # 设置背景
        if status and (not self.swap_buffer):
            """
            self.setting()
            self.obj_window.draw_gl_pixels(self.obj_window.pixels, self.obj_window.pixels_w, self.obj_window.pixels_h)
            """
            # restart the programe
            # print("buffer size change")
            Basic.__init__(self, self.width, self.height, title=self.title, swap_buffer=self.swap_buffer,
                           obj_window=self.obj_window)
            Environment.__init__(self, self)
            ColorSetting.__init__(self, self)
            Mouse.__init__(self, self)
            Keyboard.__init__(self, self)
            Shape2D.__init__(self, self)
            ShapeAttributes.__init__(self, self)
            self.clear()
            self.setting()
            self.refresh = True

    def setting(self):
        if self.background_color:
            self.background(*self.background_color)

    def run(self, setup, draw):
        self.setting()
        self.loop(setup, draw)
