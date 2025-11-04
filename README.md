# 🚚 Cargo Loading Optimizer - Flask Edition

> Educational web application for solving cargo loading problems using Knapsack algorithms

## 📋 Features

- **5 Knapsack Algorithms**
  - Greedy Algorithm (O(n log n))
  - DP Tabulation (O(n × W))
  - Memoization (O(n × W))
  - Pure Recursion (O(2^n))
  - Branch & Bound

- **Interactive UI**
  - Add/Edit/Remove items
  - Load preset data scenarios
  - Real-time input validation
  - Algorithm comparison
  - Results visualization

- **Export Functionality**
  - Export to JSON
  - Export to CSV
  - Copy to clipboard

- **Algorithm Recommendation**
  - AI-based algorithm selection
  - Confidence scoring
  - Performance estimation

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

pip install -r requirements.txt

### Step 2: Run the Application

python app.py

### Step 3: Access the Application

Open your browser and navigate to:

http://localhost:5000


## 📂 Project Structure

cargo-optimizer-flask/
├── algorithms/ # Algorithm implementations
├── services/ # Business logic
├── constants/ # Data constants
├── static/ # CSS & JavaScript
├── templates/ # HTML templates
├── app.py # Flask backend
└── requirements.txt # Python dependencies

## 🎯 Usage

1. **Load Preset Data** or **Add Custom Items**
2. **Select an Algorithm**
3. **Click "Solve Problem"**
4. **View Results** with algorithm steps
5. **Compare Algorithms** to see performance differences
6. **Export Results** to JSON or CSV

## 📊 Algorithm Comparison

| Algorithm | Time Complexity | Space | Optimal | Best For |
|-----------|----------------|--------|---------|----------|
| Greedy | O(n log n) | O(1) | No | Fast approximate solutions |
| DP Tabulation | O(n × W) | O(n × W) | Yes | Guaranteed optimal |
| Memoization | O(n × W) | O(n × W) | Yes | Recursive style |
| Pure Recursion | O(2^n) | O(n) | Yes | Educational (small n) |
| Branch & Bound | O(2^n) | O(n) | Yes | Medium datasets |

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS, Vanilla JavaScript
- **Algorithms**: Dynamic Programming, Greedy, Backtracking

## 📝 License

Educational project - free to use and modify

## 🤝 Contributing

Contributions welcome! Feel free to open issues or pull requests.
