from typing import List, Dict
import random

DEFAULT_PARAM_GRID = {
    "spread_bps": [5, 10, 15, 20],
    "inventory_clip": [0.1, 0.2, 0.5],
    "hold_time": [60, 120, 300],
}


def generate_from_research(papers: List[Dict]) -> Dict[str, float]:
    """Very naive strategy parameter generator that random-selects values influenced by num of papers."""
    # In a real pipeline this would parse titles/abstracts for keywords and map to parameters.
    # Here we just adjust spread narrower if many papers mention order book depth or liquidity.
    titles = " ".join(p["title"] for p in papers).lower()
    spread_options = DEFAULT_PARAM_GRID["spread_bps"]
    if "liquidity" in titles or "depth" in titles:
        spread_options = [x for x in spread_options if x <= 10]
    params = {
        "spread_bps": random.choice(spread_options),
        "inventory_clip": random.choice(DEFAULT_PARAM_GRID["inventory_clip"]),
        "hold_time": random.choice(DEFAULT_PARAM_GRID["hold_time"]),
    }
    return params


if __name__ == "__main__":
    sample = [{"title": "Order Book Depth and Liquidity Provision", "summary": "", "url": ""}]
    print(generate_from_research(sample))