# dashboard.py
import streamlit as st
import requests
import json
import pandas as pd
import os

# --- Configuration ---
# When deployed together, FastAPI runs on port 8000, Streamlit on $PORT
API_URL = os.getenv("API_URL", "http://localhost:8000/predict_churn")
st.set_page_config(layout="wide", page_title="AI Customer Churn Action System")

# --- Default Customer Data for Demo ---
DEFAULT_CUSTOMER_DATA = {
    "Gender": "Male", "SeniorCitizen": 0, "Partner": "No", "Dependents": "No",
    "tenure": 1, "PhoneService": "Yes", "MultipleLines": "No", 
    "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
    "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No", 
    "StreamingMovies": "No", "Contract": "Month-to-month", 
    "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check", 
    "MonthlyCharges": 70.35, "TotalCharges": 70.35,
}

# --- Streamlit UI Setup ---
st.title("💡 AI-Powered Teleco Churn Action System")
st.markdown("Use this dashboard to assess a customer's churn risk and get an immediate, actionable recommendation from the AI engine.")

col1, col2, col3 = st.columns([1, 1, 1.5])

# --- Input Form (Column 1 & 2) ---
form_data = {}

with col1:
    st.header("👤 Customer Demographics")
    form_data["Gender"] = st.selectbox("Gender", ["Female", "Male"], index=["Female", "Male"].index(DEFAULT_CUSTOMER_DATA["Gender"]))
    form_data["SeniorCitizen"] = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x==1 else "No", index=DEFAULT_CUSTOMER_DATA["SeniorCitizen"])
    form_data["Partner"] = st.selectbox("Partner", ["Yes", "No"], index=["Yes", "No"].index(DEFAULT_CUSTOMER_DATA["Partner"]))
    form_data["Dependents"] = st.selectbox("Dependents", ["Yes", "No"], index=["Yes", "No"].index(DEFAULT_CUSTOMER_DATA["Dependents"]))
    form_data["tenure"] = st.slider("Tenure (Months)", 0, 72, DEFAULT_CUSTOMER_DATA["tenure"])

with col2:
    st.header("🛠️ Service Details")
    form_data["PhoneService"] = st.selectbox("Phone Service", ["Yes", "No"], index=["Yes", "No"].index(DEFAULT_CUSTOMER_DATA["PhoneService"]))
    form_data["MultipleLines"] = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"], index=["Yes", "No", "No phone service"].index(DEFAULT_CUSTOMER_DATA["MultipleLines"]))
    form_data["InternetService"] = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], index=["DSL", "Fiber optic", "No"].index(DEFAULT_CUSTOMER_DATA["InternetService"]))
    
    st.header("💰 Contract & Billing")
    form_data["Contract"] = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"], index=["Month-to-month", "One year", "Two year"].index(DEFAULT_CUSTOMER_DATA["Contract"]))
    form_data["PaperlessBilling"] = st.selectbox("Paperless Billing", ["Yes", "No"], index=["Yes", "No"].index(DEFAULT_CUSTOMER_DATA["PaperlessBilling"]))
    form_data["PaymentMethod"] = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], index=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"].index(DEFAULT_CUSTOMER_DATA["PaymentMethod"]))
    
    # Numerical Inputs (ensuring they always have a value)
    form_data["MonthlyCharges"] = st.number_input("Monthly Charges", value=DEFAULT_CUSTOMER_DATA["MonthlyCharges"], min_value=0.0, max_value=120.0, step=0.1)
    form_data["TotalCharges"] = st.number_input("Total Charges", value=DEFAULT_CUSTOMER_DATA["TotalCharges"], min_value=0.0, step=0.1)

col2_expander = st.expander("Security & Streaming Services (Click to view/edit)")
with col2_expander:
    form_data["OnlineSecurity"] = st.selectbox("Online Security", ["Yes", "No", "No internet service"], index=["Yes", "No", "No internet service"].index(DEFAULT_CUSTOMER_DATA["OnlineSecurity"]))
    form_data["OnlineBackup"] = st.selectbox("Online Backup", ["Yes", "No", "No internet service"], index=["Yes", "No", "No internet service"].index(DEFAULT_CUSTOMER_DATA["OnlineBackup"]))
    form_data["DeviceProtection"] = st.selectbox("Device Protection", ["Yes", "No", "No internet service"], index=["Yes", "No", "No internet service"].index(DEFAULT_CUSTOMER_DATA["DeviceProtection"]))
    form_data["TechSupport"] = st.selectbox("Tech Support", ["Yes", "No", "No internet service"], index=["Yes", "No", "No internet service"].index(DEFAULT_CUSTOMER_DATA["TechSupport"]))
    form_data["StreamingTV"] = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"], index=["Yes", "No", "No internet service"].index(DEFAULT_CUSTOMER_DATA["StreamingTV"]))
    form_data["StreamingMovies"] = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"], index=["Yes", "No", "No internet service"].index(DEFAULT_CUSTOMER_DATA["StreamingMovies"]))


# --- Prediction and Action Output (Column 3) ---
with col3:
    st.header("🎯 Prediction & AI Action")
    st.markdown("---")
    
    if st.button("Analyze Customer & Get Action Plan", use_container_width=True, type="primary"):
        with st.spinner('Analyzing risk and generating action plan...'):
            try:
                # 1. Send data to the running FastAPI endpoint
                response = requests.post(API_URL, json=form_data)
                response.raise_for_status() # Check for 4xx/5xx errors

                # 2. Check for successful response
                result = response.json()
                prob = result["churn_probability"]
                action = result["recommended_action"]
                is_risk = result["is_high_risk"]

                # 3. Display Results
                st.success("Analysis Complete!")
                st.metric(
                    label="Predicted Churn Probability", 
                    value=prob, 
                    delta=f"Risk: {'High' if is_risk else 'Low'}"
                )
                
                st.subheader("Action Recommendation")
                if is_risk:
                    st.error(action, icon="🚨")
                else:
                    st.info(action, icon="✅")

                st.markdown("---")
                st.caption("Raw Input Data Sent:")
                st.json(form_data)
                    
            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Could not connect to the FastAPI backend. Ensure 'python -m uvicorn main_api:app --reload' is running in a separate terminal.")
            except requests.exceptions.HTTPError as e:
                st.error(f"API HTTP Error (Code: {response.status_code}): An error occurred processing the request. Check the FastAPI terminal for a traceback.")
                st.json(response.json())
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")