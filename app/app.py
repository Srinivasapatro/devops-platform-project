from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest
import socket
import time

app = Flask(__name__)

# Prometheus Metrics
REQUEST_COUNT = Counter(
    "flask_http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP Request Latency",
    ["endpoint"]
)


@app.route("/")
def home():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()

    start = time.time()

    response = jsonify({
        "application": "DevOps Platform Project",
        "version": "3.0.0",
        "status": "running",
        "environment": "production",
        "release": "Application Metrics",
        "hostname": socket.gethostname()
    })

    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)

    return response


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )