import torch.nn as nn 
from models.base import BaseNN 
class CNN(BaseNN):
    def __init__(self):
        super(CNN,self).__init__(name="cnn")
        self.features =nn.Sequential(
            nn.Conv2d(1,16,kernel_size=3,padding=1,stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            #features map 
            #nn.Dropout2d(0.1),
            nn.Conv2d(16,32,kernel_size=3,padding=1,stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            #nn.Dropout2d(0.1),
        )
        
        self.classifier =nn.Sequential(
            nn.Flatten(),
            nn.Linear(32*7*7,128),
            nn.ReLU(),
            #nn.Dropout(0.1),
            nn.Linear(128,10)
        ) 
        
    def forward(self,x):
        features=self.features(x)
        out=self.classifier(features)
        return out
