import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from charts import render_tv_chart

def render_sentinel_dashboard(page_title, engine_type, symbols, market_data, current_rekt, bids, asks, magnets, history_key, last_prices):
    # This now runs INSIDE the placeholder container provided by cex.py/dex.py
    st.title(f"🛡️ {page_title}")

    # --- 1. Top Charts ---
    c1, c2, c3 = st.columns(3)
    for i, s in enumerate(symbols):
        with [c1, c2, c3][i]: 
            render_tv_chart(s)

    st.markdown("---")

    # --- 2. Magnet Alerts ---
    a1, a2 = st.columns(2)
    if magnets['short_risk'][1] > 0:
        dist = ((magnets['short_risk'][0] - market_data[symbols[0]]['price']) / market_data[symbols[0]]['price']) * 100
        a1.error(f"🧲 **{engine_type} Upper Magnet:** ${magnets['short_risk'][0]:,.0f} ({dist:.2f}% away)")
    if magnets['long_risk'][1] > 0:
        dist = ((market_data[symbols[0]]['price'] - magnets['long_risk'][0]) / market_data[symbols[0]]['price']) * 100
        a2.warning(f"🧲 **{engine_type} Lower Magnet:** ${magnets['long_risk'][0]:,.0f} ({dist:.2f}% away)")

    # --- 3. Metrics Bar ---
    m_cols = st.columns(3)
    for i, s in enumerate(symbols):
        p = market_data[s]['price']
        spread = market_data[s]['spread']
        v_status, v_color = ("!! VOLATILE !!", "inverse") if last_prices.get(s) and abs((p - last_prices[s])/last_prices[s]) > 0.0001 else ("STABLE", "normal")
        
        label = f"{s} (Binance vs Kraken: ${spread:.2f})" if engine_type == "CEX" else f"Hyperliquid {s}"
        m_cols[i].metric(label=label, value=f"${p:,.2f}", delta=v_status, delta_color=v_color)
        last_prices[s] = p

    # --- 4. Liquidation Depth ---
    st.subheader(f"📊 {symbols[0]} Liquidity Depth")
    if not bids.empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(y=asks['cluster'], x=asks['vol'], orientation='h', name='Short Risk', marker_color="#EF5350"))
        fig.add_trace(go.Bar(y=bids['cluster'], x=bids['vol'], orientation='h', name='Long Risk', marker_color="#26A69A"))
        fig.update_layout(height=250, barmode='overlay', paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#D1D4DC", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    # --- 5. REKT Feeds ---
    st.subheader("🔥 Live REKT Feed")
    if not current_rekt.empty:
        r_cols = st.columns(3)
        for idx, row in current_rekt.head(3).iterrows():
            with r_cols[idx]:
                emoji = "🟢" if row['side'] == 'SELL' else "🔴"
                st.info(f"**{emoji} {row['symbol']}**\n\n{row['origQty']:.2f} Liquidated @ {row['price']:,.2f}")
    else: 
        st.info("🛡️ Market calm... monitoring live exchange liquidations.")
    
    st.subheader(f"📜 {engine_type} Historical Ledger")
    st.dataframe(st.session_state[history_key], width="stretch", hide_index=True)