from typing import List

def min_max_normalise(values: List[float], target_min: float = 0.0, target_max: float = 10.0) -> List[float]:
    """
    Normalises a list of numbers to a target scale (default 0-10).
    If all values are the same, returns the midpoint (5.0).
    """
    if not values:
        return []
    
    val_min = min(values)
    val_max = max(values)
    
    if val_max == val_min:
        return [target_max / 2.0 for _ in values]
    
    normalised = [
        target_min + (v - val_min) * (target_max - target_min) / (val_max - val_min)
        for v in values
    ]
    return normalised
