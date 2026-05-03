import streamlit as st
import pandas as pd
import time
from datetime import datetime
from liquidations import LiquidationEngine
from ui_layout import render_sentinel_dashboard

st.set_page_config(page_title="CEX Sentinel", layout="wide")

if 'engine' not in st.session_state: st.session_state.engine = LiquidationEngine()
if 'cex_history' not in st.session_state: st.session_state.cex_history = pd.DataFrame(columns=['symbol', 'side', 'price', 'origQty', 'time'])
if 'audit_log' not in st.session_state: st.session_state.audit_log = pd.DataFrame(columns=['Timestamp', 'Asset', 'Price', 'Status'])
if 'cex_last_prices' not in st.session_state: st.session_state.cex_last_prices = {}

symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
dashboard_spot = st.empty()

while True:
    data = st.session_state.engine.get_market_data(symbols, "CEX")
    rekt = st.session_state.engine.get_rekt_feed("CEX")
    bids, asks = st.session_state.engine.get_liquidity_depth(symbols[0], "CEX")
    magnets = st.session_state.engine.get_liquidity_magnets(symbols[0], data[symbols[0]]['price'], "CEX")
    cvd = st.session_state.engine.get_cvd_series(symbols[0], "CEX")
    
    # Update Audit Log
    for s in symbols:
        p = data[s]['price']
        v_status = "STABLE"
        if st.session_state.cex_last_prices.get(s) and abs((p - st.session_state.cex_last_prices[s])/st.session_state.cex_last_prices[s]) > 0.0001:
            v_status = "!! VOLATILE !!"
        
        new_log = {'Timestamp': datetime.now().strftime('%H:%M:%S'), 'Asset': s, 'Price': f"${p:,.2f}", 'Status': v_status}
        st.session_state.audit_log = pd.concat([pd.DataFrame([new_log]), st.session_state.audit_log]).head(20)

    if not rekt.empty:
        st.session_state.cex_history = pd.concat([rekt, st.session_state.cex_history]).drop_duplicates(subset=['time', 'price']).head(50)

    with dashboard_spot.container():
        render_sentinel_dashboard("CEX Sentinel | Binance", "CEX", symbols, data, rekt, bids, asks, magnets, cvd, 'cex_history', 'audit_log', st.session_state.cex_last_prices)
    
    time.sleep(2)