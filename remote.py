# -*- coding: utf-8 -*-
__author__ = ' CHENHUI'
import socket
import threading
import ctypes


class Client(threading.Thread):
    def __init__(self, host, post):
        super(Client, self).__init__()
        self._socket = socket.socket()
        self._host = host
        self._post = post
        self._so = ctypes.CDLL("libCarLib.so")
        self._so.GPIOInit()

    """
    Commend_Forward = 0x01      # 握拳
    Commend_Back = 0x02         # 张手
    Commend_TurnRight = 0x03    # 内翻
    Commend_TurnLeft = 0x04     # 外翻
    Commend_Stop = 0x05         # 放松
    """

    def run(self):
        self._socket.connect((self._host, self._post))
        while True:
            Command = self._socket.recv(1024)
            print Command
            if Command == 0x01:
                self._so.CtrlCar('g', 50)
            elif Command == 0x02:
                self._so.CtrlCar('b', 50)
            elif Command == 0x03:
                self._so.CtrlCar('l', 50)
            elif Command == 0x04:
                self._so.CtrlCar('r', 50)
            elif Command == 0x05:
                self._so.CtrlCar('s', 50)


if __name__ == '__main__':
    client = Client("192.168.31.23", 12345)
    client.start()
