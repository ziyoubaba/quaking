import sys
from quaking import Quaking

def main():
    app = Quaking()

    def setup():
        app.frame_rate(1)
        # app.full_screen()

    def draw():
        # print(app.frame_count, app.width, app.height)
        if app.frame_count == 5:
            app.full_screen()
        elif app.frame_count == 10:
            app.full_screen()
        elif app.frame_count == 11:
            sys.exit(0)

    app.run( setup, draw )

if __name__ == '__main__':
    main()