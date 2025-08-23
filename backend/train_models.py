import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

# === Load dataset ===
data_path = os.path.join("data", "full_data.csv")
df = pd.read_csv(data_path)

# === Encode categorical variables ===
city_encoder = LabelEncoder()
crime_encoder = LabelEncoder()

df['City'] = city_encoder.fit_transform(df['City'])
df['Crime_Type'] = crime_encoder.fit_transform(df['Crime_Type'])

# === Save encoders ===
os.makedirs("encoders", exist_ok=True)
joblib.dump(city_encoder, "encoders/city_encoder.pkl")
joblib.dump(crime_encoder, "encoders/crime_encoder.pkl")

# === Prepare features and target ===
X = df[['City', 'Crime_Type', 'Year']]
y = df['Crime_Count']

# === Train-Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Train Random Forest Model ===
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# === Train XGBoost Model ===
xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
xgb_model.fit(X_train, y_train)

# === Save models ===
os.makedirs("models", exist_ok=True)
joblib.dump(rf_model, "models/rf_model.pkl")
joblib.dump(xgb_model, "models/xgb_model.pkl")

print("✅ Models and encoders saved successfully.")
