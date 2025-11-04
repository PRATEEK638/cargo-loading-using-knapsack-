import time


def solve_greedy(items, capacity):
    """
    Greedy Algorithm for Fractional Knapsack
    Sorts items by value/weight ratio and selects greedily
    Time Complexity: O(n log n)
    """
    start_time = time.perf_counter()  # ✅ CHANGED
    
    # Calculate value-to-weight ratio for each item
    for item in items:
        if item['weight'] > 0:
            item['ratio'] = item['value'] / item['weight']
        else:
            item['ratio'] = 0
    
    # Sort by ratio in descending order
    sorted_items = sorted(items, key=lambda x: x['ratio'], reverse=True)
    
    total_weight = 0
    total_value = 0
    selected_items = []
    steps = []
    
    # Select items greedily
    for i, item in enumerate(sorted_items):
        if total_weight + item['weight'] <= capacity:
            # Include full item
            total_weight += item['weight']
            total_value += item['value']
            selected_items.append({
                **item,
                'selected': True,
                'fraction': 1.0
            })
            steps.append({
                'stepNumber': i + 1,
                'description': f"✓ Including {item['item']} (Weight: {item['weight']}, Value: ${item['value']}, Ratio: {item['ratio']:.2f})",
                'currentWeight': total_weight,
                'currentProfit': total_value,
                'decision': 'include'
            })
        elif total_weight < capacity:
            # Fractional knapsack - include partial item
            remaining_capacity = capacity - total_weight
            fraction = remaining_capacity / item['weight']
            partial_value = item['value'] * fraction
            
            total_value += partial_value
            total_weight = capacity
            
            selected_items.append({
                **item,
                'selected': True,
                'fraction': fraction
            })
            steps.append({
                'stepNumber': i + 1,
                'description': f"⚡ Partially including {item['item']} ({fraction*100:.0f}% of item)",
                'currentWeight': total_weight,
                'currentProfit': total_value,
                'decision': 'partial'
            })
            break
        else:
            # Skip item
            steps.append({
                'stepNumber': i + 1,
                'description': f"✗ Skipping {item['item']} (exceeds capacity)",
                'currentWeight': total_weight,
                'currentProfit': total_value,
                'decision': 'skip'
            })
    
    execution_time = (time.perf_counter() - start_time) * 1_000_000  # ✅ CHANGED to microseconds (µs)
    
    return {
        'maxProfit': round(total_value, 2),
        'totalWeight': round(total_weight, 2),
        'selectedItems': selected_items,
        'executionTime': round(execution_time, 2),
        'algorithm': 'greedy',
        'steps': steps
    }
