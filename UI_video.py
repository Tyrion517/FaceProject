import sys
import time

import cv2
import os
import socket
import ftp
import face_recognition as fr
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from recognition import recognition
from sound import generate_welcome_wav

PATH = os.getcwd()
# TODO 确定remote path
REMOTE_PATH = '/www/wwwroot/abc'
pic_path = os.path.join(PATH, 'pics')

OPEN_DOOR = 'openDoor'

# ftp连接相关
FTP_HOST = '36.138.233.214'  # IP
FTP_PORT = 8888  # 端口
FTP_USERNAME = 'root'  # 用户名
FTP_PASSWORD = 'A@zjxyyds7'  # 密码

class MainWindow(QMainWindow):
    def __init__(self, admin: bool=False, ip: str=None,ip2: str=None, log_ip: str=None):
        super().__init__()

        # 通讯相关
        # self.audio_flag = False
        self.esp_flag = False
        self.log_flag = False
        self.ip2_flag = False

        if ip2:
            self.ip2 = ip2
            self.ip2_flag = True


        if ip or log_ip or ip2:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            self.server.bind(("0.0.0.0", 9090))

        if ip:
            self.ip = ip
            self.esp_flag = True
            # TODO 自动获取IP
            # if audio:
            #     self.ftp_socket = ftp.ftp_connect(FTP_HOST, FTP_PORT, FTP_USERNAME, FTP_PASSWORD)
        if log_ip:
            self.log_flag = True
            self.log_ip = log_ip




        self.setWindowTitle("Door locker")
        self.rec = recognition()

        if admin:
            self.setWindowTitle("Door locker - Admin Mode")


        self.output = QLabel()

        self.recognize_button = QPushButton('Recognize')
        self.recognize_button.clicked.connect(self.click_recognize_button)



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
            self.refresh_button = QPushButton('Refresh')
            self.refresh_button.clicked.connect(self.clicke_refresh_button)

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
            verifieds = self.rec.verify_faces(unknown_faces)
            str = ''
            _ = 1  # 判断是否没有一张已注册人脸
            for verified in verifieds:
                if verified:
                    str += ' '
                    str += verified
                    _ = 0
                    if self.log_flag:
                        self.server.sendto(f'{verified}刚开了门'.encode(), (self.log_ip, 1314) )
                        print('log sent')
            if _:
                self.output.setText('No registered face!')
            else:
                self.output.setText(str)
                if self.esp_flag:
                    self.server.sendto(OPEN_DOOR.encode(), (self.ip, 7788))
                    print('command-openDoor sent successfully!')
                    # if self.audio_flag:
                    #     generate_welcome_wav()
                    #     # TODO 在不阻塞程序的情况下等待生成
                    #     time.sleep(1)
                    #     ftp.upload_file(self.ftp_socket, REMOTE_PATH, f'{PATH}/welcome.wav')

                if self.ip2_flag:
                    self.server.sendto('music on'.encode(), (self.ip2, 5252))
                    print('music on')



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
        window = MainWindow(ip='192.168.187.194')

    window.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    window.show()

    app.exec()

