#!/usr/bin/env python3
"""
MCP Server Data Scraper for ModelScope
Scrapes MCP server information from modelscope.cn/mcp

Usage:
    # Method 1: Direct scraping (requires network access)
    python3 scrape_mcp_servers.py

    # Method 2: Use Selenium for JavaScript-heavy sites
    python3 scrape_mcp_servers.py --selenium

    # Method 3: Parse from local HTML file (if you downloaded the page)
    python3 scrape_mcp_servers.py --file page.html

Dependencies:
    pip3 install beautifulsoup4 requests
    # For Selenium method:
    pip3 install selenium webdriver-manager
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import json
from typing import List, Dict, Optional
import re
import argparse
import os


class MCPServerScraper:
    def __init__(self, base_url: str = "https://modelscope.cn/mcp", use_selenium: bool = False):
        self.base_url = base_url
        self.use_selenium = use_selenium

        if use_selenium:
            self._init_selenium()
        else:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
                'Referer': 'https://modelscope.cn/'
            })

    def _init_selenium(self):
        """Initialize Selenium WebDriver"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager

            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            print("Selenium WebDriver initialized successfully")
        except ImportError:
            print("ERROR: Selenium not installed. Run: pip3 install selenium webdriver-manager")
            raise
        except Exception as e:
            print(f"ERROR: Failed to initialize Selenium: {e}")
            raise

    def fetch_page(self, page: int = 1, retries: int = 3) -> str:
        """Fetch a single page with retry logic"""
        if self.use_selenium:
            return self._fetch_with_selenium(page)
        else:
            return self._fetch_with_requests(page, retries)

    def _fetch_with_requests(self, page: int, retries: int = 3) -> str:
        """Fetch using requests library"""
        url = f"{self.base_url}?page={page}"

        for attempt in range(retries):
            try:
                print(f"Fetching page {page} (attempt {attempt + 1}/{retries})...")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                print(f"Error fetching page {page}: {e}")
                if attempt < retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise

    def _fetch_with_selenium(self, page: int) -> str:
        """Fetch using Selenium WebDriver"""
        url = f"{self.base_url}?page={page}"
        print(f"Fetching page {page} with Selenium...")

        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for JavaScript to load
            return self.driver.page_source
        except Exception as e:
            print(f"Error fetching page {page} with Selenium: {e}")
            raise

    def parse_from_file(self, filepath: str) -> List[Dict]:
        """Parse MCP server data from a local HTML file"""
        print(f"Parsing from file: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        return self.parse_server_data(html)

    def parse_server_data(self, html: str) -> List[Dict]:
        """Parse MCP server data from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        servers = []

        # Try to find JSON data embedded in the page (common pattern for modern web apps)
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'window.__INITIAL_STATE__' in script.string:
                # Extract JSON data
                try:
                    json_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', script.string, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group(1))
                        print("Found initial state data!")
                        # Parse the JSON structure (will need to adjust based on actual structure)
                        return self._parse_from_json(data)
                except Exception as e:
                    print(f"Error parsing JSON: {e}")

        # Fallback: Parse from HTML structure
        print("Parsing from HTML structure...")
        return self._parse_from_html(soup)

    def _parse_from_json(self, data: dict) -> List[Dict]:
        """Parse server data from JSON"""
        servers = []
        # This will need to be adjusted based on the actual JSON structure
        # Common patterns to look for:
        # - data['servers'], data['items'], data['list'], etc.
        print(f"JSON keys: {list(data.keys())[:10]}")  # Debug
        return servers

    def _parse_from_html(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse server data from HTML elements"""
        servers = []

        # Look for common container patterns
        # Try different selectors
        selectors = [
            '.server-item',
            '.mcp-server',
            '[class*="server"]',
            '[class*="card"]',
            '.list-item',
            'article',
            '[class*="item"]'
        ]

        items = []
        for selector in selectors:
            items = soup.select(selector)
            if items:
                print(f"Found {len(items)} items with selector: {selector}")
                break

        if not items:
            print("No server items found. Page structure:")
            print(soup.prettify()[:2000])  # Print first 2000 chars for debugging
            return servers

        for item in items:
            try:
                server = {
                    'name': '',
                    'developer': '',
                    'type': '',
                    'description': '',
                    'views': '',
                    'api_calls': ''
                }

                # Extract name (try different patterns)
                name_elem = (item.find('h3') or item.find('h2') or
                           item.find(class_=re.compile(r'title|name', re.I)))
                if name_elem:
                    server['name'] = name_elem.get_text(strip=True)

                # Extract developer
                dev_elem = item.find(class_=re.compile(r'author|developer|user', re.I))
                if dev_elem:
                    server['developer'] = dev_elem.get_text(strip=True)

                # Extract type (hosted/local)
                type_elem = item.find(class_=re.compile(r'type|tag|badge', re.I))
                if type_elem:
                    type_text = type_elem.get_text(strip=True).lower()
                    server['type'] = 'hosted' if 'host' in type_text else 'local'

                # Extract description
                desc_elem = item.find(class_=re.compile(r'desc|description|summary', re.I))
                if desc_elem:
                    server['description'] = desc_elem.get_text(strip=True)

                # Extract views
                views_elem = item.find(class_=re.compile(r'view|visit|count', re.I))
                if views_elem:
                    server['views'] = views_elem.get_text(strip=True)

                # Extract API calls (only for hosted)
                if server['type'] == 'hosted':
                    api_elem = item.find(class_=re.compile(r'api|call|usage', re.I))
                    if api_elem:
                        server['api_calls'] = api_elem.get_text(strip=True)

                if server['name']:  # Only add if we found at least a name
                    servers.append(server)

            except Exception as e:
                print(f"Error parsing server item: {e}")
                continue

        return servers

    def get_total_pages(self, html: str) -> int:
        """Determine total number of pages"""
        soup = BeautifulSoup(html, 'html.parser')

        # Look for pagination info
        pagination = soup.find(class_=re.compile(r'pagination', re.I))
        if pagination:
            # Try to find total pages or last page number
            page_links = pagination.find_all('a')
            if page_links:
                numbers = []
                for link in page_links:
                    text = link.get_text(strip=True)
                    if text.isdigit():
                        numbers.append(int(text))
                if numbers:
                    return max(numbers)

        # Check for total count (7599 servers mentioned)
        # Assume ~20 items per page as default
        return 380  # 7599 / 20 ≈ 380 pages

    def scrape_all(self, max_pages: int = None, output_file: str = 'mcp_servers.csv') -> List[Dict]:
        """Scrape all pages and save to CSV"""
        all_servers = []

        # Fetch first page to determine total pages
        print("Fetching first page to determine structure...")
        first_page_html = self.fetch_page(1)

        if not max_pages:
            max_pages = self.get_total_pages(first_page_html)
            print(f"Estimated total pages: {max_pages}")

        # Parse first page
        servers = self.parse_server_data(first_page_html)
        all_servers.extend(servers)
        print(f"Page 1: Found {len(servers)} servers")

        # Fetch remaining pages
        for page in range(2, max_pages + 1):
            try:
                time.sleep(1)  # Be polite, don't hammer the server
                html = self.fetch_page(page)
                servers = self.parse_server_data(html)
                all_servers.extend(servers)
                print(f"Page {page}: Found {len(servers)} servers (Total: {len(all_servers)})")

                # Stop if no more servers found
                if not servers:
                    print("No more servers found. Stopping.")
                    break

            except KeyboardInterrupt:
                print("\nScraping interrupted by user.")
                break
            except Exception as e:
                print(f"Error on page {page}: {e}")
                continue

        # Save to CSV
        if all_servers:
            self.save_to_csv(all_servers, output_file)
            print(f"\nTotal servers scraped: {len(all_servers)}")
            print(f"Data saved to: {output_file}")
        else:
            print("\nNo servers were scraped. Please check the page structure.")

        return all_servers

    def save_to_csv(self, servers: List[Dict], filename: str):
        """Save servers data to CSV file"""
        if not servers:
            print("No data to save.")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['name', 'developer', 'type', 'description', 'views', 'api_calls']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(servers)

        print(f"Saved {len(servers)} servers to {filename}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Scrape MCP server data from ModelScope',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Scrape with requests (default)
  %(prog)s --selenium                # Use Selenium for JavaScript rendering
  %(prog)s --file page.html          # Parse from local HTML file
  %(prog)s --max-pages 10            # Scrape only first 10 pages
  %(prog)s --output data.csv         # Save to custom filename
        """
    )

    parser.add_argument('--selenium', action='store_true',
                       help='Use Selenium WebDriver instead of requests')
    parser.add_argument('--file', type=str,
                       help='Parse from local HTML file instead of scraping')
    parser.add_argument('--max-pages', type=int, default=3,
                       help='Maximum number of pages to scrape (default: 3)')
    parser.add_argument('--output', type=str, default='mcp_servers.csv',
                       help='Output CSV filename (default: mcp_servers.csv)')
    parser.add_argument('--all', action='store_true',
                       help='Scrape all pages (overrides --max-pages)')

    args = parser.parse_args()

    print("MCP Server Data Scraper")
    print("=" * 50)

    # Parse from file
    if args.file:
        if not os.path.exists(args.file):
            print(f"ERROR: File not found: {args.file}")
            return 1

        scraper = MCPServerScraper()
        servers = scraper.parse_from_file(args.file)

        if servers:
            scraper.save_to_csv(servers, args.output)
            print(f"\nTotal servers parsed: {len(servers)}")
            print(f"Data saved to: {args.output}")

            # Show sample
            print("\n" + "=" * 50)
            print("Sample data (first 3 servers):")
            print("=" * 50)
            for i, server in enumerate(servers[:3], 1):
                print(f"\nServer {i}:")
                for key, value in server.items():
                    print(f"  {key}: {value}")
        else:
            print("\nNo servers found in file.")
            return 1

        return 0

    # Scrape from web
    try:
        scraper = MCPServerScraper(use_selenium=args.selenium)

        max_pages = None if args.all else args.max_pages

        if args.all:
            print("\nStarting full scrape (all ~380 pages, ~7599 servers)...")
            print("This will take a while. Press Ctrl+C to stop.\n")
        else:
            print(f"\nStarting scrape (first {args.max_pages} pages for testing)...")
            print("Use --all flag to scrape all pages\n")

        servers = scraper.scrape_all(max_pages=max_pages, output_file=args.output)

        if servers:
            print("\n" + "=" * 50)
            print("Sample data (first 3 servers):")
            print("=" * 50)
            for i, server in enumerate(servers[:3], 1):
                print(f"\nServer {i}:")
                for key, value in server.items():
                    print(f"  {key}: {value}")

            print("\n" + "=" * 50)
            print("To scrape all ~380 pages, run:")
            print(f"  python3 {os.path.basename(__file__)} --all")
        else:
            print("\nFailed to scrape data.")
            print("\nTroubleshooting:")
            print("1. Try with Selenium: python3 scrape_mcp_servers.py --selenium")
            print("2. Download page manually and use: python3 scrape_mcp_servers.py --file page.html")
            return 1

    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
        return 0
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTry alternative methods:")
        print("1. Use Selenium: python3 scrape_mcp_servers.py --selenium")
        print("2. Parse from file: python3 scrape_mcp_servers.py --file page.html")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
