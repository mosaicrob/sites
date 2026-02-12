# Portfolio Builder

Performance tracking and analysis for algorithmic futures trading strategies running on TradeStation.

## Strategies Tracked

| Strategy Family | Variants | Data Range |
|----------------|----------|------------|
| VEGA | LE DN NI, LE UP NI, SE DN NI, SE UP NI | 2021-2025 |
| VECTOR APEX | ES, ES2 | See CSVs |

All strategies trade ES (S&P 500 E-mini) futures.

## Project Structure

```
portfolio-builder/
├── strategy-returns.xlsx           # Consolidated cross-strategy analysis (9 strategies)
├── portfolio_dashboard_v2.py       # 📊 Streamlit web app (SOVRUN branded)
├── portfolio_calculator.py         # Portfolio calculation engine
├── chart_generator.py              # Analytics image generator
├── portfolio_analytics.qmd         # 📄 Quarto analytics report
├── index.qmd                       # Quarto homepage
├── _quarto.yml                     # Quarto configuration
├── styles.css                      # Custom CSS styling
├── requirements.txt                # Python dependencies
├── PORTFOLIO_DASHBOARD_README.md   # Dashboard documentation
├── assets/
│   └── sovrun_logo_pro.svg        # SOVRUN branding logo
├── VEGA Returns/
│   ├── analyze_returns.py          # Performance statistics generator
│   ├── create_comparison.py        # EasyLanguage vs Python validation
│   ├── VEGA_Monthly_Returns.csv    # Combined monthly P&L (2021-2025)
│   ├── VEGA LE DN NI.csv           # EasyLanguage TradeStation exports
│   ├── VEGA LE UP NI.csv
│   ├── VEGA SE DN NI.csv
│   ├── VEGA SE UP NI.csv
│   ├── VEGA LE DN MAI.xlsx         # Python implementation results
│   ├── VEGA LE UP MAI.xlsx
│   ├── VEGA SE DN MAI.xlsx
│   ├── VEGA SE UP MAI.xlsx
│   └── *Comparison.xlsx            # Validation workbooks
├── VECTOR Returns/
│   ├── VECTOR ES.csv
│   ├── VECTOR ES2.csv
│   └── *.xlsx                      # Analysis workbooks
└── Data-Extraction/                # Project documentation (Obsidian vault)
```

## Portfolio Dashboard (NEW)

Interactive Streamlit web application for customizing portfolio allocations and analyzing performance.

### Quick Start

```bash
# Install dependencies
pip3 install -r requirements.txt

# Launch dashboard
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
streamlit run portfolio_dashboard.py
```

Open http://localhost:8501 in your browser.

### Features

- **Unit-Based Selection** - Select strategies by units (e.g., 1 unit GAMMA = $100,000)
- **Risk Filtering** - Filter by max drawdown (<5%, <10%, <20%, S&P level)
- **Leverage Management** - Global constraints (100%-300%)
- **Real-Time Analytics** - All 12 metrics calculated instantly
- **Visual Dashboard** - Monthly returns chart with colored bars
- **Image Export** - Download high-res PNG analytics

### Example

Select: 1 unit GAMMA ($100k) + 2 units WAVE2 ($400k)

Results:
- Total Allocation: $500,000
- Required Equity: $225,000 (considers margin factors)
- Effective Leverage: 45%

See `PORTFOLIO_DASHBOARD_README.md` for full documentation.

## Quarto Documentation (NEW)

Comprehensive analytics report with methodology, examples, and visualizations built with Quarto Markdown.

### Quick Start

```bash
# Install Quarto (if not already installed)
# Visit https://quarto.org/docs/get-started/

# Render single document
quarto render portfolio_analytics.qmd

# Build full website
quarto render

# Preview website locally
quarto preview
```

Open http://localhost:4200 in your browser.

### Features

- **Comprehensive Methodology** - Portfolio construction framework and calculations
- **Interactive Examples** - Python code blocks with live execution
- **Performance Visualizations** - Cumulative returns, monthly distributions, risk metrics
- **Risk Analysis** - Leverage constraints, drawdown monitoring, correlation risk
- **Technical Documentation** - Architecture, data flow, file structure
- **Export Formats** - HTML website, PDF reports

