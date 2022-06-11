import glfw
from quaking.basic import Basic
from quaking.environment import Environment
from quaking.color import ColorSetting
from quaking.mouse import Mouse
from quaking.keyboard import Keyboard
from quaking.shape import Shape2D, ShapeAttributes


class Quaking(Basic, Environment, ColorSetting, Mouse, Keyboard, Shape2D, ShapeAttributes):
    def __init__(self, width: int = 100, height: int = 100, title: str = '', swap_buffer: bool = False):
        Basic.__init__(self, width, height, title=title, swap_buffer=swap_buffer)
        Environment.__init__(self, self)
        ColorSetting.__init__(self, self)
        Mouse.__init__(self, self)
        Keyboard.__init__(self, self)
        Shape2D.__init__(self, self)
        ShapeAttributes.__init__(self, self)
        # 注册事件
        self.regiet_events()

    def regiet_events(self):
        # glfw.set_window_size_callback(self.obj_window.window, self.obj_window.window_size_callback)
        glfw.set_framebuffer_size_callback(self.obj_window.window, self.framebuffer_size_callback)  #
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
        self.obj_window.framebuffer_size_callback(*args, **kwargs)
        # 设置背景
        self.setting()

    def setting(self):
        if self.background_color:
            self.background(*self.background_color)

    def run(self, setup, draw):
        self.setting()
        self.loop(setup, draw)

