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
    print(f"[INFO] Cloning repo: {repo_url} to {temp_dir}")
    try:
        Repo.clone_from(repo_url, temp_dir)
        print(f"[INFO] Clone successful.")
    except Exception as e:
        print(f"[ERROR] Clone failed: {e}")
        shutil.rmtree(temp_dir)
        raise HTTPException(status_code=400, detail=f"Failed to clone repo: {e}")
    return temp_dir


def search_in_files(base_dir, patterns):
    results = []
    scanned_files = 0
    print(f"[INFO] Scanning files in: {base_dir}")
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(('.py', '.env', '.txt', '.json', '.yaml', '.yml')):
                file_path = os.path.join(root, file)
                scanned_files += 1
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for name, pattern in patterns.items():
                            matches = re.findall(pattern, content)
                            if matches:
                                print(f"[FOUND] {name} in {file_path}")
                                results.append({
                                    "file": file_path,
                                    "type": name,
                                    "matches": matches
                                })
                except Exception as e:
                    print(f"[WARN] Could not read {file_path}: {e}")
    print(f"[INFO] Total files scanned: {scanned_files}")
    return results, scanned_files


def search_dangerous_functions(base_dir):
    results = []
    scanned_files = 0
    print(f"[INFO] Scanning for dangerous functions in: {base_dir}")
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                scanned_files += 1
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for func in DANGEROUS_FUNCTIONS:
                            if func in content:
                                print(f"[FOUND] {func} in {file_path}")
                                results.append({
                                    "file": file_path,
                                    "function": func,
                                })
                except Exception as e:
                    print(f"[WARN] Could not read {file_path}: {e}")
    print(f"[INFO] Total Python files scanned: {scanned_files}")
    return results, scanned_files

@app.get("/")
def read_root():
    return {"message": "GitHub Secrets Scanner API", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "secops-scanner"}


@app.post("/scan/secrets")
def check_secrets(repo: RepoURL):
    repo_dir = clone_repo(repo.url)
    try:
        results, scanned_files = search_in_files(repo_dir, SECRET_PATTERNS)
        report = {
            "repo_url": repo.url,
            "summary": {
                "total_files_scanned": scanned_files,
                "total_secrets_found": sum(len(r["matches"]) for r in results)
            },
            "details": results
        }
        print(f"[INFO] Secrets scan complete. Found {report['summary']['total_secrets_found']} secrets.")
        return report
    finally:
        shutil.rmtree(repo_dir)


@app.post("/scan/code")
def check_dangerous(repo: RepoURL):
    repo_dir = clone_repo(repo.url)
    try:
        results, scanned_files = search_dangerous_functions(repo_dir)
        report = {
            "repo_url": repo.url,
            "summary": {
                "total_files_scanned": scanned_files,
                "total_dangerous_functions_found": len(results)
            },
            "details": results
        }
        print(f"[INFO] Dangerous functions scan complete. Found {report['summary']['total_dangerous_functions_found']} issues.")
        return report
    finally:
        shutil.rmtree(repo_dir)

