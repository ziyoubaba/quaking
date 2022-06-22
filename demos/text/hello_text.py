from quaking import Quaking
import math

def main():
    app = Quaking(200,200)

    def setup():
        app.obj_engine.text("ABC 他一个人", 50, 50, 1, )
        pass
    def draw():
        # app.obj_engine.text("ABC", 50, 50, 1, )
        if app.mouse_pressed:
            app.point(app.mouseX, app.mouseY, stroke_weight=1)

    app.run( setup, draw )

if __name__ == '__main__':
    main()