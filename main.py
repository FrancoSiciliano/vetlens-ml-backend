import io

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import numpy as np
from keras.models import load_model
import os

app = FastAPI()

model_path = os.path.abspath(os.path.join('model', 'dogsskindiseaseswithother_v1_xception.h5'))
model = load_model(model_path)
diseases = ['dermatitis_piotraumatica', 'dermatofitosis', 'miasis', 'otras']


@app.post("/infer/")
async def make_prediction(image: UploadFile = File(...)):
    if not image.file:
        raise HTTPException(status_code=400, detail="No image provided.")

    allowed_image_types = ["image/jpeg", "image/png", "image/jpg"]

    if image.content_type not in allowed_image_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, JPG and PNG are allowed.")

    image_data = await image.read()
    image = Image.open(io.BytesIO(image_data))
    image = image.resize((224, 224))
    image = np.array(image)
    image = image.astype('float32') / 255.0

    image = np.expand_dims(image, axis=0)

    predictions = model.predict(image)

    pred_dict = {}

    for idx, pred in enumerate(predictions[0]):
        pred_dict[diseases[idx]] = float(pred)

    return pred_dict


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, log_level='info')
