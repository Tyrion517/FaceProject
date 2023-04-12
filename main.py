import cv2
import face_recognition as fr
from recognition import recognition
from take_photo import take_photo
from PIL import Image
from verify_face import verify_face
import os


# TODO: 下面两行仅仅为了调试 发布时应删除
# print(f'pic_names: {rec.pic_names}')
# print(f'known_names: {rec.known_names}')

while True:
    opt=input('command:')
    dorm=input("宿舍为(组团-宿舍号):") # 先输入宿舍号，方便之后识别或者添加新用户
    if opt == 'n':
        # 首先判断输入的宿舍号有无对应文件夹，如果报错的话说明没有这个文件夹，该宿舍没成员注册
        try:
            known_face_directory = os.path.join(os.path.dirname(__file__), 'pics', 'known_faces', dorm)
            filenames = os.listdir(known_face_directory)
        except FileNotFoundError:
            print("该宿舍没有已注册成员")
        else:
            rec = recognition(dorm)  # 新增改动:在识别的时候直接识别该宿舍的人脸，既加快程序运行速率，又能区分不同宿舍的成员
            try:
                unknown_face = fr.face_encodings(take_photo())[0]  # 拍照 加载并编码人脸
            except IndexError:
                print('No face detected!!!')
            else:
                try:
                    verified = rec.verify_face(unknown_face)
                except  ValueError:
                    verified = 0
                #print(rec.known_face_directory)
                if verified:
                    print(verified)
                else:
                    print('Not registered!')
                # TODO： 下一行代码仅作调试用 发布时应删除
                # print(f'distances: {face_recognition.face_distance(rec.known_face_encodings,unknown_face)}')
    if opt == 'm':
        known_face_directory = os.path.join(os.path.dirname(__file__), 'pics', 'known_faces', dorm)
        # 下述代码作用：如果指定宿舍还未注册，则新建一个宿舍对应的文件夹储存宿舍成员的人脸照片
        try:
            filenames = os.listdir(known_face_directory)
        except FileNotFoundError:
            # 不存在指定路径即该宿舍未注册，下面新建该宿舍的文件夹，并初始化密码
            os.mkdir(known_face_directory)
            with open(known_face_directory + "/key.txt", "w") as f:
                key=input("请你为你的宿舍设置密码:")
                f.write(key)
        #比对密码
        with open(known_face_directory + "/key.txt", "r") as f:
            file_content = f.read()
        # 给三次输入密码的机会
        for i in range(3):
            password=input("请输入宿舍密码:")
            if password == file_content:
                break
            print("密码输入有误！")
            count=i
        if count == 2:
            continue
        rec = recognition(dorm)
        # 首先拍下jpg 作为新增用户的照片
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
            script_path = os.path.abspath(__file__) # 获取当前程序的路径
            project_path = os.path.dirname(script_path) # 获取程序所在项目的路径，方便确定known_faces的路径
            if verified:
                print('该用户已注册')
            if not verified:
                new_known_face_name = input("请输入新增用户名:")
                cv2.imwrite(known_face_directory+"\\" + new_known_face_name + ".jpg", frame) # 存储照片
        else:
            print('Camera is not opened')
            continue


