# VEGA Returns

Performance tracking and analysis for VEGA trading strategies.

## Strategies

Four strategy variants are tracked, all using "No Indicators" (NI) approach:

| Strategy | Description |
|----------|-------------|
| VEGA LE DN NI | Long Entry, Down direction |
| VEGA LE UP NI | Long Entry, Up direction |
| VEGA SE DN NI | Short Entry, Down direction |
| VEGA SE UP NI | Short Entry, Up direction |

## Files

| File | Contents |
|------|----------|
| `VEGA_Performance_Analysis.xlsx` | Combined analysis workbook |
| `VEGA_Monthly_Returns.csv` | Monthly P&L and cumulative returns (2021-2025) |
| `VEGA LE DN NI.csv` | Long Entry Down performance summary |
| `VEGA LE UP NI.csv` | Long Entry Up performance summary |
| `VEGA SE DN NI.csv` | Short Entry Down performance summary |
| `VEGA SE UP NI.csv` | Short Entry Up performance summary |

## Data Source

Performance data is exported from TradeStation. CSV files contain standard TradeStation performance report metrics including net profit, profit factor, win rate, and trade statistics.

## Monthly Returns Format

| Column | Description |
|--------|-------------|
| Date | Month/Year |
| P&L | Monthly profit/loss |
| Return % | Monthly return percentage |
| Cumulative Equity | Running total equity |
| Trade Count | Number of trades |
| Wins/Losses | Win and loss counts |
