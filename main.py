import face_recognition as fr
from recognition import recognition
from take_photo import take_photo


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





