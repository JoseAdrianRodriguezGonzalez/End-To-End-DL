import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
def plot_history(history,output):
    epochs=range(1,len(history["train_loss"])+1)
    fig=plt.figure()
    plt.plot(epochs,history["train_loss"],label='Training loss')
    plt.plot(epochs,history["val_loss"],label="Val loss")
    plt.xlabel("epochs")
    plt.ylabel('loss')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output,"epochs.png"),dpi=300)
    
    plt.figure() 
    plt.plot(epochs,history["learning_rate"],label="Learning rate")
    plt.xlabel("epochs")
    plt.ylabel('learning rate')
    plt.yscale("log")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output,"learning_rate.png"),dpi=300)
    
