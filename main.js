// Global state
let items = [];
let selectedAlgorithm = 'greedy';
let currentResult = null;
let presets = [];
let algorithms = {};


// API Base URL
const API_URL = 'http://localhost:5000/api';


// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadPresets();
    await loadAlgorithms();
    loadDefaultItems();
    renderItems();
});


// Load presets from API
async function loadPresets() {
    try {
        const response = await fetch(`${API_URL}/presets`);
        const data = await response.json();
        presets = data.presets;
        renderPresets();
    } catch (error) {
        console.error('Error loading presets:', error);
        showError('Failed to load presets');
    }
}


// Load algorithm metadata
async function loadAlgorithms() {
    try {
        const response = await fetch(`${API_URL}/algorithms`);
        const data = await response.json();
        algorithms = data.algorithms;
        renderAlgorithms();
    } catch (error) {
        console.error('Error loading algorithms:', error);
        showError('Failed to load algorithms');
    }
}


// Render presets grid
function renderPresets() {
    const grid = document.getElementById('presets-grid');
    grid.innerHTML = '';
    
    presets.forEach(preset => {
        const card = document.createElement('div');
        card.className = 'bg-gray-50 dark:bg-gray-700 rounded-lg p-4 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition';
        card.onclick = () => loadPreset(preset);
        
        const difficultyColors = {
            'easy': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
            'medium': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
            'hard': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
        };
        
        card.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <h3 class="font-semibold text-gray-900 dark:text-white">${preset.name}</h3>
                <span class="text-xs px-2 py-1 rounded ${difficultyColors[preset.difficulty] || 'bg-gray-200'}">${preset.difficulty}</span>
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">${preset.description}</p>
            <div class="text-xs text-gray-500 dark:text-gray-500">
                ${preset.items.length} items • Capacity: ${preset.capacity} kg
            </div>
        `;
        
        grid.appendChild(card);
    });
}


// Load preset data
function loadPreset(preset) {
    items = preset.items.map(item => ({...item}));
    document.getElementById('capacity').value = preset.capacity;
    renderItems();
    showSuccess(`Loaded preset: ${preset.name}`);
}


// Render algorithms grid
function renderAlgorithms() {
    const grid = document.getElementById('algorithm-grid');
    grid.innerHTML = '';
    
    Object.values(algorithms).forEach(algo => {
        const card = document.createElement('div');
        card.className = `algorithm-card bg-white dark:bg-gray-700 rounded-lg p-4 cursor-pointer border-2 ${selectedAlgorithm === algo.id ? 'algorithm-selected' : 'border-gray-200 dark:border-gray-600'}`;
        card.onclick = () => selectAlgorithm(algo.id);
        
        card.innerHTML = `
            <h3 class="font-semibold text-gray-900 dark:text-white mb-2">${algo.name}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">${algo.description}</p>
            <div class="text-xs text-gray-500 dark:text-gray-500">
                <div>Time: ${algo.timeComplexity}</div>
                <div>Space: ${algo.spaceComplexity}</div>
            </div>
        `;
        
        grid.appendChild(card);
    });
}


// Select algorithm
function selectAlgorithm(algorithmId) {
    selectedAlgorithm = algorithmId;
    renderAlgorithms();
}


// Load default items
function loadDefaultItems() {
    items = [
        { item: 'Package A', weight: 10, value: 60 },
        { item: 'Package B', weight: 20, value: 100 },
        { item: 'Package C', weight: 30, value: 120 }
    ];
}


// Render items table
function renderItems() {
    const tbody = document.getElementById('items-tbody');
    tbody.innerHTML = '';
    
    items.forEach((item, index) => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50 dark:hover:bg-gray-700';
        row.innerHTML = `
            <td class="px-4 py-2">
                <input 
                    type="text" 
                    value="${item.item}" 
                    onchange="updateItem(${index}, 'item', this.value)"
                    class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded dark:bg-gray-700 dark:text-white"
                >
            </td>
            <td class="px-4 py-2">
                <input 
                    type="number" 
                    value="${item.weight}" 
                    onchange="updateItem(${index}, 'weight', parseFloat(this.value))"
                    min="0.1"
                    step="0.1"
                    class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded dark:bg-gray-700 dark:text-white"
                >
            </td>
            <td class="px-4 py-2">
                <input 
                    type="number" 
                    value="${item.value}" 
                    onchange="updateItem(${index}, 'value', parseFloat(this.value))"
                    min="0"
                    step="1"
                    class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded dark:bg-gray-700 dark:text-white"
                >
            </td>
            <td class="px-4 py-2">
                <button 
                    onclick="removeItem(${index})" 
                    class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm transition"
                >
                    Remove
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
    
    document.getElementById('items-count').textContent = `${items.length} items added`;
}


// Add new item
function addItem() {
    items.push({
        item: `Item ${items.length + 1}`,
        weight: 10,
        value: 50
    });
    renderItems();
}


// Update item
function updateItem(index, field, value) {
    items[index][field] = value;
}


// Remove item
function removeItem(index) {
    items.splice(index, 1);
    renderItems();
}


// Clear all items
function clearItems() {
    if (confirm('Are you sure you want to clear all items?')) {
        items = [];
        renderItems();
    }
}


// Solve knapsack problem
async function solveKnapsack() {
    if (items.length === 0) {
        showError('Please add at least one item');
        return;
    }
    
    const capacity = parseFloat(document.getElementById('capacity').value);
    
    if (capacity <= 0) {
        showError('Capacity must be greater than 0');
        return;
    }
    
    showLoading(true);
    hideResults();
    
    try {
        // Get recommendation first
        const recResponse = await fetch(`${API_URL}/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items, capacity })
        });
        
        const recommendation = await recResponse.json();
        displayRecommendation(recommendation);
        
        // Solve with selected algorithm
        const response = await fetch(`${API_URL}/solve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                items,
                capacity,
                algorithm: selectedAlgorithm
            })
        });
        
        const result = await response.json();
        
        if (result.error) {
            showError(result.error);
            return;
        }
        
        currentResult = result;
        displayResults(result);
        showSuccess('Solution computed successfully!');
        
    } catch (error) {
        console.error('Error solving:', error);
        showError('Failed to solve problem. Please try again.');
    } finally {
        showLoading(false);
    }
}


