import streamlit as st
import ccxt
import pandas as pd
import time

# Page Configuration (The "Brilliant" Look)
st.set_page_config(page_title="Sats Trading Monitor", layout="wide")

st.title("🛡️ **Sats Trading Monitor v1.4** | Live Execution Monitor")
st.write("Real-time execution monitoring and volatility tracking.")

# 1. Initialize Exchange (Using CCXT Sync for the Dashboard)
exchange = ccxt.binance()
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']

# Create empty placeholders for the "Fast" UI updates
metrics_col = st.columns(len(symbols))
chart_placeholder = st.empty()
table_placeholder = st.empty()

# Initialize data history
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Timestamp', 'Asset', 'Price'])

while True:
    current_data = []
    
    for i, symbol in enumerate(symbols):
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        
        # Update Big Top Metrics
        metrics_col[i].metric(label=symbol, value=f"${price:,.2f}")
        
        current_data.append({
            'Timestamp': pd.Timestamp.now(),
            'Asset': symbol,
            'Price': price
        })

    # Update History Table
    new_df = pd.DataFrame(current_data)
    st.session_state.history = pd.concat([new_df, st.session_state.history]).head(20)
    
    # Render the "Fast" UI Components
    with table_placeholder.container():
        st.subheader("Live Audit Log")
        st.table(st.session_state.history)

    time.sleep(2) # Refresh rate