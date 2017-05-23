# -*- coding: utf-8 -*-

import sys
import platform
import subprocess


Image = None

class QrcodeManager(object):
    def __init__(self):
        pass
    
    def Show(self, qrcode):
        with open('D:/pyqq/qrcode.png', 'wb') as f:
            f.write(qrcode)
        osname = platform.system()
        if osname == 'Windows':
            subprocess.Popen('D:/pyqq/qrcode.png', shell=True)
        elif osname == 'Linux':
            pass
        else:
            pass
        