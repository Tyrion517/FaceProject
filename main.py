import face_recognition as fr
from recognition import recognition
from take_photo import take_photo

new_rec = recognition()
while True:
    if input('command:') == 'n':
        try:
            unknown_face = fr.face_encodings(take_photo())[0]  # 拍照 加载并编码人脸
        except IndexError:
            print('No face detected!!!')
        else:
            print(new_rec.verify_face(unknown_face))
