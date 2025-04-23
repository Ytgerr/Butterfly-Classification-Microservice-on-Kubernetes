import base64
import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from image_classifier import classify_image

app = fastapi.FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/classify")
async def read_root(image: dict):
    image_bytes = base64.b64decode(image["image"])
    top_predicts = await run_in_threadpool(classify_image, image_bytes)
    return {"Predicts": top_predicts}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2005)
