import base64
import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from image_classifier import classify_image
from prometheus_client import Counter, Histogram, make_asgi_app
import time
from fastapi.responses import PlainTextResponse

app = fastapi.FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Prometheus metrics
REQUEST_COUNT = Counter(
    'butterfly_classifier_requests_total',
    'Total number of classification requests'
)

REQUEST_LATENCY = Histogram(
    'butterfly_classifier_request_latency_seconds',
    'Time spent processing classification requests'
)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics/", metrics_app)  # Note the trailing slash


@app.get("/")
async def health_check():
    return {"status": "healthy"}


@app.post("/classify")
async def read_root(image: dict):
    start_time = time.time()
    REQUEST_COUNT.inc()

    try:
        image_bytes = base64.b64decode(image["image"])
        top_predicts = await run_in_threadpool(classify_image, image_bytes)

        # Record request latency
        REQUEST_LATENCY.observe(time.time() - start_time)

        return {"Predicts": top_predicts}
    except Exception as e:
        # Record latency even for failed requests
        REQUEST_LATENCY.observe(time.time() - start_time)
        raise e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2005)
