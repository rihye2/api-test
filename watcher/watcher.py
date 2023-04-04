# 필요한 모듈 import
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler 
from multiprocessing import Pool
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# logger 및 process 모듈 import
from filehandler import MultiprocessingHandler
from multiprocessing import current_process
from multiprocess_logging import mpLogging
import logging
import time
from time_format import time_format



class Watcher:
    def __init__(self, path, logger):
        self.observer = Observer() # Observer 객체 생성
        self.path = path

        self.logger = logger

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
multilogging = MultiprocessingHandler()
logger = multilogging.logging_child()
mplogger = mpLogging(logger)

if __name__ == '__main__':

    # logging 설정
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # 프로세스 풀 생성
    pool = Pool(5)

    # 이미지 감지 시작
    watcher = Watcher(path='images', logger=logger)
    watcher.run()
    
    # 프로세스 풀 종료
    pool.close()
    pool.join()