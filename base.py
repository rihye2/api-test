from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime

class Base64Request(BaseModel):
    base64_image: str

class ModelListRequest(BaseModel):
    model_id: str
    path: str
    create_dt: Optional[datetime] = datetime.now()

# class BaseResponse(BaseModel):
#     file_name: str = Field(None, description='이미지 파일 정보')
#     # product_code: str = Field(None, description='제품 코드')
        

