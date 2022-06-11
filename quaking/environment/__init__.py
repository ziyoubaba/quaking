import glfw

class Environment:
    def __init__(self, quaking):
        self.quaking = quaking

    @property
    def width(self):
        return self.quaking.obj_window.width

    @property
    def height(self):
        return self.quaking.obj_window.height

    def size(self, width, height):
        return self.quaking.obj_window.size(width, height)

    @property
    def display_width(self):
        return self.quaking.obj_window.display_width

    @property
    def display_height(self):
        return self.quaking.obj_window.display_height

    @property
    def focused(self):
        return self.quaking.obj_window.focused

    def full_screen(self, monitor=None):
        return self.quaking.obj_window.full_screen(monitor)

