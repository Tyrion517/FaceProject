import os
from numpy import ndarray
import face_recognition as fr
from typing import Union


class recognition:
    """用来储存人脸识别所需数据和方法的类"""

    def __init__(self,password='123456'):
        """ 获取储存了已注册人脸的人名，文件名，编码的列表
         注意: 必须保证三个列表顺序一致!!!"""

        self.password = password
        self.known_face_directory = os.path.join(os.path.dirname(__file__), 'pics', 'known_faces')
        filenames = os.listdir(self.known_face_directory)
        # 获取文件文件名
        self.pic_names = [filename for filename in filenames if filename.endswith('.jpg')]
        # 创建并填充人名列表
        self.known_names = []
        for pic_name in self.pic_names:
            self.known_names.append(pic_name.split('.')[0])

        # 创造并填充用于储存已知人脸编码的列表
        self.known_face_encodings = []
        for i in range(len(self.pic_names)):
            face_image = fr.load_image_file(f'{self.known_face_directory}/{self.pic_names[i]}')
            # fr.face_encodings 返回的是包含图片中所有人脸编码的列表
            # 这里只取第一个
            try:
                face_encoding = fr.face_encodings(face_image)[0]
            except IndexError:
                print(f'这张图里没有无效图片，图中没有人脸！。该图片index为:{i}')
                self.known_face_encodings.append(None)
            else:
                self.known_face_encodings.append(face_encoding)

    def check_registered(self, face_to_verify, tolerance=0.42) -> bool:
        """ 检验人脸是否已经注册
            参数 face_to_verify: face_encoding -待检验人脸的编码"""
        results = fr.compare_faces(self.known_face_encodings, face_to_verify, tolerance)
        return True in results

    def verify_face(self, face_to_verify: ndarray, tolerance=0.42) -> Union[str, None]:
        """ 返回待检验人脸的名字，如果未注册则返回None
            参数 face_to_verify: face_encoding -待检验人脸的编码"""
        distances = fr.face_distance(self.known_face_encodings, face_to_verify)
        target_index = distances.argmin()
        if self.check_registered(face_to_verify, tolerance):
            return self.known_names[target_index]
        return None

    def verify_faces(self, faces_to_verify: list, tolerance=0.42) -> list:
        """ 重载版本，传入列表而非单个人脸
        传出列表而非单个人名"""
        names = []
        for face_to_verify in faces_to_verify:
            distances = fr.face_distance(self.known_face_encodings, face_to_verify)
            target_index = distances.argmin()
            if self.check_registered(face_to_verify, tolerance):
                names.append(self.known_names[target_index])
        return names



