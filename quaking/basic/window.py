
import glfw

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

    def create_window(self, width, height, title,):
        window = glfw.create_window(width, height, title, monitor=None, share=None)
        if not window:
            glfw.terminate()
            raise RuntimeError("window created error")
        glfw.make_context_current(window)
        # todo : events
        # glfw.set_window_size_callback( window, self.window_size_callback )
        # glfw.set_framebuffer_size_callback(window, self.framebuffer_size_callback)  #
        # glfw.set_cursor_pos_callback(window, self.mouse_position_callback)  # 鼠标移动事件
        # glfw.set_mouse_button_callback(window, self.mouse_button_callback)  # 鼠标点击事件
        # glfw.set_scroll_callback(window, self.mouse_scroll_callback)  # 鼠标点击事件
        # glfw.set_key_callback(window, self.key_callback)  # 键盘按钮事件
        # glfw.set_char_callback(window, self.char_callback)  # 键盘按钮事件

        # corpration
        # GL.glViewport(0, 0, self.width, self.height)
        # GL.glLoadIdentity()
        # GL.glOrtho(0, self.width, self.height, 0, -10, 10)
        return window

    def setPosition(self, screen_x, screen_y):
        glfw.set_window_pos(self.window, screen_x, screen_y)
