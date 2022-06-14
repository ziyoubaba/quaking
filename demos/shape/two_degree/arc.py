
import math
from quaking import Quaking


HALF_PI = math.pi * 0.5
PI = math.pi
QUARTER_PI = math.pi * 0.25
TWO_PI = math.pi * 2

def main():
    app = Quaking(100,100)

    def setup():
        app.size(200, 200)
        app.fill(255, 255, 255)
        # app.arc(50, 55, 50, 50, 0, HALF_PI)
        app.arc(50, 55, 50, 25, 0, HALF_PI)
        app.noFill()
        # app.arc(50, 55, 60, 60, HALF_PI, PI)
        # app.arc(50, 55, 70, 70, PI, PI + QUARTER_PI)
        # app.arc(50, 55, 80, 80, PI + QUARTER_PI, TWO_PI)
        app.arc(50, 55, 60, 30, HALF_PI, PI)
        app.arc(50, 55, 70, 30, PI, PI + QUARTER_PI)
        app.arc(50, 55, 80, 40, PI + QUARTER_PI, TWO_PI)
        # app.circle(56, 46, 55)
        # app.point(56, 46)
        # app.arc(app.width/2, app.height/2, 50, 50, 0, PI+QUARTER_PI)
        # app.noFill()
        # app.arc(app.width/2, app.height/2, 60, 60, HALF_PI, PI)
        # app.arc(app.width/2, app.height/2, 70, 70, PI, PI + QUARTER_PI)
        # app.arc(app.width/2, app.height/2, 80, 80, PI + QUARTER_PI, TWO_PI)
        # app.arc(app.width/2, app.height/2, 80, 80, 0, PI + QUARTER_PI, mode=0)

    def draw():
        if app.mouse_pressed:
            app.point(app.mouseX, app.mouseY, stroke_weight=1)

    app.run( setup, draw )

if __name__ == '__main__':
    main()