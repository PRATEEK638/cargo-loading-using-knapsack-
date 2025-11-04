import time


def solve_dp_tabulation(items, capacity):
    """
    Dynamic Programming - Bottom-up Tabulation (0/1 Knapsack)
    Uses 2D table to build solution from bottom up
    Time Complexity: O(n × W)
    Space Complexity: O(n × W)
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
    
    # Create DP table: dp[i][w] = max value using first i items with capacity w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Fill the DP table
    for i in range(1, n + 1):
        item = int_items[i - 1]
        weight = item['weight']
        value = item['value']
        
        for w in range(capacity + 1):
            # Don't include item
            dp[i][w] = dp[i-1][w]
            
            # Include item if possible
            if weight <= w:
                dp[i][w] = max(dp[i][w], value + dp[i-1][w-weight])
    
    # Backtrack to find selected items
    selected_items = []
    steps = []
    w = capacity
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            item = int_items[i-1]
            selected_items.append({
                **item,
                'selected': True,
                'fraction': 1.0
            })
            steps.append({
                'stepNumber': len(steps) + 1,
                'description': f"✓ Selected {item['item']} (Value: ${item['value']}, Weight: {item['weight']})",
                'currentWeight': capacity - w + item['weight'],
                'currentProfit': dp[i][w],
                'decision': 'include'
            })
            w -= item['weight']
    
    selected_items.reverse()
    steps.reverse()
    
    execution_time = (time.perf_counter() - start_time) * 1_000_000  # ✅ CHANGED to microseconds
    
    total_weight = sum(item['weight'] for item in selected_items)
    
    return {
        'maxProfit': round(dp[n][capacity], 2),
        'totalWeight': round(total_weight, 2),
        'selectedItems': selected_items,
        'executionTime': round(execution_time, 2),
        'algorithm': 'dp-tabulation',
        'steps': steps
    }
