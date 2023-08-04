import io

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import numpy as np
from keras.models import load_model
import tensorflow as tf
import os

app = FastAPI()

model_path = os.path.abspath(os.path.join('model', 'vetlens_enb2_v1_5c.h5'))
model = load_model(model_path, compile=False)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5), loss=tf.losses.CategoricalCrossentropy(),
              metrics=['accuracy'])
diseases = ['dermatitis_piotraumatica', 'dermatofitosis', 'miasis', 'otras', 'sin_problemas']


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
    # image = tf.keras.applications.xception.preprocess_input(image)

    image = np.expand_dims(image, axis=0)

    predictions = model.predict(image)

    pred_dict = {}
    max_pred = 0.0

    for idx, pred in enumerate(predictions[0]):
        pred_dict[diseases[idx]] = float(pred)

    final_inference = {'dermatitis_piotraumatica': pred_dict[diseases[0]], 'dermatofitosis': pred_dict[diseases[1]],
            'miasis': pred_dict[diseases[2]], 'no_discernible': pred_dict[diseases[3]] + pred_dict[diseases[4]]}

    winner_class = ""
    for key in final_inference.keys():
        if final_inference[key] > max_pred:
            winner_class = key
            max_pred = final_inference[key]

    if max_pred < 0.60 and winner_class != 'no_discernible' or final_inference['no_discernible'] > 0.30:
        final_inference.update({"result": 'no_discernible'})
    else:
        final_inference.update({"result": winner_class})
    return final_inference


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, log_level='info')
