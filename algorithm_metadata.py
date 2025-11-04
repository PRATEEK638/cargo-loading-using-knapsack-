"""
Algorithm metadata - descriptions, complexity, best use cases
"""

ALGORITHM_METADATA = {
    'greedy': {
        'id': 'greedy',
        'name': 'Greedy Algorithm',
        'description': 'Sorts items by value-to-weight ratio and selects greedily. Supports fractional knapsack.',
        'timeComplexity': 'O(n log n)',
        'spaceComplexity': 'O(1)',
        'bestFor': 'Fractional knapsack problems, real-time applications needing fast solutions',
        'worstCase': 'Not optimal for 0/1 knapsack',
        'optimal': False,
        'category': 'greedy'
    },
    'dp-tabulation': {
        'id': 'dp-tabulation',
        'name': 'DP Tabulation',
        'description': 'Bottom-up dynamic programming using a 2D table. Optimal for 0/1 knapsack.',
        'timeComplexity': 'O(n × W)',
        'spaceComplexity': 'O(n × W)',
        'bestFor': 'Large datasets with predictable patterns, guaranteed optimal solution',
        'worstCase': 'High memory usage with large capacity values',
        'optimal': True,
        'category': 'dynamic-programming'
    },
    'memoization': {
        'id': 'memoization',
        'name': 'Memoization (Top-Down DP)',
        'description': 'Recursive approach with caching to avoid recomputation.',
        'timeComplexity': 'O(n × W)',
        'spaceComplexity': 'O(n × W)',
        'bestFor': 'Problems with overlapping subproblems, easier to understand than tabulation',
        'worstCase': 'Stack overflow with very large inputs',
        'optimal': True,
        'category': 'dynamic-programming'
    },
    'recursion': {
        'id': 'recursion',
        'name': 'Pure Recursion',
        'description': 'Naive recursive solution without optimization. Exponential time complexity.',
        'timeComplexity': 'O(2^n)',
        'spaceComplexity': 'O(n)',
        'bestFor': 'Educational purposes, very small datasets (n < 20)',
        'worstCase': 'Impractical for large inputs due to exponential time',
        'optimal': True,
        'category': 'backtracking'
    },
    'branch-bound': {
        'id': 'branch-bound',
        'name': 'Branch & Bound',
        'description': 'Intelligent tree search with pruning using bounds.',
        'timeComplexity': 'O(2^n) worst case, much better average',
        'spaceComplexity': 'O(n)',
        'bestFor': 'Medium-sized problems where pruning significantly reduces search space',
        'worstCase': 'Degrades to exhaustive search in worst case',
        'optimal': True,
        'category': 'backtracking'
    }
}
