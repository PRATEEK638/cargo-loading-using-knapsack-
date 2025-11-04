import time


def solve_recursion(items, capacity):
    """
    Pure Recursive Solution (0/1 Knapsack)
    Direct recursive approach without memoization
    Time Complexity: O(2^n)
    Space Complexity: O(n) for recursion stack
    """
    start_time = time.perf_counter()  # ✅ CHANGED
    
    n = len(items)
    capacity = int(capacity)
    
    # Convert weights to integers
    int_items = []
    for item in items:
        int_items.append({
            **item,
            'weight': int(item['weight'])
        })
    
    def knapsack(i, w):
        """Recursive function without memoization"""
        if i == 0 or w == 0:
            return 0
        
        item = int_items[i-1]
        weight = item['weight']
        value = item['value']
        
        if weight > w:
            # Can't include item
            return knapsack(i-1, w)
        else:
            # Max of including or excluding item
            return max(
                value + knapsack(i-1, w-weight),  # Include
                knapsack(i-1, w)                   # Exclude
            )
    
    # Calculate maximum profit
    max_profit = knapsack(n, capacity)
    
    # Backtrack to find selected items (we need to recalculate)
    selected_items = []
    w = capacity
    
    for i in range(n, 0, -1):
        if w > 0:
            item = int_items[i-1]
            without_item = knapsack(i-1, w)
            with_item = item['value'] + knapsack(i-1, w-item['weight']) if item['weight'] <= w else 0
            
            if with_item > without_item:
                selected_items.append({
                    **item,
                    'selected': True,
                    'fraction': 1.0
                })
                w -= item['weight']
    
    selected_items.reverse()
    
    execution_time = (time.perf_counter() - start_time) * 1_000_000  # ✅ CHANGED to microseconds
    
    total_weight = sum(item['weight'] for item in selected_items)
    
    return {
        'maxProfit': round(max_profit, 2),
        'totalWeight': round(total_weight, 2),
        'selectedItems': selected_items,
        'executionTime': round(execution_time, 2),
        'algorithm': 'recursion',
        'steps': []
    }
