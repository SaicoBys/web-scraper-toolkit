# Deployment Guide - Professional Web Scraper Toolkit

## Overview

This guide provides comprehensive instructions for deploying the Professional Web Scraper Toolkit in various environments, from local development to enterprise production systems.

## Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- Git for version control
- Access to target websites (ensure compliance with terms of service)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/web-scraper-toolkit.git
cd web-scraper-toolkit
```

### 2. Create Virtual Environment

```bash
# Using venv (recommended)
python3 -m venv scraper_env
source scraper_env/bin/activate  # On Windows: scraper_env\Scripts\activate

# Or using conda
conda create -n scraper_env python=3.9
conda activate scraper_env
```

### 3. Install Dependencies

```bash
# Install basic requirements
pip install -r requirements.txt

# Install with additional features
pip install -e .[full]

# Install development dependencies
pip install -e .[dev]
```

### 4. Verify Installation

```bash
# Run the quick start demo
python examples/quick_start.py

# Test individual scrapers
python src/job_scraper.py --help
python src/lead_scraper.py --help
python src/price_monitor.py --help
```

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port (if using web interface)
EXPOSE 8000

# Default command
CMD ["python", "examples/quick_start.py"]
```

### 2. Build and Run Docker Container

```bash
# Build the image
docker build -t web-scraper-toolkit .

# Run the container
docker run -v $(pwd)/data:/app/data web-scraper-toolkit

# Run with custom configuration
docker run -v $(pwd)/data:/app/data -v $(pwd)/config:/app/config web-scraper-toolkit
```

### 3. Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  web-scraper:
    build: .
    volumes:
      - ./data:/app/data
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - PYTHONPATH=/app
      - LOG_LEVEL=INFO
    restart: unless-stopped
    
  scheduler:
    build: .
    command: ["python", "-m", "schedule_scrapers"]
    volumes:
      - ./data:/app/data
      - ./config:/app/config
    depends_on:
      - web-scraper
    restart: unless-stopped
```

## Cloud Deployment

### AWS Lambda Deployment

#### 1. Create Lambda Function

```bash
# Install AWS CLI and configure credentials
aws configure

# Create deployment package
pip install -r requirements.txt -t package/
cp -r src/ package/
cp -r config/ package/

# Create ZIP file
cd package && zip -r ../lambda_deployment.zip . && cd ..

# Create Lambda function
aws lambda create-function \
    --function-name web-scraper-toolkit \
    --runtime python3.9 \
    --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
    --handler src.lambda_handler \
    --zip-file fileb://lambda_deployment.zip \
    --timeout 300 \
    --memory-size 512
```

#### 2. Lambda Handler

```python
# src/lambda_handler.py
import json
import os
from job_scraper import JobScraper
from lead_scraper import LeadScraper
from price_monitor import PriceMonitor

def lambda_handler(event, context):
    """AWS Lambda handler for web scraping toolkit"""
    
    scraper_type = event.get('scraper_type', 'job')
    
    try:
        if scraper_type == 'job':
            scraper = JobScraper()
            keywords = event.get('keywords', ['python developer'])
            location = event.get('location', 'remote')
            max_results = event.get('max_results', 100)
            
            jobs = scraper.scrape_demo_jobs(keywords, location, max_results)
            output_file = scraper.export_data('json')
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Job scraping completed successfully',
                    'jobs_count': len(jobs),
                    'output_file': output_file
                })
            }
            
        elif scraper_type == 'lead':
            scraper = LeadScraper()
            industry = event.get('industry', 'technology')
            location = event.get('location', 'usa')
            max_results = event.get('max_results', 100)
            
            leads = scraper.scrape_demo_leads(industry, location, max_results)
            output_file = scraper.export_data('json')
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Lead generation completed successfully',
                    'leads_count': len(leads),
                    'output_file': output_file
                })
            }
            
        elif scraper_type == 'price':
            monitor = PriceMonitor()
            products = event.get('products', [])
            
            price_data = monitor.monitor_demo_prices(products)
            output_file = monitor.export_data('json')
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Price monitoring completed successfully',
                    'products_count': len(price_data),
                    'output_file': output_file
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
```

### Google Cloud Functions

#### 1. Deploy to Google Cloud Functions

```bash
# Install Google Cloud SDK
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy function
gcloud functions deploy web-scraper-toolkit \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point lambda_handler \
    --source . \
    --memory 512MB \
    --timeout 540s
```

### Azure Functions

#### 1. Deploy to Azure Functions

```bash
# Install Azure CLI
az login

# Create function app
az functionapp create \
    --name web-scraper-toolkit \
    --storage-account YOUR_STORAGE_ACCOUNT \
    --consumption-plan-location eastus \
    --resource-group YOUR_RESOURCE_GROUP \
    --runtime python \
    --functions-version 4

# Deploy function
func azure functionapp publish web-scraper-toolkit
```

## Production Deployment

### 1. Environment Configuration

```bash
# Create production environment file
cat > .env.production << EOF
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/scraper_db

# API Keys (if needed)
API_KEY=your_api_key_here

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=/var/log/web-scraper-toolkit.log

# Rate Limiting
RATE_LIMIT=2
MAX_CONCURRENT_REQUESTS=5

# Data Storage
DATA_DIR=/var/data/web-scraper-toolkit
BACKUP_DIR=/var/backups/web-scraper-toolkit
EOF
```

### 2. Systemd Service Setup

```ini
# /etc/systemd/system/web-scraper-toolkit.service
[Unit]
Description=Professional Web Scraper Toolkit
After=network.target

