import torch
from torch.utils import data

from callbacks import early_stopping
def train_one_epoch(
    model,dataloader,
    criterion,optimizer,device):
    model.train()
    total_loss = 0
    total_correct = 0
    total_samples = 0 
    for inputs,labels in dataloader: 
        inputs=inputs.to(device)
        labels=labels.to(device)
        outputs=model(inputs)
        loss=criterion(outputs,labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss+=loss.item()*inputs.size(0)
        total_samples+=labels.size(0)
    avg_loss=total_loss/total_samples
    return avg_loss

def evaluate(
    model,dataloader,
    criterion,device):
    model.eval()
    total_loss = 0
    total_correct = 0
    total_samples = 0 
    with torch.no_grad():
        for inputs,labels in dataloader: 
            inputs=inputs.to(device)
            labels=labels.to(device)
            outputs=model(inputs)
            loss=criterion(outputs,labels)
            total_loss+=loss.item()*inputs.size(0)
            total_samples+=labels.size(0)
    avg_loss=total_loss/total_samples
    return avg_loss 
def fit(model,train_loader,val_loader,criterion,optimizer,device,num_epochs,early_stopping=None,scheduler=None):
    history = {"train_loss":[],
    "val_loss":[],"learning_rate":[]}
    for epoch in range(num_epochs):
        current_lr=optimizer.param_groups[0]["lr"]
        train_loss=train_one_epoch(model,train_loader,criterion,optimizer,device)
        val_loss=evaluate(model,val_loader,criterion,device)
        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["learning_rate"].append(current_lr)
        print(f"Epoch {epoch+1}/{num_epochs}|")
        print(f" train loss: {train_loss:.15f}")
        print(f" val loss: {val_loss:.15f}")
        print(f" Learning rate: {current_lr:.2e}")
        if scheduler is not None:
            scheduler.step(val_loss)
        if early_stopping is not None:
            early_stopping(model,val_loss)
            if early_stopping.early_stop:
                print("Eraly stopping triggered")
                break 
    return history

