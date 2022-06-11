from quaking import Quaking

def main():
    app = Quaking()

    def setup():
        app.size(200, 200)
        app.strokeWeight(5)
        app.point(0, 0)

    def draw():
        if app.mouseX < 100:
            app.cursor(app.MOUSE_VRESIZE)
        else :
            app.cursor(app.MOUSE_HAND)
    app.run( setup, draw )

if __name__ == '__main__':
    main()