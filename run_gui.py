"""
Single entry point — starts backend + GUI together.
Run: python run_gui.py
"""
import sys
import os
import threading
import time

# ── Start backend in background thread ───────────────────────────────────────
def start_backend():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,          # reload=False — thread safe
        log_level="warning",   # quiet logs
        app_dir=os.path.join(os.path.dirname(__file__), "backend"),
    )

backend_thread = threading.Thread(target=start_backend, daemon=True)
backend_thread.start()


time.sleep(2)

# ── Start GUI ─────────────────────────────────────────────────────────────────
from gui.app import main

if __name__ == "__main__":
    main()
