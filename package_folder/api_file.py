from fastapi import FastAPI
import pickle

app = FastAPI()

@app.get("/")
def root():
    return {'test':"Working"}

@app.get("/predict")
def predict(victim_age, latitude, longitude, day_ocurred, month_ocurred, year_ocurred):
   with open('notebooks/ml_model.pkl', 'rb') as file:
       model = pickle.load(file)

   prediction = model.predict([[float(victim_age), float(latitude), float(longitude), float(day_ocurred), float(month_ocurred), float(year_ocurred)]])
   return {"prediction": prediction[0]}
