
# -*- coding: utf-8 -*-
from qq.contactdb import rname, tType


def Fetch(self, tinfo):
    rname, ttype = rname(tinfo), tType(tinfo)
    print '���ڻ�ȡ %s' %rname
    
    try:
        if ttype == 'buddy':
            pass
    except:
        pass
            
def fetchBuddyTable(self):
    pass