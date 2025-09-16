

from fastapi.testclient import TestClient
from app.main import app
import os
import argparse

client = TestClient(app)
parser = argparse.ArgumentParser()
parser.add_argument("--github-url", type=str, required=False, help="GitHub repository URL to test")
args, unknown = parser.parse_known_args()
GITHUB_URL = args.github_url or os.environ.get("GITHUB_URL")
if not GITHUB_URL:
    raise ValueError("You must provide a GitHub repository URL via --github-url or GITHUB_URL environment variable.")

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200

def test_scan_secrets():
    url = GITHUB_URL
    response = client.post("/scan/secrets", json={"url": url})
    assert response.status_code == 200
    data = response.json()
    assert "repo_url" in data
    assert "summary" in data
    assert "details" in data

def test_scan_code():
    url = GITHUB_URL
    response = client.post("/scan/code", json={"url": url})
    assert response.status_code == 200
    data = response.json()
    assert "repo_url" in data
    assert "summary" in data
    assert "details" in data

if __name__ == "__main__":
    def test_root_endpoint():
        response = client.get("/")
        assert response.status_code == 200

    def test_scan_secrets():
        response = client.post("/scan/secrets", json={"url": GITHUB_URL})
        assert response.status_code == 200
        data = response.json()
        assert "repo_url" in data
        assert "summary" in data
        assert "details" in data

    def test_scan_code():
        response = client.post("/scan/code", json={"url": GITHUB_URL})
        assert response.status_code == 200
        data = response.json()
        assert "repo_url" in data
        assert "summary" in data
        assert "details" in data

    if __name__ == "__main__":
        print("Running API endpoint tests...")
        test_root_endpoint()
        print("[PASS] Root endpoint test passed.")
        test_scan_secrets()
        print("[PASS] Secrets scan test passed.")
        test_scan_code()
        print("[PASS] Code scan test passed.")
