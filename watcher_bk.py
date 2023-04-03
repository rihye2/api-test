from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler 
import logging
import time
import multiprocessing
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from filelog import FileLogging, MultiprocessingLog
import os
from multiprocessing import current_process
from process import Process

#LoggingEventHandler : Logs all the events captured
#observer thread that schedules watching directories and dispatches calls to event handlers

class Watcher:
    
    def __init__(self, path):
        self.observer = Observer()
        self.path = path
        self.queue = multiprocessing.Queue()
        
    def run(self): 
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        event_handler = CustomHandler(self.path, self.queue)
        # event_handler = EventHandler(self.path, self.queue)
    
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(0)
        
        except KeyboardInterrupt:
            self.observer.stop()
        
        self.observer.join()
        self.queue.put('done')
        
        return self.queue
                
class CustomHandler(FileSystemEventHandler):
    
    def __init__(self, path, queue):
        super().__init__()
        self.path = path
        self.queue = queue

    def on_created(self, event):
        # filename = os.path.basename(event.src_path)
        if event.src_path.endswith('.jpg'):
            self.queue.put(event.src_path) 
            #created된 img file path를 queue에 넣어줌
        return print('created')

class EventHandler(LoggingEventHandler):
    def __init__(self, path, queue):
        super().__init__()
        self.path = path
        self.queue = queue
        
    def on_created(self, event):
        if event.src_path.endswith('.jpg'):
            self.queue.put(event.src_path) #created된 img file path를 queue에 넣어줌
            
    # def on_moved(self, event):
        # if os.path.basename(event.src_path).endswith('.jpg'):
        

def child_process(img_path):
    response = requests.post("https://localhost:8000/inference_all", json={'img_folder': img_path})
    return response.json()


if __name__ == '__main__':
    
    watch = Watcher(path='./images/')
    multilogging = MultiprocessingLog()
    pool = multiprocessing.Pool(processes=5)

    #child에서 log 찍어서 각 pid 별로 path를 제대로 받았는지 확인
    q = watch.run()
    logger = multilogging.logging_child()

    
    
    while True:
        if not q.empty():
            img_path = q.get()
            process = Process(logger, img_path)        
                
            # pool.map(process.print_process(), img_path)
            pool.apply_async(process, print_process, args=(img_path,))
            
            logger.debug('ss')
            
            # print(img_path)
            if img_path == 'done':
                pool.close()
                break
                
        


    
