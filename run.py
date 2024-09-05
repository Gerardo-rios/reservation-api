import os
from watchgod import run_process
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from src import app

def run_app():
    uvicorn.run(app=app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))


if __name__ == "__main__":
    run_process("src", run_app)