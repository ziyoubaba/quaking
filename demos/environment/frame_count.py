from quaking import Quaking

def main():
    app = Quaking()

    def setup():
        # app.obj_window.get_monitors()
        app.frame_rate(30)
    def draw():
        app.line(0, 0, app.width, app.height)
        print(app.frame_count)

    app.run( setup, draw )

if __name__ == '__main__':
    main()