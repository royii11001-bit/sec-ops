import pytest
from fastapi.testclient import TestClient
from app.main import app
import sys
import argparse

# Create test client
client = TestClient(app)
# Set the GitHub URL to use in all tests, default if not provided
parser = argparse.ArgumentParser()
parser.add_argument("--github-url", type=str)
args, unknown = parser.parse_known_args()
GITHUB_URL = args.github_url

# Patch sys.argv for pytest so it doesn't get confused by argparse args
sys.argv = [sys.argv[0]] + unknown
class TestBasicEndpoints:
    """Test basic endpoints"""
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_scan_secrets(self):
        response = client.post("/scan/secrets", json={"url": "https://github.com/microsoft/vscode"})
        assert response.status_code == 200
        data = response.json()
        assert "repo_url" in data
        assert "summary" in data
        assert "details" in data

    def test_scan_code(self):
        response = client.post("/scan/code", json={"url": "https://github.com/facebook/react"})
        assert response.status_code == 200
        data = response.json()
        assert "repo_url" in data
        assert "summary" in data
        assert "details" in data
    
    def test_scan_code_risk_levels(self):
        """Test that risk levels are calculated correctly"""
        test_data = {
            "github_url": "https://github.com/torvalds/linux"
        }
        
        response = client.post("/scan/code", json=test_data)
        data = response.json()
        
        # Based on mock data, should be HIGH (7 vulnerabilities >= 5)
        assert data["risk_level"] == "HIGH"
        assert data["dangerous_functions_found"] >= 5
    
    def test_scan_code_invalid_url(self):
        """Test code scanning with invalid URL"""
        test_data = {
            "github_url": "https://stackoverflow.com"
        }
        
        response = client.post("/scan/code", json=test_data)
        
        assert response.status_code == 400
        assert "valid GitHub URL" in response.json()["detail"]
    
    def test_scan_code_malformed_github_url(self):
        """Test with malformed GitHub URL"""
        test_data = {
            "github_url": "https://github.com/"
        }
        
        response = client.post("/scan/code", json=test_data)
        
        assert response.status_code == 400
        assert "Invalid GitHub repository URL format" in response.json()["detail"]

class TestMultipleRepositories:
    """Test with various GitHub repositories"""
    
    @pytest.mark.parametrize("repo_url", [
        "https://github.com/microsoft/vscode",
        "https://github.com/facebook/react",
        "https://github.com/google/tensorflow",
        "https://github.com/torvalds/linux"
    ])
    def test_multiple_repos_secrets(self, repo_url):
        """Test secrets scanning with multiple repositories"""
        test_data = {"github_url": repo_url}
        
        response = client.post("/scan/secrets", json=test_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["repo_url"] == repo_url
        assert data["status"] == "completed"
    
    @pytest.mark.parametrize("repo_url", [
        "https://github.com/microsoft/vscode",
        "https://github.com/facebook/react",
        "https://github.com/google/tensorflow",
        "https://github.com/torvalds/linux"
    ])
    def test_multiple_repos_code(self, repo_url):
        """Test code scanning with multiple repositories"""
        test_data = {"github_url": repo_url}
        
        response = client.post("/scan/code", json=test_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["repo_url"] == repo_url
        assert data["status"] == "completed"
        assert data["files_scanned"] > 0

class TestErrorHandling:
    """Test error handling scenarios"""
    
    def test_invalid_http_method_secrets(self):
        """Test using GET instead of POST for secrets"""
        response = client.get("/scan/secrets")
        assert response.status_code == 405  # Method not allowed
    
    def test_invalid_http_method_code(self):
        """Test using GET instead of POST for code"""
        response = client.get("/scan/code")
        assert response.status_code == 405  # Method not allowed
    
    def test_empty_request_body(self):
        """Test with empty request body"""
        response = client.post("/scan/secrets")
        assert response.status_code == 422  # Unprocessable Entity

# Run tests with coverage
if __name__ == "__main__":

    pytest.main(["-v", "--tb=short"])
