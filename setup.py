#!/usr/bin/env python3
"""
Setup script for Professional Web Scraper Toolkit
=================================================

Enterprise-grade web scraping solution for business intelligence,
market research, and data automation.

Author: Professional Web Scraper Toolkit
Version: 2.0.0
License: MIT
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="professional-web-scraper-toolkit",
    version="2.0.0",
    author="Professional Web Scraper Toolkit",
    author_email="support@yourcompany.com",
    description="Enterprise-grade web scraping solution for business intelligence and data automation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/web-scraper-toolkit",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/web-scraper-toolkit/issues",
        "Documentation": "https://github.com/yourusername/web-scraper-toolkit/docs",
        "Source Code": "https://github.com/yourusername/web-scraper-toolkit",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "pre-commit>=2.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "myst-parser>=0.15",
        ],
        "full": [
            "selenium>=4.0",
            "scrapy>=2.5",
            "playwright>=1.20",
            "aiohttp>=3.8",
            "asyncio>=3.4",
        ],
    },
    entry_points={
        "console_scripts": [
            "job-scraper=src.job_scraper:main",
            "lead-scraper=src.lead_scraper:main",
            "price-monitor=src.price_monitor:main",
            "web-scraper-demo=examples.quick_start:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yaml", "*.yml", "*.txt", "*.md"],
    },
    keywords=[
        "web scraping",
        "data extraction",
        "business intelligence",
        "market research",
        "lead generation",
        "price monitoring",
        "automation",
        "enterprise",
        "python",
        "beautifulsoup",
        "requests",
        "pandas",
    ],
    platforms=["any"],
    license="MIT",
    zip_safe=False,
) 