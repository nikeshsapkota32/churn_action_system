# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from joblib import dump
import numpy as np

# --- 1. Load Data ---
try:
    df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
except FileNotFoundError:
    print("ERROR: WA_Fn-UseC_-Telco-Customer-Churn.csv not found. Please download it from Kaggle and place it in the project folder.")
    exit()

# --- 2. Clean and Prepare Data ---
# Convert 'TotalCharges' to numeric, replacing errors with NaN
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
# Imputation: Fill missing TotalCharges with MonthlyCharges
df['TotalCharges'].fillna(df['MonthlyCharges'], inplace=True) 

# Drop CustomerID and convert Churn target to 0/1
df.drop('customerID', axis=1, inplace=True)
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

X = df.drop('Churn', axis=1)
y = df['Churn']

# --- 3. Define Preprocessing Steps ---
categorical_features = X.select_dtypes(include=['object']).columns
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns

# Create the preprocessing transformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough' 
)

# --- 4. Create Full Pipeline ---
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', model)
])

# --- 5. Train Model ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
full_pipeline.fit(X_train, y_train)

print(f"Model accuracy on test set: {full_pipeline.score(X_test, y_test):.4f}")

# --- 6. Save Model and Feature Names ---
dump(full_pipeline, 'churn_predictor_pipeline.joblib')
dump(X_train.columns.tolist(), 'feature_names.joblib')

print("\nModel pipeline and feature names saved successfully.")