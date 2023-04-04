import logging
from logging.handlers import TimedRotatingFileHandler


class MultiprocessingHandler(logging.Handler):
    def __init__(self):
        
        self._handler = TimedRotatingFileHandler('loggingtest.log', ###변경
                                when='H', #시간 단위 저장
                                interval=1,
                                backupCount=5,)
        
    def logging_child(self):
    
        self._handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter("%(asctime)s %(processName)s %(levelname)s %(message)s")

        self._handler.suffix = '%Y%m%d_%H-%M-%S'
        self._handler.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self._handler)
        
        return logger


