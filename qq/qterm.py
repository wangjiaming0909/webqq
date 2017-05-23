# -*- coding: utf-8 -*-
import socket
import time
from qq.mainloop import Put


HOST, DEFPORT = '127.0.0.1', 8188

class Client(object):
    def __init__(self, name, sock):
        self.name = name
        self.sock = sock
        
    def Reply(self, rep):
        try:
            self.sock.sendall(rep)
        except socket.error:
            print '回复 %s 失败' % self.name
        finally:
            self.sock.close()

class QTermServer(object):
    def __init__(self, port):
        self.port = port
    
    def Run(self, onCommand=None):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.sock.testSetSockOpt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((HOST, self.port))
            self.sock.listen(5)
        except socket.error as e:
            print '无法打开 QQBot term 服务器。 %s' % e
            print 'qq命令不能使用'
        else:
            time.sleep(0.1)
            print '在%s端口开启QQBot-服务器' %self.port
            
            while True:
                try:
                    sock, addr = self.sock.accept()
                except socket.error:
                    print 'QQBot-Term 服务器出现 accept 错误'
                else:
                    name = 'QTerm客户端"%s:%s"' % addr
                    sock.settimeout(5.0)
                    try:
                        data = sock.recv(8192)
                    except socket.error:
                        sock.close()
                    else:
                        command = data
                        Put(onCommand, Client(name, sock), command)
            
            
            
            
            
            