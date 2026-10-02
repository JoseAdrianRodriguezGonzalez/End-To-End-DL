import torch.nn as nn 
from models.base import BaseNN 

class MLP(BaseNN):
    def __init__(self) -> None:
        super(MLP,self).__init__(name="MLP")
        self.network = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28,128),
            nn.ReLU(),
            nn.Linear(128,10), #logits
        )
    def forward(self,x):
        return self.network(x)