// Compare all algorithms
async function compareAlgorithms() {
    if (items.length === 0) {
        showError('Please add at least one item');
        return;
    }
    
    const capacity = parseFloat(document.getElementById('capacity').value);
    
    if (capacity <= 0) {
        showError('Capacity must be greater than 0');
        return;
    }
    
    showLoading(true);
    hideResults();
    
    try {
        const response = await fetch(`${API_URL}/compare`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items, capacity })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        displayComparison(data.results);
        showSuccess('Algorithm comparison completed!');
        
    } catch (error) {
        console.error('Error comparing:', error);
        showError('Failed to compare algorithms');
    } finally {
        showLoading(false);
    }
}


// Display recommendation
function displayRecommendation(recommendation) {
    const section = document.getElementById('recommendation-section');
    const content = document.getElementById('recommendation-content');
    
    const confidencePercent = Math.round(recommendation.confidence * 100);
    const confidenceColor = confidencePercent >= 80 ? 'text-green-600 dark:text-green-400' : confidencePercent >= 60 ? 'text-yellow-600 dark:text-yellow-400' : 'text-red-600 dark:text-red-400';
    
    content.innerHTML = `
        <div class="space-y-3">
            <div class="flex items-center justify-between">
                <div>
                    <h4 class="text-lg font-bold text-blue-900 dark:text-blue-100">${recommendation.metadata.name}</h4>
                    <p class="text-sm text-blue-700 dark:text-blue-300">${recommendation.reason}</p>
                </div>
                <div class="text-right">
                    <div class="text-2xl font-bold ${confidenceColor}">${confidencePercent}%</div>
                    <div class="text-xs text-blue-600 dark:text-blue-400">Confidence</div>
                </div>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm">
                <div class="bg-blue-100 dark:bg-blue-800 p-2 rounded">
                    <div class="font-semibold text-blue-900 dark:text-blue-100">Time Complexity</div>
                    <div class="text-blue-700 dark:text-blue-300">${recommendation.metadata.timeComplexity}</div>
                </div>
                <div class="bg-blue-100 dark:bg-blue-800 p-2 rounded">
                    <div class="font-semibold text-blue-900 dark:text-blue-100">Est. Time</div>
                    <div class="text-blue-700 dark:text-blue-300">~${recommendation.estimatedTime.toFixed(2)} µs</div>
                </div>
            </div>
        </div>
    `;
    
    section.classList.remove('hidden');
}


