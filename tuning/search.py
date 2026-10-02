import optuna

from tuning.objective import objective
import json

def run_tuning(args):

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
