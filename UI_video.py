import sys
import cv2
import os
import face_recognition as fr
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from recognition import recognition
from take_photo import take_photo

pic_path = os.path.join(os.path.dirname(__file__), 'pics')


class MainWindow(QMainWindow):
    def __init__(self, admin: bool=False):
        super().__init__()

        self.setWindowTitle("Door locker")
        self.rec = recognition()

        self.output = QLabel()

        self.recognize_button = QPushButton('Recognize')
        self.recognize_button.clicked.connect(self.click_recognize_button)

        if admin:
            self.register_button = QPushButton('Register')
            self.register_button.clicked.connect(self.click_register_button)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.clicke_refresh_button)

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(640, 480)

        layout = QVBoxLayout()
        layout.addWidget(self.recognize_button)
        if admin:
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

        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format.Format_BGR888)

            self.video_label.setPixmap(QPixmap.fromImage(image))

    def click_recognize_button(self):
        try:
            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            unknown_face = fr.face_encodings(frame)[0]  # 拍照 加载并编码人脸
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
                    name = input('Please enter your name:')
                    _ = cv2.imwrite(f'{pic_path}/known_faces/{name}.jpg', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    if _:
                        self.output.setText('successfully registered! Use "refresh" to reload')
        else:
            self.output.setText('Wrong password')

    def clicke_refresh_button(self):
        self.output.setText('Loading...Please wait')
        self.rec = recognition()
        self.output.setText('Refreshed successfully')

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    window.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    window.show()

    app.exec()

