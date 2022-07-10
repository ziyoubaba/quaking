# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFilter

class PreHandler:
    def __init__(self):
        pass

    # 1 读取图片 并将图片中的两种颜色对调
    def load_img(self, filepath):
        im = Image.open(filepath)
        # return im
        # print(im.mode)
        if im.mode == "RGBA":
            image = Image.new('RGB', size=(im.width, im.height), color=(255, 255, 255))
            image.paste(im, (0, 0), mask=im)
            im.close()
            return image
        else:
            return im

    def get_pixels(self, im):
        pixels = im.load()
        return pixels

    def get_gray_avg_pixels(self, im):
        # 转化为灰度
        grays = []
        width, height = im.size
        for x in range(width):
            for y in range(height):
                gray = im.getpixel((x, y))
                # print((x, y), pix)
                grays.append(gray)
        return int(sum(grays)/len(grays)) if grays else 0

    def crop_img(self, im, gray_avg):
        width, height = im.size
        # pixels = self.get_pixels(im)
        minx, miny, maxx, maxy = float("inf"), float("inf"), 0, 0
        for x in range(width):
            for y in range(height):
                gray = im.getpixel((x, y))
                # print((x, y), gray)
                if self.is_point(gray, gray_avg):
                    minx = min(minx, x)
                    miny = min(miny, y)
                    maxx = max(maxx, x)
                    maxy = max(maxy, y)
        box = (max(minx-2, 0), max(miny-2, 0), min(maxx+2, width), min(maxy+2, height))
        # print(box)
        im_crop = im.crop(box)
        # im_crop.show()
        return im_crop

    # 2 将图片转化为一个特殊的像素 是点的地方转化为 (254, 254, 254, )
    def transfer_img(self, im, gray_avg):
        width, height = im.size
        new_im = Image.new("RGBA", (width, height), color="#0000")
        draw = ImageDraw.Draw(new_im)
        for x in range(width):
            for y in range(height):
                pix = im.getpixel((x, y))
                # print((x, y), pix)
                if self.is_point(pix, gray_avg):
                    draw.point((x, y), (1, 1, 1, 255))
        # new_im.show()
        return new_im

    # def is_point(self, pix, r=200,g=200,b=200):
    #     try:
    #         if pix[3] < 10:
    #             return False
    #     except:
    #         pass
    #     return sum(pix[:3]) < (r+g+b)

    def is_point(self, gray, gray_avg):
        return gray < gray_avg

    def handler(self, filepath):
        im = self.load_img(filepath)
        # im.show()
        im_gray = im.convert("L")
        # im_gray.show()
        gray_avg = self.get_gray_avg_pixels(im_gray)
        im_new = self.crop_img(im_gray, gray_avg)
        im_finally = self.transfer_img(im_new, gray_avg)
        im_finally.filter(ImageFilter.SMOOTH_MORE)
        # im_finally.show()
        print("图片处理完毕...")
        return im_finally

if __name__ == '__main__':
    PreHandler().handler("./imgs/swastika.jpg")
