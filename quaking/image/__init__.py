
class Image():
    def __init__(self, quaking):
        self.quaking = quaking

    def image(self, img, x, y, width, height):
        return self.quaking.obj_engine.image(img, x, y, width, height)

    def load_image(self, img_filepath):
        return self.quaking.obj_engine.load_image(img_filepath)

    def load_pixels(self):
        return self.quaking.obj_window.load_pixels()

    def pixel(self, x, y):
        return self.quaking.obj_window.pixel(x, y)