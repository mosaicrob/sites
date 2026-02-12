# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Portfolio performance tracking and analysis for algorithmic futures trading strategies. Contains TradeStation CSV exports, Excel analysis workbooks, and Python scripts for computing portfolio-level statistics. Strategies trade ES (S&P 500 E-mini) futures.

## Structure

- **`VEGA Returns/`** - VEGA strategy family (4 variants: LE DN, LE UP, SE DN, SE UP). Has its own CLAUDE.md. Contains:
  - Per-strategy TradeStation CSVs (`*NI.csv` = EasyLanguage exports)
  - Python implementation results (`*MAI.xlsx` = trade-level XLSX with 'trades' and 'fills' tabs)
  - Combined monthly returns CSV (2021-2025)
  - Analysis scripts: `analyze_returns.py` (portfolio metrics), `create_comparison.py` (EasyLanguage vs Python validation)
  - Comparison workbooks highlighting trade discrepancies
- **`VECTOR Returns/`** - VECTOR APEX strategy (two contract variants: ES and ES2). TradeStation CSVs plus Excel analysis workbooks.
- **`Data-Extraction/`** - Obsidian vault for project documentation and recommendations.
- **`strategy-returns.xlsx`** - Top-level consolidated workbook across all strategies (9 active strategies + 3 benchmarks).
- **Portfolio Dashboard** (NEW) - Interactive Streamlit web app for custom portfolio analysis:
  - `portfolio_dashboard_v2.py` - Main Streamlit application (SOVRUN branded)
  - `portfolio_calculator.py` - Portfolio calculation logic
  - `chart_generator.py` - Analytics image generation
  - `PORTFOLIO_DASHBOARD_README.md` - Full documentation
- **Quarto Documentation** (NEW) - Comprehensive analytics reports and website:
  - `portfolio_analytics.qmd` - Main analytics report with methodology and examples
  - `index.qmd` - Homepage for Quarto website
  - `_quarto.yml` - Quarto configuration
  - `styles.css` - Custom SOVRUN-themed CSS styling
  - Generates HTML website and PDF reports
- **`.agents/skills/`** - Installed Claude Code skills:
  - `portfolio-optimization` - Python C extensions for high-performance portfolio calculations
  - `portfolio-analyzer` - Financial analysis, risk assessment, asset allocation recommendations
  - `ui-ux-pro-max` - Professional UI/UX design patterns
  - `ai-image-generation` - Analytics visualization generation

## CSV Data Format

All strategy CSVs follow the **TradeStation Performance Summary** format:
- Columns: `All Trades`, `Long Trades`, `Short Trades`
- Sections: Net Profit, Gross Profit/Loss, Profit Factor, Select metrics, Adjusted metrics, Trade counts, Win/Loss stats, Consecutive streaks, Avg bars in trades
- Dollar values formatted as `$1,234.56` or `($1,234.56)` for losses

Monthly returns CSV (`VEGA_Monthly_Returns.csv`) columns: `Month`, `Monthly_PnL`, `Return_%`, `Cumulative_PnL`, `Equity`, `Trades`, `Winners`, `Losers`

## Key Commands

### Portfolio Performance Analysis

```bash
cd "VEGA Returns"
python analyze_returns.py
```

**Dependencies:** `pandas`, `numpy`, `openpyxl`

Reads `VEGA_Monthly_Returns.csv` and 4 strategy CSVs, computes portfolio statistics (CAGR, Sharpe, Sortino, Calmar, max drawdown), outputs `VEGA_Performance_Analysis_Combined.xlsx` with formatted tables and equity curve charts.

**Assumptions:** $1,000,000 initial capital, 0% risk-free rate (hardcoded).

### Strategy Validation (EasyLanguage vs Python)

```bash
cd "VEGA Returns"
python create_comparison.py
```

Compares all 4 VEGA strategies trade-by-trade between EasyLanguage (CSV) and Python (XLSX) implementations. Generates Excel files with:
- Summary statistics comparison (total trades, P&L)
- Green highlighting for matches, red for discrepancies
- Yellow warnings for contract quantity differences
- First 30 trades side-by-side

**Key finding documented:** EasyLanguage uses 10 contracts, Python uses 1 contract, explaining ~10x P&L differences.

### Portfolio Dashboard (Interactive Web App)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Add Python bin to PATH
export PATH="$HOME/Library/Python/3.9/bin:$PATH"

# Run Streamlit dashboard
streamlit run portfolio_dashboard.py
```

**Features:**
- Unit-based strategy selection (e.g., 1 unit GAMMA = $100,000)
- Risk filtering by max drawdown (<5%, <10%, <20%, S&P level)
- Global leverage constraints (100%-300%)
- Calculates Total_Allocation and Required_Equity based on margin_equity factors
- Generates all 12 analytics + monthly return chart
- Exports high-resolution PNG dashboard

**Example Usage:**
- Select 1 unit GAMMA ($100k) + 2 units WAVE2 ($400k)
- Total_Allocation = $500,000
- Required_Equity = $100k×25% + $400k×50% = $225,000
- Effective Leverage = 45%

See `PORTFOLIO_DASHBOARD_README.md` for full documentation.

### Quarto Documentation

```bash
# Render single analytics report
quarto render portfolio_analytics.qmd

