#-*- coding:utf-8 -*-


"""
By:
Time:
Intro:

"""
import cv2

class LaterHandler:
    def __init__(self):
        pass

    # 1 glow
    def glow(self, img, ksize=11, sigmaX=1, sigmaY=1, weight_alpha=1, weight_beta=1, weight_gamma=0):
        img_blurred = cv2.GaussianBlur(img, (ksize, ksize), sigmaX, sigmaY)
        # cv2.imshow("raw1", img)
        img_blurred = cv2.blur(img_blurred, ksize=(ksize, ksize))
        # cv2.imshow("raw2", img)
        # help(cv2.blur)
        # 合并图片
        img_blurred = cv2.addWeighted(img, weight_alpha, img_blurred, weight_beta,
                                      weight_gamma)  # dst = src1*alpha + src2*beta + gamma;
        # cv2.imshow("raw3", img)
        # help(cv2.addWeighted)
        # print(weight_alpha)
        # cv2.imshow('Test', cv2.cvtColor(img_blurred, cv2.COLOR_RGB2BGR))
        # cv2.waitKey()
        return img_blurred