import multiprocessing
import time
import requests
import numpy as np
from time_format import time_format
import yaml
import logging
import logging.config

with open("watcher/conf/config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


def setup_logging():
    with open('watcher/conf/log.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        
    logger = logging.getLogger('child_logger')
    return logger


# 필요한 모듈 import
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
from multiprocessing import Pool
from logging.handlers import TimedRotatingFileHandler
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# logger 및 process 모듈 import
from filehandler import MultiprocessingHandler

from multiprocess_logging import mpLogging
import logging
import time
from time_format import time_format



class Watcher:
    def __init__(self, path, logger):
        self.observer = Observer() # Observer 객체 생성
        self.path = path

        # self.logger = logger
        self._handler = TimedRotatingFileHandler('watcher.log',
                                                 when='H',
                                                 backupCount=5)
        
        self._handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s %(processName)s %(levelname)s %(message)s")
        self._handler.suffix = 'log-%Y%m%d'
        self._handler.setFormatter(formatter)
    
    # def setup_logging():
    #     with open('watcher/conf/log.yaml', 'r') as f:
    #         config = yaml.safe_load(f.read())
    #     logging.config.dictConfig(config)
        
    #     logger = logging.getLogger('child_logger')
    #     return logger    

    def run(self): 
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(self._handler)
        
        event_handler = CustomHandler(self.path, logger)
        
        # observer에 event_handler 등록
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(0)
        
        except KeyboardInterrupt:
            self.observer.stop()
            self.observer.join()

                
class CustomHandler(FileSystemEventHandler):
    
    def __init__(self, path, logger):
        super().__init__()
        self.path = path
        self.logger = logger

    def on_created(self, event):
        # 파일 생성 이벤트 발생 시, .jpg 확장자를 가진 이미지 파일만 처리
        _, str_time = time_format()
        self.logger.info(f">>>>>>>>> [Created] {event.src_path}: {str_time}")
        
        if event.src_path.endswith('.jpg'):
            
            print(">>>>>>>>>>>>>>>1", event.src_path)
            # 이미지 파일 경로를 fn_process 함수에 전달하여 비동기적으로 처리
            pool.apply_async(fn_process, (event.src_path, ))
            
            #move or delete
        

def fn_process(img_path):
    print(">>>>>>>>> fn_process : start")
    img = mplogger.print_process(img_path)
    print(">>>>>>>>> fn_process : end - ", img)
    

# Global 변수 선언
multilogging = MultiprocessingHandler()
logger = setup_logging()
# logger = multilogging.logging_child()
mplogger = mpLogging(logger)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    pool = Pool(5)

    watcher = Watcher(path='images', logger=logger)
    watcher.run()
    
    pool.close()
    pool.join()