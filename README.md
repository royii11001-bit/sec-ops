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

### Unified SecOps Pipeline (secops-pipeline.yml)
**CI Phase:**
1. Static Application Security Testing (SAST) with Bandit, Semgrep, Safety
2. Container vulnerability scanning with Trivy
3. Security gates (blocks on critical vulnerabilities)
4. Docker build with security hardening
5. Push to DockerHub with dynamic tagging

**CD Phase (main branch only):**
1. Pull latest tagged image from DockerHub
2. Dynamic Application Security Testing (DAST) with OWASP ZAP
3. Secure container deployment with runtime hardening
4. Health verification and security compliance checks

**Reporting Phase:**
1. CI Security Assessment Report
2. CD Deployment Security Report  
3. Final Security Summary

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

- **Application**: Python FastAPI with GitPython for repository scanning
- **SAST Tools**: Bandit (Python security), Semgrep (multi-language), Safety (dependencies)
- **Container Security**: Trivy vulnerability scanner with intelligent security gates
- **DAST Tools**: OWASP ZAP with custom severity configuration
- **Platform**: Docker, GitHub Actions, DockerHub with dynamic tagging
- **Deployment**: Secure container with runtime hardening (non-root, read-only, minimal capabilities)

## Additional Documentation

- **[Security Implementation](SECURITY.md)** - Detailed security controls and best practices
- **[Threat Analysis](THREAT.md)** - Threat model and risk assessment

This implementation demonstrates how security can be seamlessly integrated into modern development workflows while maintaining development velocity and operational reliability.

