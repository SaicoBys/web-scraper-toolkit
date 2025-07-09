#!/usr/bin/env python3
"""
Quick Start Example - Professional Web Scraper Toolkit
======================================================

This example demonstrates how to use the Professional Web Scraper Toolkit
for enterprise data extraction and business intelligence.

Author: Professional Web Scraper Toolkit
Version: 2.0.0
License: MIT
"""

import sys
import os
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def demo_job_market_analysis():
    """
    Demonstrate job market intelligence capabilities
    """
    print("🔍 Job Market Intelligence Demo")
    print("=" * 50)
    
    try:
        from job_scraper import JobScraper
        
        # Initialize scraper with professional configuration
        scraper = JobScraper('config/job_scraper_config.json')
        
        # Configure search parameters
        keywords = ['python developer', 'data scientist', 'machine learning']
        location = 'remote'
        max_results = 50
        
        print(f"📊 Extracting job market data...")
        print(f"   Keywords: {', '.join(keywords)}")
        print(f"   Location: {location}")
        print(f"   Max Results: {max_results}")
        
        # Execute scraping
        jobs = scraper.scrape_demo_jobs(keywords, location, max_results)
        
        # Export results
        output_file = scraper.export_data('excel')
        
        # Generate professional report
        scraper.generate_report()
        
        print(f"✅ Job market analysis completed!")
        print(f"📁 Results saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in job market analysis: {e}")
        return False

def demo_lead_generation():
    """
    Demonstrate lead generation capabilities
    """
    print("\n🎯 Lead Generation Demo")
    print("=" * 50)
    
    try:
        from lead_scraper import LeadScraper
        
        # Initialize lead scraper
        scraper = LeadScraper('config/lead_scraper_config.json')
        
        # Configure lead generation parameters
        industry = 'technology'
        location = 'usa'
        max_results = 100
        
        print(f"📈 Generating qualified leads...")
        print(f"   Industry: {industry}")
        print(f"   Location: {location}")
        print(f"   Max Results: {max_results}")
        
        # Execute lead generation
        leads = scraper.scrape_demo_leads(industry, location, max_results)
        
        # Export results
        output_file = scraper.export_data('excel')
        
        # Generate lead quality report
        scraper.generate_lead_report()
        
        print(f"✅ Lead generation completed!")
        print(f"📁 Results saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in lead generation: {e}")
        return False

def demo_price_monitoring():
    """
    Demonstrate price monitoring capabilities
    """
    print("\n💰 Price Monitoring Demo")
    print("=" * 50)
    
    try:
        from price_monitor import PriceMonitor
        
        # Initialize price monitor
        monitor = PriceMonitor('config/price_monitor_config.json')
        
        # Configure monitoring parameters
        products = [
            {
                "name": "MacBook Pro 13\"",
                "category": "Electronics",
                "target_price": 1200,
                "urls": ["https://www.amazon.com/dp/example"]
            },
            {
                "name": "iPhone 14",
                "category": "Electronics",
                "target_price": 800,
                "urls": ["https://www.apple.com/iphone-14/"]
            }
        ]
        
        print(f"📊 Monitoring product prices...")
        print(f"   Products: {len(products)} items")
        print(f"   Categories: Electronics")
        
        # Execute price monitoring
        price_data = monitor.monitor_demo_prices(products)
        
        # Export results
        output_file = monitor.export_data('excel')
        
        # Generate price analysis report
        monitor.generate_price_report()
        
        print(f"✅ Price monitoring completed!")
        print(f"📁 Results saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in price monitoring: {e}")
        return False

def generate_executive_summary():
    """
    Generate an executive summary of all scraping activities
    """
    print("\n📋 Executive Summary")
    print("=" * 50)
    
    # Check for generated files
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith(('.csv', '.json', '.xlsx'))]
        
        print(f"📁 Generated Files: {len(files)}")
        for file in files:
            file_path = os.path.join(data_dir, file)
            size = os.path.getsize(file_path)
            print(f"   📄 {file} ({size:,} bytes)")
    
    print(f"\n⏰ Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Toolkit Version: 2.0.0")
    print(f"🚀 Status: Production Ready")

def main():
    """
    Main execution function for the quick start demo
    """
    print("🚀 Professional Web Scraper Toolkit - Quick Start Demo")
    print("=" * 60)
    print("Enterprise-grade data extraction and business intelligence")
    print("=" * 60)
    
    # Execute all demos
    results = []
    
    results.append(demo_job_market_analysis())
    results.append(demo_lead_generation())
    results.append(demo_price_monitoring())
    
    # Generate summary
    generate_executive_summary()
    
    # Final status
    successful_demos = sum(results)
    total_demos = len(results)
    
    print(f"\n🎉 Demo Execution Summary")
    print("=" * 30)
    print(f"✅ Successful: {successful_demos}/{total_demos}")
    print(f"📊 Success Rate: {(successful_demos/total_demos)*100:.1f}%")
    
    if successful_demos == total_demos:
        print(f"\n🎯 All demos completed successfully!")
        print(f"💼 Your toolkit is ready for enterprise use!")
    else:
        print(f"\n⚠️  Some demos encountered issues.")
        print(f"🔧 Check the configuration files and dependencies.")
    
    print(f"\n📚 Next Steps:")
    print(f"   1. Review generated data files in the 'data/' directory")
    print(f"   2. Customize configuration files for your specific needs")
    print(f"   3. Deploy to production environment")
    print(f"   4. Set up automated scheduling for continuous monitoring")

if __name__ == "__main__":
    main() 