import uvicorn
from .config import app  # Import the app instance
import backend.routes           # This "activates" the routes by running the decorators

if __name__ == "__main__":
    # This starts the Uvicorn server programmatically
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
