#!/usr/bin/env python3
"""
Test script for MCP Server scraper using mock HTML data
This demonstrates how the scraper works without needing network access
"""

import os
import sys

# Create mock HTML that simulates the ModelScope MCP server listing page
MOCK_HTML = """
<!DOCTYPE html>
<html>
<head><title>MCP Servers - ModelScope</title></head>
<body>
    <div class="server-list">
        <div class="server-item">
            <h3 class="server-name">filesystem-mcp</h3>
            <div class="server-developer">Anthropic Team</div>
            <span class="server-type">local</span>
            <p class="server-description">A Model Context Protocol server providing secure file system access with configurable permissions and safety controls</p>
            <div class="server-views">1,234 views</div>
        </div>

        <div class="server-item">
            <h3 class="server-name">database-query-mcp</h3>
            <div class="server-developer">Developer from Google</div>
            <span class="server-type">hosted</span>
            <p class="server-description">Database query interface with support for PostgreSQL, MySQL, and SQLite databases</p>
            <div class="server-views">856 views</div>
            <div class="server-api-calls">15,420 API calls</div>
        </div>

        <div class="server-item">
            <h3 class="server-name">web-search-mcp</h3>
            <div class="server-developer">SearchCorp Labs</div>
            <span class="server-type">hosted</span>
            <p class="server-description">Real-time web search capabilities with advanced filtering and result ranking</p>
            <div class="server-views">2,891 views</div>
            <div class="server-api-calls">45,670 API calls</div>
        </div>

        <div class="server-item">
            <h3 class="server-name">code-analysis-mcp</h3>
            <div class="server-developer">Developer from Microsoft</div>
            <span class="server-type">local</span>
            <p class="server-description">Static code analysis and linting for multiple programming languages including Python, JavaScript, and Java</p>
            <div class="server-views">3,456 views</div>
        </div>

        <div class="server-item">
            <h3 class="server-name">image-processing-mcp</h3>
            <div class="server-developer">Vision AI Team from Alipay</div>
            <span class="server-type">hosted</span>
            <p class="server-description">Image processing and computer vision capabilities including object detection, OCR, and image enhancement</p>
            <div class="server-views">5,234 views</div>
            <div class="server-api-calls">89,340 API calls</div>
        </div>

        <div class="server-item">
            <h3 class="server-name">git-integration-mcp</h3>
            <div class="server-developer">DevTools Inc</div>
            <span class="server-type">local</span>
            <p class="server-description">Git repository integration with support for commits, branches, and pull requests</p>
            <div class="server-views">1,892 views</div>
        </div>
    </div>
</body>
</html>
"""

def create_mock_html_file():
    """Create a mock HTML file for testing"""
    filename = "mock_mcp_page.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(MOCK_HTML)
    print(f"Created mock HTML file: {filename}")
    return filename

def main():
    print("MCP Server Scraper - Mock Data Test")
    print("=" * 60)
    print()

    # Create mock HTML file
    mock_file = create_mock_html_file()

    # Import and run the scraper
    print(f"\nRunning scraper on mock data...\n")

    # Run the scraper script with the mock file
    exit_code = os.system(f"python3 scrape_mcp_servers.py --file {mock_file}")

    if exit_code == 0:
        print("\n" + "=" * 60)
        print("SUCCESS! The scraper works correctly.")
        print("=" * 60)
        print("\nTo use with the real website:")
        print("1. On a machine with internet access:")
        print("   python3 scrape_mcp_servers.py")
        print()
        print("2. To scrape all ~7599 servers (380 pages):")
        print("   python3 scrape_mcp_servers.py --all")
        print()
        print("3. If the site uses JavaScript:")
        print("   python3 scrape_mcp_servers.py --selenium")
        print()
        print("4. Or download the page manually and use:")
        print("   python3 scrape_mcp_servers.py --file downloaded_page.html")
        print()

        # Show the CSV file
        if os.path.exists('mcp_servers.csv'):
            print("\n" + "=" * 60)
            print("Generated CSV file content:")
            print("=" * 60)
            with open('mcp_servers.csv', 'r', encoding='utf-8') as f:
                print(f.read())
    else:
        print("\nTest failed. Check error messages above.")
        return 1

    # Cleanup
    print("\nCleaning up mock files...")
    for f in [mock_file]:
        if os.path.exists(f):
            os.remove(f)
            print(f"Removed {f}")

    return 0

if __name__ == "__main__":
    exit(main())
