import numpy as np
import cv2
import face_recognition as fr
from verify_face import verify_face
from recognition import recognition

rec = recognition()

# 储存已注册人脸的人名和文件名的列表
# 为了效率和配合其他部分，并未使用字典
# TODO: 每次添加或删除已注册人脸后应手动修改此处
# TODO: 或者想办法自动获取

known_names = ['joe biden', 'barack obama']
known_filenames = ['biden.jpg', 'obama.jpg']


known_path = 'pics/known_faces' # file path for known face pic
unknown_path = 'pics/unknown_faces' # file path for unknown face pic

# 以np arrays的形式加载人脸图片
biden_image = fr.load_image_file(f'{known_path}/biden.jpg')
obama_image = fr.load_image_file(f'{known_path}/obama.jpg')
unknown_image = fr.load_image_file(f'{unknown_path}/obama2.jpg')

# 获取已注册人脸的encodings
try:
    biden_face_encoding = fr.face_encodings(biden_image)[0]
    obama_face_encoding = fr.face_encodings(obama_image)[0]
    unknown_face_encoding = fr.face_encodings(unknown_image)[0]
except IndexError:
    print('有的图片中没有人脸。推出程序中。。。')
    quit()

known_faces = [
    biden_face_encoding,
    obama_face_encoding
]

print(rec.check_registered(unknown_face_encoding))
