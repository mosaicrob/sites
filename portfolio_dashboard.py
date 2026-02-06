"""
Portfolio Analytics Dashboard
Streamlit web application for portfolio analysis and visualization
"""

import streamlit as st
import pandas as pd
from portfolio_calculator import (
    load_strategy_data,
    get_sp500_drawdown,
    filter_strategies_by_risk,
    calculate_portfolio_metrics
)
from chart_generator import generate_analytics_image


# Page configuration
st.set_page_config(
    page_title="Portfolio Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1976d2;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1976d2;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">📊 Portfolio Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Customize your trading portfolio and analyze performance metrics</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar Inputs
st.sidebar.header("⚙️ Portfolio Configuration")
st.sidebar.markdown("Configure your portfolio parameters below:")

# Load strategy data
try:
    data = load_strategy_data("strategy-returns.xlsx")
    all_strategies = data['strategies']
    monthly_returns = data['monthly_returns']
    sp500_dd = get_sp500_drawdown(data)

    st.sidebar.success(f"✅ Loaded {len(all_strategies)} strategies")

except Exception as e:
    st.error(f"Error loading strategy data: {e}")
    st.stop()

# Input 1: Total Investment
st.sidebar.markdown("### 💰 Investment Amount")
total_investment = st.sidebar.number_input(
    "Total Investment ($)",
    min_value=10000,
    max_value=100000000,
    value=1000000,
    step=50000,
    help="Total capital to allocate across strategies"
)

# Input 2: Maximum Leverage
st.sidebar.markdown("### ⚖️ Leverage Constraint")
max_leverage = st.sidebar.selectbox(
    "Maximum Leverage",
    options=[100, 150, 200, 300],
    format_func=lambda x: f"{x}%",
    help="Maximum portfolio-level leverage allowed (cross margining)"
)

# Input 3: Risk Appetite
st.sidebar.markdown("### 🎯 Risk Tolerance")
risk_appetite = st.sidebar.selectbox(
    "Risk Appetite (Max Drawdown)",
    options=["<5% peak to valley", "<10% peak to valley", "<20% peak to valley", "S&P level"],
    index=1,  # Default to <10%
    help="Filter strategies by maximum drawdown threshold"
)

# Filter strategies by risk
eligible_strategies = filter_strategies_by_risk(all_strategies, risk_appetite, sp500_dd)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Strategy Selection")
st.sidebar.info(f"**{len(eligible_strategies)}** strategies meet your risk criteria ({risk_appetite})")

# Unit selectors for each eligible strategy
unit_selections = {}

if len(eligible_strategies) == 0:
    st.sidebar.warning("⚠️ No strategies meet the selected risk criteria. Please adjust your risk tolerance.")
else:
    for strategy in eligible_strategies:
        st.sidebar.markdown(f"**{strategy['name']}**")

        col1, col2 = st.sidebar.columns([3, 1])

        with col1:
            units = st.number_input(
                f"Units (${strategy['total_equity']:,.0f}/unit)",
                min_value=0,
                max_value=20,
                value=0,
                step=1,
                key=f"units_{strategy['name']}",
                label_visibility="collapsed"
            )

        with col2:
            st.metric(
                label="Max DD",
                value=f"{strategy['max_drawdown']:.1%}",
                label_visibility="collapsed"
            )

        if units > 0:
            unit_selections[strategy['name']] = units

st.sidebar.markdown("---")

# Calculate button
calculate_btn = st.sidebar.button(
    "🚀 Calculate Portfolio Analytics",
    type="primary",
    use_container_width=True
)

# Main content area
if calculate_btn:
    if not unit_selections:
        st.error("❌ Please select at least one strategy unit.")
    else:
        try:
            # Calculate portfolio metrics
            with st.spinner("Calculating portfolio metrics..."):
                portfolio = calculate_portfolio_metrics(
                    unit_selections,
                    all_strategies,
                    monthly_returns,
                    max_leverage
                )

            # Display summary metrics
            st.markdown("### 📈 Portfolio Summary")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Allocation",
                    f"${portfolio['total_equity']:,.0f}",
                    help="Total capital allocated across all selected strategies"
                )

            with col2:
                st.metric(
                    "Required Equity",
                    f"${portfolio['required_equity']:,.0f}",
                    help="Actual capital required considering margin factors"
                )

            with col3:
                effective_leverage = portfolio['required_equity'] / portfolio['total_equity']
                st.metric(
                    "Effective Leverage",
                    f"{effective_leverage:.1%}",
                    help="Required equity as percentage of total allocation"
                )

            with col4:
                win_rate = portfolio['winning_trades'] / portfolio['total_trades'] if portfolio['total_trades'] > 0 else 0
                st.metric(
                    "Win Rate",
                    f"{win_rate:.1%}",
                    help="Percentage of winning trades"
                )

            st.markdown("---")

            # Display all 12 analytics
            st.markdown("### 📊 Detailed Analytics")

            # Row 1: Basic metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Equity", f"${portfolio['total_equity']:,.0f}")

            with col2:
                st.metric("Total Trades", f"{portfolio['total_trades']:.0f}")

            with col3:
                st.metric("Winning Trades", f"{portfolio['winning_trades']:.0f}")

            with col4:
                st.metric("Losing Trades", f"{portfolio['losing_trades']:.0f}")

            # Row 2: Trade performance
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Average Winner", f"${portfolio['average_winner']:,.0f}")

            with col2:
                st.metric("Average Loser", f"${portfolio['average_loser']:,.0f}")

            with col3:
                st.metric("Average Net", f"${portfolio['average_net']:,.0f}")

            with col4:
                st.metric("Max Drawdown", f"{portfolio['max_drawdown']:.2%}")

            # Row 3: Risk-adjusted metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Avg Year Return", f"{portfolio['average_year']:.2%}")

            with col2:
                st.metric("Sharpe Ratio", f"{portfolio['sharpe_ratio']:.3f}")

            with col3:
                st.metric("Sortino Ratio", f"{portfolio['sortino_ratio']:.3f}")

            with col4:
                st.metric("Calmar Ratio", f"{portfolio['calmar_ratio']:.3f}")

            st.markdown("---")

            # Display selected strategies
            st.markdown("### 📋 Selected Strategies")

            strategy_data = []
            for name, units in unit_selections.items():
                strategy = next((s for s in all_strategies if s['name'] == name), None)
                if strategy:
                    allocation = units * strategy['total_equity']
                    required = allocation * strategy['margin_equity']
                    strategy_data.append({
                        'Strategy': name,
                        'Units': units,
                        'Allocation': f"${allocation:,.0f}",
                        'Required Equity': f"${required:,.0f}",
                        'Margin %': f"{strategy['margin_equity']:.0%}",
                        'Max DD': f"{strategy['max_drawdown']:.2%}",
                        'Sharpe': f"{strategy['sharpe_ratio']:.2f}"
                    })

            st.dataframe(strategy_data, use_container_width=True, hide_index=True)

            st.markdown("---")

            # Generate analytics image
            st.markdown("### 🖼️ Analytics Visualization")

            with st.spinner("Generating analytics image..."):
                image_path = generate_analytics_image(
                    portfolio,
                    unit_selections,
                    all_strategies,
                    monthly_returns
                )

            # Display image
            st.image(image_path, use_container_width=True)

            # Download button
            with open(image_path, "rb") as f:
                st.download_button(
                    label="📥 Download Analytics Image",
                    data=f,
                    file_name="portfolio_analytics.png",
                    mime="image/png",
                    use_container_width=True
                )

            st.success("✅ Portfolio analytics calculated successfully!")

        except ValueError as e:
            st.error(f"❌ {str(e)}")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

