class Shape2D():
    def __init__(self, quaking):
        self.quaking = quaking

    def point(self, *args, **kwargs):
        return self.quaking.obj_engine.point(*args, **kwargs)

    def line(self, *args, **kwargs):
        return self.quaking.obj_engine.line(*args, **kwargs)

    def ellipse(self, *args, **kwargs):
        return self.quaking.obj_engine.ellipse(*args, **kwargs)

    def circle(self, x, y, diameter, stroke_color=None, stroke_weight=None, fill_color=None):
        return self.quaking.obj_engine.circle(x, y, diameter, stroke_color=stroke_color, stroke_weight=stroke_weight,
                                              fill_color=fill_color)

    def arc(self, x, y, rw, rh, ts, te, stroke_color=None, stroke_weight=None, fill_color=None, mode=0):
        return self.quaking.obj_engine.arc(x, y, rw, rh, ts, te, stroke_color=stroke_color, stroke_weight=stroke_weight,
                                           fill_color=fill_color, mode=mode)

    def quad(self, *args, **kwargs):
        return self.quaking.obj_engine.quad(*args, **kwargs)

    def rect(self, *args, **kwargs):
        return self.quaking.obj_engine.rect(*args, **kwargs)

    def square(self, *args, **kwargs):
        return self.quaking.obj_engine.square(*args, **kwargs)

    def triangle(self, *args, **kwargs):
        return self.quaking.obj_engine.triangle(*args, **kwargs)
