# coding: utf-8
# import os
from ftplib import FTP
import datetime

"""

可以实现上传 下载单个文件

"""


def ftp_connect(host, port, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, port)
    ftp.login(username, password)
    # ftp.set_pasv(False)
    return ftp


"""

从ftp服务器下载文件

remotepath:远程路径
localpath：本地路径

"""


def download_file(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


"""

从本地上传文件到ftp

remotepath:远程路径
localpath：本地路径

"""


def upload_file(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')

    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


if __name__ == "__main__":
    host = '192.168.0.18'  # IP
    port = 21  # 端口
    username = 'root'  # 用户名
    password = 'A@zjxyyds7'  # 密码
    ftp = ftp_connect(host, port, username, password)

    upload_file(ftp, r"/CMAQ/ftp.log", r"/run/media/test/mydata/data_post/ftp.log")

    download_file(ftp, r"/CMAQ/ftp.log", r"/run/media/test/mydata/data_post/ftp.log")

    ftp.quit()


