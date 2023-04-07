import os
import numpy as np
import face_recognition as fr

def add_new_user(self, new_face):
    verified = self.verify_face(new_face)  # 首先判断新输入的人脸是否已经注册过
    if not verified:
        new_known_face_name = input("请输入新增用户名:")