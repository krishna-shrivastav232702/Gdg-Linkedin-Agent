"""
Uses external APIs to search the web.
"""

from typing import Literal
import core.config
from tavily import TavilyClient

class SearchEngine:
    def __init__(self, tavily_config: core.config.Tavily):
        self.client = TavilyClient(api_key=tavily_config.api_key)
    def search(
            self,
            query: str,
            search_depth: Literal["basic", "advanced"],
            topic: Literal["web", "news", "finance"],
            num_results: int = 10,
    ) -> list[dict[str, str]]:
        raw_results = self.client.search(
            query=query,
            search_depth=search_depth,
            topic=topic,
            num_results=num_results,
            include_raw_content="markdown"
        ).get("results", [])
        results = []
        for r in raw_results:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("raw_content", ""),
            })
        return results
