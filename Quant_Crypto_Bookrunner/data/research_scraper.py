from typing import List, Tuple
import arxiv

ARXIV_QUERY = "cryptocurrency market making OR order book dynamics"


def fetch_arxiv_papers(query: str = ARXIV_QUERY, max_results: int = 20) -> List[Tuple[str, str, str]]:
    """Return list of (title, summary, url) for recent arXiv papers matching query."""
    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)
    papers = []
    for result in search.results():
        papers.append((result.title, result.summary, result.entry_id))
    return papers

if __name__ == "__main__":
    for title, _, url in fetch_arxiv_papers(max_results=5):
        print(f"{title} -> {url}")