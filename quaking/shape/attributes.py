
class ShapeAttributes():
    def __init__(self, quaking):
        self.quaking = quaking

    def strokeWeight(self, *args, **kwargs):
        return self.quaking.obj_engine.strokeWeight(*args, **kwargs)

    # def strokeJoin(self, *args, **kwargs):
    #     return self.quaking.obj_engine.strokeJoin(*args, **kwargs)
    #
    # def ellipse(self, *args, **kwargs):
    #     return self.quaking.obj_engine.ellipse(*args, **kwargs)
    #
    # def circle(self, *args, **kwargs):
    #     return self.quaking.obj_engine.circle(*args, **kwargs)
    #
    # def arc(self, *args, **kwargs):
    #     return self.quaking.obj_engine.arc(*args, **kwargs)
    #
    # def quad(self, *args, **kwargs):
    #     return self.quaking.obj_engine.quad(*args, **kwargs)
    #
    # def rect(self, *args, **kwargs):
    #     return self.quaking.obj_engine.rect(*args, **kwargs)
    #
    # def square(self, *args, **kwargs):
    #     return self.quaking.obj_engine.square(*args, **kwargs)
    #
    # def triangle(self, *args, **kwargs):
    #     return self.quaking.obj_engine.triangle(*args, **kwargs)