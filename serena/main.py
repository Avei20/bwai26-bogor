import os
import uvicorn
from dotenv import load_dotenv
from google.adk.cli.fast_api import get_fast_api_app

load_dotenv()

# Create the FastAPI app pointing to the directory containing agent packages
app = get_fast_api_app(
    agents_dir=".",           # Current dir contains task_manager/ package
    web=True,                # Enable Dev UI
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
