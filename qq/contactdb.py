# -*- coding: utf-8 -*-
import sqlite3

class QContact(object):
    def __init__(self, *fields):
        for k, field in zip(self.fields, fields):
            self.__dict__[k] = field
        self.__dict__['ctype'] = self.__class__.ctype

    def __repr__(self):
        return '%s“%s”' % (self.chs_type, self.name)

    def __setattr__(self, k, v):
        raise TypeError("QContact object is readonly")

class Buddy(QContact):
    columns = '''\
        qq VARCHAR(12),
        uin VARCHAR(12) PRIMARY KEY,
        nick VARCHAR(80),
        mark VARCHAR(80),
        name VARCHAR(80)
    '''

class Group(QContact):
    columns = '''\
        qq VARCHAR(12),
        uin VARCHAR(12) PRIMARY KEY,
        nick VARCHAR(80),
        mark VARCHAR(80),
        name VARCHAR(80),
        gcode VARCHAR(12)
    '''

class Discuss(QContact):
    columns = '''\
        uin VARCHAR(12) PRIMARY KEY,
        name VARCHAR(80)
    '''

class GroupMember(QContact):
    columns = '''\
        qq VARCHAR(12),
        uin VARCHAR(12) PRIMARY KEY,
        nick VARCHAR(80),
        mark VARCHAR(80),
        card  VARCHAR(80),
        name VARCHAR(80),
        join_time INTEGER,
        last_speak_time INTEGER,
        role VARCHAR(12),
        role_id INTEGER,
        is_buddy INTEGER,
        level INTEGER,
        levelname VARCHAR(36),
        point INTEGER
    '''

class DiscussMember(QContact):
    columns = '''\
        uin VARCHAR(12) PRIMARY KEY,
        name VARCHAR(80)
    '''

CTYPES = {
    'buddy': 'friend',
    'group': 'group',
    'discuss': 'discuss group',
    'group-member':'group-member',
    'discuss-member':'discuss-member'
    
}

TAGS = ('qq=', 'name=', 'nick=', 'mark=', 'card=', 'uin=')

    
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

contactMaker = {}

for cls in [Buddy, Group, Discuss, GroupMember, DiscussMember]:
    cls.ctype = cls.__name__.lower().replace('member', '-member')
    cls.chs_type = CTYPES[cls.ctype]
    cls.field = [row.strip().split(None, 1)[0]
                  for row in cls.columns.strip().split('\n')]
    contactMaker[cls.ctype] = cls
       
def tName(tinfo):
    if tinfo in ('buddy', 'group', 'discuss'):
        return tinfo
    else:
        return tinfo.ctype + '_member_' + tinfo.uin
    
def tMaker(tinfo):
    return contactMaker[tType(tinfo)]

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