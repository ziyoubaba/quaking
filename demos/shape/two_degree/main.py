import random
import sys
from quaking import Quaking


def main():
    app = Quaking(100,100)

    def setup():
        # app.stroke(0,0,0)
        # app.strokeWeight(1)
        app.fps = 60

        app.circle(56, 46, 55)
        app.fill(200, 0, 0)
        app.ellipse(56, 46, 55, 28)
        app.line(30, 20, 85, 75)
        app.strokeWeight(5)
        app.point(30, 20)
        app.point(85, 20)
        app.point(85, 75)
        app.point(30, 73)

    def draw():
        # app.background(235, 235, 235, 50)
        # app.clear()
        # print(random.randint(0, 100))
        if app.mouse_pressed:
            app.point(app.mouseX, app.mouseY, stroke_weight=1)
        # app.point(random.randint(0, 100), random.randint(0, 100))

    app.run( setup, draw )

if __name__ == '__main__':
    main()