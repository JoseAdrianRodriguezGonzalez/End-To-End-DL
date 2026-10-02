import optuna

from tuning.objective import objective
import json
import os 
def run_tuning(args):
    dirname=os.path.dirname(args.output_path)
    if dirname:
        os.makedirs(dirname,exist_ok=True)
    print("Starting hyperparameter tuning...")
    study = optuna.create_study(
        direction="minimize"
    )

    study.optimize(
        objective,
        n_trials=args.trials
    )

    print("Best parameters:")
    print(study.best_params)

    print("Best value:")
    print(study.best_value)
    with open(args.output_path,"w") as file : 
        json.dump(study.best_params,file,indent=4)
