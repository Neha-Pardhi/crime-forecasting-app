from fastapi import FastAPI, HTTPException
import uvicorn
import joblib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Initialize app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models and encoders
rf_model = joblib.load("models/rf_model.pkl")
xgb_model = joblib.load("models/xgb_model.pkl")
city_encoder = joblib.load("encoders/city_encoder.pkl")
crime_encoder = joblib.load("encoders/crime_encoder.pkl")

# Input schema
class PredictionRequest(BaseModel):
    city: str
    crime_type: str
    year: int

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        city_encoded = city_encoder.transform([request.city])[0]
        crime_encoded = crime_encoder.transform([request.crime_type])[0]
        features = [[city_encoded, crime_encoded, request.year]]

        rf_pred = rf_model.predict(features)[0]
        xgb_pred = xgb_model.predict(features)[0]
        final_pred = (rf_pred + xgb_pred) / 2

        return {
            "city": request.city,
            "crime_type": request.crime_type,
            "year": request.year,
            "final_prediction": round(float(final_pred), 2)  # only one value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cities")
def get_cities():
    try:
        return {"cities": city_encoder.classes_.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/crime_types")
def get_crime_types():
    try:
        return {"crime_types": crime_encoder.classes_.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
