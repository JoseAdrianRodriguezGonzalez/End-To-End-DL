import torch 
from functools import cache
@cache
def get_device():
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')
print(get_device())
