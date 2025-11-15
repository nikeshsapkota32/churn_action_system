# AI-Powered Customer Churn Action System

A telco customer churn prediction system with AI-powered action recommendations, built with FastAPI and Streamlit.

## Features

- **FastAPI Backend**: RESTful API for churn prediction
- **Streamlit Dashboard**: Interactive UI for customer analysis
- **ML Model**: Trained on telco customer data
- **Action Recommendations**: AI-powered suggestions based on churn risk

## Local Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd churn_action_system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the model (if not already done):
```bash
python train_model.py
```

4. Start the FastAPI backend:
```bash
uvicorn main_api:app --reload --host 0.0.0.0 --port 8000
```

5. In a separate terminal, start the Streamlit dashboard:
```bash
streamlit run dashboard.py
```

## Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

**Backend (FastAPI):**
1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main_api:app --host 0.0.0.0 --port $PORT`

**Frontend (Streamlit):**
1. Create another Web Service
2. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0`
3. Update `dashboard.py` to use your backend URL

### Option 2: Railway

1. Create new project on [Railway](https://railway.app)
2. Deploy from GitHub
3. Add start command: `uvicorn main_api:app --host 0.0.0.0 --port $PORT`

### Option 3: Streamlit Cloud (Dashboard Only)

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Deploy directly from GitHub
3. Host the FastAPI backend separately

## Environment Variables

For production deployment, update the API_URL in `dashboard.py`:
```python
API_URL = "https://your-backend-url.com/predict_churn"
```

## Files

- `main_api.py` - FastAPI backend
- `dashboard.py` - Streamlit frontend
- `train_model.py` - Model training script
- `churn_predictor_pipeline.joblib` - Trained model
- `feature_names.joblib` - Feature names
- `WA_Fn-UseC_-Telco-Customer-Churn.csv` - Training data
