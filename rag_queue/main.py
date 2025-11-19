from .server import app
import uvicorn
import os


def main():
    print("main is running")
    uvicorn.run(app, port=8000, host="0.0.0.0")

main()