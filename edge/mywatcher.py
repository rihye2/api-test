import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from multiprocessing import Pool
import multiprocessing as mp
import time
import os

def func(img_path):
    c_proc = mp.current_process()
    print("Running on Process",c_proc.name,"PID",c_proc.pid, ">>>", img_path)
    time.sleep(2)
    print("Ended",img_path,"Process",c_proc.name)
    return num


class Target:
    watchDir = "./images"
    #watchDir에 감시하려는 디렉토리를 명시한다.

    def __init__(self):
        self.observer = Observer()   #observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
#FileSystemEventHandler 클래스를 상속받음.
#아래 핸들러들을 오버라이드 함

    #파일, 디렉터리가 move 되거나 rename 되면 실행
    def on_moved(self, event):
        print(event)

    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        p.apply_async(func,(event.src_path,))
        print(event)

    def on_deleted(self, event): #파일, 디렉터리가 삭제되면 실행
        print(event)

    def on_modified(self, event): #파일, 디렉터리가 수정되면 실행
        print(event)

p = Pool(4)
start = time.time()

w = Target()
w.run()