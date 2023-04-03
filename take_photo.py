# 拍照，转化为RGB形式 并加载
import cv2
import numpy as np


def take_photo():
    """用电脑摄像头拍照，获取人脸图片，转化为RGB形式，并加载

    :param None
    :return np.ndarray - RGB形式的图片"""

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        print('Camera is not opened')
        return None
    return rgb_frame


