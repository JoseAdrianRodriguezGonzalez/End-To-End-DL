import torch 
import onnx 
import onnxruntime as ort  
from models.factory import create_model
import os 
def model_extract(args):
    dirname=os.path.dirname(args.output)
    if dirname:
        os.makedirs(dirname,exist_ok=True)
    device=torch.device(args.device)
    model=create_model(args.name,args.labels)
    state_dict= torch.load(args.model,
                           map_location=device,
                           weights_only=True)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval() 
    dummy_input=torch.randn(
        8,1,28,28,
        device=device
    )

    onnx_program= torch.onnx.export(model,(dummy_input,),
                                    input_names=["input"],
                                    output_names=["output"],
                                    dynamic_shapes={
                                    "x":{0:"batch_size"}},dynamo=True)
    onnx_program.save(args.output)
    onnx_model = onnx.load(args.output)
    onnx.checker.check_model(onnx_model)
    with torch.inference_mode():
        torch_output= model(dummy_input)
    providers=(["CUDAExecutionProvider","CPUExecutionProvider"] 
               if args.device == "cuda"
               else
               ["CPUExecutionProvider"])
    session= ort.InferenceSession(args.output,
                                  providers=providers)
    onnx_output=session.run(["output"],{"input":dummy_input.cpu().numpy()})[0]
    torch.testing.assert_close(torch_output.cpu(),torch.tensor(onnx_output),
                              rtol=1e-3,atol=1e-5)
    print("ONNX export succesful")
    print("pytorch and onnx outputs match. ")

