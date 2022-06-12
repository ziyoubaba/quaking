import random
import sys
from quaking import Quaking


def main():
    app = Quaking(800,800)

    def setup():
        # app.stroke(0,0,0)
        # app.strokeWeight(1)

        app.circle(224, 184, 220)
        app.fill(255, 0, 0)
        app.ellipse(224, 184, 220, 110)
        app.line(120, 80, 340, 300)
        app.strokeWeight(5)
        app.point(120, 80)
        app.point(340, 80)
        app.point(340, 300)
        app.point(120, 300)

    def draw():
        # app.background(235, 235, 235, 235)
        # app.clear()
        print(random.randint(0, 800))
        app.point(random.randint(0, 800), random.randint(0, 800))

    app.run( setup, draw )

if __name__ == '__main__':
    main()