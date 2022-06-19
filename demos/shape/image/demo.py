from quaking import Quaking
from PIL import Image

def main():
    app = Quaking(800, 800)

    def setup():
        # app.stroke(0,0,0)
        # app.strokeWeight(1)
        app.fps = 10
        im = app.obj_engine.load_image('./img.png')
        # im = im.transpose(Image.FLIP_TOP_BOTTOM)
        # print(im,dir(im))
        # print(im.tobytes())
        app.obj_engine.image(im, 0,0,400, 400)
        app.obj_engine.image_light(im, 400, 0, 400, 400)


    def draw():
        # app.background(0,0,0,10)

        pass


    app.run( setup, draw )

if __name__ == '__main__':
    main()