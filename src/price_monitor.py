import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
import argparse
from datetime import datetime
import os

class PriceMonitor:
    """Professional price monitoring toolkit for e-commerce and competitive analysis"""
    
    def __init__(self, config_file='config/price_monitor_config.json'):
        """Initialize price monitor with configuration"""
        self.config = self.load_config(config_file)
        self.price_data = []
        self.session = requests.Session()
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
        print("💰 Price Monitor Toolkit initialized")
        print(f"📊 Products to monitor: {len(self.config.get('products', []))}")
        print(f"🔄 Check interval: {self.config.get('check_interval', 300)} seconds")
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "products": [],
                "check_interval": 300,
                "price_change_threshold": 0.05,
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
    
    def generate_demo_price_data(self, num_products=20):
        """
        Generate demo price data for portfolio demonstration
        In production, this would scrape actual e-commerce sites
        """
        print("🔍 Generating demo price monitoring data...")
        
        # Demo products and categories
        products = [
            {"name": "MacBook Pro 13\"", "category": "Electronics", "base_price": 1299.99},
            {"name": "iPhone 14", "category": "Electronics", "base_price": 899.99},
            {"name": "Samsung Galaxy S23", "category": "Electronics", "base_price": 799.99},
            {"name": "Dell XPS 13", "category": "Electronics", "base_price": 999.99},
            {"name": "Sony WH-1000XM4", "category": "Electronics", "base_price": 349.99},
            {"name": "Nike Air Max 90", "category": "Footwear", "base_price": 119.99},
            {"name": "Adidas Ultraboost 22", "category": "Footwear", "base_price": 179.99},
            {"name": "Levi's 501 Jeans", "category": "Apparel", "base_price": 89.99},
            {"name": "Patagonia Fleece", "category": "Apparel", "base_price": 149.99},
            {"name": "Instant Pot Duo", "category": "Kitchen", "base_price": 79.99}
        ]
        
        sites = ["Amazon", "Best Buy", "Target", "Walmart", "Newegg"]
        
        for product in products[:num_products]:
            for site in sites:
                # Simulate price variations
                price_variation = random.uniform(-0.2, 0.3)  # -20% to +30%
                current_price = product["base_price"] * (1 + price_variation)
                
                # Simulate availability
                availability = random.choice([True, True, True, False])  # 75% available
                
                # Simulate discount info
                discount = random.uniform(0, 0.25) if random.random() < 0.3 else 0
                
                price_record = {
                    'product_name': product["name"],
                    'category': product["category"],
                    'site': site,
                    'current_price': round(current_price, 2),
                    'original_price': product["base_price"],
                    'discount_percentage': round(discount * 100, 1),
                    'availability': availability,
                    'stock_status': 'In Stock' if availability else 'Out of Stock',
                    'price_change': round(current_price - product["base_price"], 2),
                    'price_change_percent': round(((current_price - product["base_price"]) / product["base_price"]) * 100, 1),
                    'last_updated': datetime.now().isoformat(),
                    'scraped_at': datetime.now().isoformat()
                }
                
                self.price_data.append(price_record)
                
                # Progress indicator
                if len(self.price_data) % 20 == 0:
                    print(f"📊 Monitored {len(self.price_data)} price points...")
                
                # Respectful rate limiting
                time.sleep(random.uniform(0.1, 0.3))
        
        print(f"✅ Successfully monitored {len(self.price_data)} price points")
        return self.price_data
    
    def detect_price_changes(self, threshold=0.05):
        """Detect significant price changes"""
        changes = []
        
        for record in self.price_data:
            change_percent = abs(record['price_change_percent']) / 100
            if change_percent >= threshold:
                changes.append(record)
        
        return changes
    
    def export_data(self, output_format='csv', filename=None):
        """Export price data to specified format"""
        if not self.price_data:
            print("❌ No price data to export")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/price_monitor_{timestamp}"
        
        df = pd.DataFrame(self.price_data)
        
        if output_format.lower() == 'csv':
            output_file = f"{filename}.csv"
            df.to_csv(output_file, index=False)
        elif output_format.lower() == 'json':
            output_file = f"{filename}.json"
            df.to_json(output_file, orient='records', indent=2)
        elif output_format.lower() == 'excel':
            output_file = f"{filename}.xlsx"
            df.to_excel(output_file, index=False)
        
        print(f"💾 Price data exported to: {output_file}")
        print(f"📊 Total records: {len(self.price_data)}")
        return output_file
    
    def generate_report(self):
        """Generate price monitoring summary report"""
        if not self.price_data:
            return
        
        df = pd.DataFrame(self.price_data)
        
        # Calculate statistics
        avg_price = df['current_price'].mean()
        price_changes = self.detect_price_changes(0.1)  # 10% threshold
        available_products = df[df['availability'] == True]
        
        print("\n" + "="*50)
        print("💰 PRICE MONITORING REPORT")
        print("="*50)
        print(f"📊 Total price points monitored: {len(self.price_data)}")
        print(f"🛍️  Unique products: {df['product_name'].nunique()}")
        print(f"🏪 Sites monitored: {df['site'].nunique()}")
        print(f"💵 Average price: ${avg_price:.2f}")
        print(f"📈 Significant price changes: {len(price_changes)}")
        print(f"✅ Products available: {len(available_products)}")
        print(f"❌ Products out of stock: {len(df) - len(available_products)}")
        
        print("\n📊 Price Changes by Category:")
        category_changes = df.groupby('category')['price_change_percent'].mean().round(1)
        print(category_changes.to_string())
        
        print("\n🏪 Average Prices by Site:")
        site_prices = df.groupby('site')['current_price'].mean().round(2)
        print(site_prices.to_string())
        
        print("\n🔥 Top 5 Price Drops:")
        top_drops = df.nsmallest(5, 'price_change_percent')[['product_name', 'site', 'price_change_percent']]
        print(top_drops.to_string(index=False))
        
        print("="*50)

def main():
    """Main function to run the price monitor"""
    parser = argparse.ArgumentParser(description='Professional Price Monitor Toolkit')
    parser.add_argument('--products', type=int, default=20, 
                       help='Number of products to monitor')
    parser.add_argument('--output', choices=['csv', 'json', 'excel'], default='csv',
                       help='Output format')
    parser.add_argument('--config', default='config/price_monitor_config.json',
                       help='Configuration file path')
    parser.add_argument('--threshold', type=float, default=0.1,
                       help='Price change threshold for alerts')
    
    args = parser.parse_args()
    
    # Initialize monitor
    monitor = PriceMonitor(args.config)
    
    # Generate demo data
    monitor.generate_demo_price_data(args.products)
    
    # Export data
    monitor.export_data(args.output)
    
    # Generate report
    monitor.generate_report()
    
    print("\n🎉 Price monitoring completed successfully!")

if __name__ == "__main__":
    main()