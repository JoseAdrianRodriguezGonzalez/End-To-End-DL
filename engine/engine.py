import torch
from torch.utils import data
from sklearn.metrics import accuracy_score, f1_score
from callbacks import early_stopping
def train_one_epoch(
    model,dataloader,
    criterion,optimizer,device):
    model.train()
    total_loss = 0
    total_correct = 0
    total_samples = 0 
    all_predictions=[]
    all_labels=[]
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
        
        predictions=outputs.argmax(dim=1)
        all_labels.append(labels.detach().cpu())
        all_predictions.append(predictions.detach().cpu())
    avg_loss=total_loss/total_samples
    all_predictions=torch.cat(all_predictions).numpy()
    all_labels=torch.cat(all_labels).numpy()
    accuracy=accuracy_score(all_labels,all_predictions)
    f1_macro=f1_score(all_labels,all_predictions,average="macro",zero_division=0)
    f1_weighted=f1_score(all_labels,all_predictions,average="weighted",zero_division=0)
    return {"loss":avg_loss,
            "accuracy":accuracy,
            "macro_f1":f1_macro,
            "weighted_f1":f1_weighted}

def evaluate(
    model,dataloader,
    criterion,device):
    model.eval()
    total_loss = 0
    total_correct = 0
    total_samples = 0 
    all_predictions=[]
    all_labels=[]
    with torch.no_grad():
        for inputs,labels in dataloader: 
            inputs=inputs.to(device)
            labels=labels.to(device)
            outputs=model(inputs)
            loss=criterion(outputs,labels)
            total_loss+=loss.item()*inputs.size(0)
            total_samples+=labels.size(0)
            predictions=outputs.argmax(dim=1)
            all_labels.append(labels.cpu())
            all_predictions.append(predictions.cpu())
    avg_loss=total_loss/total_samples
    all_labels=torch.cat(all_labels).numpy()
    all_predictions=torch.cat(all_predictions).numpy()
    accuracy=accuracy_score(all_labels,all_predictions)
    f1_macro=f1_score(all_labels,all_predictions,average="macro",zero_division=0)
    f1_weighted=f1_score(all_labels,all_predictions,average="weighted",zero_division=0)
    return {"loss":avg_loss,
            "accuracy":accuracy,
            "macro_f1":f1_macro,
            "weighted_f1":f1_weighted}

    return avg_loss 
def fit(model,train_loader,val_loader,criterion,optimizer,device,num_epochs,early_stopping=None,scheduler=None):
    history = {
        "train_loss": [],
        "val_loss": [],

        "train_accuracy": [],
        "val_accuracy": [],

        "train_macro_f1": [],
        "val_macro_f1": [],

        "train_weighted_f1": [],
        "val_weighted_f1": [],

        "learning_rate": []
    }
    for epoch in range(num_epochs):
        current_lr=optimizer.param_groups[0]["lr"]
        train_metrics=train_one_epoch(model,train_loader,criterion,optimizer,device)
        val_metrics=evaluate(model,val_loader,criterion,device)
        
        history["train_loss"].append(train_metrics["loss"])
        history["val_loss"].append(val_metrics["loss"])

        history["train_accuracy"].append(train_metrics["accuracy"])
        history["val_accuracy"].append(val_metrics["accuracy"])

        history["train_macro_f1"].append(train_metrics["macro_f1"])
        history["val_macro_f1"].append(val_metrics["macro_f1"])

        history["train_weighted_f1"].append(
            train_metrics["weighted_f1"]
        )

        history["val_weighted_f1"].append(
            val_metrics["weighted_f1"]
        )

        history["learning_rate"].append(current_lr)
        print(
            f"\nEpoch {epoch + 1}/{num_epochs}"
        )

        print(
            f"  Train | "
            f"Loss: {train_metrics['loss']:.4f} | "
            f"Acc: {train_metrics['accuracy']:.4f} | "
            f"Macro F1: {train_metrics['macro_f1']:.4f}"
        )

        print(
            f"  Val   | "
            f"Loss: {val_metrics['loss']:.4f} | "
            f"Acc: {val_metrics['accuracy']:.4f} | "
            f"Macro F1: {val_metrics['macro_f1']:.4f}"
        )

        print(
            f"  LR: {current_lr:.2e}"
        )
        if scheduler is not None:
            scheduler.step(val_metrics["loss"])
        if early_stopping is not None:
            early_stopping(model,val_metrics["loss"])
            if early_stopping.early_stop:
                print("Eraly stopping triggered")
                break 
    return history

