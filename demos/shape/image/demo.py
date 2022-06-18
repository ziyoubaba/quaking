from quaking import Quaking
from PIL import Image

def main():
    app = Quaking(800, 800)

    def setup():
        # app.stroke(0,0,0)
        # app.strokeWeight(1)
        app.fps = 10
        im = app.obj_engine.load_image('./image.jpg')
        # im = im.transpose(Image.FLIP_TOP_BOTTOM)
        # print(im,dir(im))
        # print(im.tobytes())
        app.obj_engine.image(im, 100,100,200, 200)


    def draw():
        app.background(0,0,0,10)

    app.run( setup, draw )

if __name__ == '__main__':
    main()