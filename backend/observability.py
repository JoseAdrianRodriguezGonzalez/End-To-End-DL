from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import httpx
from prometheus_client.parser import text_string_to_metric_families
from config import TRITON_SERVER_URL, TRITON_MODEL_NAME,TRITON_METRICS_URL
def setup_observability(app):
    Instrumentator().instrument(app).expose(app,endpoint="/api/metrics")

async def get_triton_observability() -> dict:
    result = {
        "status": "unhealthy",
        "server": TRITON_SERVER_URL,
        "model": TRITON_MODEL_NAME,
    }

    try:
        async with httpx.AsyncClient() as client:
            health_response = await client.get(
                f"{TRITON_SERVER_URL}/v2/health/ready",
                timeout=5.0,
            )

            model_response = await client.get(
                f"{TRITON_SERVER_URL}/v2/models/"
                f"{TRITON_MODEL_NAME}/ready",
                timeout=5.0,
            )

        result.update({
            "status": (
                "healthy"
                if health_response.status_code == 200
                else "unhealthy"
            ),
            "triton_ready": health_response.status_code == 200,
            "model_ready": model_response.status_code == 200,
        })

    except httpx.RequestError as error:
        result["error"] = str(error)

    return result
async def get_triton_metrics() -> dict:
    """Retrieve and parse Triton's Prometheus metrics."""

    metrics = {
        "requests": {
            "successful": 0,
            "failed": 0,
        },
        "inference": {
            "count": 0,
            "executions": 0,
        },
        "latency_us": {
            "request": 0,
            "request_avg":0,
            "queue": 0,
            "compute_input": 0,
            "compute_infer": 0,
            "compute_output": 0,
        },
        "pending_requests": 0,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{TRITON_METRICS_URL}/metrics",
                timeout=5.0,
            )
            response.raise_for_status()

        for family in text_string_to_metric_families(response.text):
            for sample in family.samples:
                if sample.labels.get("model") != TRITON_MODEL_NAME:
                    continue

                name = sample.name
                value = sample.value

                if name == "nv_inference_request_success_total":
                    metrics["requests"]["successful"] = int(value)

                elif name == "nv_inference_request_failure_total":
                    metrics["requests"]["failed"] += int(value)

                elif name == "nv_inference_count_total":
                    metrics["inference"]["count"] = int(value)

                elif name == "nv_inference_exec_count_total":
                    metrics["inference"]["executions"] = int(value)

                elif name == "nv_inference_request_duration_us_total":
                    metrics["latency_us"]["request"] = value

                elif name == "nv_inference_queue_duration_us_total":
                    metrics["latency_us"]["queue"] = value

                elif name == "nv_inference_compute_input_duration_us_total":
                    metrics["latency_us"]["compute_input"] = value

                elif name == "nv_inference_compute_infer_duration_us_total":
                    metrics["latency_us"]["compute_infer"] = value

                elif name == "nv_inference_compute_output_duration_us_total":
                    metrics["latency_us"]["compute_output"] = value

                elif name == "nv_inference_pending_request_count":
                    metrics["pending_requests"] = int(value)
                successful_requests = metrics["requests"]["successful"]
                if successful_requests > 0:
                    for metric in (
                        "request",
                        "queue",
                        "compute_input",
                        "compute_infer",
                        "compute_output",
                    ):
                        metrics["latency_us"][f"{metric}_avg"] = (
                            metrics["latency_us"][metric]
                            / successful_requests
                        )
    except (httpx.RequestError, httpx.HTTPStatusError) as error:
        metrics["error"] = str(error)

    return metrics
