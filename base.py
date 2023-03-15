from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime

class Base64Request(BaseModel):
    base64_image: str

class Base64Response(Base64Request):
    response_result: int


class BaseResponse(BaseModel):
    img_folder: str

# class ModelListRequest(BaseModel):
    # model_id: str
    # path: str
    # create_dt: Optional[datetime] = datetime.now()