// Display results
function displayResults(result) {
    const section = document.getElementById('results-section');
    const content = document.getElementById('results-content');
    
    const algoInfo = algorithms[result.algorithm];
    
    let stepsHtml = '';
    if (result.steps && result.steps.length > 0) {
        stepsHtml = `
            <div class="mt-6">
                <h3 class="text-lg font-semibold mb-3 text-gray-900 dark:text-white">Algorithm Steps</h3>
                <div class="space-y-2">
                    ${result.steps.map(step => `
                        <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
                            <div class="flex items-start gap-3">
                                <span class="bg-blue-600 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0">${step.stepNumber}</span>
                                <div class="flex-1">
                                    <p class="text-sm text-gray-900 dark:text-white">${step.description}</p>
                                    <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                                        Weight: ${step.currentWeight} kg | Profit: $${step.currentProfit}
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    content.innerHTML = `
        <div class="space-y-6">
            <!-- Summary Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-green-50 dark:bg-green-900 p-4 rounded-lg border-2 border-green-200 dark:border-green-700">
                    <div class="text-sm text-green-600 dark:text-green-400 font-semibold">Max Profit</div>
                    <div class="text-3xl font-bold text-green-900 dark:text-green-100">$${result.maxProfit}</div>
                </div>
                <div class="bg-blue-50 dark:bg-blue-900 p-4 rounded-lg border-2 border-blue-200 dark:border-blue-700">
                    <div class="text-sm text-blue-600 dark:text-blue-400 font-semibold">Total Weight</div>
                    <div class="text-3xl font-bold text-blue-900 dark:text-blue-100">${result.totalWeight} kg</div>
                </div>
                <div class="bg-purple-50 dark:bg-purple-900 p-4 rounded-lg border-2 border-purple-200 dark:border-purple-700">
                    <div class="text-sm text-purple-600 dark:text-purple-400 font-semibold">Execution Time</div>
                    <div class="text-3xl font-bold text-purple-900 dark:text-purple-100">${result.executionTime} µs</div>
                </div>
            </div>


            <!-- Algorithm Info -->
            <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                <h3 class="font-semibold text-gray-900 dark:text-white mb-2">${algoInfo.name}</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">${algoInfo.description}</p>
                <div class="flex gap-4 text-sm text-gray-500 dark:text-gray-500">
                    <span>Time: ${algoInfo.timeComplexity}</span>
                    <span>Space: ${algoInfo.spaceComplexity}</span>
                </div>
            </div>


            <!-- Selected Items -->
            <div>
                <h3 class="text-lg font-semibold mb-3 text-gray-900 dark:text-white">Selected Items</h3>
                <div class="overflow-x-auto">
                    <table class="w-full border-collapse">
                        <thead>
                            <tr class="bg-gray-100 dark:bg-gray-700">
                                <th class="px-4 py-2 text-left text-gray-700 dark:text-gray-300">Item</th>
                                <th class="px-4 py-2 text-left text-gray-700 dark:text-gray-300">Weight (kg)</th>
                                <th class="px-4 py-2 text-left text-gray-700 dark:text-gray-300">Value ($)</th>
                                <th class="px-4 py-2 text-left text-gray-700 dark:text-gray-300">Fraction</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${result.selectedItems.map(item => `
                                <tr class="border-t border-gray-200 dark:border-gray-600">
                                    <td class="px-4 py-2 text-gray-900 dark:text-white">${item.item}</td>
                                    <td class="px-4 py-2 text-gray-900 dark:text-white">${item.weight}</td>
                                    <td class="px-4 py-2 text-gray-900 dark:text-white">${item.value}</td>
                                    <td class="px-4 py-2">
                                        <span class="badge ${item.fraction === 1 ? 'badge-success' : 'badge-warning'}">
                                            ${(item.fraction * 100).toFixed(0)}%
                                        </span>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>


            ${stepsHtml}
        </div>
    `;
    
    section.classList.remove('hidden');
    section.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Render charts
    renderResultCharts(result);
}


// Display comparison
function displayComparison(results) {
    const section = document.getElementById('comparison-section');
    const content = document.getElementById('comparison-content');
    
    // Find best performers
    const fastest = results.reduce((prev, curr) => prev.executionTime < curr.executionTime ? prev : curr);
    const mostProfit = results.reduce((prev, curr) => prev.maxProfit > curr.maxProfit ? prev : curr);
    
    content.innerHTML = `
        <div class="space-y-6">
            <!-- Summary -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-purple-50 dark:bg-purple-900 p-4 rounded-lg border-2 border-purple-200 dark:border-purple-700">
                    <div class="text-sm text-purple-600 dark:text-purple-400 font-semibold">⚡ Fastest Algorithm</div>
                    <div class="text-xl font-bold text-purple-900 dark:text-purple-100">${algorithms[fastest.algorithm].name}</div>
                    <div class="text-sm text-purple-700 dark:text-purple-300">${fastest.executionTime} µs</div>
                </div>
                <div class="bg-green-50 dark:bg-green-900 p-4 rounded-lg border-2 border-green-200 dark:border-green-700">
                    <div class="text-sm text-green-600 dark:text-green-400 font-semibold">💰 Most Profitable</div>
                    <div class="text-xl font-bold text-green-900 dark:text-green-100">${algorithms[mostProfit.algorithm].name}</div>
                    <div class="text-sm text-green-700 dark:text-green-300">$${mostProfit.maxProfit}</div>
                </div>
            </div>


            <!-- Comparison Table -->
            <div class="overflow-x-auto">
                <table class="w-full border-collapse">
                    <thead>
                        <tr class="bg-gray-100 dark:bg-gray-700">
                            <th class="px-4 py-2 text-left text-gray-700 dark:text-gray-300">Algorithm</th>
                            <th class="px-4 py-2 text-left text-gray-700 dark:text-gray-300">Max Profit</th>
                            <th class="px-4 py-2 text-left text-gray-700 dark:text-gray-300">Total Weight</th>
                            <th class="px-4 py-2 text-left text-gray-700 dark:text-gray-300">Items Selected</th>
                            <th class="px-4 py-2 text-left text-gray-700 dark:text-gray-300">Execution Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${results.map(result => `
                            <tr class="border-t border-gray-200 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700">
                                <td class="px-4 py-2">
                                    <div class="font-semibold text-gray-900 dark:text-white">${algorithms[result.algorithm].name}</div>
                                    <div class="text-xs text-gray-500 dark:text-gray-400">${algorithms[result.algorithm].timeComplexity}</div>
                                </td>
                                <td class="px-4 py-2 text-gray-900 dark:text-white font-semibold">
                                    $${result.maxProfit}
                                    ${result.algorithm === mostProfit.algorithm ? '<span class="ml-2 text-green-600">🏆</span>' : ''}
                                </td>
                                <td class="px-4 py-2 text-gray-900 dark:text-white">${result.totalWeight} kg</td>
                                <td class="px-4 py-2 text-gray-900 dark:text-white">${result.selectedItems.length}</td>
                                <td class="px-4 py-2 text-gray-900 dark:text-white">
                                    ${result.executionTime} µs
                                    ${result.algorithm === fastest.algorithm ? '<span class="ml-2 text-purple-600">⚡</span>' : ''}
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    section.classList.remove('hidden');
    section.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Render comparison charts
    renderComparisonCharts(results);
}


// Export to JSON
async function exportJSON() {
    if (!currentResult) {
        showError('No results to export');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/export/json`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                result: currentResult, 
                includeSteps: true 
            })
        });
        
        const blob = await response.blob();
        downloadFile(blob, 'knapsack-result.json');
        showSuccess('Exported to JSON successfully!');
    } catch (error) {
        console.error('Export error:', error);
        showError('Failed to export JSON');
    }
}


