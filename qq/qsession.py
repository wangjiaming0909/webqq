# -*- coding: utf-8 -*-
from qq.basicqsession import BasicQSession
from qq.qconf import QConf
import pickle
from qq.qcontactdb import QContactDB

def QLogin(qq=None, user=None):
    conf = QConf()
    conf.Display()
    
    if conf.qq:
        print '开始自动登陆。。。'
    
    
    print '开始手动登陆'
    session = QSession()
    session.Login(conf)
    picklePath = conf.PicklePath()
    try:
        with open(picklePath, 'wb') as f:
            pickle.dump((session.__dict__), f)
    except Exception as e:
        print '保存登陆信息失败： %s %s ' %(e, picklePath)
    else:
        print '登陆信息已保存： file://%s' %picklePath
    return session, QContactDB(session), conf
    
class QSession(BasicQSession):
    pass


if __name__ == '__main__':
    print 'a'