import uvicorn
import os

if __name__ == "__main__":
    dev_mode = os.getenv("DEV_MODE", "0") == "1"
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=dev_mode,
        reload_dirs=["app"] if dev_mode else [],
    )