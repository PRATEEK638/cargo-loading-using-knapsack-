"""
Preset data scenarios for quick testing
"""

DATA_PRESETS = [
    {
        'name': 'Small Delivery',
        'category': 'logistics',
        'difficulty': 'easy',
        'description': 'Light cargo delivery scenario with 3 packages',
        'capacity': 50,
        'items': [
            {'item': 'Package A', 'weight': 10, 'value': 60},
            {'item': 'Package B', 'weight': 20, 'value': 100},
            {'item': 'Package C', 'weight': 30, 'value': 120}
        ]
    },
    {
        'name': 'Cross-Country Freight',
        'category': 'logistics',
        'difficulty': 'medium',
        'description': 'Long-haul trucking optimization with mixed cargo',
        'capacity': 150,
        'items': [
            {'item': 'Electronics', 'weight': 40, 'value': 200},
            {'item': 'Furniture', 'weight': 60, 'value': 180},
            {'item': 'Clothing', 'weight': 25, 'value': 100},
            {'item': 'Books', 'weight': 30, 'value': 90},
            {'item': 'Tools', 'weight': 50, 'value': 150}
        ]
    },
    {
        'name': 'Container Ship Loading',
        'category': 'logistics',
        'difficulty': 'hard',
        'description': 'Large-scale container optimization',
        'capacity': 500,
        'items': [
            {'item': 'Container 1', 'weight': 100, 'value': 500},
            {'item': 'Container 2', 'weight': 150, 'value': 600},
            {'item': 'Container 3', 'weight': 80, 'value': 400},
            {'item': 'Container 4', 'weight': 120, 'value': 550},
            {'item': 'Container 5', 'weight': 90, 'value': 450},
            {'item': 'Container 6', 'weight': 110, 'value': 520},
            {'item': 'Container 7', 'weight': 70, 'value': 350}
        ]
    },
    {
        'name': 'Portfolio Optimization',
        'category': 'finance',
        'difficulty': 'medium',
        'description': 'Investment allocation with budget constraint',
        'capacity': 100000,
        'items': [
            {'item': 'Stock A', 'weight': 20000, 'value': 15000},
            {'item': 'Bond B', 'weight': 30000, 'value': 12000},
            {'item': 'Stock C', 'weight': 25000, 'value': 10000},
            {'item': 'Bond D', 'weight': 15000, 'value': 8000},
            {'item': 'Stock E', 'weight': 35000, 'value': 18000}
        ]
    },
    {
        'name': 'Resource Allocation',
        'category': 'resource-allocation',
        'difficulty': 'medium',
        'description': 'Project resource distribution',
        'capacity': 200,
        'items': [
            {'item': 'Project A', 'weight': 50, 'value': 250},
            {'item': 'Project B', 'weight': 70, 'value': 300},
            {'item': 'Project C', 'weight': 40, 'value': 180},
            {'item': 'Project D', 'weight': 60, 'value': 270},
            {'item': 'Project E', 'weight': 30, 'value': 150}
        ]
    },
    {
        'name': 'Hiking Backpack',
        'category': 'general',
        'difficulty': 'easy',
        'description': 'Pack essential items for a hiking trip',
        'capacity': 15,
        'items': [
            {'item': 'Water Bottle', 'weight': 2, 'value': 10},
            {'item': 'Food', 'weight': 3, 'value': 15},
            {'item': 'First Aid', 'weight': 1, 'value': 12},
            {'item': 'Tent', 'weight': 8, 'value': 20},
            {'item': 'Sleeping Bag', 'weight': 5, 'value': 18}
        ]
    }
]
