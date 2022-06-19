# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw

class PreHandler:
    def __init__(self):
        pass

    # 1 读取图片 并将图片中的两种颜色对调
    def load_img(self, filepath):
        im = Image.open(filepath)
        return im

    def get_pixels(self, im):
        pixels = im.load()
        return pixels

    def crop_img(self, im):
        width, height = im.size
        # pixels = self.get_pixels(im)
        minx, miny, maxx, maxy = float("inf"), float("inf"), 0, 0
        for x in range(width):
            for y in range(height):
                pix = im.getpixel((x, y))
                # print((x, y), pix)
                if self.is_point(pix):
                    minx = min(minx, x)
                    miny = min(miny, y)
                    maxx = max(maxx, x)
                    maxy = max(maxy, y)
        box = (minx-1, miny-1, maxx+1, maxy+1)
        # print(box)
        im_crop = im.crop(box)
        # im_crop.show()
        return im_crop

    # 2 将图片转化为一个特殊的像素 是点的地方转化为 (254, 254, 254, )
    def transfer_img(self, im):
        width, height = im.size
        new_im = Image.new("RGBA", (width, height), color="#0000")
        draw = ImageDraw.Draw(new_im)
        for x in range(width):
            for y in range(height):
                pix = im.getpixel((x, y))
                # print((x, y), pix)
                if self.is_point(pix):
                    draw.point((x, y), (1, 1, 1, 255))
        # new_im.show()
        return new_im

    def is_point(self, pix, r=150,g=150,b=150):
        return sum(pix) < (r+g+b)

    def handler(self, filepath):
        im = self.load_img(filepath)
        im_new = self.crop_img(im)
        im_finally = self.transfer_img(im_new)
        return im_finally

if __name__ == '__main__':
    PreHandler().handler("./imgs/demo.png")