// Export to CSV
async function exportCSV() {
    if (!currentResult) {
        showError('No results to export');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/export/csv`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ result: currentResult })
        });
        
        const blob = await response.blob();
        downloadFile(blob, 'knapsack-result.csv');
        showSuccess('Exported to CSV successfully!');
    } catch (error) {
        console.error('Export error:', error);
        showError('Failed to export CSV');
    }
}


// Download file helper
function downloadFile(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}


// Show/hide loading
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}


// Hide results
function hideResults() {
    document.getElementById('results-section').classList.add('hidden');
    document.getElementById('comparison-section').classList.add('hidden');
    document.getElementById('recommendation-section').classList.add('hidden');
    document.getElementById('charts-section').classList.add('hidden');
    document.getElementById('comparison-charts').classList.add('hidden');
    
    // Destroy existing charts
    if (valueChart) { valueChart.destroy(); valueChart = null; }
    if (weightChart) { weightChart.destroy(); weightChart = null; }
    if (timeComparisonChart) { timeComparisonChart.destroy(); timeComparisonChart = null; }
    if (profitComparisonChart) { profitComparisonChart.destroy(); profitComparisonChart = null; }
}


// Show success message
function showSuccess(message) {
    showToast(message, 'success');
}


// Show error message
function showError(message) {
    showToast(message, 'error');
}


// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    const bgColor = type === 'success' ? 'bg-green-600' : type === 'error' ? 'bg-red-600' : 'bg-blue-600';
    
    toast.className = `fixed bottom-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 fade-in`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}


// ============================================
// CHART.JS VISUALIZATION FUNCTIONS
// ============================================


let valueChart = null;
let weightChart = null;
let timeComparisonChart = null;
let profitComparisonChart = null;


// Render charts for single result
function renderResultCharts(result) {
    const chartsSection = document.getElementById('charts-section');
    chartsSection.classList.remove('hidden');
    
    // Destroy existing charts
    if (valueChart) valueChart.destroy();
    if (weightChart) weightChart.destroy();
    
    // Value Distribution Chart (Doughnut)
    const valueCtx = document.getElementById('valueChart').getContext('2d');
    const valueData = result.selectedItems.map(item => item.value * (item.fraction || 1));
    const valueLabels = result.selectedItems.map(item => item.item);
    
    valueChart = new Chart(valueCtx, {
        type: 'doughnut',
        data: {
            labels: valueLabels,
            datasets: [{
                data: valueData,
                backgroundColor: [
                    '#3b82f6', // blue
                    '#10b981', // green
                    '#f59e0b', // yellow
                    '#ef4444', // red
                    '#8b5cf6', // purple
                    '#ec4899', // pink
                    '#14b8a6', // teal
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#1f2937',
                        padding: 10,
                        font: {
                            size: 11
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': $' + context.parsed.toFixed(2);
                        }
                    }
                }
            }
        }
    });
    
    // Weight Distribution Chart (Bar)
    const weightCtx = document.getElementById('weightChart').getContext('2d');
    const weightData = result.selectedItems.map(item => item.weight * (item.fraction || 1));
    const weightLabels = result.selectedItems.map(item => item.item);
    
    weightChart = new Chart(weightCtx, {
        type: 'bar',
        data: {
            labels: weightLabels,
            datasets: [{
                label: 'Weight (kg)',
                data: weightData,
                backgroundColor: '#10b981',
                borderColor: '#059669',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#1f2937'
                    },
                    grid: {
                        color: document.documentElement.classList.contains('dark') ? '#374151' : '#e5e7eb'
                    }
                },
                x: {
                    ticks: {
                        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#1f2937'
                    },
                    grid: {
                        color: document.documentElement.classList.contains('dark') ? '#374151' : '#e5e7eb'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Weight: ' + context.parsed.y.toFixed(2) + ' kg';
                        }
                    }
                }
            }
        }
    });
}


// Render comparison charts
function renderComparisonCharts(results) {
    const chartsSection = document.getElementById('comparison-charts');
    chartsSection.classList.remove('hidden');
    
    // Destroy existing charts
    if (timeComparisonChart) timeComparisonChart.destroy();
    if (profitComparisonChart) profitComparisonChart.destroy();
    
    const algoNames = results.map(r => algorithms[r.algorithm].name);
    const executionTimes = results.map(r => r.executionTime);
    const profits = results.map(r => r.maxProfit);
    
    // Execution Time Comparison (Bar)
    const timeCtx = document.getElementById('timeComparisonChart').getContext('2d');
    
    timeComparisonChart = new Chart(timeCtx, {
        type: 'bar',
        data: {
            labels: algoNames,
            datasets: [{
                label: 'Execution Time (µs)',
                data: executionTimes,
                backgroundColor: [
                    '#3b82f6',
                    '#10b981',
                    '#f59e0b',
                    '#ef4444',
                    '#8b5cf6'
                ],
                borderColor: [
                    '#2563eb',
                    '#059669',
                    '#d97706',
                    '#dc2626',
                    '#7c3aed'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#1f2937'
                    },
                    grid: {
                        color: document.documentElement.classList.contains('dark') ? '#374151' : '#e5e7eb'
                    }
                },
                x: {
                    ticks: {
                        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#1f2937',
                        font: {
                            size: 10
                        }
                    },
                    grid: {
                        color: document.documentElement.classList.contains('dark') ? '#374151' : '#e5e7eb'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
    
    // Profit Comparison (Horizontal Bar)
    const profitCtx = document.getElementById('profitComparisonChart').getContext('2d');
    
    profitComparisonChart = new Chart(profitCtx, {
        type: 'bar',
        data: {
            labels: algoNames,
            datasets: [{
                label: 'Max Profit ($)',
                data: profits,
                backgroundColor: [
                    '#10b981',
                    '#3b82f6',
                    '#f59e0b',
                    '#ef4444',
                    '#8b5cf6'
                ],
                borderColor: [
                    '#059669',
                    '#2563eb',
                    '#d97706',
                    '#dc2626',
                    '#7c3aed'
                ],
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#1f2937'
                    },
                    grid: {
                        color: document.documentElement.classList.contains('dark') ? '#374151' : '#e5e7eb'
                    }
                },
                y: {
                    ticks: {
                        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#1f2937',
                        font: {
                            size: 10
                        }
                    },
                    grid: {
                        color: document.documentElement.classList.contains('dark') ? '#374151' : '#e5e7eb'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}
