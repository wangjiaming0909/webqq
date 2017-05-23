# -*- coding: utf-8 -*-
from qq.qqbotcls import QQBot, QQBotSlot as qqbotslot

@qqbotslot
def onQQMessage(bot, contact, member, content):
    if content == '--version':
        bot.SendTo(contact, 'QQbot-'+bot.conf.version)

@qqbotslot
def onInterval(bot):
    pass

@qqbotslot
def onStartupComplete(bot):
    print 'STARTUP-COMPLETE'
    pass

def onTermCommand(bot, client, command):
    if command.startswith('GET /'):
        http = True
        end = command.find('\r\n')
        if end == -1 or not command[:end-3].endswith(' HTTP/'):
            argv = []
            pass
       

QQBot.onTermCommand = onTermCommand
