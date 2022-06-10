#-*- coding:utf-8 -*-


"""
By:
Time:
Intro:

"""
import math
import random

class PVector(object):
    def __init__(self, x, y, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return PVector( self.x+other.x, self.y+other.y, self.z+other.z )

    def __sub__(self, other):
        return PVector( self.x-other.x, self.y-other.y, self.z-other.z )

    def __mul__(self, numer):
        # 向量积
        return PVector( self.x * numer, self.y * numer, self.z * numer )

    def __divmod__(self, numer):
        # 除法
        return PVector(self.x / numer, self.y / numer, self.z / numer)

    def dist(self, other):
        return  ( (self.x - other.x) ** 2 +
                  (self.y - other.y) ** 2 +
                  (self.z - other.z) ** 2 ) ** 0.5

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def random2D(cls):
        x = 2 * (random.random() ) - 1
        y = random.choice((-1, 1)) * (1-x**2) ** 0.5
        return PVector(x, y, 0)

    @classmethod
    def random3D(cls):
        x = 2 * (random.random()) - 1
        y = 2 * (random.random()) - 1
        z = random.choice((-1, 1)) * (1 - x**2 - y**2) ** 0.5
        return PVector(x, y, z)

    @classmethod
    def fromAngle(cls, angle):
        #  Calculates and returns a new 2D unit vector from the specified angle value (in radians 弧度制).
        return PVector( math.cos(angle), math.sin(angle) )

    def mag(self):
        # sqrt(x * x + y * y + z * z).)
        return (  (self.x ) ** 2 +
                  (self.y ) ** 2 +
                  (self.z ) ** 2 ) ** 0.5

    def magSq(self):
        return ((self.x) ** 2 +
                (self.y) ** 2 +
                (self.z) ** 2)

    def dot(self, other):
        # 点积
        return (self.x * other.x +
                self.y * other.y +
                self.z * other.z)

    def cross(self, other):
        # 叉积
        return PVector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def array(self):
        return [self.x, self.y, self.z]

    def normalize(self):
        mag = self.mag()
        if mag:
            return PVector(self.x/mag, self.y/mag, self.z/mag)
        else:
            return PVector(0, 0, 0)

    def limit(self, max_numer):
        mag = self.mag()
        if mag:
            numer = min(max_numer, mag)
            return PVector(self.x/mag * numer, self.y/mag * numer, self.z/mag * numer)
        else:
            return PVector(0, 0, 0)

    def setMag(self, numer):
        return self.normalize() * numer

    def heading(self):
        return math.atan2(self.y, self.x)

    def rotate(self, theta):
        """
        # 2D
        :param theta:
        :return:
        """
        return PVector(
            self.x * math.cos(theta) - self.y * math.sin( theta),
            self.x * math.sin(theta) + self.y * math.cos( theta),
            self.z
        )

    def lerp(self, other, amt=0.5):
        """
        :param other: a other PVector Obj
        :param amt:  PVector: the vector to lerp to
amt	float: The amount of interpolation; some value between 0.0 (old vector) and 1.0 (new vector). 0.1 is very near the old vector; 0.5 is halfway in between.
        :return:
        """
        return PVector(
            self.x + (other.x - self.x ) * amt,
            self.y + (other.y - self.y ) * amt,
            self.z + (other.z - self.z ) * amt,
        )

    def angleBetween(self, other):
        dot_num = self.dot( other )

        mag_self = self.mag()
        mag_other = other.mag()
        mul_mag = mag_self * mag_other
        if mul_mag:
            cos_theta = dot_num / mul_mag
            return math.acos( cos_theta )   # 弧度
        else:
            return 0


if __name__ == '__main__':
    a = PVector(10, 20)
    b = PVector(60, 80)
    c = a + b
    d = a - b
    print(c.x, c.y, c.z)
    print(a.x, a.y, a.z)
    print(b.x, b.y, b.z)
    print(d.x, d.y, d.z)
    print(a.dist(b))
    print(PVector(20, 30, 40).mag())
    print(PVector(20, 30, 40).magSq())
    print(PVector(10, 20, 0).dot(PVector( 60, 80, 0 )))
    e = PVector(10, 20, 2).cross(PVector( 60, 80, 6 ))
    print( e.array() )
    print(PVector( 10, 20, 2 ).normalize().array())
    print(PVector( 10, 20, 2 ).limit(100).array())
    print(PVector( 3, 4, 0 ).limit(10).array())
    print(PVector( 10.0, 20.0, 0 ).heading())
    # print(math.pi)
    print(PVector( 10.0, 20.0, 0 ).rotate( math.pi / 2 ).array())
    print(PVector( 10.0, 20.0, 0 ).rotate( 90).array())
    print(PVector( 0.0, 0.0, 0 ).lerp( PVector(100.0, 100.0, 0)).array() )
    print(PVector( 10.0, 20.0, 0 ).angleBetween( PVector(60, 80, 0)) )
    print(PVector.fromAngle( 0.01 ).array() )
    print(PVector.random2D( ).array() )
    print(PVector.random3D( ).array() )
    _sum = 0
    for i in PVector.random3D().array():
        _sum += i ** 2
    print(_sum)

