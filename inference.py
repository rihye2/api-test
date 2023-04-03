from autologging import logged
import logging
import torch
from torch.utils.data import DataLoader
from models.dataset import TestDataset
from models.model import TestModel
from torchvision import transforms
import numpy as np
import io
from PIL import Image
import cv2



@logged
class InferenceModel:
    """
    """
    def __init__(self,
                 model: TestModel,
                 device,
                 model_name: str,
                 model_version: str
                )-> None:
    
        self.model = model
        self.device = device
        self.model_name = model_name
        self.model_version = model_version
        
    def inference_all(self, image_path):
        infer_dataset = TestDataset(image_path)
        infer_loader = DataLoader(infer_dataset, batch_size=1, shuffle=False)
        
        self.model.eval()
        
        for file, imgs in infer_loader:
            
            imgs = imgs.to(self.device)
            
            with torch.no_grad():
                output = self.model(imgs)
                # pred = output.argmax(dim=1).item()
                pred = output.argmax(dim=1).tolist()
                
        return pred
    
    
    def inference(self, image_bytes):
        transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((512,512)),
            transforms.ToTensor(),
            #transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                        ])
        dataByteIo = io.BytesIO(image_bytes)
        image = Image.open(dataByteIo).convert('RGB')
        array_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        
        image = transform(array_image).unsqueeze(0)
        self.model.eval()
        with torch.no_grad():
            output = self.model(image)
            pred = output.argmax(dim=1).item()
            
        return pred
    
    
        