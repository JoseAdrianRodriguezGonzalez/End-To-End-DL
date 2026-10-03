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
)


class TritonClient:
    def __init__(self, base_url: str = TRITON_SERVER_URL):
        self.base_url = base_url.rstrip("/")

    async def preprocess_image(
        self, image_bytes: bytes, width: int = INPUT_SIZE, height: int = INPUT_SIZE
    ) -> np.ndarray:
        image = Image.open(io.BytesIO(image_bytes)).convert("L")
        image = image.resize((width, height), Image.LANCZOS)
        arr = np.array(image).astype(np.float32) / 255.0
        arr = np.expand_dims(arr, axis=0)
        return arr

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

        outputs = data["outputs"][0]
        predictions = np.frombuffer(
            base64.b64decode(outputs["binary_data"]), dtype=np.float32
        ).reshape(outputs["shape"])

        return {"predictions": predictions.tolist(), "top": self._top_k(predictions, k=5)}

    @staticmethod
    def _top_k(predictions: np.ndarray, k: int = 5) -> list[dict]:
        idx = np.argsort(predictions)[::-1][:k]
        return [
            {"index": int(i), "confidence": float(predictions[i])} for i in idx
        ]
