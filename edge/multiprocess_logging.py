import multiprocessing
import time
import requests
import numpy as np
class mpLogging():
    def __init__(self, logger):
        self.logger = logger
        self.api_url = 'http://localhost:8000/inference_image'           
        
    def infer(self, img_path, process_id):
        infer_start = np.round(time.time(), 3)
        self.logger.info(f">>>>>>>>> [Inference start] [Process]-{process_id} : {infer_start}")
        
        response = requests.post(self.api_url, 
                            headers={'Content-type': 'application/json'},
                            json={'img_folder':img_path})
        
        assert response.status_code == 200
    
        infer_time = np.round(time.time() - infer_start, 3)
        
        output = response.json()
        print('>>>>>>>>> API response:', output)
        self.logger.info(f">>>>>>>>> [Inference Result] [Process]-{process_id} : {output}")
        self.logger.info(f">>>>>>>>> [Inference total time] [Process]-{process_id} : {infer_time}")
        
    def print_process(self, img_path):
        time.sleep(2)
        
        c_proc = multiprocessing.current_process()
        process_id = c_proc.pid
        # process_name = c_proc.name
        self.logger.info(f">>>>>>>>> [Image path] [Process]-{process_id} : {img_path} .")
        
        
        self.infer(img_path, process_id)
        
        
        return img_path