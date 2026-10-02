import torch 
from torch.utils.data import DataLoader 
from torchvision import datasets 
from torchvision.transforms import functional as TF 
from torchvision.transforms import InterpolationMode 
class SegmentationTransform:

    def __init__(self,size=(256,256),augment=Flase):
        self.size =size 
        self.augment =augmnet 
    def __call__(self, img):
        image = TF.resize(img,self.size,interpolation=InterpolationMode.BILINEAR,antialias=True)
        mask = TF.resize(mask,self.size,interpolation=InterpolationMode.NEAREST)
        image=TF.to_tensor(image)
        mask =TF.pil_to_tensor(mask)
        mask = mask.squeeze(0)
        mask = mask.long() 
        return image,mask
