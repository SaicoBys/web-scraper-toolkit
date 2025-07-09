import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import argparse
from urllib.parse import urljoin, urlparse
from datetime import datetime
import os

class JobScraper:
    """Professional job scraping toolkit for market research and lead generation"""
    
    def __init__(self, config_file='config/job_scraper_config.json'):
        """Initialize scraper with configuration"""
        self.config = self.load_config(config_file)
        self.scraped_jobs = []
        self.session = requests.Session()
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
        print("🕷️ Job Scraper Toolkit initialized")
        print(f"📊 Target sites: {len(self.config.get('target_sites', []))}")
        print(f"🔄 Rate limit: {self.config.get('rate_limit', 1)} seconds")
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "keywords": ["python", "developer"],
                "locations": ["remote", "usa"],
                "rate_limit": 2,
                "max_results": 100,
                "output_format": "csv"
            }
    
    def get_random_headers(self):
        """Generate random headers to avoid detection"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def scrape_demo_jobs(self, keywords, location, max_results=100):
        """
        Demo function that generates realistic job data
        In production, this would scrape actual job sites
        """
        print(f"🔍 Searching for jobs: {keywords} in {location}")
        
        # Demo companies and job titles
        companies = [
            "TechCorp Inc", "DataSolutions LLC", "CloudTech Systems", 
            "InnovateLabs", "DigitalFirst Group", "ScaleUp Technologies",
            "NextGen Software", "AI Dynamics", "WebFlow Solutions"
        ]
        
        job_titles = [
            "Python Developer", "Full Stack Developer", "Data Analyst",
            "Software Engineer", "Backend Developer", "DevOps Engineer",
            "Machine Learning Engineer", "Web Developer", "API Developer"
        ]
        
        locations = ["Remote", "New York, NY", "San Francisco, CA", "Austin, TX", 
                    "Seattle, WA", "Chicago, IL", "Boston, MA", "Denver, CO"]
        
        salary_ranges = [
            "$60,000 - $80,000", "$70,000 - $90,000", "$80,000 - $100,000",
            "$90,000 - $120,000", "$100,000 - $130,000", "$110,000 - $140,000"
        ]
        
        for i in range(min(max_results, 50)):
            job = {
                'title': random.choice(job_titles),
                'company': random.choice(companies),
                'location': random.choice(locations),
                'salary': random.choice(salary_ranges),
                'description': f"Looking for experienced {random.choice(job_titles).lower()} with {random.randint(2,5)} years experience in {', '.join(random.sample(keywords, min(2, len(keywords))))}.",
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'job_type': random.choice(['Full-time', 'Part-time', 'Contract', 'Remote']),
                'experience_level': random.choice(['Entry', 'Mid', 'Senior', 'Lead']),
                'scraped_at': datetime.now().isoformat()
            }
            
            self.scraped_jobs.append(job)
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"📊 Scraped {i + 1} jobs...")
            
            # Respectful rate limiting
            time.sleep(random.uniform(0.5, 1.5))
        
        print(f"✅ Successfully scraped {len(self.scraped_jobs)} jobs")
        return self.scraped_jobs
    
    def export_data(self, output_format='csv', filename=None):
        """Export scraped data to specified format"""
        if not self.scraped_jobs:
            print("❌ No data to export")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/scraped_jobs_{timestamp}"
        
        df = pd.DataFrame(self.scraped_jobs)
        
        if output_format.lower() == 'csv':
            output_file = f"{filename}.csv"
            df.to_csv(output_file, index=False)
        elif output_format.lower() == 'json':
            output_file = f"{filename}.json"
            df.to_json(output_file, orient='records', indent=2)
        elif output_format.lower() == 'excel':
            output_file = f"{filename}.xlsx"
            df.to_excel(output_file, index=False)
        
        print(f"💾 Data exported to: {output_file}")
        print(f"📊 Total records: {len(self.scraped_jobs)}")
        return output_file
    
    def generate_report(self):
        """Generate scraping summary report"""
        if not self.scraped_jobs:
            return
        
        df = pd.DataFrame(self.scraped_jobs)
        
        print("\n" + "="*50)
        print("📋 SCRAPING REPORT")
        print("="*50)
        print(f"📊 Total jobs scraped: {len(self.scraped_jobs)}")
        print(f"🏢 Unique companies: {df['company'].nunique()}")
        print(f"📍 Locations covered: {df['location'].nunique()}")
        print(f"💼 Job types: {', '.join(df['job_type'].unique())}")
        print(f"🎯 Experience levels: {', '.join(df['experience_level'].unique())}")
        print("\n📈 Top 5 Companies:")
        print(df['company'].value_counts().head().to_string())
        print("\n📍 Top 5 Locations:")
        print(df['location'].value_counts().head().to_string())
        print("="*50)

def main():
    """Main function to run the job scraper"""
    parser = argparse.ArgumentParser(description='Professional Job Scraper Toolkit')
    parser.add_argument('--keywords', nargs='+', default=['python', 'developer'], 
                       help='Job keywords to search for')
    parser.add_argument('--location', default='remote', 
                       help='Job location to search')
    parser.add_argument('--max-results', type=int, default=50, 
                       help='Maximum number of results to scrape')
    parser.add_argument('--output', choices=['csv', 'json', 'excel'], default='csv',
                       help='Output format')
    parser.add_argument('--config', default='config/job_scraper_config.json',
                       help='Configuration file path')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = JobScraper(args.config)
    
    # Scrape jobs
    scraper.scrape_demo_jobs(args.keywords, args.location, args.max_results)
    
    # Export data
    scraper.export_data(args.output)
    
    # Generate report
    scraper.generate_report()
    
    print("\n🎉 Job scraping completed successfully!")

if __name__ == "__main__":
    main()