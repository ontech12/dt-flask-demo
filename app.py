from flask import Flask
import time, random

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from AWS via Dynatrace!"

@app.route("/slow")
def slow():
    time.sleep(2)
    return "That was slow..."

@app.route("/error")
def fail():
    if random.random() < 0.9:
        raise RuntimeError("Simulated 500 error")
    return "Got lucky this time!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
