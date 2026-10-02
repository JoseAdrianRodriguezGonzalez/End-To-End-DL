import torch

from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms


class ImageDataset:
    def __init__(self,data_dir,batch_size=64,val_split=0.2,test_split=0.1,image_size=(224, 224),seed=42):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.val_split = val_split
        self.test_split = test_split
        self.image_size = image_size
        self.seed = seed

    def get_loaders(self):

        train_transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize(
                (0.485, 0.456, 0.406),
                (0.229, 0.224, 0.225)
            )
        ])

        eval_transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize(
                (0.485, 0.456, 0.406),
                (0.229, 0.224, 0.225)
            )
        ])

        base_dataset = datasets.ImageFolder(self.data_dir)

        total_size = len(base_dataset)

        test_size = int(total_size * self.test_split)
        val_size = int(total_size * self.val_split)
        train_size = total_size - val_size - test_size

        generator = torch.Generator().manual_seed(self.seed)

        indices = torch.randperm(total_size,generator=generator).tolist()

        train_indices = indices[:train_size]

        val_indices = indices[train_size:train_size + val_size]

        test_indices = indices[train_size + val_size:]

        train_dataset = Subset(
            datasets.ImageFolder(
                self.data_dir,
                transform=train_transform
            ),
            train_indices
        )

        val_dataset = Subset(
            datasets.ImageFolder(
                self.data_dir,
                transform=eval_transform
            ),
            val_indices
        )

        test_dataset = Subset(
            datasets.ImageFolder(
                self.data_dir,
                transform=eval_transform
            ),
            test_indices
        )

        train_loader = DataLoader(
            train_dataset,
            batch_size=self.batch_size,
            shuffle=True
        )

        val_loader = DataLoader(
            val_dataset,
            batch_size=self.batch_size,
            shuffle=False
        )

        test_loader = DataLoader(
            test_dataset,
            batch_size=self.batch_size,
            shuffle=False
        )

        return train_loader, val_loader, test_loader
