import base64
import io

import httpx
import numpy as np
from PIL import Image

from config import (
    TRITON_SERVER_URL,
    TRITON_MODEL_NAME,
    TRITON_INPUT_NAME,
    TRITON_OUTPUT_NAME,
    INPUT_SIZE,
    CLASS_NAMES
)

#iMAGENET noramlization 
MEAN=np.array(
    [0.485,0.456,0.406],
    dtype=np.float32
)
STD=np.array(
    [0.229,0.224,0.225],
    dtype=np.float32
)
class TritonClient:
    def __init__(self, base_url: str = TRITON_SERVER_URL):
        self.base_url = base_url.rstrip("/")

    async def preprocess_image(
        self, image_bytes: bytes, width: int = INPUT_SIZE, height: int = INPUT_SIZE
    ) -> np.ndarray:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        arr = np.asarray(image,dtype=np.float32)/255.0
        arr=(arr-MEAN)/STD 
        arr=np.transpose(arr,(2,0,1))
        arr = np.expand_dims(arr, axis=0)
        return np.ascontiguousarray(arr,dtype=np.float32)

    async def infer(self, model_name: str, image_bytes: bytes) -> dict:
        arr = await self.preprocess_image(image_bytes)

        payload = {
            "inputs": [
                {
                    "name": TRITON_INPUT_NAME,
                    "datatype": "FP32",
                    "shape": list(arr.shape),
                    "binary_data": base64.b64encode(arr.tobytes()).decode("utf-8"),
                }
            ],
            "outputs":[
                {
                    "name":TRITON_OUTPUT_NAME,
                    "binary_data":True 
                }
            ]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v2/models/{model_name}/infer",
                json=payload,
                timeout=120.0,
            )
            response.raise_for_status()
            data = response.json()
        output=next(output for output in data["outputs"] if output["name"]==TRITON_OUTPUT_NAME)
        predictions = np.frombuffer(
            base64.b64decode(output["binary_data"]), dtype=np.float32
        ).reshape(output["shape"])
        probabilities=self._softmax(predictions)

        return {"logits":predictions.tolist(),"probabilities":probabilities.tolist(),"top":self._top_k(probabilities,k=5)}

    @staticmethod
    def _softmax(logits:np.ndarray)->np.ndarray:
        logits=logits-np.max(logits,axis=1,keepdims=True)
        probabilites=np.exp(logits)
        probabilites/=probabilites.sum(axis=1,keepdims=True)
        return probabilites

    @staticmethod
    def _top_k(predictions: np.ndarray, k: int = 5) -> list[dict]:
        idx = np.argsort(predictions)[::-1][:k]
        return [
            {"index": int(i), "confidence": float(predictions[i])} for i in idx
        ]
