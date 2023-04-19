from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QImage, QPixmap
import sys
import cv2


class DisplayImageWidget(QWidget):
    def __init__(self):
        super(DisplayImageWidget, self).__init__()
        self.image = cv2.imread('/home/tyrion/PycharmProjects/FaceProject/pics/known_faces/biden.jpg')
        self.convert = QImage(self.image, self.image.shape[1], self.image.shape[0], QImage.Format.Format_BGR888)
        self.frame = QLabel()
        self.frame.setPixmap(QPixmap.fromImage(self.convert))

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.frame)


if __name__ == '__main__':
    app = QApplication([])

    main_window = QMainWindow()
    main_window.setWindowTitle('Video Frame Acquisition')
    main_window.setFixedSize(500, 500)

    central_widget = QWidget()
    main_layout = QGridLayout()
    central_widget.setLayout(main_layout)
    main_window.setCentralWidget(central_widget)

    display_image_widget = DisplayImageWidget()
    main_layout.addWidget(display_image_widget, 0, 0)

    main_window.show()
    sys.exit(app.exec())
