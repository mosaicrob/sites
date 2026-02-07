# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **financial trading data analysis project** for tracking VEGA trading strategy performance. It contains CSV exports from TradeStation and an Excel workbook for analysis—no executable code.

## File Structure

- **VEGA_Performance_Analysis.xlsx** - Main analysis workbook consolidating all strategy data
- **VEGA_Monthly_Returns.csv** - Monthly P&L, returns %, and cumulative equity (2021-2025)
- **VEGA LE DN NI.csv** - Long Entry Down, No Indicators strategy
- **VEGA LE UP NI.csv** - Long Entry Up, No Indicators strategy
- **VEGA SE DN NI.csv** - Short Entry Down, No Indicators strategy
- **VEGA SE UP NI.csv** - Short Entry Up, No Indicators strategy

## Data Format

CSV files contain TradeStation performance summaries with metrics:
- Net profit (total, select, adjusted)
- Profit factor
- Win rate and trade counts
- Consecutive wins/losses
- Average bars in trades

Monthly returns track: Date, P&L, Return %, Cumulative Equity, Trade Count, Wins/Losses.

## Working with This Project

- Data is exported from TradeStation
- Analysis is spreadsheet-based (no scripts to run)
- When asked to analyze performance, read the CSV files directly
- The Excel workbook provides integrated views but CSVs contain the raw data

## Claude Code Skills

Install these skills to extend Claude Code capabilities:

```bash
# Read and write Excel files
npx skills add https://github.com/anthropics/skills --skill xlsx

# Marketing and strategy
npx skills add https://github.com/coreyhaines31/marketingskills --skill marketing-psychology
npx skills add https://github.com/coreyhaines31/marketingskills --skill marketing-ideas
npx skills add https://github.com/coreyhaines31/marketingskills --skill pricing-strategy

# AI image generation
npx skills add https://github.com/inference-sh/skills --skill ai-image-generation
```