# Build full Quarto website (index.qmd + portfolio_analytics.qmd)
quarto render

# Preview website locally
quarto preview
```

**Outputs:**
- HTML website at `_site/` (index.html, portfolio_analytics.html)
- PDF reports when `--to pdf` format is specified
- Includes interactive Python code execution with embedded charts

**Features:**
- Comprehensive methodology documentation
- Live Python code examples using portfolio_calculator.py
- Performance visualizations (cumulative returns, monthly distributions)
- Risk analysis sections (leverage, drawdown, correlation)
- Exports to HTML and PDF formats

**Dependencies:** Requires Quarto CLI installed ([quarto.org](https://quarto.org))

## Data Architecture

### File Naming Conventions
- `*NI.csv` - EasyLanguage strategy results exported from TradeStation
- `*MAI.xlsx` - Python strategy implementation results with trade details
- `*Comparison.xlsx` - Validation workbooks comparing implementations

### Data Flow
1. **Source of Truth:** TradeStation CSVs (`*NI.csv`) contain EasyLanguage performance data
2. **Python Implementation:** Generates `*MAI.xlsx` files with 'trades' and 'fills' tabs
3. **Validation:** `create_comparison.py` compares implementations trade-by-trade
4. **Analysis:** `analyze_returns.py` aggregates monthly data for portfolio-level metrics

### Parsing Notes
- Handle TradeStation CSV format: `($value)` notation for negative numbers
- Monthly return calculation: `Monthly_PnL / Beginning_Equity` (beginning equity = previous month's ending equity)
- Trade parsing: Look for "TradeStation Trades List" section in CSVs; entry lines have trade number in column 0, exit lines have empty column 0
- XLSX trade data: Read from 'trades' tab (columns: trade_id, entry_time, exit_time, entry_price, qty, pnl)
- VECTOR Returns: Has both original `VECTOR_Returns_Analysis.xlsx` and `_CORRECTED` version

## Installed Skills

The following Claude Code skills are available (installed in `.agents/skills/`):

- **portfolio-optimization** - High-performance portfolio calculations using Python C extensions for matrix operations, covariance calculations, risk metrics. Apply when performance speedup is required (≥1.2x) for large datasets.
  - Source: `https://github.com/letta-ai/skills`

- **portfolio-analyzer** - Financial analysis, risk assessment, diversification review, asset allocation recommendations, tax-loss harvesting, rebalancing strategies.
  - Source: `https://github.com/onewave-ai/claude-skills`

- **ui-ux-pro-max** - Professional UI/UX design patterns for creating clean, modern interfaces. Used for portfolio dashboard design.
  - Source: `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`

- **ai-image-generation** - Analytics visualization generation for creating high-quality dashboard images and charts.
  - Source: `https://github.com/inference-sh/skills`

- **pdf** - PDF generation and manipulation. Enables export of portfolio analytics as PDF documents.
  - Source: `https://github.com/anthropics/skills`

- **nano-banana-pro** - AI image generation using Google's Nano Banana Pro (Gemini 3 Pro Image) API. Supports text-to-image generation and image editing with configurable resolution (1K, 2K, 4K). Requires GEMINI_API_KEY.
  - Source: `https://github.com/intellectronica/agent-skills`

- **nano-banana** - Image generation and editing via Gemini CLI's nanobanana extension. Professional image generation for logos, featured images, thumbnails, diagrams, and visual assets. Requires Gemini CLI installed.
  - Source: `https://github.com/kkoppenhaver/cc-nano-banana`

- **ai-avatar-video** - AI avatar video generation for creating professional video content with talking avatars and presentations.
  - Source: `https://github.com/inference-sh/skills`

- **clone-website** - Clone and replicate website structures, layouts, and designs. Useful for analyzing competitor sites or recreating design patterns.
  - Source: `https://github.com/julianromli/ai-skills`

- **premium_web_design** - Professional website templates and modern design systems. Provides pre-built patterns for creating high-quality websites.
  - Source: `https://github.com/jerrar670/surf-website`

- **content-research-writer** - High-quality copywriting and content strategy. Generates professional content with research-backed approaches.
  - Source: `https://github.com/davila7/claude-code-templates`

- **marketing-psychology** - Persuasive design principles and psychological triggers for effective marketing. Applies behavioral psychology to design decisions.
  - Source: `https://github.com/coreyhaines31/marketingskills`

- **roier-seo** - SEO optimization for better search engine visibility. Implements SEO best practices, meta tags, and structured data.
  - Source: `https://github.com/davila7/claude-code-templates`

- **web-performance-optimization** - Page speed optimization and Core Web Vitals improvements. Focuses on performance metrics and user experience.
  - Source: `https://github.com/davila7/claude-code-templates`

### Additional Skills Available

```bash
# Read and write Excel files
npx skills add https://github.com/anthropics/skills --skill xlsx

# Marketing and strategy
npx skills add https://github.com/coreyhaines31/marketingskills --skill marketing-psychology
npx skills add https://github.com/coreyhaines31/marketingskills --skill marketing-ideas
npx skills add https://github.com/coreyhaines31/marketingskills --skill pricing-strategy
```
