from math import pi


class Transform():
    def __init__(self, quaking):
        self.quaking = quaking

    def translate(self, x, y, z=0):
        return self.quaking.obj_engine.translate(x, y, z)

    def rotate(self, radian, x=0, y=0, z=1):
        degree = 180/pi * radian
        return self.quaking.obj_engine.rotate(degree, x, y, z)

    def rotate_x(self, radian):
        return self.rotate(radian, 1, 0, 0)

    def rotate_y(self, radian):
        return self.rotate(radian, 0, 1, 0)

    def rotate_z(self, radian):
        return self.rotate(radian, 0, 0, 1)