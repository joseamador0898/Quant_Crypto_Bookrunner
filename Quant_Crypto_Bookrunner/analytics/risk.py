from typing import Dict


def compute_var(inventory: Dict[str, float], price_map: Dict[str, float], confidence: float = 0.95) -> float:
    """Compute a naive Value-at-Risk assuming independence & normal returns (demo only)."""
    # Placeholder implementation
    exposure = sum(value * price_map.get(asset, 0.0) for asset, value in inventory.items())
    var = exposure * 0.02  # assume 2% daily move at 95% conf
    return var