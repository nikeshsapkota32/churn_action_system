#!/bin/bash

# Start FastAPI in the background
uvicorn main_api:app --host 0.0.0.0 --port 8000 &

# Wait a bit for FastAPI to start
sleep 5

# Start Streamlit on the PORT provided by the hosting service
streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0
