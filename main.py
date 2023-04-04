from fastapi import (
    FastAPI, 
    status,
    UploadFile,
    File,
)
import torch
from dependency_injector.wiring import (
    inject,
)
from typing import List
from base import Base64Request, BaseResponse
from inference import InferenceModel
from models.model import TestModel
# import args

import base64
import cv2
import io
from PIL import Image
import numpy as np

import logging
from logging.handlers import RotatingFileHandler
import os
import time
from filelog import FileLogging
import yaml

# __all__ =[
#     "create_upload_files"
# ]

with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

# logger = logging.getLogger('inference_history')
# logger.setLevel(logging.DEBUG)


path = os.path.join(cfg['log_dir'], cfg['log_main_file'])

# rotating_file_handler = RotatingFileHandler(path, mode='w', maxBytes=1024, backupCount=5)
# formatter = logging.Formatter('[%(levelname)s] :: %(asctime)s :: %(module)s ::%(name)s :: %(message)s\n')

# rotating_file_handler.setFormatter(formatter)

# logger.addHandler(rotating_file_handler)


logger = FileLogging('infer', path)
log = logger.rotating_file_handler()


'''
model load 

'''
device = torch.device("cuda" if cfg['cuda'] else "cpu")
#model structure load
model = TestModel()

#model weight file
# checkpoint = torch.load('path')
# model.load_state_dict(checkpoint['model_state_dict']) 

model.to(device)
# model = nn.DataParallel(model)

'''

inference
'''

def base64_img_to_str(img_string):
    
    img_data = base64.b64decode(img_string)
    dataByteIo = io.BytesIO(img_data)
    image = Image.open(dataByteIo).convert('RGB')
    
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)


app = FastAPI()

@app.post("/inference_base64str/",
        status_code=status.HTTP_200_OK,
        summary="Inference base64 결과")
@inject
async def inference(request: Base64Request):
    
    image = base64_img_to_str(request.base64_image)
    infer_model = InferenceModel(model, device)
    result = infer_model.inference(image)
    return {"prediction":result}
    

@app.post("/inference_all/", 
          status_code=status.HTTP_200_OK,
          summary="inference folder all img")
@inject
async def inference_path(path: BaseResponse):
    infer_model = InferenceModel(model, device)
    pred = infer_model.inference_all(path.img_folder)
    return {"prediction": pred}


@app.post("/inference_image/", 
          status_code=status.HTTP_200_OK,
          summary="inference image")
@inject
async def inference_image(path: BaseResponse):
    
    with open(path.img_folder, 'rb') as f:
        img_data = f.read()
    
    if len(img_data) == 0:
        raise ValueError("image가 존재하지 않습니다.")

    infer_model = InferenceModel(model, device)
    pred = infer_model.inference(img_data)
    
    return {"prediction": pred}



@app.post("/uploadimages/",
          status_code=status.HTTP_200_OK,
          summary="upload image files")
@inject
async def create_upload_files(imagefile: UploadFile = File(...)):
    #start time 
    start_time = time.time()
    
    image_bytes = await imagefile.read()

    img_load_end = time.time()
    infer_model = InferenceModel(model, device)
    
    result = infer_model.inference(image_bytes)
    #end time
    end_time = time.time()
    
    msg = str(
                {"image_id": imagefile.filename,
            #    "model_name": infer_model.model_name,
                # "model_version": infer_model.model_version,
                "image load time": np.round(img_load_end - start_time, 3),
                "inference time": np.round(end_time - img_load_end, 3)
               }
    )
    
    log.debug(msg)
    
    return {"prediction":result}



@app.post("/stat/", 
          status_code=status.HTTP_200_OK,
          summary="stat")
@inject
async def stat():
    return {'aa'}
    