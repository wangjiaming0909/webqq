# -*- coding: utf-8 -*-
import requests
import random
from qq.qrcodemanager import QrcodeManager
import pickle, sys, time
from qq.common import JsonLoads, JsonDumps, Partition
from requests.packages.urllib3.exceptions import RequestError
from qq.qconf import QConf
from qq.mainloop import Put


class BasicQSession(object):
    def Login(self, conf):
        self.prepareSession()
        self.waitForAuth(conf)
        self.getPtwebqq()
        self.getVfwebqq()
        self.getUinAndPsessionid()
        self.testLogin()
    
    def prepareSession(self):
        self.clientid = 53999199
        self.msgId = 6000000
        self.lastSendTime = 0
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent':('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9;'
                           ' rv:27.0) Gecko/20100101 Firefox/27.0'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })
        #print self.session.cookies
        """self.urlGet(
            'https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&'
            'style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&'
            'no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&'
            'f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001'
        )"""
        #c = self.session.cookies
        #d = c.get_dict()
        
    def urlGet(self, url, data=None, Referer=None, Origin=None):
        Referer and self.session.headers.update({'Referer': Referer})
        Origin and self.session.headers.update({'Origin': Origin})
        timeout = 30 if url != 'https://d1.web2.qq.com/channel/poll2' else 120
        
        try:
            if data is None:
                return self.session.get(url, timeout=timeout)
            else:
                return self.session.post(url, data=data, timeout=timeout)
        except(requests.exceptions.SSLError, AttributeError):
            print 'SSLError, AttributeError'
            #sys.exit(2)
            if self.session.verify:
                print '无法和腾讯服务器建立https连接\n使用http连接'
                try:
                    time.sleep(0.5)
                except KeyboardInterrupt:
                    Put(sys.exit, 0)
                    sys.exit(1)
                self.session.verify = False
                requests.packages.urllib3.disable_warnings(
                    requests.packages.urllib3.exceptions.
                    InsecureRequestWarning
                )
                return self.urlGet(url, data, Referer, Origin)
        else:
            raise
            
    def getUinAndPsessionid(self):
        result = self.smartRequest(
            url = 'http://d1.web2.qq.com/channel/login2',
            data = {
                'r': JsonDumps({
                    'ptwebqq':self.ptwebqq,
                    'clientid': self.clientid,
                    'psessionid':'',
                    'status': 'online'
                })
            }, 
            Referer = ('http://d1.web2.qq.com/proxy.html?v=20151105001'
                       '&callback=1&id=2'), 
            Origin = 'http://d1.web2.qq.com'
        )
        self.uin = result['uin']
        self.psessionid = result['psessionid']
        self.hash = qHash(self.uin, self.ptwebqq)
        self.bkn = bknHash(self.session.cookies['skey'])
        print 'already get uin and psessionid'
    
    def testLogin(self):
        if not self.session.verify:
            print 'not self.session.verify'
            requests.packages.urllib3.disable_warnings(
                requests.packages.urllib3.exceptions.InsecureRequestWarning
            )
        
            
        self.smartRequest(
            url = ('http://d1.web2.qq.com/channel/get_online_buddies2?'
                   'vfwebqq=%s&clientid=%d&psessionid=%s&t={rand}') %
                  (self.vfwebqq, self.clientid, self.psessionid),
            Referer = ('http://d1.web2.qq.com/proxy.html?v=20151105001&'
                       'callback=1&id=2'),
            Origin = 'http://d1.web2.qq.com',
            repeatOnDeny = 0
        )
            
        print 'login success %s(%s)' %(self.nick,self.qq)
    
    def Copy(self):
        c = self.__class__()
        #print self.__dict__
        c.__dict__.update(self.__dict__)
        c.session = pickle.loads(pickle.dumps(c.session))
        #print c.session
        return c
    
    def getPtwebqq(self):
        self.urlGet(self.urlPtwebqq)
        self.ptwebqq = self.session.cookies['ptwebqq']
        print '已获取ptwebqq'
    
    def getVfwebqq(self):
        self.vfwebqq = self.smartRequest(
            url = ('http://s.web2.qq.com/api/getvfwebqq?ptwebqq=%s&'
                   'clientid=%s&psessionid=&t={rand}') %
                  (self.ptwebqq, self.clientid),
            Referer = ('http://s.web2.qq.com/proxy.html?v=20130916001'
                       '&callback=1&id=1'),
            Origin = 'http://s.web2.qq.com'
        )['vfwebqq']
        print('已获取vfwebqq')
    
    def smartRequest(self, url, data=None, Referer=None, Origin=None,
                     expectedCodes=(0, 100003, 100100), expectedKey=None,
                     timeoutRetVal=None, repeatOnDeny=2):
        nCE, nTO, nUE, nDE = 0, 0, 0, 0
        while True:
            url = url.format(rand=repr(random.random()))
            html = ''
            errorInfo = ''
            try:
                resp = self.urlGet(url, data, Referer, Origin)
            except (requests.ConnectionError,
                    requests.exceptions.ReadTimeout) as e:
                nCE += 1
                errorInfo = '网络错误  %s ' %e
            else:
                html = resp.content
                if resp.status_code in (502, 504, 404):
                    self.session.get('')
                else:
                    try:
                        rst = JsonLoads(html)
                    except ValueError:
                        nUE += 1
                        errorInfo = ' URL 地址错误'
                    else:
                        result = rst.get('result', rst)
                        
                        if expectedKey:
                            if expectedKey in result:
                                return result
                        else:
                            if 'retcode' in rst:
                                retcode = rst['retcode']
                            elif 'ec' in rst:
                                retcode = rst['ec']
                            else:
                                retcode = -1
                                
                            if (retcode in expectedCodes):
                                return result
                        nDE += 1
                        errorInfo = '请求被拒绝错误'
            n = nCE + nTO + nUE+ nDE
            
            if len(html) > 40:
                html = html[:20] + '...' + html[-20:]

            # 出现网络错误、超时、 URL 地址错误可以多试几次 
            # 若网络没有问题但 retcode 有误，一般连续 3 次都出错就没必要再试了
            if nCE < 5 and nTO < 20 and nUE < 5 and nDE <= repeatOnDeny:
                print('第%d次请求“%s”时出现 %s，html=%s',
                      n, url.split('?', 1)[0], errorInfo, repr(html))
                time.sleep(0.5)
            elif nTO == 20 and timeoutRetVal: # by @killerhack
                return timeoutRetVal
            else:
                print('第%d次请求“%s”时出现 %s, html=%s',
                      n, url.split('?', 1)[0], errorInfo, repr(html))
                raise RequestError 
        
    
    def getQrcode(self):
        qrcode = self.urlGet(
            'https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&' +
            's=5&d=72&v=4&t=' + repr(random.random())
        ).content
        print '已获取二维码'
        #print self.session.cookies
        return qrcode
    def waitForAuth(self, conf):
        qrcodeManager = QrcodeManager() 
        try:
            qrcodeManager.Show(self.getQrcode())       
            x, y =1, 1
            while True:
                time.sleep(3)
                authStatus = self.getAuthStatus()
                if '二维码未失效' in authStatus:
                    if x:
                        print '等待二维码扫描'
                        x = 0
                elif '二维码认证中' in authStatus:
                    if y:
                        print '二维码已扫描。。等待授权。。'
                        y = 0
                elif '二维码已失效' in authStatus:
                    print '二维码已失效，重新获取二维码'
                    qrcodeManager.Show(self.getQrcode())
                    x, y = 1, 1
                elif '\xe7\x99\xbb\xe5\xbd\x95\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x81' in authStatus:
                    print '登陆成功。。'
                    items = authStatus.split(',')
                    self.nick = str(items[-1].split("'")[1])#DOGGGGG
                    self.qq = str(int(self.session.cookies['superuin'][1:]))#
                    self.urlPtwebqq = items[2].strip().strip("'")#去掉两边的空格，再去掉两边的单引号
                    t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
                    self.dbbasename = '%s-%s-contact.db' %(t, self.qq)
                    self.dbname = conf.absPath(self.dbbasename)
                    conf.SetQQ(self.qq)
                    break
                else:
                    print '获取二维码扫描状态出错， html="%s"' % authStatus
                    sys.exit(1)
        finally:
            #qrcodeManager.Destroy() 
            pass
            
    #
    def getAuthStatus(self):

        result = self.urlGet(
            url='https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=' + 
                str(bknHash(self.session.cookies['qrsig'], init_str=0)) +
                '&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106' +
                '&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26' +
                'webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&' +
                'from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-' +
                repr(random.random() * 900000 + 1000000) +
                '&mibao_css=m_webqq&t=undefined&g=1&js_type=0' +
                '&js_ver=10141&login_sig=&pt_randsalt=0',
            Referer=('https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&'
                     'target=self&style=16&mibao_css=m_webqq&appid=501004106&'
                     'enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2F'
                     'w.qq.com%2Fproxy.html&f_url=loginerroralert&'
                     'strong_login=1&login_state=10&t=20131024001')
        ).content
        print '-----result:' + result
        return result
    
    def Poll(self):
        result = self.smartRequest(
            url = 'https://d1.web2.qq.com/channel/poll2',
            data = {
                'r': JsonDumps({
                'ptwebqq': self.ptwebqq, 
                'clientid': self.clientid, 
                'psessionid': self.psessionid, 
                'key': ''
                })
            },
            Referer = ('http://d1.web2.qq.com/proxy.html?v=20151105001&'
                       'callback=1&id=2'),
            expectedCodes = (0, 100003, 100100, 1202, 100001)
        )
        if (not result) or (not isinstance(result, list)):
            return 'timeout', '', '', ''
        else:
            result = result[0]
            ctype = {
                'message': 'buddy',
                'group_message': 'group', 
                'discu_message': 'discuss'
            }[result['poll_type']]
            fromUin = str(result['value']['from_uin'])
            memberUin = str(result['value'].get('send_uin', ''))
            #content = FaceRev        #表情？？
            content = None              #暂时不要表情
            return ctype, fromUin, memberUin, content   
    
    def send(self, ctype, uin, content, epCodes=[0]):
        self.msgId += 1
        sendUrl = {
            'buddy': 'http://d1.web2.qq.com/channel/send_buddy_msg2',
            'group': 'http://d1.web2.qq.com/channel/send_qun_msg2',
            'discuss': 'http://d1.web2.qq.com/channel/send_discu_msg2'
        }
        sendTag = {'buddy':'to', 'group':'group_uin', 'discuss':'did'}
        self.smartRequest(
            url = sendUrl[ctype], 
            data = {
                'r':JsonDumps({
                    sendTag[ctype]: int(uin),
                    'content':JsonDumps(
                        [['font', {'name': '宋体', 'size':10, 
                                   'stype': [0,0,0], 'color': '000000'}]]
                    ),
                    'face': 522,
                    'clientid':self.clientid,
                    'msg_id': self.msgId,
                    'psessionid': self.psessionid
                })
            }, 
            Referer = ('http://d1.web2.qq.com/proxy.html?v=20151105001&'
                       'callback=1&id=2'), 
            expectedCodes = epCodes
        )
        
    def SendTo(self, contact, content, resendOn1202=True):
        result = None
        
        if not hasattr(contact, 'ctype'):
            result = '错误， 消息接受者必须为一个 QContact 对象'    
        
        if contact.ctype.endswith('-member'):
            result = '错误， 不能给群成员或讨论组成员发送消息'
        else:
            if isinstance(content, str):
                content = content
            elif isinstance(content, unicode):
                content = content.encode('utf8')
            else:
                result = '错误， 消息内容必须为str或unicode对象'
        
        if not content:
            result = '错误， 消息内容不能为空'
        
        if result:
            print result
            return result
        
        epCodes = resendOn1202 and [0] or [0, 1202]
        result = '向 %s 发送消息成功' %contact
        
        while content:
            front, content = Partition(content)
            try:
                self.send(contact.ctype, contact.uin, front, epCodes)
            except Exception as e:
                result = '错误：send message to %s error %s' %(str(contact), e)
                print result
                break
            else:
                print '%s: %s' %(result, front)
        return result
        
def bknHash(skey, init_str=5381):
    hash_str = init_str
    for i in skey:
        hash_str += (hash_str << 5) + ord(i)
    hash_str = int(hash_str & 2147483647)
    return hash_str



def qHash(x, K):
    N = [0] * 4
    for T in range(len(K)):
        N[T%4] ^= ord(K[T])

    U, V = 'ECOK', [0] * 4
    V[0] = ((x >> 24) & 255) ^ ord(U[0])
    V[1] = ((x >> 16) & 255) ^ ord(U[1])
    V[2] = ((x >>  8) & 255) ^ ord(U[2])
    V[3] = ((x >>  0) & 255) ^ ord(U[3])

    U1 = [0] * 8
    for T in range(8):
        U1[T] = N[T >> 1] if T % 2 == 0 else V[T >> 1]

    N1, V1 = '0123456789ABCDEF', ''
    for aU1 in U1:
        V1 += N1[((aU1 >> 4) & 15)]
        V1 += N1[((aU1 >> 0) & 15)]

    return V1
   
if __name__ == '__main__':
    qsession = BasicQSession()
    conf = QConf()
    qsession.Login(conf)
    #qsession.Copy()
    #qsession.prepareSession()

        
        
        