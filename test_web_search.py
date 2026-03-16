#!/usr/bin/env python3
"""Test script to verify web search functionality."""

import asyncio
import httpx
from urllib.parse import unquote
import re

# Shared constants
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36"


def _strip_tags(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<script[\s\S]*?</script>', '', text, flags=re.I)
    text = re.sub(r'<style[\s\S]*?</style>', '', text, flags=re.I)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


async def test_duckduckgo_search():
    """Test DuckDuckGo search functionality."""
    try:
        query = "上证指数 2026年3月12日"
        n = 5
        
        # Use DuckDuckGo HTML API
        search_url = "https://html.duckduckgo.com/html/"
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                search_url,
                data={"q": query, "b": f"{(n - 1) * 11}"},
                headers={"Accept": "application/json", "User-Agent": USER_AGENT}
            )
            r.raise_for_status()
            print(f"Status code: {r.status_code}")
            print(f"Response length: {len(r.text)}")

        # Parse HTML results
        results = []
        # Match result blocks
        result_pattern = re.compile(r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.+?)</a>.*?<a class="result__snippet"[^>]*>(.+?)</a>', re.DOTALL)
        for match in result_pattern.finditer(r.text):
            url = match.group(1)
            title = _strip_tags(match.group(2))
            snippet = _strip_tags(match.group(3))
            # Skip tracker URLs
            if "uddg=" not in url:
                results.append({"title": title, "url": url, "description": snippet})
            else:
                # Extract actual URL from UDDG parameter
                actual_url = re.search(r'uddg=([^&]+)', url)
                if actual_url:
                    results.append({"title": title, "url": unquote(actual_url.group(1)), "description": snippet})
        
        results = results[:n]
        if not results:
            print(f"No results for: {query}")
        else:
            print(f"Results for: {query}")
            for i, item in enumerate(results, 1):
                print(f"{i}. {item.get('title', '')}")
                print(f"   {item.get('url', '')}")
                if desc := item.get("description"):
                    print(f"   {desc}")
                print()
    except Exception as e:
        print(f"Error: {e}")


async def test_web_fetch():
    """Test web fetch functionality."""
    try:
        url = "https://quote.eastmoney.com/sh/000001.html"
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            r = await client.get(url, headers={"User-Agent": USER_AGENT})
            r.raise_for_status()
            print(f"Status code: {r.status_code}")
            print(f"Response length: {len(r.text)}")
            print(f"Content type: {r.headers.get('content-type', '')}")
            print("\nFirst 500 characters:")
            print(r.text[:500])
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Testing DuckDuckGo search...")
    asyncio.run(test_duckduckgo_search())
    
    print("\nTesting web fetch...")
    asyncio.run(test_web_fetch())