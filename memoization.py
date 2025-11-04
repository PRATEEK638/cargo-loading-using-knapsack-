import time

def solve_memoization(items, capacity):
    """
    Dynamic Programming - Top-down Memoization (0/1 Knapsack)
    Recursive approach with caching
    Time Complexity: O(n × W)
    Space Complexity: O(n × W)
    """
    start_time = time.perf_counter()  # ✅ CHANGED

    n = len(items)
    capacity = int(capacity)
    memo = {}

    # Convert weights to integers
    int_items = []
    for item in items:
        int_items.append({
            **item,
            'weight': int(item['weight'])
        })

    def knapsack(i, w):
        """Recursive function with memoization"""
        if i == 0 or w == 0:
            return 0

        if (i, w) in memo:
            return memo[(i, w)]

        item = int_items[i-1]
        weight = item['weight']
        value = item['value']

        if weight > w:
            # Can't include item
            result = knapsack(i-1, w)
        else:
            # Max of including or excluding item
            result = max(
                value + knapsack(i-1, w-weight),  # Include
                knapsack(i-1, w)                  # Exclude
            )

        memo[(i, w)] = result
        return result

    # Calculate maximum profit
    max_profit = knapsack(n, capacity)

    # Backtrack to find selected items
    selected_items = []
    w = capacity

    for i in range(n, 0, -1):
        if w > 0 and (i, w) in memo and (i-1, w) in memo:
            if memo[(i, w)] != memo[(i-1, w)]:
                item = int_items[i-1]
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
        'algorithm': 'memoization',
        'steps': []
    }
