from callbacks.early_stopping import EarlyStopping
from utils.device import get_device
from utils.plotting import plot_history
from datasets.animals import ImageDataset
from engine.engine import evaluate, fit
from models.factory import create_model 

import torch
import torch.nn as nn
import torch.optim as optim


def train_model(**params):
    batch_size = params.get("batch_size", 64)
    learning_rate = params.get("learning_rate", 1e-3)
    epochs = params.get("epochs", 100)
    patience = params.get("patience", 10)
    min_delta = params.get("min_delta", 1e-3)
    device = get_device()
    print(f"Training on {device}")
    
    dataset_class=ImageDataset("data",batch_size)
    
    train, val, test = dataset_class.get_loaders()

    model = create_model("vgg11")
    model.to(device)

    # Función de pérdida
    criterion = nn.CrossEntropyLoss()

    # Optimizador
    optimizer = optim.AdamW(
        model.parameters(),
        lr=learning_rate
    )

    # Scheduler
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=0.1,
        patience=2
    )

    # Early stopping
    early_stopping = EarlyStopping(patience,min_delta)

    # Entrenamiento
    history = fit(
        model,
        train,
        val,
        criterion,
        optimizer,
        device,
        epochs,
        early_stopping,
        scheduler
    )
    early_stopping.restore_model(model)
    return model, history, test, criterion, device



