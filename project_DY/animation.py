# -*- coding:utf-8 -*-
import random, cv2
import numpy as np
from quaking import Quaking
from project_DY.pre_handler import PreHandler
from project_DY.later_handler import LaterHandler
from PIL import Image, ImageOps

class Animation:
    def __init__(self, filepath, w=720, h=1280):
        """
        视频尺寸一般为宽高9：16的比例，分辨率为540*960。也可以使用更高分辨率的视频，例如720/1280、1080/1920等。
        :param w:
        :param h:
        """
        self.app = Quaking(w, h, swap_buffer=True)
        self.im = PreHandler().handler(filepath)
        self.pos_x, self.pos_y, self.im_w, self.im_h = self.ana_img()

    def ana_img(self, padding_x=30, padding_y=54):
        # 1 使图片居中
        im_w, im_h = self.im.size
        # self.app.width, self.app.height
        x_rad = (self.app.width - 2*padding_x)/im_w
        y_rad = (self.app.height- 2*padding_y)/im_h
        rad = min(x_rad, y_rad)
        self.im = self.im.resize( (int(im_w*rad), int(im_h*rad)))

        # print(im_w, im_h, x_rad, y_rad, rad, self.im.size)
        # 图片居中分布 - 获取 图片左上角坐标和长宽
        im_w, im_h = self.im.size
        pos_x = int((self.app.width-im_w) * 0.5 )
        pos_y = int((self.app.height-im_h) * 0.5 )
        return (pos_x, pos_y, im_w, im_h)

    def get_shape_points(self):
        points = []
        for x in range(self.pos_x, self.pos_x + self.im_w + 1):
            for y in range(self.pos_y, self.pos_y + self.im_h):
                pixel = self.app.pixel(x, y)
                # print((x, y), pixel)
                if 1 < sum(pixel[:3]) < 10:
                    points.append((x, y))
        return points

    def get_star_points(self, num=100, outershape=False):
        points = []
        if outershape:
            pass
        else:
            for i in range(num):
                points.append( (random.randint(0, self.app.width), random.randint(0, self.app.height)))
        return points

    def init_stroke_color(self):
        self.stroke_color = [random.randint(150, 255), random.randint(150, 255), random.randint(150, 255), 255]
        color = random.randint(0, 2)
        self.stroke_color[color] = 255

    def get_background(self):
        self.background_color = (
            255 - self.stroke_color[0],
            255 - self.stroke_color[1],
            255 - self.stroke_color[2],
            255
        )

    def set_color_mode(self, mode):
        self.color_mode = mode

    def switch_color_mode(self):
        color_mode = 1 - self.color_mode
        self.set_color_mode(color_mode)

    def setup(self):
        self.app.no_smooth()
        self.app.frame_rate(20)
        self.app.background(0, 0, 0, 255)
        self.app.image(self.im, self.pos_x, self.pos_y, self.im_w, self.im_h)
        self.app.load_pixels()  # 加载像素
        self.shape_points = self.get_shape_points()
        self.star_points = self.get_star_points(num=1000)
        self.points = self.star_points + self.shape_points
        # self.stroke_color = (0, 0, 0, 255)
        self.init_stroke_color()
        self.set_color_mode(1)  # 1上升 0下降

    def draw(self):
        self.app.clear()
        # self.app.background(0,0,0,255)
        # self.app.background(255, 255, 255, 100)
        # 方案1
        # 赋予 每一个节点不同的颜色
        # counter = 0
        # for x, y in self.points:
        #     # 花点
        #     if counter == 0:
        #         color = random.randint(0, 2)
        #         stroke_color = [random.randint(100, 200), random.randint(100, 200), random.randint(100, 200), 255]
        #         stroke_color[color] = 255
        #     elif counter < 100:
        #         counter += 1
        #     else:
        #         counter = 0
        #     # stroke_color = [255, 255, 255, 255]
        #     self.app.point(x=x, y=y, stroke_color=stroke_color)

        # # 方案2
        # if self.app.frame_count % 10 == 0:
        #     color = random.randint(0, 2)
        #     self.stroke_color = [random.randint(100, 200), random.randint(100, 200), random.randint(100, 200), 255]
        #     self.stroke_color[color] = 255
        # self.app.points(self.points, stroke_color=self.stroke_color)

        # 方案3
        status = False
        for i in range(len(self.stroke_color) - 1):
            if self.color_mode == 1:
                if self.stroke_color[i] < 255:
                    self.stroke_color[i] += 1
                    status = True
                    break
            else:
                if self.stroke_color[i] > 220:
                    self.stroke_color[i] -= 1
                    status = True
                    break
        # print(self.stroke_color, self.color_mode, status)
        if not status:
            self.switch_color_mode()
        self.get_background()
        self.app.background(*self.background_color)

        self.app.points(self.star_points, stroke_color=self.stroke_color)
        self.app.points(self.shape_points, stroke_color=self.stroke_color)
        glow_params = {
            "ksize": 11,
            "sigmaX": 0,
            "sigmaY": 0,
            "weight_alpha": 1,
            "weight_beta": 1,
            "weight_gamma": 0
        }
        # glow_params['weight_beta'] = sum(self.stroke_color) / (255 * 4)

        # do glow
        # 使用opencv进行glow操作
        self.app.load_pixels()
        # opengl -> opencv
        image = Image.frombytes("RGBA", (self.app.obj_window.pixels_w, self.app.obj_window.pixels_h), self.app.obj_window.pixels)
        image = ImageOps.flip(image)
        # image.show()
        cv_image = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
        # cv2.imshow(f'CV frame {self.app.frame_count}', cv_image)
        # cv2.waitKey()
        # opencv -> opengl
        glowd_img = LaterHandler().glow(cv_image, **glow_params)
        tx_image = cv2.flip(glowd_img, 0)
        tx_image = Image.fromarray(tx_image)
        ix = tx_image.size[0]
        iy = tx_image.size[1]
        tx_image = tx_image.tobytes('raw', 'BGR', 0, -1)
        # print(ix, iy, self.app.obj_window.pixels_w, self.app.obj_window.pixels_h)
        self.app.image(tx_image, 0, 0, ix, iy)


    def run(self):
        # self.pos_x, self.pos_y, self.im_w, self.im_h = self.ana_img()
        # print(pos_x, pos_y, im_w, im_h)
        self.app.run( self.setup, self.draw )


if __name__ == '__main__':
    # Animation("./imgs/demo.png", 540, 960).run()
    Animation("./imgs/demo.png", 270, 480).run()