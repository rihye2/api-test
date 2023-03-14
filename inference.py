from autologging import logged
import logging
import torch
from torch.utils.data import DataLoader
from models.dataset import TestDataset
from models.model import TestModel
from torchvision import transforms
import numpy as np

@logged
class InferenceModel:
    """
    """
    def __init__(self,
                 model: TestModel,
                 device,
                )-> None:
    
        self.model = model
        self.device = device
    
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
    
    
    def inference(self, image):
        transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((512,512)),
            transforms.ToTensor(),
            #transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                        ])
        image = transform(image).unsqueeze(0)
        self.model.eval()
        with torch.no_grad():
            output = self.model(image)
            pred = output.argmax(dim=1).item()
            
        return pred
    
    
        