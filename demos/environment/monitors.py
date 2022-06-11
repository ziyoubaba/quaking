from quaking import Quaking

def main():
    app = Quaking()

    def setup():
        # app.obj_window.get_monitors()
        print(app.display_width, app.display_height)
    def draw():
        pass

    app.run( setup, draw )

if __name__ == '__main__':
    main()