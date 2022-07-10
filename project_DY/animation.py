# -*- coding:utf-8 -*-
import random, cv2
import traceback, shutil

import numpy as np
from quaking import Quaking
from project_DY.pre_handler import PreHandler
from project_DY.later_handler import LaterHandler
from project_DY.title import TitleHandler
from PIL import Image, ImageOps
from quaking.pvector import PVector
from quaking.basic.engine.font_v6 import face, init_font
from freetype import *

do_glow = True
do_points = True

class Point():
    def __init__(self, pos_x, pos_y, x, y, ):
        # self.x = x
        # self.y = y
        # self.pos_x = pos_x
        # self.pos_y = pos_y
        self.target = PVector(x, y)
        self.pos = PVector(pos_x, pos_y)

    def calc_new_pos(self, amt=0.1):
        if self.pos.dist(self.target)>2:
            self.pos = self.pos.lerp(self.target, amt=amt)
        else:
            self.pos = self.target

class StarFlash():
    def __init__(self, pos_x, pos_y, dir_x, dir_y):
        self.pos = PVector(pos_x, pos_y)
        self.dir = PVector(dir_x, dir_y)

    def calc_new_pos(self, amt=0.1):
        self.pos = self.pos + self.dir


class Animation:
    def __init__(self, filepath, title='', w=720, h=1280, fps=10, title_font_size=32, dir_=''):
        """
        视频尺寸一般为宽高9：16的比例，分辨率为540*960。也可以使用更高分辨率的视频，例如720/1280、1080/1920等。
        :param w:
        :param h:
        """
        self.app = Quaking(w, h, swap_buffer=True)
        self.im = PreHandler().handler(filepath)
        self.pos_x, self.pos_y, self.im_w, self.im_h = self.ana_img()
        self.title = title
        self.dir = dir_ or title
        # self.title_len = TitleHandler().calc_text_width(title)
        # 计算文字的大小 - 标题宽度最大为一半 最大为32
        self.title_font_size = title_font_size
        # self.title_font_size = self.calc_title_font()
        self.title_width, self.title_height = self.calc_title_size()
        self.title_pos_x, self.title_pos_y = self.ana_title(self.title_width, )
        self.fps = fps
        # print(self.title_font_size, self.title_pos_x, self.title_pos_y, self.title_width)

    # def calc_title_font(self):
    #     max_len =  int (self.app.width * 1/2/len(self.title))
    #     return min(max_len, 24)

    def calc_title_size(self):
        width, height, ascender, descender = init_font(self.title_font_size)
        return width*(len(self.title)), height

    def ana_title(self, title_width, padding_y=10):
        # 1 使图片居中
        pos_x = int((self.app.width - title_width) / 2)
        header_height = int((self.app.height - self.im_h)/2)
        pos_y = (header_height - self.title_height) / 2
        return (pos_x, pos_y)

    def ana_img(self, padding_x=100, padding_y=300):
        # 1 使图片居中
        im_w, im_h = self.im.size
        # self.app.width, self.app.height
        x_rad = (self.app.width - 2 * padding_x) / im_w
        y_rad = (self.app.height - 2 * padding_y) / im_h
        rad = min(x_rad, y_rad)
        self.im = self.im.resize((int(im_w * rad), int(im_h * rad)))
        # print(im_w, im_h, x_rad, y_rad, rad, self.im.size)
        # 图片居中分布 - 获取 图片左上角坐标和长宽
        im_w, im_h = self.im.size
        pos_x = int((self.app.width - im_w) * 0.5)
        pos_y = int((self.app.height - im_h) * 0.5)
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
                points.append((random.randint(0, self.app.width), random.randint(0, self.app.height)))
        return points

    def get_star_flash_points(self, num=100, outershape=False):
        points = []
        for i in range(num):
            choice = random.randint(0, 1)
            if choice:
                x = 0
                dir_x = random.random() * 20
            else:
                x = self.app.width
                dir_x = random.random() * -1 * 20
            y = random.randint(0, self.app.height)
            dir_y = random.random() * random.choice((-1, 1))
            points.append(StarFlash(x, y, dir_x, dir_y))
        return points

    def split_points(self, points):
        splited_points = []
        for point in points:
            splited_points.append(Point(
                random.randint(0, self.app.width), random.randint(0, self.app.height), *point
            ))
        return splited_points

    def update_split_points(self):
        for point in self.splited_shape_points:
            point.calc_new_pos()

    def update_flash_points(self):
        points = []
        for point in self.star_points_flash:
            point.calc_new_pos()
            points.append((point.pos.x, point.pos.y))
        return points

    def init_stroke_color(self):
        self.stroke_color = [random.randint(120, 255), random.randint(100, 255), random.randint(100, 255), 255]
        # color = random.randint(0, 2)
        # self.stroke_color[color] = 255

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
        self.app.frame_rate(self.fps)
        self.app.background(0, 0, 0, 255)
        self.app.image(self.im, self.pos_x, self.pos_y, self.im_w, self.im_h)
        self.app.load_pixels()  # 加载像素
        self.shape_points = self.get_shape_points()
        self.star_points = self.get_star_points(num=1000)
        self.points = self.star_points + self.shape_points
        self.splited_shape_points = self.split_points(self.shape_points)
        # self.stroke_color = (0, 0, 0, 255)
        self.init_stroke_color()
        self.set_color_mode(1)  # 1上升 0下降

        self.star_striper = -1   # 星星闪烁间隔
        self.star_points_shining = []   # 正在闪烁的星星
        self.star_points_flash = self.get_star_flash_points(100)

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
                if self.stroke_color[i] > 150:
                    self.stroke_color[i] -= 2
                    status = True
                    break
        # print(self.stroke_color, self.color_mode, status)
        if not status:
            self.switch_color_mode()
        self.get_background()

        if do_points:
            # self.app.background(*self.background_color)

            # 星星慢点闪烁
            if int(self.app.frame_count / 3) != self.star_striper:
                self.star_points_shining = random.sample(self.star_points, int(len(self.star_points) * (99 / 100)))
                self.star_striper = int(self.app.frame_count / 10)
            if(self.star_points_shining):
                self.app.points(self.star_points_shining, stroke_color=self.stroke_color)
            # shape_points = self.shape_points[: self.app.frame_count * 10]
            # if self.app.frame_count < len(self.shape_points):
            #     shape_points = random.sample(self.shape_points, max(self.app.frame_count, 1000))
            # else:
            #     shape_points = self.shape_points
            # self.app.points(shape_points, stroke_color=self.stroke_color)
            # self.app.points(self.shape_points, stroke_color=self.stroke_color)

            # 绘制流星
            # flash_stars = self.update_flash_points()
            # # print(flash_stars)
            # self.app.points(flash_stars, stroke_color=self.stroke_color)

            # 方案4
            self.update_split_points()
            # 展示星星
            shape_points = [(point.pos.x, point.pos.y) for point in self.splited_shape_points]
            self.app.points(shape_points, stroke_color=self.stroke_color)

        # title
        self.app.obj_engine.text(self.title, size=self.title_font_size, x=self.title_pos_x, y=self.title_pos_y,
                                 color=self.stroke_color
                                 )

        # glow_params['weight_beta'] = sum(self.stroke_color) / (255 * 4)
        if do_glow:
            glow_params = {
                "ksize": 11,
                "sigmaX": 0,
                "sigmaY": 0,
                "weight_alpha": 1,
                "weight_beta": 1,
                "weight_gamma": 0
            }
            # do glow
            # 使用opencv进行glow操作
            self.app.load_pixels()
            # opengl -> opencv
            image = Image.frombytes("RGBA", (self.app.obj_window.pixels_w, self.app.obj_window.pixels_h),
                                    self.app.obj_window.pixels)
            image = ImageOps.flip(image)
            # image.show()
            cv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
            # cv2.imshow(f'CV frame {self.app.frame_count}', cv_image)
            # cv2.waitKey()
            # opencv -> opengl
            glowd_img = LaterHandler().glow(cv_image, **glow_params)
            # 写入到视频
            if 0< self.app.frame_count <= self.video_frame_count:
                print(f"++ frame: {self.app.frame_count}")
                self.video_writer.write(glowd_img)
            elif not self.video_ok:
                self.video_ok = True
                print("video Ok")
            if self.video_ok and not self.thumb_ok and (self.stroke_color[:3]) == [255, 255, 255]:
                # 创建封面图片
                cv2.imwrite(self.thumb_path, glowd_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
                self.thumb_ok = True
                print("thumb ok")
            if self.video_ok and self.thumb_ok:
                print("Done")
                raise RuntimeError

            # cv2.imshow("raw3", glowd_img)
            tx_image = cv2.flip(glowd_img, 0)
            tx_image = Image.fromarray(tx_image)
            ix = tx_image.size[0]
            iy = tx_image.size[1]
            tx_image = tx_image.tobytes('raw', 'BGR', 0, -1)
            # print(ix, iy, self.app.obj_window.pixels_w, self.app.obj_window.pixels_h)
            self.app.image(tx_image, 0, 0, ix, iy)
        # else:


    def run(self, video_seconds=20):
        # self.pos_x, self.pos_y, self.im_w, self.im_h = self.ana_img()
        # print(pos_x, pos_y, im_w, im_h)
        # 生成video 和 封面
        # 检查路径
        dir_name = os.path.join("outputs", self.dir)
        if os.path.exists(dir_name):
            print("文件夹已经存在 检查一下")
            go = input("是否继续?")
            if go.upper() == "Y":
                shutil.rmtree(dir_name)
                os.makedirs(dir_name)
            else:
                return
        else:
            os.makedirs(dir_name)
        # 视频 图片数字
        self.video_frame_count = video_seconds * self.fps
        # 创建视频文件
        video_path = os.path.join(dir_name, f"{self.title}.mp4")
        thumb_path = os.path.join(dir_name, f"{self.title}.png")
        fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")    # mp4
        self.video_writer = cv2.VideoWriter(video_path, fourcc, self.fps, (self.app.width, self.app.height) )
        # 写入视频
        self.video_ok = False
        self.thumb_ok = False
        self.info_ok = False
        self.thumb_path = thumb_path
        try:
            self.app.run(self.setup, self.draw)
        except RuntimeError:
            print("finished")
            print()
        except:
            traceback.print_exc()
        finally:
            self.video_writer.release()

if __name__ == '__main__':
    Animation("./imgs/demo.png", 'TestDemo', w=540, h=960, fps=30).run()
    # Animation("./imgs/demo.png", 'Test Demo', w=270, h=480).run()
