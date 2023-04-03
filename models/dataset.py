import os
import numpy as np
import cv2
import torch
import torch.nn as nn
from PIL import Image
import pandas as pd
from torchvision import transforms


## 데이터 로더를 구현하기
class Dataset(torch.utils.data.Dataset):
    def __init__(self, transform=None):
        self.transform = transform
        img_path = '/home/user01/pill_data/pill_test_only/220426'

        img_lst = os.listdir(img_path)

        cls_input=[]
        cls_label=[]
        
        # import pdb; pdb.set_trace()
        for i in img_lst:
            input_ = cv2.imread(os.path.join(img_path, i))
            cls_input.append(input_)
            cls_label.append(int(i[-5]))

        self.cls_input = cls_input
        self.cls_label = cls_label
        

    def __len__(self):
        return len(self.cls_input)

    def __getitem__(self, index):
        input_ = self.cls_input[index]
        label = self.cls_label[index]
        # input = Image.open(os.path.join(self.data_dir, img_lst))

        # data = {'input': input, 'label': label}

        if self.transform:
            input_ = self.transform(input_)

        return input_, label

#20220607 real test image 확인용
#input file name, input, label
class TestDataset(torch.utils.data.Dataset):
    def __init__(self, img_path):
        
        self.transform = transforms.Compose([transforms.ToPILImage(), transforms.Resize((512,512)),
                                        transforms.ToTensor(), #transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                        ])
        
        self.img_lst = os.listdir(img_path)
        
        
        self.input_list=[]
        self.cls_input=[]
        
        for i in self.img_lst:
            image = cv2.imread(os.path.join(img_path, i))
            self.input_list.append(i)
            self.cls_input.append(image)
        
            
    def __len__(self):
        return len(self.cls_input)

    def __getitem__(self, index):
        file_list = self.input_list[index]
        image = self.cls_input[index]
        
        if self.transform:
            image = self.transform(image)

        return file_list, image
