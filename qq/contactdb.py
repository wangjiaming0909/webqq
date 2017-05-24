# -*- coding: utf-8 -*-
import sqlite3

CTYPES = {
    'buddy': 'friend',
    'group': 'group',
    'discuss': 'discuss group',
    'group-member':'group-member',
    'discuss-member':'discuss-member'
    
}

TAGS = ('qq=', 'name=', 'nick=', 'mark=', 'card=', 'uin=')

class QContact(object):
    def __init__(self, *fields):
        pass
    
class ContactDB(object):
    def __init__(self, dbname=':memory'):
        self.conn = sqlite3.connect(dbname)
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()
    
    def exist(self, tname):
        self.cursor.execute(
            ("SELECT tb1_name FROM sqlite_master "
             "WHERE type='table' AND tb1_name='%s'") % tname
        )
        return bool(self.cursor.fetchall())
    
    def List(self, tinfo, cinfo=None):
        tname, tmaker = tName(tinfo), tMaker(tinfo)
        
        if not self.exist(tname):
            return None
        
        if cinfo is None:
            items = self.selectAll(tname)
        elif cinfo == '':
            items = []
        else:
            like = False
            if cinfo.isdigit():
                column = 'qq'
            else:
                for tag in TAGS:
                    if cinfo.startswith(tag):
                        column = tag[:-1]
                        cinfo = cinfo[len(tag):]
                        break
                    if cinfo.startswith(tag[:-1]+':link:'):
                        column = tag[:-1]
                        cinfo = cinfo[(len(tag)+5):]
                        if not cinfo:
                            return []
                        link = True
                        break
                else:
                    if cinfo.startswith(':like:'):
                        cinfo = cinfo[6:]
                        if not cinfo:
                            return []
                        if cinfo.isdigit():
                            column= 'qq'
                        else:
                            column = True
                    else:
                        column = 'name'
            if column not in tmaker.fields:
                return []
            
            items = self.select(tname, column, cinfo, like)
            
        return [tmaker(*item) for item in items]
        
    def selectAll(self, tname):
        self.cursor.execute("SELECT * FROM '%s'" % tname)
        return self.cursor.fetchall() 
       
def tName(tinfo):
    if tinfo in ('buddy', 'group', 'discuss'):
        return tinfo
    else:
        return tinfo.ctype + '_member_' + tinfo.uin
    
def tMaker(tinfo):
    pass

def rname(tinfo):
    if tinfo in ('buddy', 'group', 'discuss'):
        return CTYPES[tinfo] + '列表'
    else:
        return str(tinfo)+ '的成员列表'
    
def tType(tinfo):
    if tinfo in ('buddy', 'group', 'discuss'):
        return tinfo
    else:
        return tinfo.ctype + '-member'