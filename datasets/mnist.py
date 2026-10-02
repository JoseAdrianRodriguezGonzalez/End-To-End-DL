from numpy import full
import torch
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
def get_mnist_loader(data_dir,batch_size=64,val_split=0.2):
    train_transform = transforms.Compose([
        transforms.RandomRotation(10),
        transforms.RandomAffine(degrees=0,translate=(0.1,0.1),),
        transforms.ToTensor(),
        #MNIST mean 0.1307 std 0.3081 
        transforms.Normalize((0.1307,),(0.3081,))]
    )
    val_transform =transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,),(0.3081,))]
    )
    full_train_dataset = datasets.MNIST(
        data_dir,
        train=True,
        transform=train_transform,
        download=True
    )
    
    test_dataset = datasets.MNIST(
        data_dir,
        train=False,
        transform=val_transform,
        download=True
    )
    val_size= int(len(full_train_dataset)*val_split)
    train_size=len(full_train_dataset)-val_size
    train_dataset,val_dataset = random_split(full_train_dataset,[train_size,val_size],generator=torch.Generator().manual_seed(42))
    
    train_loader=DataLoader(train_dataset,batch_size=batch_size,shuffle=True)
    val_loader=DataLoader(val_dataset,batch_size=batch_size,shuffle=False)
    test_loader=DataLoader(test_dataset,batch_size=batch_size,shuffle=False)
    return train_loader,val_loader,test_loader
