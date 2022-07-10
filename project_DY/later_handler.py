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

    # def img2video(self, image, video_path, fps=1, seconds=1, size=(720, 1280)):
    #     """
    #     单张图片 -> 视频
    #     :param image: pil image data: cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR) -> cv2
    #     :param video_path:
    #     :param fps:
    #     :param size:
    #     :return:
    #     """
    #     fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")    # mp4
    #     video_writer = cv2.VideoWriter(video_path, fourcc, fps, image.size)
    #     # for image in images:
    #     frame = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    #     for i in range(seconds):
    #         video_writer.write(frame)
    #     video_writer.release()

    def video_frame(self, video, frame, ):
        video.write(frame)