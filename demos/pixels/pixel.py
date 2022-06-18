from quaking import Quaking
import math

def main():
    app = Quaking(200, 50)

    def setup():
        # app.translate(app.width/2, app.height/2)
        # app.rotate(math.pi/3.0)
        # app.rect(-26, -26, 52, 52)
        # app.obj_window.read_gl_pixels()
        # print(app.obj_window.pixels)
        # pixels = app.obj_window.pixels
        # print(len(pixels))
        # print(app.width, app.height, app.width * app.height)
        # app.no_smooth()
        # app.strokeWeight(5)
        app.stroke( 200, 0, 0,255)
        # app.point(100, 26, )
        # app.point(0, 0)
        # app.point(1, 0)
        # app.point(0, 1)
        # app.point(1, 1)
        app.point(0, 0)
        app.point(1,1)
        app.point(0, 1)
        app.point(0, 10, )
        app.point(100, 40)
        # app.line(0,0, 100, 25)
        app.obj_window.load_pixels()
        # result = app.obj_window.pixel(50, 49)
        # result = app.obj_window.pixel(0, 0)
        # result = app.obj_window.pixel(100, 25)
        # print(result)
        points = 0

        for y in range(app.height):
            for x in range(app.width):
                points += 1
                color = app.obj_window.pixel(x, y)
                # if color[1] == color[2] == 0:
                print(x, y, color, points)
        # print(points)
        # print((0, 0), app.obj_window.pixel(0, 0))
        print(len(app.obj_window.pixels )/4, app.obj_window.pixels_w, app.obj_window.pixels_h, app.obj_window.pixels_w*app.obj_window.pixels_h)


    def draw():
        # if app.mouse_pressed:
        #     app.point(app.mouseX, app.mouseY, stroke_weight=1)
        pass

    app.run( setup, draw )

if __name__ == '__main__':
    main()