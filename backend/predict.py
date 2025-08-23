import pandas as pd
import os
import joblib

# === Load encoders and models ===
city_encoder = joblib.load("encoders/city_encoder.pkl")
crime_encoder = joblib.load("encoders/crime_encoder.pkl")

rf_model = joblib.load("models/rf_model.pkl")
xgb_model = joblib.load("models/xgb_model.pkl")

# === Load future data ===
future_data_path = os.path.join("data", "future_years.csv")
future_df = pd.read_csv(future_data_path)

# === Encode City and Crime_Type (keep original column names) ===
future_df['City'] = city_encoder.transform(future_df['City'])
future_df['Crime_Type'] = crime_encoder.transform(future_df['Crime_Type'])

# === Predict ===
X_future = future_df[['City', 'Crime_Type', 'Year']]

rf_predictions = rf_model.predict(X_future)
xgb_predictions = xgb_model.predict(X_future)

# === Save predictions ===
future_df['RF_Predicted_Crime_Count'] = rf_predictions
future_df['XGB_Predicted_Crime_Count'] = xgb_predictions

output_path = os.path.join("data", "predictions.csv")
future_df.to_csv(output_path, index=False)

print("✅ Predictions saved to data/predictions.csv")

def make_predictions(df, rf_model, xgb_model, city_encoder, crime_encoder):
    df['City'] = city_encoder.transform(df['City'])
    df['Crime_Type'] = crime_encoder.transform(df['Crime_Type'])

    X_input = df[['City', 'Crime_Type', 'Year']]

    rf_pred = rf_model.predict(X_input)[0]
    xgb_pred = xgb_model.predict(X_input)[0]

    return {
        "RandomForest": float(rf_pred),
        "XGBoost": float(xgb_pred)
    }
