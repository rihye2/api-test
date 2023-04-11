# 필요한 모듈 import
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
from multiprocessing import Pool
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from multiprocess_logging import mpLogging
import logging
import logging.config
import time
from time_format import time_format
import yaml


with open("watcher/conf/config.yaml",'r') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


def setup_logging(logger_name):
    with open('watcher/conf/log.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        
    logger = logging.getLogger(logger_name)
    return logger


class Watcher:
    def __init__(self, path, logger):
        self.observer = Observer() # Observer 객체 생성
        self.path = path
        self.logger = setup_logging('watcher_logger')
        
    def run(self): 
        
        event_handler = CustomHandler(self.path, self.logger)
        
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
logger = setup_logging('child_logger')
mplogger = mpLogging(logger)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    pool = Pool(5)

    watcher = Watcher(path='images', logger=logger)
    watcher.run()
    
    pool.close()
    pool.join()