# API Reference - Professional Web Scraper Toolkit

## Overview

This document provides comprehensive API reference for the Professional Web Scraper Toolkit, an enterprise-grade solution for data extraction and business intelligence.

## Core Modules

### JobScraper Class

**Purpose**: Extract comprehensive job market data for competitive analysis and recruitment insights.

#### Constructor
```python
JobScraper(config_file='config/job_scraper_config.json')
```

**Parameters**:
- `config_file` (str): Path to configuration JSON file

#### Methods

##### `scrape_demo_jobs(keywords, location, max_results=100)`
Extract job listings based on specified criteria.

**Parameters**:
- `keywords` (list): List of job keywords to search for
- `location` (str): Job location filter
- `max_results` (int): Maximum number of results to extract

**Returns**: List of job dictionaries

**Example**:
```python
scraper = JobScraper()
jobs = scraper.scrape_demo_jobs(
    keywords=['python developer', 'data scientist'],
    location='remote',
    max_results=200
)
```

##### `export_data(output_format='csv', filename=None)`
Export scraped data to specified format.

**Parameters**:
- `output_format` (str): Output format ('csv', 'json', 'excel')
- `filename` (str): Custom filename (optional)

**Returns**: Path to exported file

##### `generate_report()`
Generate comprehensive scraping summary report.

### LeadScraper Class

**Purpose**: Build high-quality prospect databases for sales and marketing campaigns.

#### Constructor
```python
LeadScraper(config_file='config/lead_scraper_config.json')
```

#### Methods

##### `scrape_demo_leads(industry, location, max_results=100)`
Extract qualified leads based on industry and location criteria.

**Parameters**:
- `industry` (str): Target industry
- `location` (str): Geographic location
- `max_results` (int): Maximum number of leads to extract

**Returns**: List of lead dictionaries

##### `export_data(output_format='csv', filename=None)`
Export lead data to specified format.

##### `generate_lead_report()`
Generate lead quality and scoring report.

### PriceMonitor Class

**Purpose**: Track competitor pricing strategies and market dynamics in real-time.

#### Constructor
```python
PriceMonitor(config_file='config/price_monitor_config.json')
```

#### Methods

##### `monitor_demo_prices(products)`
Monitor prices for specified products across multiple sites.

**Parameters**:
- `products` (list): List of product dictionaries with monitoring criteria

**Returns**: List of price data dictionaries

##### `export_data(output_format='csv', filename=None)`
Export price monitoring data to specified format.

##### `generate_price_report()`
Generate price analysis and trend report.

## Configuration

### Job Scraper Configuration

```json
{
  "scraper_name": "Job Market Intelligence Engine",
  "version": "2.0.0",
  "target_sites": [
    {
      "name": "LinkedIn Jobs",
      "base_url": "https://www.linkedin.com/jobs",
      "enabled": true,
      "priority": 1
    }
  ],
  "search_parameters": {
    "default_keywords": ["python developer", "data scientist"],
    "default_locations": ["remote", "san francisco"]
  },
  "extraction_settings": {
    "max_results": 1000,
    "rate_limit": 2,
    "include_salary": true
  }
}
```

### Lead Scraper Configuration

```json
{
  "scraper_name": "Lead Generation Engine",
  "version": "2.0.0",
  "target_industries": [
    {
      "name": "Technology",
      "keywords": ["software", "saas", "tech"],
      "enabled": true
    }
  ],
  "verification_settings": {
    "verify_emails": true,
    "verify_phones": true
  },
  "lead_scoring": {
    "enabled": true,
    "criteria": {
      "company_size_weight": 0.2,
      "industry_relevance": 0.25
    }
  }
}
```

### Price Monitor Configuration

```json
{
  "scraper_name": "Price Monitoring System",
  "version": "2.0.0",
  "target_ecommerce_sites": [
    {
      "name": "Amazon",
      "base_url": "https://www.amazon.com",
      "enabled": true,
      "rate_limit": 5
    }
  ],
  "monitoring_settings": {
    "check_interval_minutes": 60,
    "max_products_per_site": 500
  },
  "alert_system": {
    "enabled": true,
    "price_drop_alerts": true,
    "alert_threshold_percent": 5.0
  }
}
```

## Data Structures

### Job Data Structure
```python
{
    'title': 'Python Developer',
    'company': 'TechCorp Inc',
    'location': 'San Francisco, CA',
    'salary': '$80,000 - $100,000',
    'description': 'Job description text...',
    'posted_date': '2024-01-15',
    'job_type': 'Full-time',
    'experience_level': 'Mid',
    'scraped_at': '2024-01-15T10:30:00'
}
```

