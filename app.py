from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import json

# Import algorithms
from algorithms.greedy import solve_greedy
from algorithms.dp_tabulation import solve_dp_tabulation
from algorithms.memoization import solve_memoization
from algorithms.recursion import solve_recursion
from algorithms.branch_bound import solve_branch_bound

# Import services
from services.validation import validate_items, validate_capacity, validate_algorithm
from services.export_service import export_to_json, export_to_csv, export_comparison_to_csv
from services.recommendation import recommend_algorithm

# Import constants
from constants.presets import DATA_PRESETS
from constants.algorithm_metadata import ALGORITHM_METADATA

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Algorithm mapping
ALGORITHMS = {
    'greedy': solve_greedy,
    'dp-tabulation': solve_dp_tabulation,
    'memoization': solve_memoization,
    'recursion': solve_recursion,
    'branch-bound': solve_branch_bound
}


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/solve', methods=['POST'])
def solve():
    """
    Solve knapsack problem with selected algorithm
    Request body: { items: [], capacity: number, algorithm: string }
    """
    try:
        data = request.json
        
        # Extract parameters
        items = data.get('items', [])
        capacity = data.get('capacity', 50)
        algorithm = data.get('algorithm', 'greedy')
        
        # Validate inputs
        valid_items, items_msg = validate_items(items)
        if not valid_items:
            return jsonify({'error': items_msg}), 400
        
        valid_capacity, capacity_msg = validate_capacity(capacity)
        if not valid_capacity:
            return jsonify({'error': capacity_msg}), 400
        
        valid_algo, algo_msg = validate_algorithm(algorithm)
        if not valid_algo:
            return jsonify({'error': algo_msg}), 400
        
        # Solve using selected algorithm
        result = ALGORITHMS[algorithm](items, capacity)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/compare', methods=['POST'])
def compare():
    """
    Compare all algorithms on same dataset
    Request body: { items: [], capacity: number }
    """
    try:
        data = request.json
        items = data.get('items', [])
        capacity = data.get('capacity', 50)
        
        # Validate inputs
        valid_items, items_msg = validate_items(items)
        if not valid_items:
            return jsonify({'error': items_msg}), 400
        
        valid_capacity, capacity_msg = validate_capacity(capacity)
        if not valid_capacity:
            return jsonify({'error': capacity_msg}), 400
        
        # Run all algorithms
        results = []
        for algo_name, algo_func in ALGORITHMS.items():
            try:
                result = algo_func(items, capacity)
                results.append(result)
            except Exception as e:
                results.append({
                    'algorithm': algo_name,
                    'error': str(e),
                    'maxProfit': 0,
                    'totalWeight': 0,
                    'executionTime': 0,
                    'selectedItems': []
                })
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    Get algorithm recommendation based on dataset
    Request body: { items: [], capacity: number }
    """
    try:
        data = request.json
        items = data.get('items', [])
        capacity = data.get('capacity', 50)
        
        # Validate inputs
        valid_items, items_msg = validate_items(items)
        if not valid_items:
            return jsonify({'error': items_msg}), 400
        
        valid_capacity, capacity_msg = validate_capacity(capacity)
        if not valid_capacity:
            return jsonify({'error': capacity_msg}), 400
        
        # Get recommendation
        recommendation = recommend_algorithm(items, capacity)
        
        return jsonify(recommendation)
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/presets', methods=['GET'])
def get_presets():
    """Get all data presets"""
    return jsonify({'presets': DATA_PRESETS})


@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    """Get all algorithm metadata"""
    return jsonify({'algorithms': ALGORITHM_METADATA})


@app.route('/api/export/json', methods=['POST'])
def export_json():
    """
    Export result as JSON
    Request body: { result: {}, includeSteps: boolean }
    """
    try:
        data = request.json
        result = data.get('result', {})
        include_steps = data.get('includeSteps', False)
        
        json_output = export_to_json(result, include_steps)
        
        return Response(
            json_output,
            mimetype='application/json',
            headers={
                'Content-Disposition': 'attachment; filename=knapsack-result.json'
            }
        )
    
    except Exception as e:
        return jsonify({'error': f'Export error: {str(e)}'}), 500


@app.route('/api/export/csv', methods=['POST'])
def export_csv():
    """
    Export result as CSV
    Request body: { result: {} }
    """
    try:
        data = request.json
        result = data.get('result', {})
        
        csv_output = export_to_csv(result)
        
        return Response(
            csv_output,
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=knapsack-result.csv'
            }
        )
    
    except Exception as e:
        return jsonify({'error': f'Export error: {str(e)}'}), 500


@app.route('/api/export/comparison-csv', methods=['POST'])
def export_comparison_csv():
    """
    Export comparison results as CSV
    Request body: { results: [] }
    """
    try:
        data = request.json
        results = data.get('results', [])
        
        csv_output = export_comparison_to_csv(results)
        
        return Response(
            csv_output,
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=algorithm-comparison.csv'
            }
        )
    
    except Exception as e:
        return jsonify({'error': f'Export error: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'API endpoint not found'}), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Cargo Loading Optimizer - Flask Backend")
    print("📊 Starting server on http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
