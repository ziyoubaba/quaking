from quaking import Quaking


def main():
    app = Quaking(400,400)

    def setup():
        im = app.obj_engine.load_image('../shape/image/image.jpg')

        # app.obj_engine.text("ABC ", 50, 50, 1, )
        # app.line(0, 0, 50, 50)  #
        # app.noFill()
        # app.image(im, 0, 50, 100, 100)
        # app.ellipse(70, 0, 50, 50)

        # app.point(0, 0)  #
        # app.image(im, 0, 50, 100, 100)
        # app.image(im, 150, 50, 100, 100)
        app.obj_engine.text("ABC ", 0, 50,  )
        # app.obj_engine.text("ABC ", 100, 50, 1, )
        # app.rect(0, 0, 50, 50)

    def draw():
        # app.obj_engine.text("ABC", 50, 50, 1, )
        if app.mouse_pressed:
            app.point(app.mouseX, app.mouseY, stroke_weight=1)

    app.run( setup, draw )

if __name__ == '__main__':
    main()