import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json

interpreter = tf.lite.Interpreter(model_path="model/model_quantized.tflite")


interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

with open("model/class_names.json") as f:
    class_names = json.load(f)

def preprocess_image(image_bytes: bytes, target_size=(150, 150)) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(target_size)
    image_array = np.array(image).astype("float32") / 255.0  
    return np.expand_dims(image_array, axis=0) 

def classify_image(image: bytes) -> list[tuple[str, float]]:
    preprocessed = preprocess_image(image)

    interpreter.set_tensor(input_details[0]['index'], preprocessed)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]

    top_indices = predictions.argsort()[-3:][::-1]
    top_predictions = [(class_names[i], float(predictions[i])) for i in top_indices]
    print(top_predictions)
    return top_predictions

