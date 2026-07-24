from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "application": "DevOps Platform Project",
        "status": "running",
        "version": "1.0.0",
        "hostname": socket.gethostname(),
        "environment": os.getenv("APP_ENV", "development")
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
