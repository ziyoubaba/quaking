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
    app = Quaking(100, 100)

    def setup():
        app.background(235, 235, 235)
        app.frame_rate(10)
        app.stroke(255,0,0)
        app.strokeWeight(3)

    def draw():
        # app.background(random.randint(50, 100), random.randint(50, 100), random.randint(50, 100))
        # app.size(random.randint(50, 100), random.randint(50, 100))
        app.point(random.randint(50, 100), random.randint(50, 100))
        app.point(app.mouseX, app.mouseY, stroke_color=(0,0,0,255), stroke_weight=2)

    app.run( setup, draw )

if __name__ == '__main__':
    demo2()