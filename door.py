import socket
import cv2
import io
from PIL import Image
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.bind(("0.0.0.0", 9090))
#前面的ip不用改，只需要保证esp32_cam发送的端口与此端口一致

# data, IP = s.recvfrom(100000)
print('Successfully connected!')

while True:
    _ = input('command:')
    s.sendto(_.encode(), ("192.168.18.202", 7788))