[Service]
Type=simple
User=scraper
Group=scraper
WorkingDirectory=/opt/web-scraper-toolkit
Environment=PATH=/opt/web-scraper-toolkit/scraper_env/bin
ExecStart=/opt/web-scraper-toolkit/scraper_env/bin/python src/scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Nginx Configuration

```nginx
# /etc/nginx/sites-available/web-scraper-toolkit
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/web-scraper-toolkit/static/;
    }
}
```

## Monitoring and Logging

### 1. Logging Configuration

```python
# src/logging_config.py
import logging
import logging.handlers
import os

def setup_logging():
    """Configure logging for production environment"""
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                'logs/web-scraper-toolkit.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)
```

### 2. Health Checks

```python
# src/health_check.py
import requests
import json
from datetime import datetime

def health_check():
    """Perform health check on scraping services"""
    
    health_status = {
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy',
        'services': {}
    }
    
    try:
        # Test job scraper
        from job_scraper import JobScraper
        scraper = JobScraper()
        health_status['services']['job_scraper'] = 'healthy'
        
    except Exception as e:
        health_status['services']['job_scraper'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    try:
        # Test lead scraper
        from lead_scraper import LeadScraper
        scraper = LeadScraper()
        health_status['services']['lead_scraper'] = 'healthy'
        
    except Exception as e:
        health_status['services']['lead_scraper'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    return health_status
```

### 3. Prometheus Metrics

```python
# src/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
SCRAPING_REQUESTS = Counter('scraping_requests_total', 'Total scraping requests', ['scraper_type'])
SCRAPING_DURATION = Histogram('scraping_duration_seconds', 'Scraping duration in seconds', ['scraper_type'])
SCRAPING_SUCCESS = Counter('scraping_success_total', 'Successful scraping operations', ['scraper_type'])
SCRAPING_ERRORS = Counter('scraping_errors_total', 'Failed scraping operations', ['scraper_type'])
ACTIVE_SCRAPERS = Gauge('active_scrapers', 'Number of active scrapers')

def track_scraping_metrics(scraper_type):
    """Decorator to track scraping metrics"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            SCRAPING_REQUESTS.labels(scraper_type=scraper_type).inc()
            ACTIVE_SCRAPERS.inc()
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                SCRAPING_SUCCESS.labels(scraper_type=scraper_type).inc()
                return result
            except Exception as e:
                SCRAPING_ERRORS.labels(scraper_type=scraper_type).inc()
                raise
            finally:
                duration = time.time() - start_time
                SCRAPING_DURATION.labels(scraper_type=scraper_type).observe(duration)
                ACTIVE_SCRAPERS.dec()
        
        return wrapper
    return decorator
```

## Security Considerations

### 1. API Key Management

```python
# src/security.py
import os
from cryptography.fernet import Fernet

class SecureConfig:
    """Secure configuration management"""
    
    def __init__(self):
        self.key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
        self.cipher = Fernet(self.key)
    
    def encrypt_value(self, value):
        """Encrypt sensitive configuration values"""
        return self.cipher.encrypt(value.encode()).decode()
    
    def decrypt_value(self, encrypted_value):
        """Decrypt sensitive configuration values"""
        return self.cipher.decrypt(encrypted_value.encode()).decode()
    
    def get_secure_config(self, key, default=None):
        """Get configuration value with encryption support"""
        value = os.getenv(key, default)
        if value and value.startswith('encrypted:'):
            return self.decrypt_value(value[10:])
        return value
```

### 2. Rate Limiting

```python
# src/rate_limiter.py
import time
import threading
from collections import defaultdict

class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def can_proceed(self, domain):
        """Check if request can proceed for given domain"""
        with self.lock:
            now = time.time()
            domain_requests = self.requests[domain]
            
            # Remove old requests
            domain_requests[:] = [req_time for req_time in domain_requests 
                                if now - req_time < self.time_window]
            
            if len(domain_requests) < self.max_requests:
                domain_requests.append(now)
                return True
            
            return False
    
    def wait_if_needed(self, domain):
        """Wait if rate limit is exceeded"""
        while not self.can_proceed(domain):
            time.sleep(1)
```

## Backup and Recovery

### 1. Automated Backups

```python
# src/backup.py
import shutil
import os
from datetime import datetime
import zipfile

def create_backup():
    """Create automated backup of data and configuration"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = f'backups/backup_{timestamp}'
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup data files
    if os.path.exists('data'):
        shutil.copytree('data', f'{backup_dir}/data')
    
    # Backup configuration
    if os.path.exists('config'):
        shutil.copytree('config', f'{backup_dir}/config')
    
    # Create ZIP archive
    zip_filename = f'{backup_dir}.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, backup_dir)
                zipf.write(file_path, arcname)
    
    # Clean up temporary directory
    shutil.rmtree(backup_dir)
    
    return zip_filename
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Rate Limiting**: Adjust rate limits in configuration files
3. **Memory Issues**: Increase memory allocation for large datasets
4. **Network Timeouts**: Configure appropriate timeout values

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python src/job_scraper.py --debug

# Run with verbose output
python -v src/job_scraper.py
```

## Support

For deployment support:
- [Documentation](https://github.com/yourusername/web-scraper-toolkit/docs)
- [Issues](https://github.com/yourusername/web-scraper-toolkit/issues)
- [Discussions](https://github.com/yourusername/web-scraper-toolkit/discussions) 