### Output Formats

- **HTML**: Interactive website with navigation, charts, and code folding
- **PDF**: Professional reports with formatted equations and tables

The Quarto documentation integrates with the Streamlit dashboard and provides in-depth analysis using the same `portfolio_calculator.py` engine.

## Analysis Scripts

The `analyze_returns.py` script computes:
- CAGR, monthly/annual standard deviation
- Sharpe, Sortino, and Calmar ratios
- Maximum drawdown (% and $)
- Aggregate trade statistics (win rate, avg winner/loser)

Output is a formatted Excel workbook with monthly returns table, equity curve chart, and monthly returns chart.

### Running

```bash
cd "VEGA Returns"
pip install pandas numpy openpyxl
python analyze_returns.py
```

## Data Source

All CSV data is exported from TradeStation's performance report feature. See each subdirectory's documentation for format details.

## Claude Code Skills

### Installed Skills

The following skills are already installed in `.agents/skills/`:

- ✅ **portfolio-optimization** - High-performance portfolio calculations with Python C extensions
  ```bash
  npx skills add https://github.com/letta-ai/skills --skill portfolio-optimization
  ```

- ✅ **portfolio-analyzer** - Financial analysis, risk assessment, asset allocation recommendations
  ```bash
  npx skills add https://github.com/onewave-ai/claude-skills --skill portfolio-analyzer
  ```

- ✅ **ui-ux-pro-max** - Professional UI/UX design patterns (used for dashboard)
  ```bash
  npx skills add https://github.com/nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max
  ```

- ✅ **ai-image-generation** - Analytics visualization and image generation
  ```bash
  npx skills add https://github.com/inference-sh/skills --skill ai-image-generation
  ```

- ✅ **pdf** - PDF generation and manipulation for exporting analytics
  ```bash
  npx skills add https://github.com/anthropics/skills --skill pdf
  ```

- ✅ **nano-banana-pro** - AI image generation using Gemini 3 Pro Image API (requires GEMINI_API_KEY)
  ```bash
  npx skills add https://github.com/intellectronica/agent-skills --skill nano-banana-pro
  ```

- ✅ **nano-banana** - Professional image generation via Gemini CLI (requires Gemini CLI installed)
  ```bash
  npx skills add https://github.com/kkoppenhaver/cc-nano-banana --skill nano-banana
  ```

- ✅ **ai-avatar-video** - AI avatar video generation for creating professional video content
  ```bash
  npx skills add https://github.com/inference-sh/skills --skill ai-avatar-video
  ```

- ✅ **clone-website** - Clone and replicate website structures and designs
  ```bash
  npx skills add https://github.com/julianromli/ai-skills --skill clone-website
  ```

- ✅ **premium_web_design** - Professional website templates and modern design systems
  ```bash
  npx skills add https://github.com/jerrar670/surf-website --skill premium_web_design
  ```

- ✅ **content-research-writer** - High-quality copywriting and content strategy
  ```bash
  npx skills add https://github.com/davila7/claude-code-templates --skill content-research-writer
  ```

- ✅ **marketing-psychology** - Persuasive design principles and psychological triggers
  ```bash
  npx skills add https://github.com/coreyhaines31/marketingskills --skill marketing-psychology
  ```

- ✅ **roier-seo** - SEO optimization for better search engine visibility
  ```bash
  npx skills add https://github.com/davila7/claude-code-templates --skill roier-seo
  ```

- ✅ **web-performance-optimization** - Page speed optimization and Core Web Vitals
  ```bash
  npx skills add https://github.com/davila7/claude-code-templates --skill web-performance-optimization
  ```

### Additional Skills Available

```bash
# Read and write Excel files
npx skills add https://github.com/anthropics/skills --skill xlsx

# Marketing and strategy
npx skills add https://github.com/coreyhaines31/marketingskills --skill marketing-psychology
npx skills add https://github.com/coreyhaines31/marketingskills --skill marketing-ideas
npx skills add https://github.com/coreyhaines31/marketingskills --skill pricing-strategy
```
