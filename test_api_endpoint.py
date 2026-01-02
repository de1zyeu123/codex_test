#!/usr/bin/env python3
"""
API Endpoint Tester for ModelScope MCP
This script helps identify the correct API endpoint by trying different variations
"""

import requests
import json

def test_api_endpoints():
    """Test various possible API endpoints"""

    possible_endpoints = [
        "https://www.modelscope.cn/api/v1/mcp/list",
        "https://modelscope.cn/api/v1/mcp/list",
        "https://www.modelscope.cn/api/v1/mcps",
        "https://modelscope.cn/api/v1/mcps",
        "https://www.modelscope.cn/api/mcp/list",
        "https://modelscope.cn/api/mcp/list",
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.modelscope.cn/mcp',
        'Origin': 'https://www.modelscope.cn'
    }

    params_variations = [
        {'PageNumber': 1, 'PageSize': 20},
        {'page': 1, 'pageSize': 20},
        {'Page': 1, 'Size': 20},
        {}
    ]

    print("Testing API endpoints...")
    print("=" * 60)

    for endpoint in possible_endpoints:
        for params in params_variations:
            try:
                param_str = json.dumps(params) if params else "no params"
                print(f"\nTesting: {endpoint}")
                print(f"Params: {param_str}")

                response = requests.get(endpoint, params=params, headers=headers, timeout=10)

                print(f"Status: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"✓ SUCCESS! Got JSON response")
                        print(f"Response keys: {list(data.keys())[:10]}")
                        print(f"Response preview:\n{json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")

                        # Try to find the data array
                        if 'Data' in data:
                            print(f"\nFound 'Data' key!")
                            if isinstance(data['Data'], dict) and 'Data' in data['Data']:
                                items = data['Data']['Data']
                                print(f"Items count: {len(items)}")
                                if items:
                                    print(f"First item keys: {list(items[0].keys())}")
                                    print(f"First item sample:\n{json.dumps(items[0], indent=2, ensure_ascii=False)}")

                        return endpoint, params  # Return successful endpoint

                    except json.JSONDecodeError:
                        print(f"Response is not JSON")
                        print(f"Content preview: {response.text[:200]}")

            except requests.RequestException as e:
                print(f"✗ Error: {e}")

    print("\n" + "=" * 60)
    print("No working API endpoint found. The site may require:")
    print("1. Authentication/cookies")
    print("2. Special headers")
    print("3. JavaScript rendering (use Selenium)")
    return None, None


if __name__ == "__main__":
    print("ModelScope MCP API Endpoint Tester")
    print("=" * 60)
    test_api_endpoints()
