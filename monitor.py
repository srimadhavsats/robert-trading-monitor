import streamlit as st
import ccxt
import pandas as pd
import time
from datetime import datetime
from charts import render_tv_chart 

# --- Application Configuration ---
st.set_page_config(page_title="Sats Trading Monitor", layout="wide")
st.title("🛡️ Sats Trading Monitor v1.9")

# --- UI Layout: Charts Section (Static) ---
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("Primary Asset: Bitcoin")
    render_tv_chart(symbols[0])

with col2:
    st.caption("Ecosystem Proxy: Ethereum")
    render_tv_chart(symbols[1])

with col3:
    st.caption("Performance Proxy: Solana")
    render_tv_chart(symbols[2])

st.markdown("---")

# --- Backend Engine: Live Data & State Management ---
exchange = ccxt.binance() 

if 'audit_log' not in st.session_state:
    st.session_state.audit_log = pd.DataFrame(columns=['Timestamp', 'Asset', 'Price', 'Status'])

metrics_placeholder = st.empty()
log_placeholder = st.empty()

last_prices = {symbol: None for symbol in symbols}

def calculate_volatility(price, last_price):
    """Assigns status flags based on price movement."""
    if last_price is None: return "STABLE"
    change = ((price - last_price) / last_price) * 100
    return "!! VOLATILE !!" if abs(change) > 0.01 else "STABLE"

# Core monitoring loop
while True:
    ticker_data = []
    
    for symbol in symbols:
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        status = calculate_volatility(price, last_prices[symbol])
        
        new_entry = {
            'Timestamp': datetime.now().strftime('%H:%M:%S'),
            'Asset': symbol,
            'Price': f"${price:,.2f}",
            'Status': status
        }
        
        st.session_state.audit_log = pd.concat(
            [pd.DataFrame([new_entry]), st.session_state.audit_log], 
            ignore_index=True
        )
        ticker_data.append({"symbol": symbol, "price": price, "status": status})
        last_prices[symbol] = price

    # Update dynamic Metrics Grid
    with metrics_placeholder.container():
        cols = st.columns(len(symbols))
        for i, data in enumerate(ticker_data):
            cols[i].metric(
                label=data['symbol'], 
                value=f"${data['price']:,.2f}", 
                delta=data['status']
            )

    # Update dynamic Audit Log with index suppressed
    with log_placeholder.container():
        st.write("### Live Audit Log")
        st.dataframe(
            st.session_state.audit_log.head(15), 
            width="stretch", 
            hide_index=True
        )

    # Wait for 2 seconds
    time.sleep(2)