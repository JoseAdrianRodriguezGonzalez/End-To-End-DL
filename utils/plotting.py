import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

def plot_history(history, output):
    os.makedirs(output, exist_ok=True)
    epochs = range(1, len(history["train_loss"]) + 1)
    # --------------------------------
    # Loss
    # --------------------------------

    plt.figure()

    plt.plot(epochs,history["train_loss"],label="Training loss")
    plt.plot(epochs,history["val_loss"],label="Validation loss")
    plt.xlabel("Epochs")
    plt.ylabel("Cross Entropy Loss")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output, "loss.png"),dpi=300,bbox_inches="tight")
    plt.close()

    # --------------------------------
    # Learning rate
    # --------------------------------

    plt.figure()
    plt.plot(epochs,history["learning_rate"],label="Learning rate")
    plt.xlabel("Epochs")
    plt.ylabel("Learning rate")
    plt.yscale("log")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output, "learning_rate.png"),dpi=300,bbox_inches="tight")
    plt.close()

    # --------------------------------
    # Accuracy
    # --------------------------------

    plt.figure()
    plt.plot(epochs,history["train_accuracy"],label="Training accuracy")
    plt.plot(epochs,history["val_accuracy"],label="Validation accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output, "accuracy.png"),dpi=300,bbox_inches="tight")
    plt.close()

    # --------------------------------
    # Macro F1
    # --------------------------------

    plt.figure()
    plt.plot(epochs,history["train_macro_f1"],label="Training Macro F1")
    plt.plot(epochs,history["val_macro_f1"],label="Validation Macro F1")
    plt.xlabel("Epochs")
    plt.ylabel("Macro F1")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output, "macro_f1.png"),dpi=300,bbox_inches="tight")
    plt.close()

    # --------------------------------
    # Weighted F1
    # --------------------------------

    plt.figure()
    plt.plot(epochs,history["train_weighted_f1"],label="Training Weighted F1")
    plt.plot(epochs,history["val_weighted_f1"],label="Validation Weighted F1")
    plt.xlabel("Epochs")
    plt.ylabel("Weighted F1")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output, "weighted_f1.png"),dpi=300,bbox_inches="tight")
    plt.close()
    
