from fastapi import FastAPI
import pickle

app = FastAPI()

@app.get("/")
def root():
    return {'test':"Working"}

#@app.get("/predict")

# We haven't defined this yet but code will look something like this:

#def predict():

#   with open('models/mvp_model.pkl', 'rb') as file:
#       model = picklet.load(file)

#   prediction = model.predict()

#   return {"prediction": float(prediction[0])}
