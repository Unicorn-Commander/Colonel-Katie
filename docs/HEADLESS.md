# 🖥️ Headless Server Setup - Colonel Katie

Complete guide for running Colonel Katie on headless servers, containers, and cloud environments.

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Patterns](#usage-patterns)
- [API Server Mode](#api-server-mode)
- [Automation & Scripting](#automation--scripting)
- [Container Deployment](#container-deployment)
- [Security Considerations](#security-considerations)
- [Performance Optimization](#performance-optimization)
- [Monitoring & Logging](#monitoring--logging)

---

## Overview

Colonel Katie's headless mode is optimized for:
- 🖥️ **Linux servers** without GUI
- 🐳 **Docker/Kubernetes** containers  
- ☁️ **Cloud instances** (AWS, GCP, Azure)
- 🤖 **CI/CD pipelines**
- 📡 **API backends**
- 🔧 **Automated scripting**

### Benefits of Headless Mode
- Minimal resource usage (no GUI libraries)
- Faster startup times
- Better container compatibility
- Remote access via SSH
- Scriptable automation
- API server capabilities

---

## Quick Start

```bash
# 1. Clone and enter directory
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# 2. Run headless installer
chmod +x install-headless.sh
./install-headless.sh

# 3. Start using
source venv/bin/activate
interpreter
```

---

## Installation

### Automated Installation

The `install-headless.sh` script handles everything:

```bash
# Download and run installer
curl -fsSL https://raw.githubusercontent.com/Unicorn-Commander/Colonel-Katie/main/install-headless.sh | bash
```

What it does:
- ✅ Checks Python version (3.9-3.13)
- ✅ Creates isolated virtual environment
- ✅ Installs minimal dependencies
- ✅ Skips GUI/desktop packages
- ✅ Creates wrapper scripts
- ✅ Verifies installation

### Manual Installation

For custom setups:

```bash
# Dependencies
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Core package
pip install --no-deps open-interpreter

# Headless dependencies only
pip install -r requirements-headless.txt
```

### Minimal Dependencies

Create `requirements-headless.txt`:
```txt
anthropic>=0.37.1
astor>=0.8.1
git-python>=1.0.3
google-generativeai>=0.7.1
html2image>=2.0.4.3
html2text>=2024.2.26
inquirer>=3.1.3
ipykernel>=6.26.0
jupyter-client>=8.6.0
litellm>=1.41.26
matplotlib>=3.8.2
platformdirs>=4.2.0
psutil>=5.9.6
pydantic>=2.6.4
pyperclip>=1.9.0
pyyaml>=6.0.1
rich>=13.4.2
selenium>=4.24.0
send2trash>=1.8.2
setuptools
shortuuid>=1.0.13
six>=1.16.0
toml>=0.10.2
wget>=3.2
yaspin>=3.0.2
pyautogui>=0.9.54
typer>=0.12.5
fastapi>=0.111.0
uvicorn>=0.30.1
webdriver-manager>=4.0.2
nltk>=3.8.1
tokentrim>=0.1.13
```

---

## Configuration

### Environment Variables

```bash
# Create .env file
cat > .env << EOF
# API Keys
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here

# Model Settings
DEFAULT_MODEL=gpt-4
DEFAULT_TEMPERATURE=0.7
MAX_TOKENS=4096

# Server Settings
INTERPRETER_HOST=0.0.0.0
INTERPRETER_PORT=8080
INTERPRETER_WORKERS=4

# Features
AUTO_RUN=false
SAFE_MODE=ask
OFFLINE_MODE=false
EOF
```

### Configuration File

```yaml
# ~/.interpreter/config.yaml
model: gpt-4
temperature: 0.7
context_window: 8192
max_tokens: 4096
auto_run: false
safe_mode: ask

# Headless specific
headless:
  log_level: INFO
  log_file: /var/log/interpreter.log
  
server:
  host: 0.0.0.0
  port: 8080
  workers: 4
  cors_origins: ["*"]
  
# Local models (optional)
local_models:
  provider: ollama
  base_url: http://localhost:11434
```

### systemd Service

Create `/etc/systemd/system/colonel-katie.service`:
```ini
[Unit]
Description=Colonel Katie AI Assistant
After=network.target

[Service]
Type=simple
User=katie
WorkingDirectory=/opt/colonel-katie
Environment="PATH=/opt/colonel-katie/venv/bin:/usr/local/bin:/usr/bin"
ExecStart=/opt/colonel-katie/venv/bin/interpreter --server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable colonel-katie
sudo systemctl start colonel-katie
```

---

## Usage Patterns

### Interactive CLI

```bash
# Basic usage
interpreter

# With specific model
interpreter --model claude-3-opus

# With custom prompt
interpreter --custom_instructions "You are a DevOps expert"

# Fast mode (concise responses)
interpreter --fast
```

### Non-Interactive Execution

```bash
# Single command
interpreter "analyze the nginx logs for errors"

# From file
interpreter < script.txt

# Pipe input
echo "create a backup script" | interpreter

# With auto-run (careful!)
interpreter --auto_run "fix the Python syntax errors in app.py"
```

### Batch Processing

Create `batch_tasks.sh`:
```bash
#!/bin/bash
source /opt/colonel-katie/venv/bin/activate

# Process multiple files
for file in *.log; do
    interpreter "analyze $file for security issues" > "analysis_$file.txt"
done

# Generate reports
interpreter "summarize all analysis_*.txt files into a report"
```

---

## API Server Mode

### Starting the Server

```bash
# Basic server
interpreter --server

# With options
interpreter --server --port 8080 --host 0.0.0.0

# Production with uvicorn
uvicorn interpreter.api.server:app --host 0.0.0.0 --port 8080 --workers 4
```

### API Endpoints

#### POST /chat
```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a Python function to calculate fibonacci",
    "model": "gpt-4",
    "auto_run": false
  }'
```

#### POST /execute
```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello from API\")",
    "language": "python"
  }'
```

#### GET /models
```bash
curl http://localhost:8080/models
```

### Python Client Example

```python
import requests

class InterpreterClient:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
    
    def chat(self, message, model="gpt-4", auto_run=False):
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "message": message,
                "model": model,
                "auto_run": auto_run
            }
        )
        return response.json()
    
    def execute_code(self, code, language="python"):
        response = requests.post(
            f"{self.base_url}/execute",
            json={
                "code": code,
                "language": language
            }
        )
        return response.json()

# Usage
client = InterpreterClient()
result = client.chat("Create a function to check if a number is prime")
print(result)
```

---

## Automation & Scripting

### Cron Jobs

```bash
# Add to crontab
# Daily log analysis
0 2 * * * /opt/colonel-katie/scripts/analyze_logs.sh

# Weekly system report  
0 0 * * 0 /opt/colonel-katie/scripts/system_report.sh
```

### CI/CD Integration

#### GitHub Actions
```yaml
name: Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Colonel Katie
        run: |
          curl -fsSL https://raw.githubusercontent.com/Unicorn-Commander/Colonel-Katie/main/install-headless.sh | bash
          
      - name: Review Code
        run: |
          source venv/bin/activate
          interpreter "review the changes in this PR for security issues" > review.md
          
      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

### Monitoring Scripts

```python
#!/usr/bin/env python3
# monitor.py - System monitoring with Colonel Katie

import subprocess
import json
import time

def run_interpreter(prompt):
    """Run interpreter command and return output"""
    result = subprocess.run(
        ['interpreter', prompt],
        capture_output=True,
        text=True
    )
    return result.stdout

def monitor_system():
    """Monitor system and report issues"""
    checks = [
        "check disk usage and alert if any partition is over 80%",
        "analyze system logs for errors in the last hour",
        "check if any services are down",
        "review security logs for suspicious activity"
    ]
    
    alerts = []
    for check in checks:
        result = run_interpreter(check)
        if "alert" in result.lower() or "error" in result.lower():
            alerts.append({
                "check": check,
                "result": result,
                "timestamp": time.time()
            })
    
    return alerts

if __name__ == "__main__":
    alerts = monitor_system()
    if alerts:
        print(json.dumps(alerts, indent=2))
        # Send notifications, create tickets, etc.
```

---

## Container Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -s /bin/bash katie

# Set working directory
WORKDIR /app

# Copy files
COPY --chown=katie:katie . .

# Install as user
USER katie

# Install dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements-headless.txt

# Expose port
EXPOSE 8080

# Entry point
ENTRYPOINT ["/app/venv/bin/interpreter"]
CMD ["--server", "--host", "0.0.0.0", "--port", "8080"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  colonel-katie:
    build: .
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    
volumes:
  ollama_data:
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: colonel-katie
spec:
  replicas: 3
  selector:
    matchLabels:
      app: colonel-katie
  template:
    metadata:
      labels:
        app: colonel-katie
    spec:
      containers:
      - name: colonel-katie
        image: colonel-katie:latest
        ports:
        - containerPort: 8080
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
---
apiVersion: v1
kind: Service
metadata:
  name: colonel-katie-service
spec:
  selector:
    app: colonel-katie
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

---

## Security Considerations

### API Authentication

```python
# Add to server configuration
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Verify token logic
    if not is_valid_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token
```

### Network Security

```bash
# Firewall rules (ufw)
sudo ufw allow from 10.0.0.0/8 to any port 8080
sudo ufw deny 8080

# nginx reverse proxy with SSL
server {
    listen 443 ssl;
    server_name api.example.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Resource Limits

```bash
# Limit memory and CPU
systemd-run --uid=katie --gid=katie \
  --property=MemoryLimit=2G \
  --property=CPUQuota=50% \
  interpreter --server
```

---

## Performance Optimization

### Caching

```python
# Redis caching for responses
import redis
import hashlib
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_response(prompt, response, ttl=3600):
    key = hashlib.md5(prompt.encode()).hexdigest()
    redis_client.setex(key, ttl, json.dumps(response))

def get_cached_response(prompt):
    key = hashlib.md5(prompt.encode()).hexdigest()
    cached = redis_client.get(key)
    return json.loads(cached) if cached else None
```

### Load Balancing

```nginx
upstream colonel_katie {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    location / {
        proxy_pass http://colonel_katie;
    }
}
```

---

## Monitoring & Logging

### Logging Configuration

```python
# logging_config.py
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/colonel-katie/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, generate_latest

request_count = Counter('interpreter_requests_total', 'Total requests')
request_duration = Histogram('interpreter_request_duration_seconds', 'Request duration')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Health Checks

```bash
# Simple health check
curl http://localhost:8080/health

# Detailed status
curl http://localhost:8080/status
```

---

## Troubleshooting

### Common Issues

**Connection Refused**
```bash
# Check if service is running
systemctl status colonel-katie

# Check logs
journalctl -u colonel-katie -f

# Check port
netstat -tlnp | grep 8080
```

**Out of Memory**
```bash
# Increase memory limit
export INTERPRETER_MAX_MEMORY=4G

# Monitor memory usage
watch -n 1 'ps aux | grep interpreter'
```

**Slow Response**
```bash
# Enable profiling
interpreter --profile --verbose

# Check system resources
htop
iotop
```

---

## Best Practices

1. **Resource Management**
   - Set memory limits
   - Use connection pooling
   - Implement request timeouts

2. **Security**
   - Use API authentication
   - Run as non-root user
   - Keep dependencies updated

3. **Monitoring**
   - Set up logging
   - Monitor metrics
   - Configure alerts

4. **Scaling**
   - Use load balancing
   - Implement caching
   - Horizontal scaling with containers

---

**Need Help?** Check the [FAQ](./FAQ.md) or open an [issue](https://github.com/Unicorn-Commander/Colonel-Katie/issues)