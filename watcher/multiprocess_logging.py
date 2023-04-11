import multiprocessing
import time
import requests
import numpy as np
from time_format import time_format
import yaml

with open("watcher/conf/config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


class mpLogging():
    def __init__(self, logger):
        self.logger = logger
        
    def infer(self, img_path):
        
        infer_start, str_infer_time = time_format()
        
        response = requests.post(cfg['url_inference_image'], 
                            headers={'Content-type': 'application/json'},
                            json={'img_folder':img_path})
        
        assert response.status_code == 200
        infer_time = np.round(time.time() - infer_start, 3)
        
        output = response.json()
        print('>>>>>>>>> API response:', output)
        
        msg = f'[result]: {output} | [inference start]: {str_infer_time} | [inference total time]: {infer_time}'
        
        return msg 
    
    def print_process(self, img_path):
        
        _, str_process_time = time_format()
        # time.sleep(2)
        c_proc = multiprocessing.current_process()
        process_id = c_proc.pid
        # process_name = c_proc.name
        
        msg = self.infer(img_path)
        
        self.logger.info(f">>>[process]: {process_id} | [image]: {img_path} | [process start time]: {str_process_time} | {msg}")
        
        return img_path
    
