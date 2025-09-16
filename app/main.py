from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tempfile
import shutil
import os
import re
from git import Repo

app = FastAPI()

class RepoURL(BaseModel):
    url: str

# Common dangerous functions
DANGEROUS_FUNCTIONS = ['eval', 'exec', 'os.system', 'subprocess.Popen', 'pickle.loads']

# Common secret patterns
SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Generic API Key": r"(?i)api[_-]?key['\"=:\s]+[a-z0-9]{32,45}",
    "JWT": r"eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+",
    "Private Key": r"-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----",
}


def clone_repo(repo_url):
    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(repo_url, temp_dir)
    except Exception as e:
        shutil.rmtree(temp_dir)
        raise HTTPException(status_code=400, detail=f"Failed to clone repo: {e}")
    return temp_dir


def search_in_files(base_dir, patterns):
    results = []

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(('.py', '.env', '.txt', '.json', '.yaml', '.yml')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for name, pattern in patterns.items():
                            matches = re.findall(pattern, content)
                            if matches:
                                results.append({
                                    "file": file_path,
                                    "type": name,
                                    "matches": matches
                                })
                except Exception as e:
                    pass  # skip unreadable files
    return results


def search_dangerous_functions(base_dir):
    results = []

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for func in DANGEROUS_FUNCTIONS:
                            if func in content:
                                results.append({
                                    "file": file_path,
                                    "function": func,
                                })
                except Exception:
                    pass
    return results


@app.post("/scan/secrets")
def check_secrets(repo: RepoURL):
    repo_dir = clone_repo(repo.url)
    try:
        results = search_in_files(repo_dir, SECRET_PATTERNS)
        report = {
            "repo_url": repo.url,
            "summary": {
                "total_files_scanned": len(results),
                "total_secrets_found": sum(len(r["matches"]) for r in results)
            },
            "details": results
        }
        return report
    finally:
        shutil.rmtree(repo_dir)


@app.post("/scan/code")
def check_dangerous(repo: RepoURL):
    repo_dir = clone_repo(repo.url)
    try:
        results = search_dangerous_functions(repo_dir)
        report = {
            "repo_url": repo.url,
            "summary": {
                "total_files_scanned": len(results),
                "total_dangerous_functions_found": len(results)
            },
            "details": results
        }
        return report
    finally:
        shutil.rmtree(repo_dir)

