import face_recognition as fr
from recognition import recognition
from take_photo import take_photo
import socket

rec = recognition()
# TODO: 下面两行仅仅为了调试 发布时应删除
# print(f'pic_names: {rec.pic_names}')
# print(f'known_names: {rec.known_names}')

# 创建并初始化UDP对象
SEVER_IP_ADDR = '127.0.0.1'
PORT_NO = 1314
severSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
severSock.bind((SEVER_IP_ADDR, PORT_NO))
# 获取板子地址
_, esp_addr = severSock.recvfrom(1024)


while True:
    if input('command:') == 'n':
        try:
            unknown_face = fr.face_encodings(take_photo())[0]  # 拍照 加载并编码人脸
        except IndexError:
            print('No face detected!!!')
        else:
            verified = rec.verify_face(unknown_face)
            if verified:
                print(verified)
                # 向单片机发送开门信号
                # TODO： 如何获取esp_addr
                severSock.sendto('openDoor'.encode(), esp_addr)
            else:
                print('Not registered!')
            # TODO： 下一行代码仅作调试用 发布时应删除
            # print(f'distances: {face_recognition.face_distance(rec.known_face_encodings,unknown_face)}')
