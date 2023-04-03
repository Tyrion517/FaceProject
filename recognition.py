import face_recognition as fr
from typing import Union


class recognition:
    """用来储存人脸识别所需数据和方法的类"""

    def __init__(self):
        # 储存已注册人脸的人名和文件名的列表
        # 为了效率和配合其他部分，并未使用字典
        # 注意: 必须保证文件名和人名顺序一致!!!
        # TODO: 每次添加或删除已注册人脸后应手动修改此处
        # TODO: 或者想办法自动获取
        self.known_names = ['joe biden', 'barack obama', 'Xiang Bo']
        self.known_filenames = ['biden.jpg', 'obama.jpg', 'XiangBo.jpg']

        # 创造并填充用于储存已知人脸编码的列表
        # TODO: 用try/exception语句重构，以防图片中一个人脸也没有识别
        self.known_face_encodings = []
        for i in range(len(self.known_filenames)):
            face_image = fr.load_image_file(self.known_filenames[i])
            # fr.face_encodings 返回的是包含图片中所有人脸编码的列表
            # 这里只取第一个
            face_encoding = fr.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)

    def check_registered(self, face_to_verify) -> bool:
        """ 检验人脸是否已经注册
            参数 face_to_verify: face_encoding -待检验人脸的编码"""
        results = fr.compare_faces(self.known_face_encodings, face_to_verify)
        return True in results

    def verify_face(self, face_to_verify) -> Union[str, None]:
        """ 返回待检验人脸的名字，如果未注册则返回None
            参数 face_to_verify: face_encoding -待检验人脸的编码"""
        results = fr.compare_faces(self.known_face_encodings, face_to_verify)
        if True in results:
            index = results.index(True)
            return self.known_names[index]
        return None

