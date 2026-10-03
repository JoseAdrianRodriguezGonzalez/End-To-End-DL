import torch
from engine.engine import evaluate
from utils.plotting import plot_history
from training.trainer import train_model
import json
import os 
def run_final_training(args):
    #Verficiaciones 
    directory=os.path.dirname(args.output_path)
    if directory:
        os.makedirs(directory,exist_ok=True )
    if args.output_media:
        os.makedirs(args.output_media,exist_ok=True)
    with open(args.params) as file:
        params=json.load(file)

    #Ejecuiones 
    model, history, test, criterion, device = train_model(**params)
    test_loss = evaluate(model,test,criterion,device)
    torch.save(model.state_dict(),args.output_path)


    print(f"Test loss: {test_loss}")
    with open(os.path.join(args.output_media,"test.txt"), "w") as f:
        f.write(str(test_loss))
    plot_history(history,args.output_media)

    return model
