import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json
import threading

# --- Thread-safe TFLite Interpreter Setup ---
_thread_local = threading.local()


def get_interpreter():
    if not hasattr(_thread_local, "interpreter"):
        _thread_local.interpreter = tf.lite.Interpreter(
            model_path="model/model_quantized_new.tflite",
            num_threads=4  # Optimize for multi-core CPUs
        )
        _thread_local.interpreter.allocate_tensors()
    return _thread_local.interpreter


# --- Load Class Names (Thread-safe, read-only) ---
with open("model/class_names.json") as f:
    class_names = json.load(f)

# --- Image Preprocessing ---


def preprocess_image(image_bytes: bytes, target_size=(150, 150)) -> np.ndarray:
    """Converts image bytes to normalized input tensor"""
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize(target_size)
        image_array = np.array(image).astype("float32") / 255.0
        return np.expand_dims(image_array, axis=0)
    except Exception as e:
        raise ValueError(f"Image processing failed: {str(e)}")

# --- Classification Logic ---


def classify_image(image: bytes) -> list[tuple[str, float]]:
    """Thread-safe image classification with TFLite"""
    try:
        interpreter = get_interpreter()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        preprocessed = preprocess_image(image)

        # Thread-safe tensor operations
        interpreter.set_tensor(input_details[0]['index'], preprocessed)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index']).copy()[
            0]  # Critical: .copy()

        # Get top 3 predictions
        top_indices = predictions.argsort()[-3:][::-1]
        return [(class_names[i], float(predictions[i])) for i in top_indices]
    except Exception as e:
        raise RuntimeError(f"Classification failed: {str(e)}")
