import streamlit as st
import pandas as pd
import time
from liquidations import LiquidationEngine
from ui_layout import render_sentinel_dashboard

st.set_page_config(page_title="DEX Sentinel", layout="wide")

if 'engine' not in st.session_state: st.session_state.engine = LiquidationEngine()
if 'dex_history' not in st.session_state: st.session_state.dex_history = pd.DataFrame(columns=['symbol', 'side', 'price', 'origQty', 'time'])
if 'dex_last_prices' not in st.session_state: st.session_state.dex_last_prices = {}

symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']

# --- THE FIX: Create a Master Placeholder ---
dashboard_spot = st.empty()

while True:
    data = st.session_state.engine.get_market_data(symbols, "DEX")
    rekt = st.session_state.engine.get_rekt_feed("DEX")
    bids, asks = st.session_state.engine.get_liquidity_depth(symbols[0], "DEX")
    magnets = st.session_state.engine.get_liquidity_magnets(symbols[0], data[symbols[0]]['price'], "DEX")
    
    if not rekt.empty:
        st.session_state.dex_history = pd.concat([rekt, st.session_state.dex_history]).drop_duplicates(subset=['time', 'price']).head(50)

    # Wrap the entire render in the container
    with dashboard_spot.container():
        render_sentinel_dashboard("DEX Sentinel | Hyperliquid L1", "DEX", symbols, data, rekt, bids, asks, magnets, 'dex_history', st.session_state.dex_last_prices)
    
    time.sleep(2)