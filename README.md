# SecOps CI/CD Pipeline

A security-first CI/CD implementation demonstrating end-to-end DevSecOps practices with the "Shift Left" approach.

## My Approach to This Project


My approach centered on building a security-first CI/CD pipeline that addresses real-world threats while maintaining developer productivity.

Research and Foundation:
I started by researching SecOps best practices to understand security concepts deeply. This gave me the knowledge foundation needed to make informed decisions about security controls and implementation strategies.

Threat Analysis and Planning:
Next, I broke down the development lifecycle to understand which parts needed securing and what potential threats existed at each stage. This analysis helped me identify key attack vectors like code injection, credential exposure, and supply chain vulnerabilities.

Development and Implementation:
With this understanding, I developed the application and then built the CI/CD pipeline around it. I created a comprehensive threat mapping to ensure every identified risk had corresponding security controls.

Tool Selection and Integration:
I strategically selected tools that provide comprehensive coverage without introducing unnecessary complexity or cost. My implementation follows SecOps best practices with defense-in-depth security gates: SAST scanning for code vulnerabilities, container security scanning with Trivy, and robust secrets management.
Each tool was chosen for its ability to integrate seamlessly with GitHub Actions while providing enterprise-grade security capabilities through open-source solutions.

Results:
This systematic approach demonstrates shift-left security principles, ensuring vulnerabilities are caught early in the development cycle when they're least expensive to fix, while maintaining fast build times and developer-friendly workflows. The pipeline provides multiple security layers without becoming a bottleneck for developers.

## Pipeline Overview

### CI Pipeline (ci.yml)
1. CodeQL security scan
2. Docker build with security hardening
3. Trivy vulnerability scan (blocks on critical issues)
4. Image signing with Cosign
5. Push to DockerHub

### CD Pipeline (cd.yml) 
1. Pull signed image from DockerHub
2. OWASP ZAP dynamic security testing
3. Secure container deployment
4. Health verification

## Quick Start

### Local Development
```bash
# Install dependencies
pip3 install -r requirements.txt

# Unit tests
python3 tests/test_main.py --url YOUR_GITHUB_URL

# Build and run locally  
docker build -t secops-scanner .
docker run -p 8000:8000 secops-scanner
```

### Testing the API
Once the container is running, you can test the API endpoints:

```bash
# Test basic endpoint
curl http://localhost:8000/

# Test secrets scanning
curl -X POST http://localhost:8000/scan/secrets \
  -H "Content-Type: application/json" \
  -d '{"github_url": "YOUR_GITHUB_URL"}'

# Test code scanning
curl -X POST http://localhost:8000/scan/code \
  -H "Content-Type: application/json" \
  -d '{"github_url": "YOUR_GITHUB_URL"}'
```

### GitHub Setup
Add these secrets to your repository:
```
DOCKERHUB_USERNAME: your-username
DOCKERHUB_TOKEN: your-access-token
```

Configure branch protection to require PR reviews and status checks.


## Technology Stack

- **Application**: Python FastAPI
- **Security**: CodeQL, Trivy, OWASP ZAP, Cosign
- **Platform**: Docker, GitHub Actions, DockerHub
- **Deployment**: Secure container with runtime hardening

## Additional Documentation

- **[Security Implementation](SECURITY.md)** - Detailed security controls and best practices
- **[Threat Analysis](THREAT.md)** - Threat model and risk assessment

This implementation demonstrates how security can be seamlessly integrated into modern development workflows while maintaining development velocity and operational reliability.