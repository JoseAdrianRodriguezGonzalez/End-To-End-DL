from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import httpx

from config import TRITON_SERVER_URL, TRITON_MODEL_NAME
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
        async with httpx.AsyncClient() as c:
            r = await c.get(f"{TRITON_SERVER_URL}/v2/health/live", timeout=5.0)
            if r.status_code == 200:
                return {"status": "healthy", "triton": "ok"}
    except httpx.RequestError:
        pass
    return {"status": "unhealthy", "triton": "error"}


@app.get("/api/models")
async def list_models() -> dict:
    try:
        async with httpx.AsyncClient() as c:
            r = await c.get(f"{TRITON_SERVER_URL}/v2/repository/index", timeout=10.0)
            r.raise_for_status()
            return r.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Cannot reach Triton: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@app.post("/api/predict")
async def predict(file: UploadFile = File(...)) -> dict:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    image_bytes = await file.read()

    try:
        result = await client.infer(TRITON_MODEL_NAME, image_bytes)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502, detail=f"Error en el servidor de inferencia: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

    return {"model": TRITON_MODEL_NAME, **result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
