import logging
from logging.handlers import RotatingFileHandler, QueueHandler
import multiprocessing



class FileLogging:
    def __init__(self, name, file_name) -> None:
        self.name = name
        # self.logger = logging.getLogger(name)
        
        self.formatter = logging.Formatter('[%(levelname)s] :: %(asctime)s :: %(module)s ::%(name)s :: %(message)s\n')
        self.file_name = file_name
        
    def rotating_file_handler(self):
        
        rotating_file_handler = RotatingFileHandler(self.file_name, mode='a', maxBytes=1024, backupCount=5)
        rotating_file_handler.setLevel(logging.DEBUG)
        rotating_file_handler.setFormatter(self.formatter)
        
        queue = multiprocessing.Queue()
        # queue_listener = QueueListener(queue, rotating_file_handler)
        # queue_listener.start()
        
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(rotating_file_handler)
        
            
