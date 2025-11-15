import os
import subprocess
import time
from multiprocessing import Process

def run_fastapi():
    """Run FastAPI backend"""
    subprocess.run([
        "uvicorn", 
        "main_api:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

def run_streamlit():
    """Run Streamlit frontend"""
    port = os.getenv("PORT", "8501")
    subprocess.run([
        "streamlit", 
        "run", 
        "dashboard.py",
        "--server.port", port,
        "--server.address", "0.0.0.0"
    ])

if __name__ == "__main__":
    # Start FastAPI in a separate process
    fastapi_process = Process(target=run_fastapi)
    fastapi_process.start()
    
    # Give FastAPI time to start
    print("Starting FastAPI backend...")
    time.sleep(5)
    
    # Start Streamlit (this blocks)
    print("Starting Streamlit dashboard...")
    run_streamlit()
