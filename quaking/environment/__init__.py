import glfw

class Environment:
    def __init__(self, quaking, width:int=100, height:int=100):
        self.quaking = quaking
        self.width = width
        self.height = height

    def size(self, width, height):
        if width != self.width or height != self.height:
            # 尺寸存在变动
            self.width = width
            self.height = height
            glfw.set_window_size(self.quaking.obj_window.window, width, height)
            # if self.quaking.background_color:
            #     # 更新背景颜色
            #     self.quaking.background(*self.quaking.background_color)