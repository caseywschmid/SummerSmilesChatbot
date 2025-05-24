#!/usr/bin/env python3
"""
FastAPI Server Startup Script
"""

import uvicorn

if __name__ == "__main__":
    # Run FastAPI server with uvicorn
    # Host: 0.0.0.0 for external access, 127.0.0.1 for local only
    # Port: 8000 (standard FastAPI port)
    # Reload: True for development (auto-restart on file changes)
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
