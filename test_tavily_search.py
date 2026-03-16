#!/usr/bin/env python3
"""Test script to verify web search functionality with Tavily."""

import asyncio
import httpx

# Shared constants
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36"


async def test_tavily_search():
    """Test Tavily search functionality."""
    try:
        query = "上证指数 2026年3月12日"
        count = 5
        api_key = "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"
        
        # Use Tavily API
        search_url = "https://api.tavily.com/search"
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(
                search_url,
                json={
                    "query": query,
                    "api_key": api_key,
                    "search_depth": "basic",
                    "max_results": count
                },
                headers={"User-Agent": USER_AGENT}
            )
            r.raise_for_status()
            print(f"Status code: {r.status_code}")
            data = r.json()
            print(f"Response: {data}")
        
        results = []
        for result in data.get("results", []):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("description", "")
            })
        
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


if __name__ == "__main__":
    print("Testing Tavily search...")
    asyncio.run(test_tavily_search())