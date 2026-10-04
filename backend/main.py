from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import httpx
import uvicorn
from config import TRITON_SERVER_URL, TRITON_MODEL_NAME,CLASS_NAMES
from triton_client import TritonClient

app = FastAPI(title="Inference API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = TritonClient(TRITON_SERVER_URL)

@app.get("/api/health")
async def health() -> dict:
    try:
        url = (
            f"{TRITON_SERVER_URL}/v2/models/"
            f"{TRITON_MODEL_NAME}/ready"
        )
        print("HEALTH URL:", url)
        async with httpx.AsyncClient() as c:
            r = await c.get(
                url,
                timeout=5.0,
            )

        print("HEALTH STATUS:", r.status_code)
        print("HEALTH BODY:", r.text)

        if r.status_code == 200:
            return {
                "status": "healthy",
                "triton": "ok",
                "model": TRITON_MODEL_NAME,
            }

        return {
            "status": "unhealthy",
            "triton": "error",
            "model": TRITON_MODEL_NAME,
            "triton_status": r.status_code,
        }

    except Exception as error:
        print("HEALTH ERROR:", repr(error))

        return {
            "status": "unhealthy",
            "triton": "error",
            "model": TRITON_MODEL_NAME,
            "error": repr(error),
        }

@app.get("/api/models")
async def list_models() -> dict:
    try:
        async with httpx.AsyncClient() as c:
            r = await c.get(f"{TRITON_SERVER_URL}/v2/repository/index", timeout=10.0)
            r.raise_for_status()
            return {"models":r.json()}
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Cannot reach Triton: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@app.post("/api/predict")
async def predict(file: UploadFile = File(...)) -> dict:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400,detail="El archivo esta vacio")
    try:
        result = await client.infer(TRITON_MODEL_NAME, image_bytes)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502, detail=f"Error en el servidor de inferencia: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")
    top_predictions=[
        {
            "class":CLASS_NAMES[prediction["index"]],
            "index":prediction["index"],
            "confidence":prediction["confidence"]
        }
        for prediction in result["top"]
    ]
    best_prediction=top_predictions[0]


    return {"model": TRITON_MODEL_NAME, "prediction":best_prediction,"top":top_predictions,"probabilities":result["probabilities"]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
