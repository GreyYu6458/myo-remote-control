# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = ' CHENHUI'
import socket
import time
import threading
import collections


class MyoSocket(threading.Thread):
    def __init__(self, address, port):
        super(MyoSocket, self).__init__()
        self._socket = socket.socket()
        self._address = address
        self._host = socket.gethostname()
        self._port = port
        self.current_device = None
        self.link_dict = collections.OrderedDict()

    def select_device(self, index):
        try:
            index_dict = self.link_dict.keys()[index]
            self.current_device = self.link_dict[index_dict]
        except IndexError:
            print("ERROR DEVICE")

    def get_current_link(self):
        if len(self.link_dict) == 0:
            return None
        else:
            return self.link_dict.keys()

    def send_command(self, commend):
        if self.current_device:
            self.current_device.send(bytes(commend))
        else:
            print("No Device Selected")

    def get_link(self):
        return self.link_dict.keys()

    def close_link(self, index):
        self.link_dict[index].close()
        del self.link_dict[index]

    def run(self):
        print("HOST:", self._address.ljust(15), ("PORT:%d" % self._port).ljust(10), "\tStart")
        self._socket.bind((self._address, self._port))
        while True:
            self._socket.listen(5)
            # 阻塞在此
            c, address = self._socket.accept()
            # 身份记录
            save_data = (address, int(time.time()))
            print(save_data)
            # 记录链接
            self.link_dict[address] = c
            # 开启一个接收线程
            LinkProcessRec(address, c, self).start()


class LinkProcessRec(threading.Thread):
    def __init__(self, address, link, manage_thread):
        super(LinkProcessRec, self).__init__()
        self.link = link
        self.address = address
        self.port = 20000
        self.manage_thread = manage_thread

    def run(self):
        try:
            while True:
                rec_data = self.link.recv(1024)
                if not rec_data:
                    break
                print("Message From:", self.address, ":", rec_data)
            print("Link: ", self.address, " Had Been Disconnected")
        except Exception as result:
            print(result)
        finally:
            self.manage_thread.close_link(self.address)


if __name__ == "__main__":
    local_name = socket.getfqdn(socket.gethostname())
    ip_list = socket.gethostbyname_ex(local_name)[2]
    ip_list.append("127.0.0.1")
    for ip in ip_list:
        server = MyoSocket(ip, 12345)
        server.start()
