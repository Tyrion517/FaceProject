import sys
import cv2
import os
import face_recognition as fr
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from recognition import recognition

pic_path = os.path.join(os.path.dirname(__file__), 'pics')


class MainWindow(QMainWindow):
    def __init__(self, admin: bool=False):
        super().__init__()

        self.setWindowTitle("Door locker")

        if admin:
            self.setWindowTitle("Door locker - Admin Mode")
        self.rec = recognition()

        self.output = QLabel()

        self.recognize_button = QPushButton('Recognize')
        self.recognize_button.clicked.connect(self.click_recognize_button)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.clicke_refresh_button)

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(640, 480)

        if admin:
            self.input_layout = QHBoxLayout()
            self.label_name = QLabel('Name:')
            self.input_name = QLineEdit()
            self.input_name.setPlaceholderText("Enter your name")
            self.register_button = QPushButton('Register')
            self.register_button.clicked.connect(self.click_register_button)
            self.input_layout.addWidget(self.label_name)
            self.input_layout.addWidget(self.input_name)

        layout = QVBoxLayout()
        layout.addWidget(self.recognize_button)
        if admin:
            layout.addLayout(self.input_layout)
            layout.addWidget(self.register_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.output)
        layout.addWidget(self.video_label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(int(1000 // self.cap.get(cv2.CAP_PROP_FPS)))

    def update_frame(self):
        # 给人脸画框的话会极大地增大视频延时，于是选择不画框
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format.Format_BGR888)

            self.video_label.setPixmap(QPixmap.fromImage(image))

    def click_recognize_button(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        unknown_faces = fr.face_encodings(frame)  # 拍照 加载并编码人脸
        if not unknown_faces:
            self.output.setText('No face detected')
        else:
            verifieds = self.rec.verify_face(unknown_faces)  # 只显示一个人的名字
            str = ''
            _ = 1  # 判断是否没有一张已注册人脸
            for verified in verifieds:
                if verified:
                    str += ' '
                    str += verified
                    _ = 0
            if _:
                self.output.setText('No registered face!')
            else:
                self.output.setText(str)


    def click_register_button(self):
        try:
            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            unknown_face = fr.face_encodings(frame)[0]  # 拍照 加载并编码人脸
        except IndexError:
            self.output.setText('No face detected!!!')
        else:
            verified = self.rec.verify_face(unknown_face)
            if verified:
                self.output.setText(f'Already registered, {verified}!')
                # TODO： 下一行代码仅作调试用 发布时应删除
                print(f'distances: {fr.face_distance(self.rec.known_face_encodings, unknown_face)}')
            else:
                name = self.input_name.text()
                if name:
                    _ = cv2.imwrite(f'{pic_path}/known_faces/{name}.jpg', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    if _:
                        self.output.setText('successfully registered! Use "refresh" to reload')
                else:
                    self.output.setText('Please enter your name!!!')

    def clicke_refresh_button(self):
        self.output.setText('Loading...Please wait')
        self.rec = recognition()
        self.output.setText('Refreshed successfully')

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    if len(sys.argv) > 1:
        if sys.argv[1] != '123456':
            print('Wrong password!')
            exit(0)
        else:
            window = MainWindow(True)
    else:
        window = MainWindow()

    window.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    window.show()

    app.exec()

