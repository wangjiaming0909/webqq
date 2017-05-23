# -*- coding: utf-8 -*-
from qq.qqbotcls import QQBot 

def onTermCommand(bot, client, command):
    if command.startswith('GET /'):
        http = True
        end = command.find('\r\n')
        if end == -1 or not command[:end-3].endswith(' HTTP/'):
            argv = []
            pass
       

QQBot.onTermCommand = onTermCommand
