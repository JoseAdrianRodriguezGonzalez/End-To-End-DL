import optuna

from training.trainer import train_model


def objective(trial: optuna.Trial) -> float:
    params = {
        "batch_size": trial.suggest_categorical(
            "batch_size",
            [32, 64, 128]
        ),

        "learning_rate": trial.suggest_float(
            "learning_rate",
            1e-4,
            1e-1,
            log=True
        ),

        "weight_decay": trial.suggest_float(
            "weight_decay",
            1e-6,
            1e-2,
            log=True
        ),

        "epochs": 100,
        "patience": 10,
        "min_delta": 1e-3,
    }
    model, history, _,_,_ = train_model(**params)

    return min(history["val_loss"])
