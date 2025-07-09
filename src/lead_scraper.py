import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
import argparse
from datetime import datetime
import os
import re

class LeadScraper:
    """Professional lead generation toolkit for B2B sales and marketing"""
    
    def __init__(self, config_file='config/lead_scraper_config.json'):
        """Initialize lead scraper with configuration"""
        self.config = self.load_config(config_file)
        self.leads = []
        self.session = requests.Session()
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
        print("🎯 Lead Scraper Toolkit initialized")
        print(f"🏢 Target industries: {len(self.config.get('industries', []))}")
        print(f"📍 Target locations: {len(self.config.get('locations', []))}")
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "industries": ["technology", "healthcare", "finance"],
                "locations": ["usa", "canada", "uk"],
                "company_size": ["startup", "small", "medium", "large"],
                "rate_limit": 2,
                "max_results": 100
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
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def generate_demo_leads(self, industry, location, max_results=100):
        """
        Generate demo lead data for portfolio demonstration
        In production, this would scrape actual business directories
        """
        print(f"🔍 Generating leads for {industry} industry in {location}")
        
        # Demo companies by industry
        companies_by_industry = {
            "technology": [
                "TechFlow Solutions", "DataDrive Inc", "CloudSync Systems", 
                "InnovateTech Labs", "DigitalForward Group", "NextGen Software",
                "AI Dynamics Corp", "WebScale Technologies", "CodeCraft Solutions"
            ],
            "healthcare": [
                "MedTech Solutions", "HealthCare Innovations", "BioData Systems",
                "MedFlow Technologies", "HealthSync Solutions", "CareConnect Inc",
                "MedAnalytics Corp", "HealthTech Partners", "BioInnovate Labs"
            ],
            "finance": [
                "FinTech Solutions", "Capital Analytics", "InvestTech Systems",
                "MoneyFlow Technologies", "FinanceSync Solutions", "WealthTech Inc",
                "TradingEdge Corp", "FinanceForward Group", "CryptoTech Labs"
            ]
        }
        
        # Demo contact titles
        titles = [
            "CEO", "CTO", "VP of Sales", "Marketing Director", "Head of Growth",
            "VP of Engineering", "Sales Manager", "Business Development Manager",
            "Chief Marketing Officer", "Head of Operations", "VP of Product"
        ]
        
        # Demo locations
        locations_data = {
            "usa": ["New York, NY", "San Francisco, CA", "Austin, TX", "Seattle, WA"],
            "canada": ["Toronto, ON", "Vancouver, BC", "Montreal, QC", "Calgary, AB"],
            "uk": ["London", "Manchester", "Birmingham", "Edinburgh"]
        }
        
        company_sizes = {
            "startup": "1-10 employees",
            "small": "11-50 employees", 
            "medium": "51-200 employees",
            "large": "200+ employees"
        }
        
        companies = companies_by_industry.get(industry, companies_by_industry["technology"])
        location_list = locations_data.get(location, locations_data["usa"])
        
        for i in range(min(max_results, 100)):
            company = random.choice(companies)
            first_name = random.choice(["John", "Sarah", "Michael", "Emily", "David", "Jessica", "Robert", "Amanda"])
            last_name = random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"])
            
            # Generate realistic business email
            domain = company.lower().replace(" ", "").replace("inc", "").replace("corp", "").replace("ltd", "")
            email = f"{first_name.lower()}.{last_name.lower()}@{domain}.com"
            
            # Generate phone number
            phone = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
            
            lead = {
                'company_name': company,
                'contact_name': f"{first_name} {last_name}",
                'title': random.choice(titles),
                'email': email,
                'phone': phone,
                'industry': industry,
                'location': random.choice(location_list),
                'company_size': random.choice(list(company_sizes.keys())),
                'employees': company_sizes[random.choice(list(company_sizes.keys()))],
                'website': f"https://www.{domain}.com",
                'linkedin_company': f"https://linkedin.com/company/{domain}",
                'linkedin_profile': f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}",
                'lead_score': random.randint(1, 100),
                'contact_verified': random.choice([True, False]),
                'email_valid': self.validate_email(email),
                'scraped_at': datetime.now().isoformat()
            }
            
            self.leads.append(lead)
            
            # Progress indicator
            if (i + 1) % 20 == 0:
                print(f"📊 Generated {i + 1} leads...")
            
            # Respectful rate limiting
            time.sleep(random.uniform(0.1, 0.5))
        
        print(f"✅ Successfully generated {len(self.leads)} leads")
        return self.leads
    
    def qualify_leads(self, min_score=70):
        """Filter leads based on qualification criteria"""
        qualified = [lead for lead in self.leads if lead['lead_score'] >= min_score]
        print(f"🎯 Qualified leads (score >= {min_score}): {len(qualified)}")
        return qualified
    
    def export_data(self, output_format='csv', filename=None, qualified_only=False):
        """Export lead data to specified format"""
        data_to_export = self.qualify_leads(70) if qualified_only else self.leads
        
        if not data_to_export:
            print("❌ No lead data to export")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            suffix = "_qualified" if qualified_only else ""
            filename = f"data/leads_{timestamp}{suffix}"
        
        df = pd.DataFrame(data_to_export)
        
        if output_format.lower() == 'csv':
            output_file = f"{filename}.csv"
            df.to_csv(output_file, index=False)
        elif output_format.lower() == 'json':
            output_file = f"{filename}.json"
            df.to_json(output_file, orient='records', indent=2)
        elif output_format.lower() == 'excel':
            output_file = f"{filename}.xlsx"
            df.to_excel(output_file, index=False)
        
        print(f"💾 Lead data exported to: {output_file}")
        print(f"📊 Total records: {len(data_to_export)}")
        return output_file
    
    def generate_report(self):
        """Generate lead generation summary report"""
        if not self.leads:
            return
        
        df = pd.DataFrame(self.leads)
        qualified = self.qualify_leads(70)
        
        print("\n" + "="*50)
        print("🎯 LEAD GENERATION REPORT")
        print("="*50)
        print(f"📊 Total leads generated: {len(self.leads)}")
        print(f"✅ Qualified leads (score >= 70): {len(qualified)}")
        print(f"📧 Valid emails: {df['email_valid'].sum()}")
        print(f"🔍 Verified contacts: {df['contact_verified'].sum()}")
        print(f"🏢 Unique companies: {df['company_name'].nunique()}")
        print(f"📍 Locations covered: {df['location'].nunique()}")
        
        print("\n📊 Leads by Industry:")
        industry_counts = df['industry'].value_counts()
        print(industry_counts.to_string())
        
        print("\n🏢 Leads by Company Size:")
        size_counts = df['company_size'].value_counts()
        print(size_counts.to_string())
        
        print("\n🎯 Top 5 Companies by Lead Score:")
        top_companies = df.nlargest(5, 'lead_score')[['company_name', 'contact_name', 'lead_score']]
        print(top_companies.to_string(index=False))
        
        print("\n📈 Lead Quality Distribution:")
        score_ranges = pd.cut(df['lead_score'], bins=[0, 30, 60, 80, 100], 
                             labels=['Low (0-30)', 'Medium (31-60)', 'High (61-80)', 'Premium (81-100)'])
        print(score_ranges.value_counts().to_string())
        
        print("="*50)

def main():
    """Main function to run the lead scraper"""
    parser = argparse.ArgumentParser(description='Professional Lead Scraper Toolkit')
    parser.add_argument('--industry', default='technology',
                       help='Target industry for lead generation')
    parser.add_argument('--location', default='usa',
                       help='Target location for leads')
    parser.add_argument('--max-results', type=int, default=100,
                       help='Maximum number of leads to generate')
    parser.add_argument('--output', choices=['csv', 'json', 'excel'], default='csv',
                       help='Output format')
    parser.add_argument('--qualified-only', action='store_true',
                       help='Export only qualified leads')
    parser.add_argument('--config', default='config/lead_scraper_config.json',
                       help='Configuration file path')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = LeadScraper(args.config)
    
    # Generate leads
    scraper.generate_demo_leads(args.industry, args.location, args.max_results)
    
    # Export data
    scraper.export_data(args.output, qualified_only=args.qualified_only)
    
    # Generate report
    scraper.generate_report()
    
    print("\n🎉 Lead generation completed successfully!")

if __name__ == "__main__":
    main()