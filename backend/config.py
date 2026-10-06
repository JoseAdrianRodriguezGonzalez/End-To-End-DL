import os

TRITON_SERVER_URL = os.getenv("TRITON_SERVER_URL", "http://localhost:8000")
TRITON_MODEL_NAME = os.getenv("TRITON_MODEL_NAME", "cnn")
TRITON_METRICS_URL = "http://triton:8002"
TRITON_INPUT_NAME = os.getenv("TRITON_INPUT_NAME", "input")
TRITON_OUTPUT_NAME = os.getenv("TRITON_OUTPUT_NAME", "output")
INPUT_SIZE = int(os.getenv("INPUT_SIZE", "224"))

CLASS_NAMES = [
    "perro",
    "caballo",
    "elefante",
    "mariposa",
    "gallina",
    "gato",
    "vaca",
    "oveja",
    "araña",
    "ardilla",
]

#CLASS_NAMES=[ "cane", "cavallo", "elefante", "farfalla", "gallina", "gatto", "mucca", "pecora", "ragno", "scoiattolo", ]
