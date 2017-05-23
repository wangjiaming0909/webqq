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