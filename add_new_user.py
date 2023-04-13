import os
import numpy as np
import face_recognition as fr
import numpy as np
import cv2
from verify_face import verify_face
from recognition import recognition
from PIL import Image

def add_new_user(new_face):
    verified = verify_face(new_face)  # 首先判断新输入的人脸是否已经注册过
    if verified:
        print('该用户已注册')
    if not verified:
        new_known_face_name = input("请输入新增用户名:")
        new_known_face = Image.fromarray(new_face.astype('uint8')).convert('RGB')
        print(new_known_face)
        #Image.save("D://你好.jpg")
