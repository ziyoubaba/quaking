from quaking import Quaking
import math

def main():
    app = Quaking(100,100)

    def setup():
        app.translate(app.width/2, app.height/2)
        app.rotate(math.pi/3.0)
        app.rect(-26, -26, 52, 52)

    def draw():
        if app.mouse_pressed:
            app.point(app.mouseX, app.mouseY, stroke_weight=1)

    app.run( setup, draw )

if __name__ == '__main__':
    main()