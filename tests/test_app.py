import sys
import os

sys.path.insert(0, os.path.abspath("."))

from app.app import app

client = app.test_client()


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["application"] == "DevOps Platform Project"
    assert data["status"] == "running"