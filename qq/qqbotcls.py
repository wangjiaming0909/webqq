# -*- coding: utf-8 -*-
import sys, re
import subprocess
import time
from qq.qsession import QLogin
from apscheduler.schedulers.background import BackgroundScheduler
from _collections import defaultdict
from qq.common import StartDaemonThread
from qq.qterm import QTermServer
from pip._vendor.requests.packages.urllib3.exceptions import RequestError
from qq.mainloop import Put, mainloop, MainLoop


RESTART = 201
FRESH_RESTART = 202
POLL_ERROR = 203


def runBot(botCls, qq, user):
    #print sys.argv#还是demo.py文件
    #print botCls
    #print type(botCls)
    #bot = botCls()
    #bot.Stop()
    if sys.argv[-1] == '--subprocessCall':
        isSubProcessCall = True
        sys.argv.pop()
        #print sys.argv
    else:
        isSubProcessCall = False
    
    if isSubProcessCall:
        print 'is SubprocessCall'
        bot = botCls()
        bot.Login(qq, user)
        bot.Run()
        
        
    else:    
        args = [sys.executable] + sys.argv
        args = args + ['--subprocessCall']
        #print 'args: ', args
        
        while True:
            p = subprocess.Popen(args)
            pid = p.pid
            code = p.wait()
            if code == 0:
                print '正常停止'
                sys.exit(code)
            elif code == RESTART:
                print '自动登陆'
                time.sleep(5)
            elif code == FRESH_RESTART:
                print '手动登陆'
                time.sleep(5)
            else:
                sys.exit(code)
            
def RunBot(botCls=None, qq=None, user=None):
    runBot((botCls or QQBot), qq, user)

class QQBot(object):
    def Login(self, qq=None, user=None):
        print 'function --QQBot.Login run'
        session, contactdb, self.conf = QLogin(qq, user)
        
        #print self.conf.termServerport
        self.poll = session.Copy().Poll
        self.termForver = QTermServer(self.conf.termServerPort).Run
        self.findSender = contactdb.FindSender
    
    scheduler = BackgroundScheduler(daemon=True)
    schedTable = defaultdict(list)
    
    @classmethod
    def initScheduler(cls, bot):
        cls._bot = bot
        cls.scheduler.start()
        
    
    def Run(self):
        print '---------function -- QQBot.Run run'
        QQBot.initScheduler(self)
        
        import qq.qslots as _x; _x
        
        self.onStartupComplete()
        
        StartDaemonThread(self.pollForever)
        StartDaemonThread(self.termForver, self.onTermCommand)
        StartDaemonThread(self.intervalForever)
        
        MainLoop()
    
    def intervalForever(self):
        while True:
            time.sleep(300)
            Put(self.onInterval)
     
    def pollForever(self):
        while True:
            try:
                result = self.poll() #return ctype, fromUin, memberUin, content
            except RequestError:
                self.conf.StoreQQ()
                Put(sys.exit, POLL_ERROR)
                break;    
            except:
                print 'qsession.Poll方法出错'
                sys.exit(1)
            else:
                pass
                #Put(self.onPollComplete, 
    
    def onPollComplete(self, ctype, fromUin, membUin, content):
        if ctype == 'timeout':
            return 
        
        contact,member, nameInGroup = \
            self.findSender(ctype, fromUin, membUin, self.conf.qq)
        if ctype == 'buddy':
            print 'Message from %s: |%s|' %(contact, content)
        else:
            print 'Message from %s[%s]:|%s|' %(contact, member, content)
        
        self.onQQMessage(contact, member, content)
        
        
    
    def Stop(self):
        sys.exit(0)
    
    
    
    slotsTable = {
        'onQQMessage': [],
        'onInterval': [],
        'onStartupComplete': []
    }
    
    @classmethod
    def AddSched(cls, **triggerArgs):
        pass
    @classmethod
    def AddSlot(cls, func):
        cls.slotsTable[func.__name__].append(func)
        return func
    
def wrap(slots):
    return lambda *a, **kw: [f(*a, **kw) for f in slots[:]]

for name, slots in QQBot.slotsTable.items():
        setattr(QQBot, name, wrap(slots))
        
QQBotSlot = QQBot.AddSlot
QQBotSched = QQBot.AddSched
if __name__ == '__main__':
    #QQBot.onQQMessage()
    RunBot()
    #print QQBot.onQQMessage()