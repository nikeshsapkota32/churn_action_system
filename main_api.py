# main_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd
import numpy as np
from typing import List

# --- 1. Load Model and Feature Names ---
try:
    model_pipeline = load('churn_predictor_pipeline.joblib')
    feature_names = load('feature_names.joblib')
    print("Model and features loaded successfully.")
except FileNotFoundError:
    print("ERROR: Model or feature names file not found. Ensure train_model.py was run successfully!")
    exit()

# --- 2. Initialize FastAPI App ---
app = FastAPI(title="Customer Churn Prediction and Action System")

# --- 3. Define Input Schema (Pydantic Model) ---
class CustomerData(BaseModel):
    Gender: str = "Female"
    SeniorCitizen: int = 0
    Partner: str = "Yes"
    Dependents: str = "No"
    tenure: int = 2
    PhoneService: str = "No"
    MultipleLines: str = "No phone service"
    InternetService: str = "DSL"
    OnlineSecurity: str = "No"
    OnlineBackup: str = "Yes"
    DeviceProtection: str = "No"
    TechSupport: str = "No"
    StreamingTV: str = "No"
    StreamingMovies: str = "No"
    Contract: str = "Month-to-month"
    PaperlessBilling: str = "Yes"
    PaymentMethod: str = "Electronic check"
    MonthlyCharges: float = 29.85
    TotalCharges: float = 29.85


# --- 4. Define Prediction Endpoint ---

@app.post("/predict_churn")
async def predict_churn(data: CustomerData):
    data_dict = data.model_dump()

    # Create a DataFrame in the exact order the model expects
    input_df = pd.DataFrame([data_dict], columns=feature_names) 

    # CRITICAL FIX: Explicitly cast types to ensure the ColumnTransformer works
    input_df['SeniorCitizen'] = input_df['SeniorCitizen'].astype(int)
    input_df['tenure'] = input_df['tenure'].astype(int)
    input_df['MonthlyCharges'] = input_df['MonthlyCharges'].astype(float)
    input_df['TotalCharges'] = input_df['TotalCharges'].astype(float)
    
    # Get probability (returns [Prob_No_Churn, Prob_Churn])
    churn_prob_array = model_pipeline.predict_proba(input_df)[0]
    churn_probability = round(churn_prob_array[1] * 100, 2)

    # --- 5. AI-Powered Action Engine ---
    recommended_action = "Monitor usage. Customer is stable."
    is_high_risk = False

    if churn_probability >= 70:
        is_high_risk = True
        recommended_action = "**CRITICAL RISK:** Immediate proactive call from Sales/Retention Team. Focus on service usage and pricing dissatisfaction."
    elif churn_probability >= 50:
        is_high_risk = True
        if data.tenure < 12 and data.Contract == "Month-to-month":
             recommended_action = "**HIGH RISK:** Offer a 3-month discount to move to a 1-year contract to improve retention."
        else:
             recommended_action = "**HIGH RISK:** Send a targeted email campaign highlighting two key features the customer is not using."

    # --- 6. Return Results ---
    return {
        "churn_probability": f"{churn_probability}%",
        "is_high_risk": is_high_risk,
        "recommended_action": recommended_action,
        "model_output": "Prediction generated successfully."
    }