"""
SOVRUN Portfolio Analytics Dashboard v2.0
Self-directed investment platform - Risk-first portfolio allocation
"""

import streamlit as st
import pandas as pd
import base64
from pathlib import Path
from portfolio_calculator import (
    load_strategy_data,
    get_sp500_drawdown,
    filter_strategies_by_risk,
    calculate_portfolio_metrics
)
from chart_generator import generate_analytics_image


# Page configuration
st.set_page_config(
    page_title="SOVRUN - Portfolio Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load logo
def load_svg(svg_path):
    with open(svg_path, "r") as f:
        svg = f.read()
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" style="height: 60px;"/>'

# Custom CSS - Dark theme with blue hues
st.markdown("""
    <style>
    /* Import Aptos font */
    @import url('https://fonts.googleapis.com/css2?family=Calibri:wght@300;400;600;700&display=swap');

    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Aptos', 'Calibri', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
    }

    /* Header */
    .sovrun-header {
        background: linear-gradient(90deg, #1e3a5f 0%, #2d5a8f 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .sovrun-tagline {
        color: #5ba2f0;
        font-size: 0.9rem;
        font-weight: 300;
        margin-top: 0.5rem;
        letter-spacing: 1px;
    }

    /* Input sections */
    .input-section {
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 1.5rem 0;
        margin-bottom: 1.5rem;
    }

    .input-section h3 {
        color: #c5e3ff;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0;
        letter-spacing: 0.5px;
    }

    /* Strategy cards */
    .strategy-card {
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 0.5rem 0;
        margin-bottom: 0.3rem;
        transition: all 0.2s ease;
    }

    .strategy-card:hover .strategy-name {
        color: #6db3ff;
    }

    .strategy-name {
        color: #5ba2f0;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    .strategy-stats {
        color: #4a90e2;
        font-size: 0.85rem;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #ff8c42 0%, #ff6b35 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.8rem 2.5rem;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 140, 66, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(255, 140, 66, 0.5);
        transform: translateY(-2px);
    }

    /* Number inputs and selects */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        background: transparent;
        color: #5ba2f0;
        border: none;
        border-bottom: 1px solid rgba(91, 162, 240, 0.3);
        border-radius: 0;
        padding: 0.6rem 0.3rem;
    }

    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-bottom-color: #5ba2f0;
        box-shadow: none;
        outline: none;
    }

    /* Hide number input arrows */
    .stNumberInput button {
        background: transparent;
        border: none;
        color: #5ba2f0;
    }

    /* Labels and captions - INCREASED SIZE */
    label {
        color: #5ba2f0 !important;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.3px;
    }

    .stCaptionContainer, [data-testid="stCaptionContainer"] {
        color: #4a90e2 !important;
        font-size: 1rem;
    }

    /* Success/Error messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.15);
        border-left: 4px solid #22c55e;
        color: #86efac;
    }

    .stError {
        background: rgba(239, 68, 68, 0.15);
        border-left: 4px solid #ef4444;
        color: #fca5a5;
    }

    .stWarning {
        background: rgba(255, 140, 66, 0.15);
        border-left: 4px solid #ff8c42;
        color: #fbbf24;
    }

    /* Info boxes */
    .stInfo {
        background: rgba(74, 144, 226, 0.15);
        border-left: 4px solid #4a90e2;
        color: #93c5fd;
    }

    /* Metrics - BRILLIANT PROFESSIONAL DESIGN */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(30, 58, 95, 0.4) 0%, rgba(74, 144, 226, 0.2) 100%);
        border: 2px solid rgba(91, 162, 240, 0.4);
        border-radius: 12px;
        padding: 1.5rem 1rem;
        box-shadow: 0 8px 32px rgba(74, 144, 226, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    [data-testid="stMetric"]:hover {
        border-color: #5ba2f0;
        box-shadow: 0 12px 40px rgba(74, 144, 226, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }

    [data-testid="stMetricValue"] {
        color: #5ba2f0;
        font-size: 2.4rem;
        font-weight: 800;
        text-shadow: 0 2px 8px rgba(91, 162, 240, 0.3);
        letter-spacing: -0.5px;
    }

    [data-testid="stMetricLabel"] {
        color: #e2e8f0;
        font-size: 1.05rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    /* Modal/Dialog styling */
    .modal-content {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d3748 100%);
        border-radius: 12px;
        padding: 2rem;
    }

    /* Divider */
    hr {
        border-color: rgba(74, 144, 226, 0.2);
        margin: 2rem 0;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #1a1f2e;
    }

    ::-webkit-scrollbar-thumb {
        background: #4a90e2;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #5ba2f0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None
if 'image_path' not in st.session_state:
    st.session_state.image_path = None

# Header
logo_path = Path("assets/sovrun_logo_pro.svg")
if logo_path.exists():
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(load_svg(logo_path), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="sovrun-tagline">Self-Directed Investment Platform | Risk-First Portfolio Allocation</div>', unsafe_allow_html=True)
else:
    st.markdown('<h1 style="color: #4a90e2; font-weight: 700;">SOVRUN</h1>', unsafe_allow_html=True)
    st.markdown('<div class="sovrun-tagline">Self-Directed Investment Platform | Risk-First Portfolio Allocation</div>', unsafe_allow_html=True)

st.markdown("---")

# Load strategy data
try:
    data = load_strategy_data("strategy-returns.xlsx")
    all_strategies = data['strategies']
    monthly_returns = data['monthly_returns']
    sp500_dd = get_sp500_drawdown(data)
except Exception as e:
    st.error(f"❌ Error loading strategy data: {e}")
    st.stop()

# TOP INPUT SECTION
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("### ⚙️ Portfolio Configuration")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_investment = st.number_input(
        "💰 Total Investment ($)",
        min_value=10000,
        max_value=100000000,
        value=1000000,
        step=50000,
        help="Total capital to allocate across strategies"
    )

with col2:
    max_leverage = st.selectbox(
        "⚖️ Maximum Leverage",
        options=[100, 150, 200, 300],
        format_func=lambda x: f"{x}%",
        help="Maximum portfolio-level leverage allowed"
    )

with col3:
    risk_appetite = st.selectbox(
        "🎯 Risk Alert Threshold",
        options=["<5% peak to valley", "<10% peak to valley", "<20% peak to valley", "S&P level"],
        index=1,
        help="Alert if portfolio drawdown exceeds this threshold"
    )

with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    st.metric("Available Strategies", len(all_strategies), help="Total strategies in database")

st.markdown('</div>', unsafe_allow_html=True)

# STRATEGY SELECTION SECTION
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("### 📊 Strategy Selection")
st.caption("Select units for each strategy (1 unit = strategy's allocated capital)")

unit_selections = {}

# Vertical layout - one strategy per row
for strategy in all_strategies:
    # Create columns: name/stats (wide) | units selector (narrow)
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(f'<div class="strategy-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="strategy-name">📊 {strategy["name"]}</div>', unsafe_allow_html=True)

        # Strategy stats in single line
        st.markdown(
            f'<div class="strategy-stats">'
            f'${strategy["total_equity"]:,.0f}/unit • '
            f'Margin: {strategy["margin_equity"]:.0%} • '
            f'Max DD: {strategy["max_drawdown"]:.1%} • '
            f'Sharpe: {strategy["sharpe_ratio"]:.2f}'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        units = st.number_input(
            "Units",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            key=f"units_{strategy['name']}",
            label_visibility="collapsed"
        )

        if units > 0:
            unit_selections[strategy['name']] = units

st.markdown('</div>', unsafe_allow_html=True)

# CALCULATE BUTTON
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    calculate_btn = st.button("🚀 ANALYZE PORTFOLIO", use_container_width=True)

# CALCULATION LOGIC
if calculate_btn:
    if not unit_selections:
        st.error("❌ Please select at least one strategy unit before analyzing.")
    else:
        try:
            with st.spinner("🔄 Calculating portfolio analytics..."):
                portfolio = calculate_portfolio_metrics(
                    unit_selections,
                    all_strategies,
                    monthly_returns,
                    max_leverage
                )

                # Generate analytics image
                image_path = generate_analytics_image(
                    portfolio,
                    unit_selections,
                    all_strategies,
                    monthly_returns,
                    total_investment
                )

                # Store in session state
                st.session_state.portfolio_data = portfolio
                st.session_state.image_path = image_path
                st.session_state.unit_selections = unit_selections
                st.session_state.show_results = True

        except ValueError as e:
            st.error(f"❌ {str(e)}")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# RESULTS MODAL/POPUP
if st.session_state.show_results and st.session_state.portfolio_data:
    portfolio = st.session_state.portfolio_data
    image_path = st.session_state.image_path

    st.markdown("---")
    st.markdown("## 📊 Portfolio Analysis Results")

    # Check risk alert
    risk_thresholds = {
        "<5% peak to valley": -0.05,
        "<10% peak to valley": -0.10,
        "<20% peak to valley": -0.20,
        "S&P level": sp500_dd
    }

    threshold = risk_thresholds.get(risk_appetite, -0.20)

    if portfolio['max_drawdown'] < threshold:
        st.warning(f"⚠️ **RISK ALERT**: Portfolio max drawdown ({portfolio['max_drawdown']:.2%}) exceeds your risk threshold ({abs(threshold):.1%}).")
    else:
        st.success(f"✅ Portfolio drawdown ({portfolio['max_drawdown']:.2%}) is within your risk tolerance ({abs(threshold):.1%}).")

    # Key metrics at top
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Allocation", f"${portfolio['total_equity']:,.0f}")

    with col2:
        st.metric("Required Equity", f"${portfolio['required_equity']:,.0f}")

    with col3:
        effective_leverage = portfolio['required_equity'] / portfolio['total_equity']
        st.metric("Effective Leverage", f"{effective_leverage:.1%}")

    with col4:
        win_rate = portfolio['winning_trades'] / portfolio['total_trades'] if portfolio['total_trades'] > 0 else 0
        st.metric("Win Rate", f"{win_rate:.1%}")

    with col5:
        st.metric("Sharpe Ratio", f"{portfolio['sharpe_ratio']:.3f}")

    # Analytics image
    st.markdown("### 📈 Analytics Dashboard")
    st.image(image_path, use_container_width=True)

    # Export options
    st.markdown("### 💾 Export Options")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with open(image_path, "rb") as f:
            st.download_button(
                label="📥 Download PNG",
                data=f,
                file_name="sovrun_portfolio_analytics.png",
                mime="image/png",
                use_container_width=True
            )

    with col2:
        # Convert to JPEG
        from PIL import Image
        img = Image.open(image_path)
        jpeg_path = image_path.replace('.png', '.jpg')
        rgb_img = img.convert('RGB')
        rgb_img.save(jpeg_path, 'JPEG', quality=95)

        with open(jpeg_path, "rb") as f:
            st.download_button(
                label="📥 Download JPEG",
                data=f,
                file_name="sovrun_portfolio_analytics.jpg",
                mime="image/jpeg",
                use_container_width=True
            )

    with col3:
        # PDF export will be added with pdf skill
        st.button("📥 Download PDF", disabled=True, use_container_width=True, help="PDF export coming soon")

    with col4:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.show_results = False
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #6b7280; font-size: 0.85rem; padding: 1rem;">'
    'SOVRUN Portfolio Analytics | Risk-First Investment Platform | Powered by Advanced Analytics'
    '</div>',
    unsafe_allow_html=True
)
