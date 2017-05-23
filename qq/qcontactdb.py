# -*- coding: utf-8 -*-
from qq.display import DBDisplayer
from qq.contactdb import ContactDB
from qq.fetch import Fetch

class QContactDB(DBDisplayer):
    
    def __init__(self, session):
        self.session = session.Copy()
        dbname = session.dbname
        self.db = ContactDB(dbname)
        print 'friends db file： %s' % dbname
    
    def List(self, tinfo, cinfo=None):#tinfo: ctype
        result = self.db.List(tinfo, cinfo)
        if result is None:
            pass
            
    
    def find(self, tinfo, uin):#tinfo: ctype--dict
        cl = self.List(tinfo, 'uin='+uin)
        if cl is None:
            return None
        elif not cl:
            self.Update(tinfo)
            cl = self.List(tinfo, 'uin='+uin)
        else:
            pass
    
    def Update(self, tinfo):
        contacts = Fetch(self.session, tinfo)
        if contacts is None:
            return False
        else:
            rname = self.db.Update(tinfo, contacts)
            if rname is None:
                return False
            else:
                print '已经获取并更新 %s ' % rname
                return True
    
    def FindSender(self, ctype, fromUin, membUin, thisQQ):
        contact = self.find(ctype, fromUin)