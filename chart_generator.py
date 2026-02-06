"""
Chart Generator Module
Creates PNG visualization of portfolio analytics and monthly returns
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd


def generate_analytics_image(portfolio, unit_selections, all_strategies, monthly_returns_df, output_dir="."):
    """
    Generate PNG with analytics dashboard and monthly return chart

    Args:
        portfolio: dict with portfolio metrics
        unit_selections: dict mapping strategy names to units
        all_strategies: list of strategy dicts
        monthly_returns_df: DataFrame with monthly returns
        output_dir: str - directory to save image

    Returns:
        str: Path to generated image file
    """
    from portfolio_calculator import calculate_weighted_returns

    # Create figure with subplots - increased height for chart
    fig = plt.figure(figsize=(18, 20))
    gs = fig.add_gridspec(6, 4, hspace=0.4, wspace=0.3, top=0.96, bottom=0.04, left=0.05, right=0.95)

    # Title and summary header
    fig.suptitle('Portfolio Analytics Dashboard', fontsize=24, fontweight='bold', y=0.97)

    # Summary metrics at top
    summary_text = (
        f"Total Allocation: ${portfolio['total_equity']:,.0f}  |  "
        f"Required Equity: ${portfolio['required_equity']:,.0f}  |  "
        f"Effective Leverage: {portfolio['required_equity']/portfolio['total_equity']:.1%}"
    )
    fig.text(0.5, 0.93, summary_text, ha='center', fontsize=12, style='italic', color='#555555')

    # Metrics grid (3 rows × 4 columns) = 12 metrics
    metrics = [
        ("Total Equity", f"${portfolio['total_equity']:,.0f}", 0, 0, '#e3f2fd'),
        ("Total Trades", f"{portfolio['total_trades']:.0f}", 0, 1, '#fff3e0'),
        ("Winning Trades", f"{portfolio['winning_trades']:.0f}", 0, 2, '#e8f5e9'),
        ("Losing Trades", f"{portfolio['losing_trades']:.0f}", 0, 3, '#ffebee'),

        ("Average Winner", f"${portfolio['average_winner']:,.0f}", 1, 0, '#e8f5e9'),
        ("Average Loser", f"${portfolio['average_loser']:,.0f}", 1, 1, '#ffebee'),
        ("Average Net", f"${portfolio['average_net']:,.0f}", 1, 2, '#fff3e0'),
        ("Max Drawdown", f"{portfolio['max_drawdown']:.2%}", 1, 3, '#ffebee'),

        ("Avg Year Return", f"{portfolio['average_year']:.2%}", 2, 0, '#e8f5e9'),
        ("Sharpe Ratio", f"{portfolio['sharpe_ratio']:.3f}", 2, 1, '#e3f2fd'),
        ("Sortino Ratio", f"{portfolio['sortino_ratio']:.3f}", 2, 2, '#e3f2fd'),
        ("Calmar Ratio", f"{portfolio['calmar_ratio']:.3f}", 2, 3, '#e3f2fd'),
    ]

    for label, value, row, col, color in metrics:
        ax = fig.add_subplot(gs[row, col])

        # Add colored box
        rect = mpatches.FancyBboxPatch(
            (0.05, 0.15), 0.9, 0.7,
            boxstyle="round,pad=0.05",
            edgecolor='#cccccc',
            facecolor=color,
            linewidth=1.5
        )
        ax.add_patch(rect)

        # Value (larger font)
        ax.text(0.5, 0.6, value, ha='center', va='center',
                fontsize=20, fontweight='bold', color='#212121')

        # Label (smaller font, gray)
        ax.text(0.5, 0.3, label, ha='center', va='center',
                fontsize=11, color='#666666')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    # Cumulative returns chart (bottom, full width, 2x height)
    ax_chart = fig.add_subplot(gs[3:6, :])

    # Calculate portfolio monthly returns
    portfolio_monthly_returns = calculate_weighted_returns(
        unit_selections,
        all_strategies,
        monthly_returns_df,
        portfolio['total_equity']
    )

    # Get dates from monthly_returns_df
    if 'DATE' in monthly_returns_df.columns:
        dates = pd.to_datetime(monthly_returns_df['DATE'])
    else:
        # Use the first column as dates
        dates = pd.to_datetime(monthly_returns_df.iloc[:, 0])

    # Calculate cumulative returns for portfolio
    cumulative_portfolio = [0]
    for ret in portfolio_monthly_returns:
        cumulative_portfolio.append((1 + cumulative_portfolio[-1]) * (1 + ret) - 1)
    cumulative_portfolio = cumulative_portfolio[1:]  # Remove initial 0

    # Get S&P 500 returns from monthly_returns_df
    sp500_column = None
    for col in monthly_returns_df.columns:
        if 'S&P' in str(col) and 'DELTA' not in str(col) and 'GAMMA' not in str(col) and 'VEGA' not in str(col):
            sp500_column = col
            break

    # Calculate cumulative returns for S&P 500
    cumulative_sp500 = [0]
    if sp500_column and sp500_column in monthly_returns_df.columns:
        sp500_returns = monthly_returns_df[sp500_column].fillna(0).tolist()
        for ret in sp500_returns:
            cumulative_sp500.append((1 + cumulative_sp500[-1]) * (1 + ret) - 1)
        cumulative_sp500 = cumulative_sp500[1:]

    # Plot cumulative returns
    ax_chart.plot(dates, [r * 100 for r in cumulative_portfolio],
                  linewidth=3, color='#4a90e2', label='Portfolio', alpha=0.9)

    if sp500_column and len(cumulative_sp500) == len(dates):
        ax_chart.plot(dates, [r * 100 for r in cumulative_sp500],
                      linewidth=2.5, color='#ff8c42', linestyle='--',
                      label='S&P 500', alpha=0.8)

    ax_chart.axhline(0, color='#666666', linestyle='-', linewidth=1, alpha=0.5)

    # Styling
    ax_chart.set_xlabel('Date', fontsize=13, fontweight='bold', color='#333333')
    ax_chart.set_ylabel('Cumulative Return (%)', fontsize=13, fontweight='bold', color='#333333')
    ax_chart.set_title('Cumulative Returns vs S&P 500', fontsize=16, fontweight='bold', pad=15, color='#1e3a5f')
    ax_chart.grid(True, alpha=0.2, linestyle=':', linewidth=0.8)
    ax_chart.legend(loc='upper left', fontsize=12, framealpha=0.95, edgecolor='#cccccc')

    # Format dates on x-axis
    ax_chart.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax_chart.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.setp(ax_chart.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Set y-axis label format
    ax_chart.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))

    # Set Y-axis starting value based on total equity
    # Start from 0 for cumulative returns (or negative if portfolio has negative returns)
    y_min = min(min(cumulative_portfolio), min(cumulative_sp500) if sp500_column and len(cumulative_sp500) == len(dates) else 0) * 100
    y_max = max(max(cumulative_portfolio), max(cumulative_sp500) if sp500_column and len(cumulative_sp500) == len(dates) else 0) * 100
    ax_chart.set_ylim(y_min - 5, y_max + 10)

    # Set background
    ax_chart.set_facecolor('#fafafa')

    # Calculate required equity rounded up to nearest $100,000
    import math
    required_equity_rounded = math.ceil(portfolio['required_equity'] / 100000) * 100000

    # Add annotation box with Max Drawdown and Average Year Return
    annotation_text = (
        f"Required Equity: ${required_equity_rounded:,.0f}\n"
        f"Max Drawdown: {portfolio['max_drawdown']:.2%}\n"
        f"Avg Year Return: {portfolio['average_year']:.2%}"
    )

    # Add text box in upper right
    props = dict(boxstyle='round,pad=0.8', facecolor='white', edgecolor='#4a90e2', linewidth=2, alpha=0.95)
    ax_chart.text(0.98, 0.97, annotation_text,
                  transform=ax_chart.transAxes,
                  fontsize=11,
                  verticalalignment='top',
                  horizontalalignment='right',
                  bbox=props,
                  fontweight='bold',
                  color='#1e3a5f')

    # Save to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = f"{output_dir}/portfolio_analytics_{timestamp}.png"

    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()

    return output_path


def generate_comparison_chart(portfolio, benchmark_data):
    """
    Generate comparison chart between portfolio and benchmarks

    Args:
        portfolio: dict with portfolio metrics
        benchmark_data: dict with benchmark returns

    Returns:
        str: Path to generated comparison chart
    """
    # Placeholder for future enhancement
    pass
