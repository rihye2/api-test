import time
import base64
import requests
import cv2
from PIL import Image
import io
import numpy as np

 

class testapi:
    def __init__(self, count, path) -> None:
        self.host = 'http://localhost:8000/'
        self.urls = [
            'inference_base64str',
            'inference_all',
            'uploadimages'
        ]
        self.count = count
        self.headers = {'Content-type': 'application/json'}
        self.path = path
    
    def base64_requests(self):
        url_ = self.host + self.urls[0]
        result = []
        with open(self.path, "rb") as image_file:
            img_string = base64.b64encode(image_file.read())
            for _ in range(self.count):
                start_time = time.time()
                response = requests.post(url_, 
                                headers=self.headers, 
                                json={'base64_image': img_string.decode('utf-8')})
                assert response.status_code == 200
                end_time = time.time()
                total_time = end_time - start_time
                result.append(total_time)
        
        return print("Base64 average time:", np.round(sum(result)/self.count,3))
        
    def uploadimage_requests(self):
        url_ = self.host + self.urls[2]
        result = []
        with open(self.path, "rb") as image_file:
            files = {'image': image_file}
            for _ in range(self.count):
                start_time = time.time()
                response = requests.post(url_, files=files)
                assert response.status_code == 200
                end_time = time.time()
                total_time = end_time - start_time
                result.append(total_time)
        # print(response.json())
        return print("uploadFile average time:", np.round(sum(result)/self.count),3)
    
        
if __name__ == '__main__':
    path = "/Users/hyeri/Downloads/images/30_1.jpg"
    tester = testapi(10, path)
    tester.base64_requests()
    # tester.uploadimage_requests()
    