from models.base import BaseNN
import torch 
import torch.nn as nn 
import torch.nn.functional as F 
from torchvision.models import vgg11, VGG11_Weights
class VGG11(BaseNN):
    def __init__(self,num_classes) -> None:
        super(VGG11,self).__init__(name="vgg11")
        self.network= vgg11(VGG11_Weights.DEFAULT)
        for parameter in self.network.features.parameters():
            parameter.requires_grad =False
        in_features=self.network.classifier[-1].in_features
        self.network.classifier[-1] =nn.Linear(in_features,num_classes)

    
    def forward(self,x):

        return self.network(x)
    
