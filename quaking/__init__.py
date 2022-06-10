import glfw
from quaking.basic import Basic
from quaking.environment import Environment
from quaking.color import ColorSetting
from quaking.mouse import Mouse
from quaking.keyboard import Keyboard


class Quaking(Basic, Environment, ColorSetting, Mouse, Keyboard):
    def __init__(self, width: int = 100, height: int = 100, title: str = '', swap_buffer: bool = False):
        Basic.__init__(self, width, height, title=title, swap_buffer=swap_buffer)
        Environment.__init__(self, self, width, height)
        ColorSetting.__init__(self, self)
        Mouse.__init__(self, self)
        Keyboard.__init__(self, self)
        # 注册事件
        self.regiet_events()

    def regiet_events(self):
        # glfw.set_framebuffer_size_callback(self.obj_window.window, self.framebuffer_size_callback)  #
        # Mouse
        glfw.set_cursor_pos_callback(self.obj_window.window, self.mouse_position_callback)  # 鼠标移动事件
        glfw.set_mouse_button_callback(self.obj_window.window, self.mouse_button_callback)  # 鼠标点击事件
        glfw.set_scroll_callback(self.obj_window.window, self.mouse_scroll_callback)  # 鼠标滚动事件
        # Keyboard
        glfw.set_key_callback(self.obj_window.window, self.key_callback)  # 键盘按钮事件
        glfw.set_char_callback(self.obj_window.window, self.char_callback)  # 键盘按钮事件

    def run(self, setup, draw):
        self.loop(setup, draw)

