"""
Algorithm recommendation service
"""

from constants.algorithm_metadata import ALGORITHM_METADATA


def recommend_algorithm(items, capacity):
    """
    Recommend the best algorithm based on dataset characteristics
    Returns algorithm ID and confidence score
    """
    n = len(items)
    
    # Calculate dataset characteristics
    avg_weight = sum(item['weight'] for item in items) / n if n > 0 else 0
    avg_value = sum(item['value'] for item in items) / n if n > 0 else 0
    
    # Simple recommendation logic
    recommendations = []
    
    # Greedy - fast, good for fractional knapsack
    if capacity > sum(item['weight'] for item in items):
        recommendations.append({
            'algorithm': 'greedy',
            'confidence': 0.85,
            'reason': 'Capacity exceeds total weight - greedy algorithm is optimal for fractional knapsack',
            'estimatedTime': n * 0.01  # Rough estimate in ms
        })
    
    # DP Tabulation - optimal for 0/1 knapsack with reasonable capacity
    if n <= 50 and capacity <= 1000:
        recommendations.append({
            'algorithm': 'dp-tabulation',
            'confidence': 0.95,
            'reason': 'Medium dataset with reasonable capacity - DP tabulation guarantees optimal solution',
            'estimatedTime': n * capacity * 0.001
        })
    
    # Memoization - good alternative to tabulation
    if n <= 40 and capacity <= 500:
        recommendations.append({
            'algorithm': 'memoization',
            'confidence': 0.90,
            'reason': 'Dataset size suitable for memoization with good performance',
            'estimatedTime': n * capacity * 0.0015
        })
    
    # Branch & Bound - good for medium datasets
    if 10 <= n <= 30:
        recommendations.append({
            'algorithm': 'branch-bound',
            'confidence': 0.80,
            'reason': 'Medium dataset where branch & bound can effectively prune search space',
            'estimatedTime': n * 5
        })
    
    # Recursion - only for very small datasets
    if n <= 15:
        recommendations.append({
            'algorithm': 'recursion',
            'confidence': 0.60,
            'reason': 'Small dataset suitable for pure recursion (educational purpose)',
            'estimatedTime': 2 ** n * 0.01
        })
    
    # Default to greedy if no specific recommendation
    if not recommendations:
        recommendations.append({
            'algorithm': 'greedy',
            'confidence': 0.75,
            'reason': 'Default recommendation - fast and practical for large datasets',
            'estimatedTime': n * 0.01
        })
    
    # Sort by confidence
    recommendations.sort(key=lambda x: x['confidence'], reverse=True)
    
    # Return top recommendation with metadata
    top_rec = recommendations[0]
    top_rec['metadata'] = ALGORITHM_METADATA[top_rec['algorithm']]
    
    return top_rec
