import sys
import cv2
import os
import face_recognition as fr
from PyQt6.QtWidgets import *
from recognition import recognition
from take_photo import take_photo

pic_path = os.path.join(os.path.dirname(__file__), 'pics')
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Door locker")
        self.rec = recognition()

        self.output = QLabel()

        self.recognize_button = QPushButton('Recognize')
        self.recognize_button.clicked.connect(self.click_recognize_button)

        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.click_register_button)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.clicke_refresh_button)


        layout = QVBoxLayout()
        layout.addWidget(self.recognize_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.output)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def click_recognize_button(self):
        try:
            unknown_face = fr.face_encodings(take_photo())[0]  # 拍照 加载并编码人脸
        except IndexError:
            self.output.setText('No face detected')
        else:
            verified = self.rec.verify_face(unknown_face)
            if verified:
                self.output.setText(verified)
            else:
                self.output.setText('Not registered!')

    def click_register_button(self):
        _password = input('Please enter the password:')
        if _password == self.rec.password:
            try:
                new_face = take_photo()
                unknown_face = fr.face_encodings(new_face)[0]  # 拍照 加载并编码人脸
            except IndexError:
                self.output.setText('No face detected!!!')
            else:
                verified = self.rec.verify_face(unknown_face)
                if verified:
                    self.output.setText(f'Already registered, {verified}!')
                    # TODO： 下一行代码仅作调试用 发布时应删除
                    print(f'distances: {fr.face_distance(self.rec.known_face_encodings, unknown_face)}')
                else:
                    name = input('Please enter your name:')
                    _ = cv2.imwrite(f'{pic_path}/known_faces/{name}.jpg', cv2.cvtColor(new_face, cv2.COLOR_RGB2BGR))
                    if _:
                        self.output.setText('successfully registered! Use "refresh" to reload')
        else:
            self.output.setText('Wrong password')
    def clicke_refresh_button(self):
        self.output.setText('Loading...Please wait')
        self.rec = recognition()
        self.output.setText('Refreshed successfully')

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
