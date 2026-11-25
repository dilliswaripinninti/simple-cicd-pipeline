"""Simple CI/CD Pipeline using GitHub Actions - Flask application."""

import os
import time
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

APP_NAME = "simple-cicd-pipeline"
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
START_TIME = time.time()

app = Flask(__name__)


def deployment_info():
    """Describe where the app is running (Render sets these variables)."""
    on_render = os.environ.get("RENDER") == "true"
    commit = os.environ.get("RENDER_GIT_COMMIT", "")
    return {
        "environment": "Render" if on_render else "Local",
        "commit": commit[:7] if commit else "not available",
        "branch": os.environ.get("RENDER_GIT_BRANCH", "not available"),
    }


def status_payload():
    info = deployment_info()
    return {
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION,
        "environment": info["environment"],
        "commit": info["commit"],
        "branch": info["branch"],
        "uptime_seconds": int(time.time() - START_TIME),
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


@app.route("/")
def home():
    return render_template(
        "index.html",
        app_name=APP_NAME,
        version=APP_VERSION,
        info=deployment_info(),
    )


@app.route("/health")
def health():
    return jsonify(status="healthy"), 200


@app.route("/api/status")
def api_status():
    return jsonify(status_payload()), 200


@app.errorhandler(404)
def not_found(_error):
    if request.path.startswith("/api/"):
        return jsonify(error="Not found", path=request.path), 404
    return render_template("404.html", path=request.path), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
