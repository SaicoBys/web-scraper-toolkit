import pandas as pd
import json
import os
from typing import List, Dict

class SiteManager:
    """Professional site management for mass site addition"""
    
    def __init__(self, config_file='config/job_scraper_config.json'):
        """Initialize site manager with configuration"""
        self.config = self.load_config(config_file)
        self.sites_df = None
        self.active_sites = []
        self.load_sites()
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def load_sites(self):
        """Load sites from CSV file with filtering"""
        csv_file = self.config.get('target_sites_csv')
        
        if not csv_file or not os.path.exists(csv_file):
            print(f"⚠️  CSV file not found: {csv_file}")
            return
        
        # Load CSV
        self.sites_df = pd.read_csv(csv_file)
        
        # Apply filters
        filtered_sites = self.sites_df.copy()
        
        # Filter by enabled
        filtered_sites = filtered_sites[filtered_sites['enabled'] == True]
        
        # Filter by categories
        target_categories = self.config.get('target_categories', [])
        if target_categories:
            filtered_sites = filtered_sites[filtered_sites['category'].isin(target_categories)]
        
        # Filter by priority
        min_priority = self.config.get('min_priority', 'low')
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        min_priority_value = priority_order.get(min_priority, 1)
        
        filtered_sites = filtered_sites[
            filtered_sites['priority'].map(priority_order) >= min_priority_value
        ]
        
        # Extract site URLs
        self.active_sites = filtered_sites['site_url'].tolist()
        
        print(f"✅ Loaded {len(self.active_sites)} active sites from {len(self.sites_df)} total sites")
        
        return self.active_sites
    
    def get_sites_by_category(self, category: str) -> List[str]:
        """Get sites filtered by category"""
        if self.sites_df is None:
            return []
        
        category_sites = self.sites_df[
            (self.sites_df['category'] == category) & 
            (self.sites_df['enabled'] == True)
        ]
        
        return category_sites['site_url'].tolist()
    
    def get_sites_by_priority(self, priority: str) -> List[str]:
        """Get sites filtered by priority"""
        if self.sites_df is None:
            return []
        
        priority_sites = self.sites_df[
            (self.sites_df['priority'] == priority) & 
            (self.sites_df['enabled'] == True)
        ]
        
        return priority_sites['site_url'].tolist()
    
    def add_sites_bulk(self, sites_data: List[Dict]):
        """Add multiple sites at once"""
        if self.sites_df is None:
            self.sites_df = pd.DataFrame(columns=['site_url', 'category', 'priority', 'enabled'])
        
        new_sites_df = pd.DataFrame(sites_data)
        self.sites_df = pd.concat([self.sites_df, new_sites_df], ignore_index=True)
        
        # Remove duplicates
        self.sites_df = self.sites_df.drop_duplicates(subset=['site_url'], keep='last')
        
        # Save back to CSV
        csv_file = self.config.get('target_sites_csv')
        if csv_file:
            self.sites_df.to_csv(csv_file, index=False)
            print(f"✅ Added {len(sites_data)} sites and saved to {csv_file}")
        
        # Reload active sites
        self.load_sites()
    
    def enable_disable_sites(self, site_urls: List[str], enabled: bool):
        """Enable or disable specific sites"""
        if self.sites_df is None:
            return
        
        mask = self.sites_df['site_url'].isin(site_urls)
        self.sites_df.loc[mask, 'enabled'] = enabled
        
        # Save changes
        csv_file = self.config.get('target_sites_csv')
        if csv_file:
            self.sites_df.to_csv(csv_file, index=False)
            
        action = "enabled" if enabled else "disabled"
        print(f"✅ {action.capitalize()} {len(site_urls)} sites")
        
        # Reload active sites
        self.load_sites()
    
    def get_site_stats(self):
        """Get statistics about loaded sites"""
        if self.sites_df is None:
            return {
                'total_sites': 0,
                'active_sites': 0,
                'disabled_sites': 0,
                'by_category': {},
                'by_priority': {}
            }
        
        stats = {
            'total_sites': len(self.sites_df),
            'active_sites': len(self.active_sites),
            'disabled_sites': len(self.sites_df[self.sites_df['enabled'] == False]),
            'by_category': self.sites_df['category'].value_counts().to_dict(),
            'by_priority': self.sites_df['priority'].value_counts().to_dict()
        }
        
        return stats
    
    def print_site_stats(self):
        """Print formatted site statistics"""
        stats = self.get_site_stats()
        
        print("\n" + "="*50)
        print("📊 SITE MANAGER STATISTICS")
        print("="*50)
        print(f"📈 Total sites: {stats['total_sites']}")
        print(f"✅ Active sites: {stats['active_sites']}")
        print(f"❌ Disabled sites: {stats['disabled_sites']}")
        
        print("\n📊 By Category:")
        for category, count in stats['by_category'].items():
            print(f"  {category}: {count}")
        
        print("\n🎯 By Priority:")
        for priority, count in stats['by_priority'].items():
            print(f"  {priority}: {count}")
        
        print("="*50)

def main():
    """Demo of site manager functionality"""
    manager = SiteManager()
    
    # Show current stats
    manager.print_site_stats()
    
    # Show active sites
    print(f"\n🔍 Active Sites ({len(manager.active_sites)}):")
    for site in manager.active_sites:
        print(f"  - {site}")
    
    # Show sites by category
    print(f"\n🏢 Company Sites:")
    company_sites = manager.get_sites_by_category('company')
    for site in company_sites:
        print(f"  - {site}")
    
    print(f"\n📋 Job Board Sites:")
    job_sites = manager.get_sites_by_category('job_board')
    for site in job_sites:
        print(f"  - {site}")

if __name__ == "__main__":
    main()