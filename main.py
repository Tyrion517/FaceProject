import cv2
import face_recognition as fr
from recognition import recognition
from take_photo import take_photo
from PIL import Image
from verify_face import verify_face
import os

rec = recognition()
# TODO: 下面两行仅仅为了调试 发布时应删除
# print(f'pic_names: {rec.pic_names}')
# print(f'known_names: {rec.known_names}')

while True:
    opt=input('command:')
    if opt == 'n':
        try:
            unknown_face = fr.face_encodings(take_photo())[0]  # 拍照 加载并编码人脸
        except IndexError:
            print('No face detected!!!')
        else:
            verified = rec.verify_face(unknown_face)
            #print(rec.known_face_directory)
            if verified:
                print(verified)
            else:
                print('Not registered!')
            # TODO： 下一行代码仅作调试用 发布时应删除
            # print(f'distances: {face_recognition.face_distance(rec.known_face_encodings,unknown_face)}')
    if opt == 'm':
        #首先拍下jpg 作为新增用户的照片
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            try:
                unknown_face = fr.face_encodings(rgb_frame)[0]
            except IndexError:
                print('No face detected!!!')
                break
            verified = rec.verify_face(unknown_face)  # 首先判断新输入的人脸是否已经注册过
            script_path = os.path.abspath(__file__)#获取当前程序的路径
            project_path = os.path.dirname(script_path)#获取程序所在项目的路径，方便确定known_faces的路径
            if verified:
                print('该用户已注册')
            if not verified:
                new_known_face_name = input("请输入新增用户名:")
                cv2.imwrite(project_path+"\\pics\\known_faces\\" + new_known_face_name + ".jpg", frame)#存储照片
        else:
            print('Camera is not opened')
            continue


