from fastapi import FastAPI
import numpy as np
import pickle

app = FastAPI()

with open('models/lr_model_2.pkl', 'rb') as file:
    model = pickle.load(file)

victim_sex_mapping = {'Female': [1, 0, 0], 'Male': [0, 1, 0], 'Transgender': [0, 0, 1]}

@app.get("/")
def root():
    return {'test':"Working"}

@app.get("/predict")
def predict(area: int, victim_age: int, year_occurred: int,
            month_occurred: int, day_occurred: int, victim_sex: str):
    victim_sex_encoded = victim_sex_mapping.get(victim_sex, [0, 0, 0])
    input_features = np.array([
        area, victim_age, year_occurred,
        month_occurred, day_occurred, *victim_sex_encoded,
    ]).reshape(1, -1)

    prediction = model.predict(input_features)
    return {"prediction": int(prediction[0])}
