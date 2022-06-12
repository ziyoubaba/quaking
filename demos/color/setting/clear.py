import random

from quaking import Quaking

def main():
    app = Quaking()

    def setup():
        # app.noCursor()
        app.frame_rate(10)
        app.strokeWeight(3)
        app.stroke(255, 0, 0)

    def draw():
        if app.mouse_pressed:
            app.clear()
        else:
            app.point(random.randint(0, app.width), random.randint(0, app.height))
    app.run( setup, draw )

if __name__ == '__main__':
    main()