### Lead Data Structure
```python
{
    'company_name': 'TechStartup Inc',
    'contact_name': 'John Doe',
    'title': 'CTO',
    'email': 'john.doe@techstartup.com',
    'phone': '+1-555-0123',
    'industry': 'Technology',
    'location': 'New York, NY',
    'company_size': '50-200',
    'website': 'https://techstartup.com',
    'linkedin_profile': 'https://linkedin.com/in/johndoe',
    'lead_score': 85,
    'contact_verified': True,
    'email_valid': True,
    'scraped_at': '2024-01-15T10:30:00'
}
```

### Price Data Structure
```python
{
    'product_name': 'MacBook Pro 13"',
    'category': 'Electronics',
    'site': 'Amazon',
    'current_price': 1199.99,
    'original_price': 1299.99,
    'discount_percentage': 7.7,
    'availability': 'In Stock',
    'stock_status': 'Available',
    'price_change': -100.0,
    'price_change_percent': -7.7,
    'last_updated': '2024-01-15T10:30:00',
    'scraped_at': '2024-01-15T10:30:00'
}
```

## Error Handling

### Common Exceptions

#### `ScrapingError`
Raised when scraping operations fail.

```python
try:
    jobs = scraper.scrape_demo_jobs(keywords, location)
except ScrapingError as e:
    print(f"Scraping failed: {e}")
```

#### `ConfigurationError`
Raised when configuration files are invalid.

```python
try:
    scraper = JobScraper('invalid_config.json')
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

#### `ExportError`
Raised when data export fails.

```python
try:
    output_file = scraper.export_data('excel')
except ExportError as e:
    print(f"Export failed: {e}")
```

## Performance Optimization

### Rate Limiting
All scrapers implement built-in rate limiting to respect website policies:

```python
# Configure rate limiting in config files
{
  "extraction_settings": {
    "rate_limit": 2,  # seconds between requests
    "retry_attempts": 3
  }
}
```

### Caching
Enable caching to improve performance:

```python
{
  "performance_optimization": {
    "caching_enabled": true,
    "cache_duration_hours": 24
  }
}
```

### Parallel Processing
Configure concurrent requests:

```python
{
  "monitoring_settings": {
    "concurrent_requests": 5
  }
}
```

## Logging

### Log Levels
- `DEBUG`: Detailed debugging information
- `INFO`: General information about scraping progress
- `WARNING`: Warning messages for non-critical issues
- `ERROR`: Error messages for failed operations

### Log Configuration
```python
{
  "monitoring": {
    "log_level": "INFO",
    "track_performance": true,
    "alert_on_errors": true
  }
}
```

## Best Practices

### Ethical Scraping
- Always respect robots.txt files
- Implement appropriate rate limiting
- Use rotating user agents
- Monitor for blocking and adjust accordingly

### Data Quality
- Validate extracted data
- Implement duplicate detection
- Clean and normalize data
- Verify contact information

### Performance
- Use appropriate timeouts
- Implement retry mechanisms
- Monitor memory usage
- Optimize for large datasets

### Security
- Never store sensitive credentials in code
- Use environment variables for API keys
- Implement proper error handling
- Log security-relevant events

## Examples

### Complete Job Market Analysis
```python
from job_scraper import JobScraper
import pandas as pd

# Initialize scraper
scraper = JobScraper('config/job_scraper_config.json')

# Extract job data
keywords = ['python developer', 'data scientist', 'machine learning']
jobs = scraper.scrape_demo_jobs(keywords, 'remote', 500)

# Analyze data
df = pd.DataFrame(jobs)
print(f"Total jobs: {len(df)}")
print(f"Average salary range: {df['salary'].mode()[0]}")
print(f"Top companies: {df['company'].value_counts().head()}")

# Export results
output_file = scraper.export_data('excel')
scraper.generate_report()
```

### Lead Generation Pipeline
```python
from lead_scraper import LeadScraper

# Initialize lead scraper
scraper = LeadScraper('config/lead_scraper_config.json')

# Generate leads
leads = scraper.scrape_demo_leads('technology', 'usa', 1000)

# Filter high-quality leads
high_quality_leads = [lead for lead in leads if lead['lead_score'] >= 80]

# Export to CRM
output_file = scraper.export_data('excel')
scraper.generate_lead_report()
```

### Price Monitoring System
```python
from price_monitor import PriceMonitor

# Initialize price monitor
monitor = PriceMonitor('config/price_monitor_config.json')

# Define products to monitor
products = [
    {
        "name": "MacBook Pro 13\"",
        "category": "Electronics",
        "target_price": 1200,
        "urls": ["https://www.amazon.com/dp/example"]
    }
]

# Monitor prices
price_data = monitor.monitor_demo_prices(products)

# Check for price drops
price_drops = [item for item in price_data if item['price_change_percent'] < -5]

# Export results
output_file = monitor.export_data('excel')
monitor.generate_price_report()
```

## Support

For additional support and documentation:
- [Configuration Guide](configuration.md)
- [Deployment Guide](deployment.md)
- [Troubleshooting](troubleshooting.md)
- [GitHub Issues](https://github.com/yourusername/web-scraper-toolkit/issues) 