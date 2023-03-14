

from fastapi import (
    FastAPI, 
    status,
    UploadFile,
    File
) 
import torch
import torch.nn as nn
from dependency_injector.wiring import (
    inject,
)
from typing import List
from base import Base64Response, Base64Request
from inference import InferenceModel
from models.model import TestModel
# import args

import base64
import cv2
import io
from PIL import Image
import numpy as np


import os

cuda = False
lr = 0.001
'''
model load 

'''
device = torch.device("cuda" if cuda else "cpu")
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
          summary="inference path")
@inject
async def inference_path(img_path: str):
    infer_model = InferenceModel(model, device)
    file, pred = infer_model.inference_all(img_path)
    return {"prediction": pred}


@app.post("/uploadimages/",
          status_code=status.HTTP_200_OK,
          summary="upload image files")
@inject
async def create_upload_files(image: UploadFile = File(...)):
    image_bytes = await image.read()
    dataByteIo = io.BytesIO(image_bytes)
    image = Image.open(dataByteIo).convert('RGB')
    array_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    
    infer_model = InferenceModel(model, device)
    result = infer_model.inference(array_image)
    return {"prediction":result}



# @app.post("/inference")
# async def inference(img_path: str):
    
#     file_list = os.listdir(img_path)
    
#     input_list = []
#     for file_name in file_list:
#         image_path = os.path.join(img_path, file_name)
#         image = Image.open(image_path).convert('RGB')
#         input_list.append(image)
        
        
        
        
    
    