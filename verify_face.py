# face_recognition包的文档：https://face-recognition.readthedocs.io/en/latest/face_recognition.html
# 为了方便表示，将用face_encoding表示face_recognition.api.face_encodings方法的返回值（list）的成员
"""
用来确定新拍摄的人脸是否已经注册过的函数
有两个重载版本
第一个只返回bool值
第二个返回False（没有注册）或者人名（已经注册）
"""
from typing import Union
import face_recognition as fr


def verify_face(known_face_encodings: list, face_to_verify) -> bool:
    """第一个重载版本，判断face_to_verify是否在known_face_encodings中，
    是则返回True,否则返回False

    参数：known_face_encodings: list<face_encoding> - 已注册人脸的encodings
    参数:face_to_verify: face_encoding - 要识别的人脸的encoding
    返回值： bool 是否已经注册

    对face_recognition.api.compare_faces进行封装即可

    下一个版本: 在参数列表中添加name_mode: bool参数
    默认为False，第一个版本.
    若为True则返回Union[bool,str]，第二个版本
    """

    results = fr.compare_faces(known_face_encodings, face_to_verify)
    return True in results
