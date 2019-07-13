'''
emotion recognize

TODO: signal and slot
'''
import sys
import numpy as np
import cv2

from PyQt5.QtCore import pyqtSignal, QBasicTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()

        #打开相机
        self.btn_open_cam()

    def set_ui(self):
        # 布局设置
        self.layout_main = QHBoxLayout()  # 整体框架是水平布局
        self.layout_button = QVBoxLayout()  # 按键布局是垂直布局

        # 按钮设置
        self.btn_photo = QPushButton(u'拍照识别')
        self.btn_video = QPushButton(u'实时识别')
        self.btn_quit = QPushButton(u'退出')

        # 显示视频
        self.label_show_camera = QLabel()

        # 显示捕获的图片
        self.label_capture = QLabel()
        self.label_capture.setFixedSize(100, 75)
        self.label_capture.setStyleSheet('background-color:#00f')

        # 显示文本框
        self.text = QTextEdit(self)

        self.label_show_camera.setFixedSize(800, 600)
        self.label_show_camera.setAutoFillBackground(False)
        self.label_show_camera.setStyleSheet('background-color: #ff0')

        # 布局
        self.layout_button.addWidget(self.btn_photo)
        self.layout_button.addWidget(self.btn_video)
        self.layout_button.addWidget(self.btn_quit)
        self.layout_button.addWidget(self.label_capture)
        self.layout_button.addWidget(self.text)

        self.layout_main.addWidget(self.label_show_camera)
        self.layout_main.addLayout(self.layout_button)

        self.setLayout(self.layout_main)
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("人脸识别软件")

        # 拍照识别
        self.btn_photo.clicked.connect(self.btn_video_capture)
        # 实时识别
        self.btn_video.clicked.connect(self.btn_video_capture)

    def btn_open_cam(self):
        camera_record = CameraRecord()
        image_data = camera_record.image_data

        height, width, colors = image_data.shape
        bytesPerLine = colors * width
        # 变换彩色空间
        cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB, image_data)

        #转换为Qimage
        image = QImage(
            image_data.data,
            width,
            height,
            bytesPerLine,
            QImage.Format_RGB888
        )

        self.label_show_camera.setPixmap(QPixmap.fromImage(image))
        pass

    def btn_photo_capture(self):
        pass

    def btn_video_capture(self):
        pass

    def emotion_recognition(self, picture):
        pass

class CameraRecord(QWidget):

    image_data = pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0):
        super().__init__()
        self.camera = cv2.VideoCapture(camera_port)

        self.timer = QBasicTimer()
        self.timer.start(1000, self)

    def timerEvent(self, QTimerEvent):
        if QTimerEvent.timerId() != self.timer.timerId():
            return
        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())
