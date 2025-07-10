from typing import List, Dict
import concurrent.futures
import requests
from .research_scraper import fetch_arxiv_papers

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
CROSSREF_URL = "https://api.crossref.org/works"


def _fetch_semantic_scholar(query: str, limit: int = 50) -> List[Dict]:
    params = {"query": query, "limit": limit, "fields": "title,abstract,url,year"}
    r = requests.get(SEMANTIC_SCHOLAR_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json().get("data", [])
    return [
        {
            "title": p.get("title"),
            "summary": p.get("abstract"),
            "url": p.get("url"),
            "source": "SemanticScholar",
        }
        for p in data
    ]


def _fetch_crossref(query: str, limit: int = 50) -> List[Dict]:
    params = {"query": query, "rows": limit}
    r = requests.get(CROSSREF_URL, params=params, timeout=15)
    r.raise_for_status()
    items = r.json().get("message", {}).get("items", [])
    res = []
    for it in items:
        res.append(
            {
                "title": it.get("title", [""])[0],
                "summary": it.get("abstract", ""),
                "url": it.get("URL"),
                "source": "CrossRef",
            }
        )
    return res


def gather_research(query: str, min_results: int = 120) -> List[Dict]:
    """Fetch research paper metadata from multiple sources until threshold reached."""
    results: List[Dict] = []

    # Prepare tasks
    tasks = [
        (fetch_arxiv_papers, {"query": query, "max_results": 50}),
        (_fetch_semantic_scholar, {"query": query, "limit": 70}),
        (_fetch_crossref, {"query": query, "limit": 70}),
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as pool:
        futures = [pool.submit(func, **kwargs) for func, kwargs in tasks]
        for fut in concurrent.futures.as_completed(futures):
            results.extend(fut.result())
            if len(results) >= min_results:
                break
    return results[:min_results]


if __name__ == "__main__":
    papers = gather_research("crypto market making", min_results=120)
    print(f"Fetched {len(papers)} papers")
    for p in papers[:5]:
        print(f"{p['title']} ({p['source']}) -> {p['url']}")