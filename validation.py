"""
Input validation service
"""

def validate_items(items):
    """Validate items data structure"""
    if not items or not isinstance(items, list):
        return False, "Items must be a non-empty list"
    
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            return False, f"Item {i+1} must be an object"
        
        if 'item' not in item:
            return False, f"Item {i+1} missing 'item' (name) field"
        
        if 'weight' not in item:
            return False, f"Item {i+1} missing 'weight' field"
        
        if 'value' not in item:
            return False, f"Item {i+1} missing 'value' field"
        
        try:
            weight = float(item['weight'])
            value = float(item['value'])
            
            if weight <= 0:
                return False, f"Item '{item['item']}' has invalid weight (must be > 0)"
            
            if value < 0:
                return False, f"Item '{item['item']}' has invalid value (must be >= 0)"
        
        except (ValueError, TypeError):
            return False, f"Item '{item.get('item', i+1)}' has invalid numeric values"
    
    return True, "Valid"


def validate_capacity(capacity):
    """Validate capacity value"""
    try:
        cap = float(capacity)
        if cap <= 0:
            return False, "Capacity must be greater than 0"
        return True, "Valid"
    except (ValueError, TypeError):
        return False, "Capacity must be a valid number"


def validate_algorithm(algorithm):
    """Validate algorithm selection"""
    valid_algorithms = ['greedy', 'dp-tabulation', 'memoization', 'recursion', 'branch-bound']
    
    if algorithm not in valid_algorithms:
        return False, f"Invalid algorithm. Must be one of: {', '.join(valid_algorithms)}"
    
    return True, "Valid"
