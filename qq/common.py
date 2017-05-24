import json, threading

def encJson(obj):
    if hasattr(obj, 'encode'):
            return obj.encode('utf8')
    elif isinstance(obj, list):
        return [encJson(e) for e in obj]
    elif isinstance(obj, dict):
        return dict((encJson(k), encJson(v)) for k,v in obj.items())
    else:
        return obj

JsonLoads = lambda s:encJson(json.loads(s))
JsonDumps = json.dumps

def StartDaemonThread(target, *args, **kwargs):
    t = threading.Thread(target=target, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()
    
def Partition(msg):
    n = 720
    if len(msg) < n:
        f, b = msg, b''
    else:
        for i in range(n-1, n-101, -1):
            if isSpace(msg[i]):
                f, b = msg[:i+1], msg[i+1:]
                break
        else:
            for i in range(n-1, n-301, -1):
                x = ord(msg[i])
                if (x >> 6) != 2:
                    f, b = msg[:i], msg[i:]
                    break
            else:
                f, b = msg[:n], msg[n:]
    return f, b
 
import HTMLParser; htmlUnescape = HTMLParser.HTMLParser().unescape
def HTMLUnescape(s):
    return htmlUnescape(s.decode('utf8')).replace(u'\xa0', u' ').encode('utf8')
            
def isSpace(b):
    return b in[' ', '\t', '\n', '\r', 32, 9, 10, 13]