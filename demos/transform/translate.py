from quaking import Quaking


def main():
    app = Quaking(100,100)

    def setup():
        # app.stroke(0,0,0)
        # app.strokeWeight(1)
        # print(app.obj_engine.fill_color)
        # print(app.obj_engine.stroke_weight)
        # print(app.obj_engine.stroke_color)
        app.rect(0, 0, 55, 55)  # Draw rect at original 0,0
        app.translate(30, 20)
        app.rect(0, 0, 55, 55, stroke_weight=1)  # Draw rect at 0,0
        app.translate(14, 14)
        app.rect(0, 0, 55, 55)  # Draw rect at 0,0

    def draw():
        if app.mouse_pressed:
            app.point(app.mouseX, app.mouseY, stroke_weight=1)

    app.run( setup, draw )

if __name__ == '__main__':
    main()