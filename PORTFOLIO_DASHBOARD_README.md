# Portfolio Analytics Dashboard

Interactive web application for analyzing custom trading portfolios with unit-based strategy selection.

## Features

- **Unit-Based Selection**: Select strategies by units (e.g., 1 unit GAMMA = $100,000)
- **Risk Filtering**: Filter strategies by maximum drawdown tolerance
- **Leverage Management**: Global portfolio leverage constraints (100%-300%)
- **Real-Time Calculations**: Instant portfolio metrics computation
- **Visual Analytics**: Professional dashboard with monthly return charts
- **Image Export**: Download high-resolution analytics images

## Quick Start

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Run the Dashboard

```bash
# Add Python bin to PATH
export PATH="$HOME/Library/Python/3.9/bin:$PATH"

# Launch Streamlit
streamlit run portfolio_dashboard.py
```

Or use the full path:

```bash
$HOME/Library/Python/3.9/bin/streamlit run portfolio_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## How to Use

### Step 1: Configure Portfolio Parameters

**In the sidebar:**

1. **Total Investment**: Enter your capital (e.g., $1,000,000)
2. **Maximum Leverage**: Select constraint (100%, 150%, 200%, or 300%)
3. **Risk Appetite**: Choose max drawdown tolerance:
   - `<5% peak to valley` - Ultra-conservative
   - `<10% peak to valley` - Conservative
   - `<20% peak to valley` - Moderate
   - `S&P level` - Match benchmark risk

### Step 2: Select Strategies

For each eligible strategy, enter the number of units:
- **1 unit** = strategy's total_equity (e.g., GAMMA = $100,000/unit)
- **2 units** = 2× the allocation

The dashboard shows each strategy's max drawdown for reference.

### Step 3: Calculate Analytics

Click **"Calculate Portfolio Analytics"** to generate:
- Portfolio-level metrics (12 analytics)
- Monthly return chart
- Downloadable analytics image

## Understanding the Calculations

### Total Allocation vs Required Equity

**Example:** 1 unit GAMMA + 2 units WAVE2

- **Total Allocation** = 1×$100,000 + 2×$200,000 = **$500,000**
- **Required Equity** = ($100,000 × 25%) + ($400,000 × 50%) = **$225,000**
- **Effective Leverage** = $225,000 / $500,000 = **45%**

The `margin_equity` row (row 15 in strategy-returns.xlsx) determines exposure per strategy.

### Portfolio Metrics

**Trade Statistics** (aggregated):
- Total Trades, Winning Trades, Losing Trades
- Average Winner, Average Loser, Average Net

**Risk-Adjusted Returns** (weighted by allocation):
- Sharpe Ratio - Risk-adjusted return
- Sortino Ratio - Downside risk-adjusted return
- Calmar Ratio - Return per unit of drawdown

**Performance**:
- Max Drawdown - Calculated from weighted monthly returns
- Average Year Return - Weighted annual return

## File Structure

```
portfolio-builder/
├── portfolio_dashboard.py       # Main Streamlit app
├── portfolio_calculator.py      # Portfolio calculation logic
├── chart_generator.py           # Image generation module
├── requirements.txt             # Python dependencies
├── strategy-returns.xlsx        # Strategy data (source)
└── portfolio_analytics_*.png    # Generated images
```

## Key Functions

### `portfolio_calculator.py`

- `load_strategy_data()` - Load strategy-returns.xlsx
- `filter_strategies_by_risk()` - Filter by max drawdown
- `calculate_portfolio_metrics()` - Compute all analytics
- `calculate_portfolio_drawdown()` - Portfolio-level drawdown

### `chart_generator.py`

- `generate_analytics_image()` - Create PNG dashboard with:
  - 12 metrics in grid layout
  - Monthly return chart with colored bars
  - Professional formatting

### `portfolio_dashboard.py`

- Streamlit web interface
- Interactive input controls
- Real-time validation
- Image download functionality

## Testing

Run the test suite:

```bash
# Test data loading and filtering
python3 << 'EOF'
from portfolio_calculator import load_strategy_data, filter_strategies_by_risk, get_sp500_drawdown

data = load_strategy_data("strategy-returns.xlsx")
print(f"Loaded {len(data['strategies'])} strategies")

filtered = filter_strategies_by_risk(data['strategies'], "<10% peak to valley", get_sp500_drawdown(data))
print(f"Filtered to {len(filtered)} strategies")
EOF

# Test portfolio calculation
python3 << 'EOF'
from portfolio_calculator import load_strategy_data, calculate_portfolio_metrics

data = load_strategy_data("strategy-returns.xlsx")
portfolio = calculate_portfolio_metrics(
    {"GAMMA S&P": 1, "WAVE2": 2},
    data['strategies'],
    data['monthly_returns'],
    max_leverage=200
)
print(f"Total Allocation: ${portfolio['total_equity']:,.0f}")
print(f"Required Equity: ${portfolio['required_equity']:,.0f}")
EOF

# Test chart generation
python3 << 'EOF'
from portfolio_calculator import load_strategy_data, calculate_portfolio_metrics
from chart_generator import generate_analytics_image

data = load_strategy_data("strategy-returns.xlsx")
portfolio = calculate_portfolio_metrics(
    {"GAMMA S&P": 1, "WAVE2": 2},
    data['strategies'],
    data['monthly_returns'],
    200
)
image_path = generate_analytics_image(portfolio, {"GAMMA S&P": 1, "WAVE2": 2}, data['strategies'], data['monthly_returns'])
print(f"Generated: {image_path}")
EOF
```

## Dependencies

- **streamlit** - Web application framework
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **openpyxl** - Excel file reading
- **matplotlib** - Chart generation
- **plotly** - Interactive visualizations (optional)
- **pillow** - Image processing

## Skills Used

This project leverages two Claude Code skills:

1. **ui-ux-pro-max** - Professional UI/UX design patterns
2. **ai-image-generation** - Analytics visualization generation

Install skills:
```bash
npx skills add https://github.com/nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max
npx skills add https://github.com/inference-sh/skills --skill ai-image-generation
```

## Troubleshooting

### Streamlit not found

```bash
# Add Python bin to PATH
export PATH="$HOME/Library/Python/3.9/bin:$PATH"

# Or use full path
$HOME/Library/Python/3.9/bin/streamlit run portfolio_dashboard.py
```

### ModuleNotFoundError

```bash
pip3 install -r requirements.txt
```

### Data not loading

Ensure `strategy-returns.xlsx` exists in the same directory as the scripts.

### Leverage constraint violated

Reduce the number of units or increase the maximum leverage setting.

## Future Enhancements

- [ ] Historical backtest simulation
- [ ] Monte Carlo risk analysis
- [ ] Correlation matrix visualization
- [ ] Multi-period performance tracking
- [ ] Custom benchmark comparison
- [ ] PDF report generation
- [ ] Strategy recommendation engine

## License

Internal use only - Robot Trading Strategies Portfolio
