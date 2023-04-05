# 出现路径错误请将recognition.py中的路径改为绝对路径

import os
import unittest
import pytest
import face_recognition as fr

from recognition import recognition
# unknown_path = os.path.join(os.path.dirname(__file__), 'pics', 'unknown_faces')
unknown_path = '/home/tyrion/PycharmProjects/FaceProject/pics/unknown_faces'


class RecognitionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.rec = recognition()

    @pytest.mark.task(taskno=1)
    def test_init(self):
        print(f'pic_names: {self.rec.pic_names}')
        print(f'known_names: {self.rec.known_names}')

    @pytest.mark.task(taskno=2)
    def test_verify_face(self):
        """测试大量人脸是否能正确识别
        将供识别和待识别图片分别放在pics下的正确目录里"""
        # 加载测试文件
        filenames = os.listdir(unknown_path)
        names = []
        for filename in filenames:
            names.append(filename.split('.')[0])
        # 测试加载是否成功
        print('')
        print('loading test:')
        print(f'filenames: {filenames}')
        print(f'names: {names}')

        # 测试本体
        for i, filenames in enumerate(filenames):
            loaded_face = fr.load_image_file(f'{unknown_path}/{filenames}')
            try:
                face_to_verify = fr.face_encodings(loaded_face)[0]
            except IndexError:
                print(f'[{names[i]}]: No face detected!!!')
            else:
                print(f'real name:{names[i]};\tdetected name: {self.rec.verify_face(face_to_verify)};\tdistances: {fr.face_distance(self.rec.known_face_encodings, face_to_verify)}')


if __name__ == '__main__':
    unittest.main()
