"""
Export service for generating JSON and CSV outputs
"""

import json
import csv
from io import StringIO


def export_to_json(result, include_steps=False):
    """Export result to JSON format"""
    output = {
        'algorithm': result['algorithm'],
        'maxProfit': result['maxProfit'],
        'totalWeight': result['totalWeight'],
        'executionTime': result['executionTime'],
        'selectedItems': result['selectedItems']
    }
    
    if include_steps and 'steps' in result and result['steps']:
        output['steps'] = result['steps']
    
    return json.dumps(output, indent=2)


def export_to_csv(result):
    """Export selected items to CSV format"""
    output = StringIO()
    
    if not result['selectedItems']:
        return "No items selected"
    
    # Define CSV columns
    fieldnames = ['item', 'weight', 'value', 'selected', 'fraction']
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for item in result['selectedItems']:
        writer.writerow({
            'item': item['item'],
            'weight': item['weight'],
            'value': item['value'],
            'selected': item.get('selected', True),
            'fraction': item.get('fraction', 1.0)
        })
    
    # Add summary row
    output.write(f"\nSummary:\n")
    output.write(f"Algorithm,{result['algorithm']}\n")
    output.write(f"Max Profit,${result['maxProfit']}\n")
    output.write(f"Total Weight,{result['totalWeight']} kg\n")
    output.write(f"Execution Time,{result['executionTime']} ms\n")
    
    return output.getvalue()


def export_comparison_to_csv(results):
    """Export algorithm comparison to CSV"""
    output = StringIO()
    
    fieldnames = ['algorithm', 'maxProfit', 'totalWeight', 'executionTime', 'itemsSelected']
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for result in results:
        writer.writerow({
            'algorithm': result['algorithm'],
            'maxProfit': result['maxProfit'],
            'totalWeight': result['totalWeight'],
            'executionTime': result['executionTime'],
            'itemsSelected': len(result['selectedItems'])
        })
    
    return output.getvalue()
