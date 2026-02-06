"""
Portfolio Calculator Module
Loads strategy data, filters by risk appetite, and calculates portfolio-level metrics
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_strategy_data(file_path="strategy-returns.xlsx"):
    """
    Load strategy data from Excel file

    Returns:
        dict: Strategy metadata and returns data
            - strategies: list of strategy dicts with metrics
            - monthly_returns: DataFrame with monthly returns
            - stats_df: Raw stats DataFrame
    """
    # Load the Excel file
    xl_file = pd.ExcelFile(file_path)

    # Load Stats sheet
    stats_df = pd.read_excel(xl_file, sheet_name='Stats', header=None)

    # Load Monthly Returns sheet
    monthly_df = pd.read_excel(xl_file, sheet_name='Monthly Returns')

    # Extract metric names from column A (first column)
    metric_names = stats_df.iloc[:, 0].tolist()

    # Map row indices for each metric
    metric_row_map = {
        'total_equity': 1,         # Row 2 in Excel (0-indexed = 1)
        'total_trades': 2,          # Row 3
        'winning_trades': 3,        # Row 4
        'losing_trades': 4,         # Row 5
        'average_winner': 5,        # Row 6
        'average_loser': 6,         # Row 7
        'average_net': 7,           # Row 8
        'max_drawdown': 8,          # Row 9
        'average_year': 9,          # Row 10
        'sharpe_ratio': 10,         # Row 11
        'sortino_ratio': 11,        # Row 12
        'calmar_ratio': 12,         # Row 13
        'margin_equity': 14         # Row 15
    }

    # Extract strategy names from row 1 (header row)
    # Column B onwards are strategies
    strategy_columns = stats_df.iloc[0, 1:].tolist()

    # Build strategy list
    strategies = []
    for col_idx, strategy_name in enumerate(strategy_columns, start=1):
        if pd.isna(strategy_name) or strategy_name == '':
            continue

        strategy = {'name': strategy_name}

        # Extract metrics for this strategy
        for metric_name, row_idx in metric_row_map.items():
            value = stats_df.iloc[row_idx, col_idx]

            # Handle NaN and empty values
            if pd.isna(value):
                strategy[metric_name] = 0
            else:
                strategy[metric_name] = float(value) if isinstance(value, (int, float)) else value

        # Only include strategies with valid total_equity
        if strategy['total_equity'] > 0:
            strategies.append(strategy)

    return {
        'strategies': strategies,
        'monthly_returns': monthly_df,
        'stats_df': stats_df
    }


def get_sp500_drawdown(data):
    """
    Get max drawdown for S&P 500 benchmark

    Args:
        data: dict returned from load_strategy_data()

    Returns:
        float: S&P 500 max drawdown (as decimal, e.g., -0.15 for -15%)
    """
    stats_df = data['stats_df']

    # Find S&P column
    strategy_names = stats_df.iloc[0, 1:].tolist()

    for col_idx, name in enumerate(strategy_names, start=1):
        if name and 'S&P' in str(name) and 'DELTA' not in str(name) and 'GAMMA' not in str(name) and 'VEGA' not in str(name):
            # Found S&P benchmark column
            max_dd_value = stats_df.iloc[8, col_idx]  # Row 9 (0-indexed = 8)
            return float(max_dd_value) if not pd.isna(max_dd_value) else -0.20

    # Default to -20% if S&P not found
    return -0.20


def filter_strategies_by_risk(strategies, risk_appetite, sp500_drawdown=None):
    """
    Filter strategies based on risk appetite (max drawdown threshold)

    Args:
        strategies: list of strategy dicts
        risk_appetite: str - one of:
            - "<5% peak to valley"
            - "<10% peak to valley"
            - "<20% peak to valley"
            - "S&P level"
        sp500_drawdown: float - S&P max drawdown (for "S&P level" option)

    Returns:
        list: Filtered strategies meeting risk criteria
    """
    # Map risk appetite to max_drawdown threshold
    thresholds = {
        "<5% peak to valley": -0.05,
        "<10% peak to valley": -0.10,
        "<20% peak to valley": -0.20,
        "S&P level": sp500_drawdown if sp500_drawdown is not None else -0.20
    }

    threshold = thresholds.get(risk_appetite, -0.20)

    # Filter strategies where max_drawdown >= threshold (less negative = better)
    # e.g., -0.08 is better than -0.15
    filtered = [s for s in strategies if s['max_drawdown'] >= threshold]

    return filtered


def calculate_portfolio_metrics(unit_selections, all_strategies, monthly_returns_df, max_leverage):
    """
    Calculate portfolio-level metrics based on unit selections

    Args:
        unit_selections: dict mapping strategy names to unit counts
            e.g., {"DELTA S&P": 2, "GAMMA S&P": 1}
        all_strategies: list of all strategy dicts
        monthly_returns_df: DataFrame with monthly returns
        max_leverage: int - maximum leverage percentage (100, 150, 200, 300)

    Returns:
        dict: Portfolio metrics
    """
    if not unit_selections:
        raise ValueError("No strategies selected")

    # Build strategy lookup
    strategy_map = {s['name']: s for s in all_strategies}

    # Calculate allocations
    total_allocation = 0
    required_equity = 0
    weighted_metrics = {
        'total_trades': 0,
        'winning_trades': 0,
        'losing_trades': 0,
        'average_winner_sum': 0,
        'average_loser_sum': 0,
        'average_net_sum': 0,
        'average_year_sum': 0,
        'sharpe_sum': 0,
        'sortino_sum': 0,
        'calmar_sum': 0,
    }

    # First pass: calculate allocations
    for strategy_name, units in unit_selections.items():
        if units <= 0:
            continue

        strategy = strategy_map.get(strategy_name)
        if not strategy:
            continue

        allocation = units * strategy['total_equity']
        equity_required = allocation * strategy['margin_equity']

        total_allocation += allocation
        required_equity += equity_required

    # Check leverage constraint
    if total_allocation > 0:
        effective_leverage = required_equity / total_allocation
        max_leverage_decimal = max_leverage / 100.0

        if effective_leverage > max_leverage_decimal:
            raise ValueError(
                f"Leverage constraint violated: {effective_leverage:.1%} exceeds maximum {max_leverage}%"
            )

    # Second pass: calculate weighted metrics
    for strategy_name, units in unit_selections.items():
        if units <= 0:
            continue

        strategy = strategy_map.get(strategy_name)
        if not strategy:
            continue

        allocation = units * strategy['total_equity']
        weight = allocation / total_allocation if total_allocation > 0 else 0

        # Aggregate trade counts
        weighted_metrics['total_trades'] += units * strategy['total_trades']
        weighted_metrics['winning_trades'] += units * strategy['winning_trades']
        weighted_metrics['losing_trades'] += units * strategy['losing_trades']

        # Weighted averages
        weighted_metrics['average_winner_sum'] += weight * strategy['average_winner']
        weighted_metrics['average_loser_sum'] += weight * strategy['average_loser']
        weighted_metrics['average_net_sum'] += weight * strategy['average_net']
        weighted_metrics['average_year_sum'] += weight * strategy['average_year']
        weighted_metrics['sharpe_sum'] += weight * strategy['sharpe_ratio']
        weighted_metrics['sortino_sum'] += weight * strategy['sortino_ratio']
        weighted_metrics['calmar_sum'] += weight * strategy['calmar_ratio']

    # Calculate portfolio max drawdown from monthly returns
    portfolio_max_dd = calculate_portfolio_drawdown(
        unit_selections,
        all_strategies,
        monthly_returns_df,
        total_allocation
    )

    # Build final portfolio metrics
    portfolio = {
        'total_equity': total_allocation,
        'required_equity': required_equity,
        'total_trades': weighted_metrics['total_trades'],
        'winning_trades': weighted_metrics['winning_trades'],
        'losing_trades': weighted_metrics['losing_trades'],
        'average_winner': weighted_metrics['average_winner_sum'],
        'average_loser': weighted_metrics['average_loser_sum'],
        'average_net': weighted_metrics['average_net_sum'],
        'max_drawdown': portfolio_max_dd,
        'average_year': weighted_metrics['average_year_sum'],
        'sharpe_ratio': weighted_metrics['sharpe_sum'],
        'sortino_ratio': weighted_metrics['sortino_sum'],
        'calmar_ratio': weighted_metrics['calmar_sum'],
    }

    return portfolio


def calculate_portfolio_drawdown(unit_selections, all_strategies, monthly_returns_df, total_allocation):
    """
    Calculate portfolio max drawdown from monthly returns

    Args:
        unit_selections: dict mapping strategy names to units
        all_strategies: list of strategy dicts
        monthly_returns_df: DataFrame with monthly returns (DATE, strategy1, strategy2, ...)
        total_allocation: float - total capital allocated

    Returns:
        float: Maximum drawdown (as decimal, e.g., -0.15 for -15%)
    """
    if total_allocation == 0:
        return 0

    # Build strategy lookup
    strategy_map = {s['name']: s for s in all_strategies}

    # Calculate allocation weights
    weights = {}
    for strategy_name, units in unit_selections.items():
        if units <= 0:
            continue
        strategy = strategy_map.get(strategy_name)
        if strategy:
            allocation = units * strategy['total_equity']
            weights[strategy_name] = allocation / total_allocation

    # Calculate portfolio monthly returns
    portfolio_returns = []

    for idx, row in monthly_returns_df.iterrows():
        monthly_return = 0
        for strategy_name, weight in weights.items():
            # Get return for this strategy this month
            if strategy_name in row:
                strategy_return = row[strategy_name]
                if not pd.isna(strategy_return):
                    monthly_return += weight * strategy_return

        portfolio_returns.append(monthly_return)

    # Calculate max drawdown from equity curve
    equity_curve = [1.0]  # Start at 100%

    for ret in portfolio_returns:
        new_equity = equity_curve[-1] * (1 + ret)
        equity_curve.append(new_equity)

    # Calculate running maximum and drawdown
    running_max = equity_curve[0]
    max_drawdown = 0

    for equity in equity_curve:
        running_max = max(running_max, equity)
        if running_max > 0:
            drawdown = (equity - running_max) / running_max
            max_drawdown = min(max_drawdown, drawdown)

    return max_drawdown


def calculate_weighted_returns(unit_selections, all_strategies, monthly_returns_df, total_allocation):
    """
    Calculate portfolio monthly returns for charting

    Args:
        unit_selections: dict mapping strategy names to units
        all_strategies: list of strategy dicts
        monthly_returns_df: DataFrame with monthly returns
        total_allocation: float - total capital allocated

    Returns:
        list: Portfolio monthly returns (as decimals)
    """
    if total_allocation == 0:
        return []

    # Build strategy lookup
    strategy_map = {s['name']: s for s in all_strategies}

    # Calculate allocation weights
    weights = {}
    for strategy_name, units in unit_selections.items():
        if units <= 0:
            continue
        strategy = strategy_map.get(strategy_name)
        if strategy:
            allocation = units * strategy['total_equity']
            weights[strategy_name] = allocation / total_allocation

    # Calculate portfolio monthly returns
    portfolio_returns = []

    for idx, row in monthly_returns_df.iterrows():
        monthly_return = 0
        for strategy_name, weight in weights.items():
            if strategy_name in row:
                strategy_return = row[strategy_name]
                if not pd.isna(strategy_return):
                    monthly_return += weight * strategy_return

        portfolio_returns.append(monthly_return)

    return portfolio_returns
