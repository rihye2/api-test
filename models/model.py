import torchvision.models as models
import torch.nn as nn
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class TestModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = models.resnet18(pretrained='ResNet18_Weights.DEFAULT')
        # self.num_features = self.net.fc.in_features
        
    def forward(self, x):
        model = self.net(x)
        
        # model.fc = nn.Sequential(
        #     nn.Dropout(0.5),
        #     nn.Linear(self.num_features, 512),
        #     nn.Dropout(0.2),
        #     nn.Linear(256, 128),
        #     nn.Dropout(0.1),
        #     nn.Linear(128, 4),
        # )
        
        return model

