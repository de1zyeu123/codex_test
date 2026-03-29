#!/usr/bin/env python3
"""
Debug script to save and inspect the Selenium-rendered HTML
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def save_rendered_html():
    """Fetch page with Selenium and save the HTML"""

    print("Initializing Selenium...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    print("Loading page...")
    driver.get('https://modelscope.cn/mcp?page=1')

    # Wait for JavaScript to load
    print("Waiting for JavaScript to render...")
    time.sleep(5)

    # Save the rendered HTML
    html = driver.page_source

    with open('rendered_page.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Saved rendered HTML to: rendered_page.html")
    print(f"  File size: {len(html)} bytes")

    # Extract and show a snippet of the items
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find items
    items = soup.select('[class*="item"]')
    print(f"\n✓ Found {len(items)} items with selector [class*='item']")

    if items:
        print("\n" + "="*60)
        print("First item HTML structure:")
        print("="*60)
        print(items[0].prettify()[:1500])
        print("...")

        # Try to find common patterns
        print("\n" + "="*60)
        print("Looking for data patterns in first item:")
        print("="*60)

        first_item = items[0]

        # Look for text content
        all_text = first_item.get_text(strip=True)
        if all_text:
            print(f"Text content: {all_text[:200]}...")

        # Look for specific tags
        for tag in ['h1', 'h2', 'h3', 'h4', 'a', 'span', 'div', 'p']:
            elements = first_item.find_all(tag, limit=5)
            if elements:
                print(f"\n{tag.upper()} tags found:")
                for elem in elements[:3]:
                    text = elem.get_text(strip=True)[:80]
                    classes = elem.get('class', [])
                    if text:
                        print(f"  - {text} (classes: {classes})")

    driver.quit()
    print("\n✓ Done! Now you can:")
    print("  1. Open 'rendered_page.html' in a browser to see the structure")
    print("  2. Run: python3 scrape_mcp_servers.py --file rendered_page.html")

if __name__ == "__main__":
    save_rendered_html()