else:
    # Welcome screen when no calculation has been done
    st.info("👈 Configure your portfolio in the sidebar and click **Calculate Portfolio Analytics** to begin.")

    st.markdown("### 📚 How to Use")

    st.markdown("""
    1. **Set Investment Amount**: Enter your total capital to allocate
    2. **Choose Leverage**: Select maximum leverage constraint (100%-300%)
    3. **Set Risk Tolerance**: Filter strategies by maximum drawdown
    4. **Select Strategies**: Choose number of units for each strategy
    5. **Calculate**: Click the button to generate analytics and visualizations

    ### 📊 Understanding the Metrics

    - **Total Allocation**: Sum of all strategy units × unit size
    - **Required Equity**: Actual capital needed after applying margin factors
    - **Effective Leverage**: How much exposure you have vs. capital
    - **Sharpe Ratio**: Risk-adjusted return (higher is better)
    - **Sortino Ratio**: Like Sharpe, but only considers downside risk
    - **Calmar Ratio**: Annual return divided by max drawdown
    - **Max Drawdown**: Largest peak-to-valley decline

    ### 💡 Tips

    - Start with conservative risk tolerance (<10%) to see stable strategies
    - Monitor effective leverage to stay within your constraint
    - Higher Sharpe/Sortino/Calmar ratios indicate better risk-adjusted performance
    - Diversify across multiple strategies to reduce portfolio drawdown
    """)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #888; font-size: 0.9rem;">'
    'Portfolio Analytics Dashboard | Built with Streamlit | Data from strategy-returns.xlsx'
    '</div>',
    unsafe_allow_html=True
)
