import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler 

#LoggingEventHandler : Logs all the events captured
#observer thread that schedules watching directories and dispatches calls to event handlers

class Watcher:
    
    def __init__(self, path):
        self.observer = Observer()
        self.path = path
    def run(self):
         
        logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        # event_handler = LoggingEventHandler()
        # event_handler = CustomHandler()
        event_handler = EventHandler()
    
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            self.observer.stop()
        
        self.observer.join()
                
class CustomHandler(FileSystemEventHandler):
    # def on_created(self, event):
    #     return super().on_created(event)
    def on_any_event(self, event):
        
        if event.is_directory:
            return None
        elif event.event_type == "created":
            # model inference 
            print('file created')
        elif event.event_type == "modified":
            # img modified.. -> re-infer?
            print('file modified')
        elif event.event_type == "deleted":
            print('file deleted')

class EventHandler(LoggingEventHandler):
    def on_any_event(self, event):
        
        if event.event_type == "created":
            return print('file create')
        elif event.event_type == "modified":
            return print('file create')
        elif event.event_type == "deleted":
            return print('file deleted')



if __name__ == '__main__':
    watch = Watcher(path='.')
    watch.run()

    
