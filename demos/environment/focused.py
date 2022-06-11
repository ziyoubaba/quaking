
from quaking import Quaking

def main():
    app = Quaking()

    def setup():
        pass
        # app.obj_window.get_monitors()
        # print(app.display_width, app.display_height)
    def draw():
        app.background(255,255,255)
        if (app.focused):
            app.ellipse(25, 25, 50, 50)
        else:
            app.line(0, 0, 100, 100)
            app.line(100, 0, 0, 100)

    app.run( setup, draw )

if __name__ == '__main__':
    main()