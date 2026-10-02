import argparse
from tuning.search import run_tuning 
from training.runner import run_final_training
from serving.export_cnn_onnx import model_extract
def main():
    parser = argparse.ArgumentParser(description="End-To-End deep learning pipelin")
    subparsers = parser.add_subparsers(dest="command",required=True)

    tune_parser=subparsers.add_parser("tune")
    tune_parser.add_argument("--trials",type=int, default=20)
    tune_parser.add_argument("--output_path",type=str, default="artifacts/best_params.json")
    tune_parser.set_defaults(func=run_tuning)


    train_parser =subparsers.add_parser("trainer")

    train_parser.add_argument("--params",required=True)
    train_parser.add_argument("--output_path",required=True) 
    train_parser.add_argument("--output_media",required=True)
    train_parser.set_defaults(func=run_final_training)
    export_parser = subparsers.add_parser("export")

    export_parser.add_argument("--model",type=str,default="artifacts/best_model.pth")
    export_parser.add_argument("--name",type=str,default="mlp")
    export_parser.add_argument("--labels",type=int,default=10)
    export_parser.add_argument("--output", type=str,default="serving/model_repository/cnn/1/model.onnx")
    export_parser.add_argument("--device", type=str,default="cpu",choices=["cpu","cuda","mps"])
    export_parser.set_defaults(func=model_extract)
if __name__ == "__main__":
    main()
