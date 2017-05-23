# -*- coding: utf-8 -*-
import Queue
import traceback

def workAt(taskQueue):
    while True:
        try:
            #Remove and return an item from the queue. get()
            func, args, kwargs = taskQueue.get(timeout=0.5)
        except Queue.Empty:
            pass
        else:
            try:
                func(*args, **kwargs)
            except SystemExit:
                raise
            except:
                traceback.print_exc()

class TaskLoop(object):
    def __init__(self):
        self.mainQueue = Queue.Queue()
        self.childQueues = {}
        
    def Put(self, func, *args, **kwargs):
        self.mainQueue.put((func, args, kwargs))


    def Run(self):
        workAt(self.mainQueue)
        

mainloop = TaskLoop()
MainLoop = mainloop.Run
Put = mainloop.Put
#PutTo = mainloop.Put         
#AddWorkerTo = 