# Backend - Inference API (FastAPI)

API que conecta con el servidor de inferencia Triton para el frontend.

## Instalación

```bash
uv sync
```

## Variables de entorno

Copia `.env.example` a `.env` y ajusta:

```
TRITON_SERVER_URL=http://localhost:8000
TRITON_MODEL_NAME=cnn
TRITON_INPUT_NAME=input
TRITON_OUTPUT_NAME=output
INPUT_SIZE=28
```

## Ejecutar

```bash
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /api/health` — estado de conexión con Triton
- `GET /api/models` — lista de modelos disponibles en el repositorio de Triton
- `POST /api/predict` — sube una imagen (`multipart/form-data`, campo `file`) y devuelve predicciones:
  ```json
  {
    "model": "cnn",
    "predictions": [...],
    "top": [
      { "index": 3, "confidence": 0.92 },
      ...
    ]
  }
  ```
