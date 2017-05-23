# -*- coding: utf-8 -*-
import os
import argparse
import sys, ast
from globalvar import usage, version, sampleConfStr
import platform
from qq.globalvar import rootConf


class ConfError(Exception):
    pass

class QConf(object):
    def __init__(self, qq=None, user=None):
        self.qq = None if qq is None else str(qq)
        self.user = None if user is None else str(user)
        self.version = version
        self.bench = 'D:\pyqq'
        self.readCmdLine()
        self.readConfFile()
        
    def readCmdLine(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-h', '--help', action = 'store_true')#判断是否存在-h选项
        parser.add_argument('-q', '--qq')
        try:
            opts = parser.parse_args()
        except:
            print usage
            sys.exit(1)
        
        if opts.help:
            print usage
            sys.exit(0)
        
        
        
    
    def readConfFile(self):
        confPath = self.ConfPath()
        conf = rootConf.copy()
        
        if os.path.exists(confPath):
            print '用已有配置文件：'+ confPath
            try:
                with open(confPath, 'rb') as f:
                    cusConf = ast.literal_eval(f.read())
                    print cusConf.keys()
                    print '\n'
                    print cusConf.values()
                    print '\n'
                    print cusConf.items()

                if type(cusConf) is not dict:
                    print '文件内容必须是一个dict'
                    sys.exit(1)
                    
                if type(cusConf.get('默认配置', {})) is not dict:
                    print '默认配置必须是一个dict'
                    sys.exit(1)
                    
                if self.user is not None:
                    if self.user not in cusConf:
                        print '用户 %s 不存在' % self.user
                        sys.exit(1)
                    elif type(cusConf[self.user]) is not dict:
                        print '用户 %s 的配置必须是一个dict' % self.user
                        sys.exit(1)
                    else:
                        names = ['默认配置', self.user]
                else:
                    print '--------------1'
                    names = ['默认配置']
                
                for name in names:
                    print '-------------name'
                    print name#默认配置
                    #    dict.get(key[, default])    当key不在dict中时，default返回
                    for k, v in list(cusConf.get(name, {}).items()):
                        if k not in conf:
                            raise ConfError('不存在的配置选项 %s.%s' % (name, k))
                        elif type(v) is not type(conf[k]):
                            t = type(conf[k].__name__)
                            raise ConfError('%s.%s 必须是一个 %s' % (name, k, t))
                        else:
                            conf[k] = v
                
                
                        
                        
            except(IOError, SyntaxError, ValueError) as e:
                print'配置文件  %s 错误: %s\n' %(confPath, e)
                sys.exit(1)
        else:
            try:
                with open(confPath, 'wb') as f:
                    f.write(sampleConfStr)
            except IOError:
                pass
            else:
                print '在目录：' + confPath + '未发现配置文件。\n已自动创建'
        
        for k, v in list(conf.items()):
            if getattr(self, k, None) is None:
                setattr(self, k, v)    
    
    def configure(self):
        p = self.absPath('plugins')
        print p
        
    def ConfPath(self):
        return self.absPath('%s.conf' %self.version[:4])
    
    def PicklePath(self):
        return self.absPath('%s-py%s-%s.pickle' %(self.version[:4], platform.python_revision(), self.qq))
    
    def Display(self):
        pass
    
    def SetQQ(self, qq):
        self.qq = qq
    
    def absPath(self, rela):
        return os.path.join(self.bench, rela)
    
    def StoreQQ(self):
        fn = self.absPath('qq(pid%s)' % os.getpid())
        with open(fn, 'w') as f:
            f.write(self.qq)
    
if __name__ == '__main__':
    qconf = QConf()
