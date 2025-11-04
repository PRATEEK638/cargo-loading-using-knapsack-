import time
from queue import PriorityQueue


def solve_branch_bound(items, capacity):
    """
    Branch and Bound algorithm (0/1 Knapsack)
    Intelligent tree search with pruning using bounds
    Time Complexity: O(2^n) worst case, much better average
    Space Complexity: O(n)
    """
    start_time = time.perf_counter()  # ✅ CHANGED
    
    n = len(items)
    capacity = int(capacity)
    
    # Convert weights to integers and calculate ratios
    int_items = []
    for item in items:
        int_item = {
            **item,
            'weight': int(item['weight'])
        }
        if int_item['weight'] > 0:
            int_item['ratio'] = int_item['value'] / int_item['weight']
        else:
            int_item['ratio'] = 0
        int_items.append(int_item)
    
    # Sort by value/weight ratio
    sorted_items = sorted(int_items, key=lambda x: x['ratio'], reverse=True)
    
    class Node:
        def __init__(self, level, profit, weight, bound, items_taken):
            self.level = level
            self.profit = profit
            self.weight = weight
            self.bound = bound
            self.items_taken = items_taken
        
        def __lt__(self, other):
            return self.bound > other.bound  # Max-heap based on bound
    
    def calculate_bound(node):
        """Calculate upper bound of profit in subtree"""
        if node.weight >= capacity:
            return 0
        
        profit_bound = node.profit
        j = node.level + 1
        total_weight = node.weight
        
        # Add items greedily to calculate bound
        while j < n and total_weight + sorted_items[j]['weight'] <= capacity:
            total_weight += sorted_items[j]['weight']
            profit_bound += sorted_items[j]['value']
            j += 1
        
        # Add fractional part of next item
        if j < n:
            profit_bound += (capacity - total_weight) * sorted_items[j]['ratio']
        
        return profit_bound
    
    pq = PriorityQueue()
    root = Node(-1, 0, 0, 0, [])
    root.bound = calculate_bound(root)
    pq.put(root)
    
    max_profit = 0
    best_items = []
    
    while not pq.empty():
        node = pq.get()
        
        if node.bound > max_profit:
            level = node.level + 1
            
            if level < n:
                # Include item
                new_weight = node.weight + sorted_items[level]['weight']
                new_profit = node.profit + sorted_items[level]['value']
                new_items = node.items_taken + [level]
                
                if new_weight <= capacity and new_profit > max_profit:
                    max_profit = new_profit
                    best_items = new_items
                
                new_node = Node(level, new_profit, new_weight, 0, new_items)
                new_node.bound = calculate_bound(new_node)
                
                if new_node.bound > max_profit:
                    pq.put(new_node)
                
                # Exclude item
                new_node = Node(level, node.profit, node.weight, 0, node.items_taken)
                new_node.bound = calculate_bound(new_node)
                
                if new_node.bound > max_profit:
                    pq.put(new_node)
    
    # Reconstruct solution
    selected_items = []
    for idx in best_items:
        selected_items.append({
            **sorted_items[idx],
            'selected': True,
            'fraction': 1.0
        })
    
    execution_time = (time.perf_counter() - start_time) * 1_000_000  # ✅ CHANGED to microseconds
    
    total_weight = sum(item['weight'] for item in selected_items)
    
    return {
        'maxProfit': round(max_profit, 2),
        'totalWeight': round(total_weight, 2),
        'selectedItems': selected_items,
        'executionTime': round(execution_time, 2),
        'algorithm': 'branch-bound',
        'steps': []
    }
