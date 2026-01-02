# MCP Server Data Scraper

A Python script to scrape MCP (Model Context Protocol) server data from ModelScope (https://modelscope.cn/mcp).

## Features

- Scrapes MCP server information including:
  - Server name
  - Developer information
  - Server type (hosted/local)
  - Description
  - View count
  - API call count (for hosted servers only)

- Multiple scraping methods:
  - Direct HTTP requests (default)
  - Selenium WebDriver (for JavaScript-heavy pages)
  - Parse from local HTML files

- Exports data to CSV format

## Installation

```bash
# Install required dependencies
pip3 install -r requirements.txt

# Optional: Install Selenium dependencies for JavaScript rendering
pip3 install selenium webdriver-manager
```

## Usage

### Method 1: Direct Scraping (Default)

```bash
# Test with first 3 pages
python3 scrape_mcp_servers.py

# Scrape all pages (~7599 servers across ~380 pages)
python3 scrape_mcp_servers.py --all

# Scrape first 10 pages
python3 scrape_mcp_servers.py --max-pages 10

# Save to custom filename
python3 scrape_mcp_servers.py --output my_data.csv
```

### Method 2: Using Selenium (for JavaScript-rendered content)

```bash
# Make sure Selenium is installed first
pip3 install selenium webdriver-manager

# Run with Selenium
python3 scrape_mcp_servers.py --selenium

# Scrape all pages with Selenium
python3 scrape_mcp_servers.py --selenium --all
```

### Method 3: Parse from Local HTML File

If you manually download the page or face network restrictions:

```bash
# Download the page manually in your browser, then:
python3 scrape_mcp_servers.py --file downloaded_page.html
```

## Output Format

The script generates a CSV file with the following columns:

| Column      | Description                                      |
|-------------|--------------------------------------------------|
| name        | MCP server name                                  |
| developer   | Developer/organization (e.g., "Team from Alipay")|
| type        | Server type: "hosted" or "local"                 |
| description | Description of the server's functionality        |
| views       | Number of views/visitors                         |
| api_calls   | Number of API calls (hosted servers only)        |

### Example Output

```csv
name,developer,type,description,views,api_calls
filesystem-mcp,Anthropic Team,local,Secure file system access with configurable permissions,1234 views,
database-query-mcp,Developer from Google,hosted,Database query interface for PostgreSQL/MySQL/SQLite,856 views,15420 API calls
web-search-mcp,SearchCorp Labs,hosted,Real-time web search with advanced filtering,2891 views,45670 API calls
```

## Testing

Run the test script with mock data to verify functionality:

```bash
python3 test_scraper_mock.py
```

This will:
1. Create mock HTML data
2. Test the scraper functionality
3. Generate a sample CSV
4. Show you what the output looks like

## Troubleshooting

### Network/Proxy Errors

If you encounter `403 Forbidden` or proxy errors:

1. **Try Selenium method:**
   ```bash
   python3 scrape_mcp_servers.py --selenium
   ```

2. **Download page manually:**
   - Open https://modelscope.cn/mcp?page=1 in your browser
   - Save the page (Ctrl+S or Cmd+S)
   - Run: `python3 scrape_mcp_servers.py --file saved_page.html`

### Website Structure Changed

If the scraper finds no data, the website structure may have changed. The script includes debug output to help identify the issue:

- Check the console output for found HTML elements
- The script will print the page structure for debugging
- You may need to update the CSS selectors in the `_parse_from_html` method

### Rate Limiting

If you're being rate-limited:

- The script includes 1-second delays between requests
- For heavy scraping, consider increasing the delay in `scrape_all` method
- Use the `--max-pages` option to scrape in batches

## Command Line Options

```
usage: scrape_mcp_servers.py [-h] [--selenium] [--file FILE] [--max-pages MAX_PAGES]
                             [--output OUTPUT] [--all]

Options:
  -h, --help            Show help message
  --selenium            Use Selenium WebDriver instead of requests
  --file FILE           Parse from local HTML file
  --max-pages N         Maximum number of pages to scrape (default: 3)
  --output FILE         Output CSV filename (default: mcp_servers.csv)
  --all                 Scrape all pages (overrides --max-pages)
```

## Note on Data Volume

The website reportedly contains **7,599 MCP servers** across approximately **380 pages**. Scraping all data:

- Will take significant time (several minutes to hours depending on method)
- Generates a large CSV file (~7600 rows)
- May trigger rate limiting - be respectful of the server

Consider testing with a small number of pages first (`--max-pages 5`) before running a full scrape.

## License

This script is for educational and research purposes. Please respect the website's terms of service and robots.txt when scraping.
