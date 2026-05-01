import streamlit as st
import ccxt
import pandas as pd
import time
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Sats Trading Monitor", layout="wide")

# Static Header
st.title("🛡️ Sats Trading Monitor | Market Sentinel")
st.write(f"Live Execution Monitor | System Status: ONLINE")
st.markdown("---")

# 1. Initialize Exchange (Using CCXT Sync for the Dashboard)
exchange = ccxt.binance()
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']

# The Master Placeholder to keep the UI stationary
dashboard_frame = st.empty()

# Initialize history in session state
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Timestamp', 'Asset', 'Price'])

try:
    while True:
        current_data = []
        
        with dashboard_frame.container():
            # Create columns for the Top Metrics
            cols = st.columns(len(symbols))
            
            for i, symbol in enumerate(symbols):
                ticker = exchange.fetch_ticker(symbol)
                price = ticker['last']
                
                # Big Metrics at the top
                cols[i].metric(label=symbol, value=f"${price:,.2f}")
                
                current_data.append({
                    'Timestamp': datetime.now().strftime('%H:%M:%S'),
                    'Asset': symbol,
                    'Price': f"${price:,.2f}"
                })

            st.markdown("### 📊 Live Market Feed")
            
            # Update history logic
            new_rows = pd.DataFrame(current_data)
            
            # ignore_index=True stops the 0,1,2 cycling behavior
            st.session_state.history = pd.concat([new_rows, st.session_state.history], ignore_index=True).head(15)
            
            # UPDATED: Using width='stretch' to match the latest Streamlit API
            st.dataframe(
                st.session_state.history, 
                hide_index=True, 
                width='stretch'
            )
            
            st.caption(f"Last UI Sync: {datetime.now().strftime('%H:%M:%S')} | Environment: Arch Linux")

        time.sleep(2)

except Exception as e:
    st.error(f"Dashboard Halted: {e}")