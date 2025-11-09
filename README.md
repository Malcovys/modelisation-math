# 📊 Mathematical Modeling Application

A **Python web application** built with **Streamlit** for solving linear systems, optimization problems, regression analysis, and simulating stochastic processes.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip

### Installation

```bash
# Clone repository
git clone <repository-url>
cd modelisation-math

# Create and activate virtual environment
python -m venv env
source env/bin/activate  # Linux/Mac
# or
.\env\Scripts\activate   # Windows

# Install dependencies and run
pip install -r requirement.txt
streamlit run main.py
```

Open `http://localhost:8501` in your browser.

---

## 📋 Modules and Features

### 1. **📐 Linear Systems** (`linear_system_page.py`)
Solve systems of linear equations of the form **Ax = b**.

- **Input methods**:
  - ✍️ **Manual entry**: Enter matrix A and vector b directly
- **Supported formats**:
  - Manual: One row per equation, space-separated coefficients
- **Output**:
  - Detailed solutions with values for each variable
  - Determinant calculation

**Example format**:
- Matrix A
   ```
   2 1 -4
   3 3 -5
   4 5 -2
   ```
- Vector b
   ```
   6, 12, 10
   ```

---

### 2. **📊 Linear Programming** (`linear_programming_page.py`)
Solve linear optimization problems (maximize/minimize).

- **Input methods**:
  - 📁 **CSV import**: Recommended for larger problems
  - ✍️ **Manual entry**: For quick calculations
- **Problem types**:
  - Maximization problems
  - Minimization problems
- **Features**:
  - Define objective function coefficients
  - Add constraints
  - Specify resource limits
- **Output**:
  - Optimal solution values
  - Variable assignments
  - Status message
- **Solver**: Uses **PuLP** library for optimization

**Example CSV format**:
```csv
Products,Farine,Eggs,Benefits
Apple pie,2,2,4
Chocolate cake,1,3,5
Available resources,50,60,
```

---

### 3. **📈 Linear Regression** (`linear_regression_page.py`)
Perform linear regression analysis.

- **Input method**:
  - 📁 **CSV import only**: Two columns (X, Y)
- **Calculations**:
  - Regression coefficients (a, b) for equation `y = ax + b`
  - Pearson correlation coefficient
  - Quality assessment (strong/moderate/weak correlation)
- **Visualizations**:
  - Scatter plot of data points
  - Regression line overlay
- **Output**:
  - Regression equation
  - Correlation strength indicator
  - Regression line overlay

**Example CSV format**:
```csv
yield, fertilizer
16, 20
18, 24
23, 28
24, 22
28, 32
```

---

### 4. **🎲 Stochastic Processes** (`stochastic_page.py`)
Simulate and analyze random processes.

- **Markov Chains**:
  - Define transition matrix
  - Set initial probability distribution
  - Simulate evolution over time
  - Visualize state probabilities over time
- **Random Walks**:
  - Define possible states
  - Set probability distribution
  - Generate random trajectories
  - Analyze visit statistics
- **Visualizations**:
  - Line graphs of probability evolution
  - Distribution charts
  - State visit statistics
  - Markov chain diagram with Graphviz

**Example formats**:
- Transition matrix (space-separated):
  ```
  0.7 0.3
  0.4 0.6
  ```
- Initial distribution (comma-separated):
  ```
  1.0, 0.0
  ```

---

## 📊 Data Formats

### Input Methods
| Module | Manual | CSV | SVG |
|--------|--------|-----|-----|
| Linear Systems | ✅ | ❌ | ❌ |
| Linear Programming | ✅ | ✅ | ❌ |
| Linear Regression | ❌ | ✅ | ❌ |
| Stochastic Processes | ✅ | ❌ | ❌ |

### CSV Examples

**Linear Programming**:
```csv
Products,Resource1,Resource2,Objective
Product1,2,3,5
Product2,1,2,4
Available,50,60,
```

**Linear Regression**:
```csv
X,Y
16,20
18,24
23,28
```

### Manual Input Formats
- **Matrix** (space-separated): `0.7 0.3` / `0.4 0.6`
- **Vector** (comma-separated): `1.0, 0.0`
- **Coefficients** (comma-separated): `5, 4`

---

## 📂 Project Structure

```
modelisation-math/
├── main.py                      # Streamlit entry point
├── core/                        # Computational modules
│   ├── linear_system.py
│   ├── linear_programmation.py
│   ├── linear_regression.py
│   └── stochastic_process.py
├── ui/                          # Streamlit UI pages
│   ├── linear_system_page.py
│   ├── linear_programming_page.py
│   ├── linear_regression_page.py
│   └── stochastic_page.py
├── data/                        # Example datasets
│   ├── linear_prog/pastry.csv
│   └── linear_reg/yield_and_fertilizer.csv
└── requirement.txt
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Streamlit | 1.51.0 | Web UI |
| NumPy | 2.3.4 | Computations |
| Pandas | 2.3.3 | Data handling |
| Matplotlib | 3.10.7 | Visualization |
| PuLP | 3.3.0 | Optimization |
| Graphviz | 0.21 | Graph visualization |

See `requirement.txt` for complete list.

---

## 🛠️ Development

### Add New Module

1. Create `core/new_solver.py` with computation functions
2. Create `ui/new_module_page.py` with `show()` function
3. Update `main.py` to import and register the new module

### Error Handling

All modules validate inputs:
- Matrix dimensions
- Probability sums
- CSV format
- Edge cases (zero variance, singular matrices)

---

## 📄 License

Academic project by **[Malcovys](https://github.com/Malcovys)**

---

## 🔗 Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [NumPy Docs](https://numpy.org/doc/)
- [PuLP Docs](https://coin-or.github.io/pulp/)
