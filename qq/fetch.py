
# -*- coding: utf-8 -*-
from qq.contactdb import rName, tType
from qq.common import JsonDumps, HTMLUnescape
import collections
import sys


def Fetch(self, tinfo):
    rname, ttype = rName(tinfo), tType(tinfo)
    print 'Fetching%s' %rname
    
    try:
        if ttype == 'buddy':
            table = fetchBuddyTable(self)
    except:
        print 'RequestError'
        table = None
    
    if table is None:
        print 'fetching failed %s ' % rname
    return table
            
def fetchBuddyTable(self):
    result = self.smartRequest(
        url = 'http://s.web2.qq.com/api/get_user_friends2',
        data = {
            'r': JsonDumps({'vfwebqq':self.vfwebqq, 'hash':self.hash})
        },
        Referer = ('http://d1.web2.qq.com/proxy.html?v=20151105001&'
                   'callback=1&id=2'),
        expectedKey = 'marknames',
        repeatOnDeny = 4
    )
    markDict = dict((str(d['uin']), str(d['markname']))
                    for d in result['marknames'])
    
    qqResult = self.smartRequest(
        url = 'http://qun.qq.com/cgi-bin/qun_mgr/get_friend_list',
        data = {'bkn': self.bkn},
        Referer = 'http://qun.qq.com/member.html'
    )

    qqDict = collections.defaultdict(list)
    for blist in list(qqResult.values()):
        for d in blist.get('mems', []):
            name = HTMLUnescape(d['name'])
            qqDict[name].append(str(d['uin']))
    
    buddies, unresolved = [], []

    for info in result['info']:
        uin = str(info['uin'])
        nick = str(info['nick'])
        mark = markDict.get(uin, '')        
        name = mark or nick
        qqlist = qqDict.get(name, [])
        if len(qqlist) == 1:
            qq = qqlist[0]
        else:
            qq = '#NULL'
            unresolved.append('好友“%s”(uin=%s)' % (name, uin))
        
        # 各属性的顺序绝对不能变
        buddies.append([qq, uin, nick, mark, name])
    
    if unresolved:
        unresolved.sort()
        print 'unresolved'
        sys.exit(1)
    
    return buddies