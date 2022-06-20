#-*- coding:utf-8 -*-


"""
By:
Time:
Intro:

"""


import cv2
import numpy as np
from typing import Tuple




# cv2.imshow('Test', cv2.cvtColor(img_blended, cv2.COLOR_RGB2BGR))
# cv2.imshow('Test', cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
# cv2.waitKey()
# cv2.imshow('Test', cv2.cvtColor(img_blended, cv2.COLOR_RGB2BGR))
# cv2.waitKey()

# cv2.imwrite('test.jpg', img_blended)
filepath= 'img.png'
img = cv2.imread(filepath, cv2.IMREAD_COLOR)

cv2.imshow("raw", img)

def clamp(pv):  # 保证 RGB三色值的数值不超过255
    if pv > 255:
        return 255
    if pv < 0:
        return 0
    else:
        return pv

def gaussian_noise(image):  # 给图片加一些噪声，高斯噪声
    h, w, c = image.shape  # 获取三个值，高度、宽度、深度
    for row in range(h):  # 在宽度、 高度中遍历进行像素点RGB的赋值
        for col in range(w):
            s = np.random.normal(0, 20, 3)  # 获取随机数  3个数的数组
            b = image[row, col, 0]  # blue   原来的蓝色值
            g = image[row, col, 1]  # green
            r = image[row, col, 2]  # red
            image[row, col, 0] = clamp(b + s[0])  # 加上处理赋值
            image[row, col, 1] = clamp(g + s[1])
            image[row, col, 2] = clamp(r + s[2])
    cv2.imshow("Gauss_noise", image)


def glow(filepath= 'img.png', ksize=11, sigmaX=1, sigmaY=1, weight_alpha=1, weight_beta=1, weight_gamma=0):
    # glow_strength = 3  # 0: no glow, no maximum
    # help(cv2.GaussianBlur)
    # gaussian_noise(img)
    img_blurred = cv2.GaussianBlur(img, (ksize, ksize), sigmaX, sigmaY)
    cv2.imshow("raw1", img)
    img_blurred = cv2.blur(img_blurred, ksize=(ksize, ksize))
    cv2.imshow("raw2", img)
    # help(cv2.blur)
    # 合并图片
    img_blurred = cv2.addWeighted(img, weight_alpha, img_blurred, weight_beta, weight_gamma) # dst = src1*alpha + src2*beta + gamma;
    cv2.imshow("raw3", img)
    # help(cv2.addWeighted)
    print(weight_alpha)
    cv2.imshow('Test', cv2.cvtColor(img_blurred, cv2.COLOR_RGB2BGR))
    cv2.waitKey()

if __name__ == '__main__':
    glow(ksize=21, sigmaX=0, sigmaY=0,  weight_alpha=1, weight_beta=2, weight_gamma=0)

    # weight_alpha = 0
    # while True:
    #     glow(weight_alpha=weight_alpha)
    #     weight_alpha += 0.1
    #     if weight_alpha>2:
    #         break


    # weight_beta = 0
    # while True:
    #     glow(weight_beta=weight_beta)
    #     weight_beta += 0.1
    #     if weight_beta>2:
    #         break

# class Colors:
#     WHITE_ISH = (246, 246, 246)
#     YELLOW_ISH = (214, 198, 136)
#     RED_ISH = (156, 60, 60)
#
#
# def create_border(image: np.ndarray, margin: int, thickness: int, color: Colors) -> np.ndarray:
#     """
#     Create a normal border around an image, with specified colors.
#
#     Args:
#         image: The image, that requires a border.
#         margin: The border distance from the sides of the image.
#         thickness: The thickness of the border.
#         color: The border color, by default a slightly yellow color.
#
#     Modifies:
#         The input image, will be modified with a border.
#
#     Returns:
#         The same image, with a border inserted.
#
#     """
#
#     # Numpy uses the convention `rows, columns`, instead of `x, y`.
#     # Therefore height, has to be before width.
#     height, width = image.shape[:2]
#     cv2.rectangle(image, (margin, margin), (width - margin, height - margin), color, thickness=thickness)
#     return image
#
#
# def apply_blooming(image: np.ndarray) -> np.ndarray:
#     # Provide some blurring to image, to create some bloom.
#     cv2.GaussianBlur(image, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=image)
#     cv2.blur(image, ksize=(5, 5), dst=image)
#     return image
#
#
# def glowing_border(image: np.ndarray, margin=20, thickness=10, color: Colors = Colors.WHITE_ISH):
#     """
#
#     Create a glowing border around an image.
#
#     Args:
#         image: The image, that requires a border.
#         margin: The border distance from the sides of the image.
#         thickness: The thickness of the border.
#         color: The border color, by default a slightly yellow color.
#
#     Modifies:
#         The input image, will be modified with a blooming border.
#
#     Returns:
#         The same image, with a blooming border inserted.
#     """
#
#     # Generate yellowish colored box
#     image = create_border(image, margin, thickness, color)
#
#     # Apply the blooming.
#     image = apply_blooming(image)
#
#     # Reassert the original border, to get a clear outline.
#     # Similar to the Watson-Scott test, two borders were added here.
#     image = create_border(image, margin - 1, 1, color)
#     image = create_border(image, margin + 1, 1, color)
#     return image
#
#
# def glowing_text(image: np.ndarray, text: str, org: Tuple[int, int], color: Colors) -> np.ndarray:
#     """
#
#     Args:
#         image: The image, that requires a border.
#         text: The text to be placed on the image.
#         org: The starting location of the text.
#         color: The color of the text.
#
#
#     Modifies:
#         The input image, will be modified with a blooming text.
#
#     Returns:
#         The same image, with a blooming text inserted.
#     """
#
#     image = cv2.putText(image, text, org, cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=.7, color=color, thickness=1)
#     image = apply_blooming(image)
#     image = cv2.putText(image, text, org, cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=.7, color=color, thickness=1)
#     return image
#
#
# def show(image, delay=0):
#     """
#     Display an image using cv2.
#
#     Notes:
#         By default cv2 uses the BGR coloring, instead RGB.
#         Hence image shown by cv2, which are meant to be RGB,
#         has to be transformed using `cvtColor`.
#
#     Args:
#         image: Input image to be displayed
#         delay: Time delay before continuing running.
#             When 0, The program will wait until a key stroke or window is closed.
#             When 1, The program will continue as quickly as possible.
#
#     Returns:
#         Nothing, it displays the image.
#
#     """
#     cv2.imshow('Test', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
#     cv2.waitKey(delay)


# if __name__ == '__main__':
#     image = np.zeros((480, 640, 3), dtype=np.uint8)
#
#     # Create the glowing border, and a copy of the image, for the text, that will be placed on it later.
#     border = glowing_border(image.copy(), color=Colors.YELLOW_ISH)
#     text = image.copy()
#
#     # This message will be incrementally written
#     message = "Welcome to this game. Don't be scared :)." + " " * 10
#
#     for idx in range(len(message) + 1):
#         text = glowing_text(image.copy(), text=message[:idx], org=(50, 70), color=Colors.YELLOW_ISH)
#
#         # We use a random time delay between keystrokes, to simulate a human.
#         show(np.bitwise_or(border, text), delay=np.random.randint(1, 250))
#
#     # Pause the screen after the full message.
#     show(np.bitwise_or(border, text), delay=0)