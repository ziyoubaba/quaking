import random
import sys
from quaking import Quaking

def demo1():
    app = Quaking()

    def setup():
        app.background(100, 0, 0)
        app.frame_rate(10)

    def draw():
        app.background(random.randint(50, 100), random.randint(50, 100), random.randint(50, 100))
        # app.size(random.randint(50, 100), random.randint(50, 100))

    app.run( setup, draw )

def demo2():
    app = Quaking(100, 200)

    def setup():
        app.background(255, 255, 255)
        app.frame_rate(10)

    def draw():
        # app.background(random.randint(50, 100), random.randint(50, 100), random.randint(50, 100))
        # app.size(random.randint(50, 100), random.randint(50, 100))
        app.point(random.randint(50, 100), random.randint(50, 100))
        app.point(app.mouseX, app.mouseY)

    app.run( setup, draw )

if __name__ == '__main__':
    demo2()