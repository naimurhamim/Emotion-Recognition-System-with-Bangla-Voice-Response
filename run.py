"""
Backend server entry point.
Run: python run.py
API: http://127.0.0.1:8000
"""
import uvicorn
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        app_dir=os.path.join(os.path.dirname(__file__), "backend"),
    )
