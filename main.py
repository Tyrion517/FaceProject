import face_recognition as fr
import cv2
import os
from recognition import recognition
from take_photo import take_photo
from welcome_phrase import welcome

pic_path = os.path.join(os.path.dirname(__file__), 'pics')

def cmd_recognize(rec: recognition):
    try:
        unknown_face = fr.face_encodings(take_photo())[0]  # 拍照 加载并编码人脸
    except IndexError:
        print('No face detected!!!')
    else:
        verified = rec.verify_face(unknown_face)
        if verified:
            print(verified)
        else:
            print('Not registered!')
        # TODO： 下一行代码仅作调试用 发布时应删除
        # print(f'distances: {fr.face_distance(rec.known_face_encodings, unknown_face)}')

def cmd_register(rec: recognition, password: str):
    _password = input('Please enter the password:')
    if _password == password:
        try:
            new_face = take_photo()
            unknown_face = fr.face_encodings(new_face)[0]  # 拍照 加载并编码人脸
        except IndexError:
            print('No face detected!!!')
        else:
            verified = rec.verify_face(unknown_face)
            if verified:
                print(f'Already registered, {verified}!')
                # TODO： 下一行代码仅作调试用 发布时应删除
                print(f'distances: {fr.face_distance(rec.known_face_encodings, unknown_face)}')
            else:
                name = input('Please enter your name:')
                _ = cv2.imwrite(f'{pic_path}/known_faces/{name}.jpg', cv2.cvtColor(new_face, cv2.COLOR_RGB2BGR))
                if _:
                    print('successfully registered! Use "refresh" to reload')
    else:
        print('Wrong password')


if __name__ == '__main__':
    rec = recognition()
    # TODO: 下面两行仅仅为了调试 发布时应删除
    # print(f'pic_names: {rec.pic_names}')
    # print(f'known_names: {rec.known_names}')

    while True:
        command = input('command:')
        if command == 'recognize':
            # 识别人脸
            cmd_recognize(rec)

        elif command == 'register':
            # 注册人脸 要求输入密码
            cmd_register(rec, rec.password)

        elif command == 'refresh':
            # 重新加载人脸
            rec = recognition()
        else:
            print(f'Command {command} not found')



