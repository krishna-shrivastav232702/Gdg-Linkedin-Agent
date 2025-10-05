import time
import requests
from serpapi import GoogleSearch   
from bs4 import BeautifulSoup
from tqdm import tqdm
from config import SERPAPI_API_KEY

def serp_search(query, num_results=5):
    """
    Use SerpAPI Google Search to fetch top results.
    Returns list of result dicts with title, link, snippet.
    """
    params = {
        "q": query,
        "hl": "en",
        "num": num_results,
        "api_key": SERPAPI_API_KEY,
    }
    search = GoogleSearch(params)
    res = search.get_dict()
    results = []
    organic = res.get("organic_results", [])
    for r in organic[:num_results]:
        results.append({
            "title": r.get("title"),
            "link": r.get("link"),
            "snippet": r.get("snippet")
        })
    return results

def fetch_article_text(url, timeout=8):
    """
    Simple scraper — fetches html and extracts visible text.
    Not perfect but OK for many articles.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.content, "html.parser")

        # Remove script/style
        for tag in soup(["script", "style", "header", "footer", "nav", "aside", "form"]):
            tag.decompose()

        # Try common article containers
        article = soup.find("article")
        if article:
            text = article.get_text(separator="\n").strip()
            if len(text) > 200:
                return text

        # fallback: gather <p> tags
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text().strip() for p in paragraphs)
        return text if len(text) > 100 else None
    except Exception as e:
        # print("fetch error", e)
        return None

def research_topic(topic, num_results=5, fetch_limit=4):
    """
    Run search and fetch top results' text.
    Returns list of sources: {title, link, snippet, content}
    """
    results = serp_search(topic, num_results=num_results)
    sources = []
    count = 0
    for r in results:
        if count >= fetch_limit:
            break
        url = r.get("link")
        txt = fetch_article_text(url)
        if txt:
            sources.append({
                "title": r.get("title"),
                "url": url,
                "snippet": r.get("snippet"),
                "content": txt
            })
            count += 1
        else:
            # keep snippet-only entries (useful)
            sources.append({
                "title": r.get("title"),
                "url": url,
                "snippet": r.get("snippet"),
                "content": None
            })
    return sources
