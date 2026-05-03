import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from charts import render_tv_chart

def render_sentinel_dashboard(page_title, engine_type, symbols, market_data, current_rekt, bids, asks, magnets, cvd_series, history_key, audit_key, last_prices):
    st.title(f"🛡️ {page_title}")

    # --- 1. Top Charts ---
    c1, c2, c3 = st.columns(3)
    for i, s in enumerate(symbols):
        with [c1, c2, c3][i]: render_tv_chart(s)

    st.markdown("---")

    # --- 2. Magnet Alerts ---
    a1, a2 = st.columns(2)
    with a1:
        if magnets['short_risk'][1] > 0:
            dist = ((magnets['short_risk'][0] - market_data[symbols[0]]['price']) / market_data[symbols[0]]['price']) * 100
            st.error(f"🧲 **{engine_type} Upper Magnet:** ${magnets['short_risk'][0]:,.0f} ({dist:.2f}% away)")
    with a2:
        if magnets['long_risk'][1] > 0:
            dist = ((market_data[symbols[0]]['price'] - magnets['long_risk'][0]) / market_data[symbols[0]]['price']) * 100
            st.warning(f"🧲 **{engine_type} Lower Magnet:** ${magnets['long_risk'][0]:,.0f} ({dist:.2f}% away)")

    # --- 3. Metrics ---
    m_cols = st.columns(3)
    for i, s in enumerate(symbols):
        p = market_data[s]['price']
        spread = market_data[s]['spread']
        v_status, v_color = ("!! VOLATILE !!", "inverse") if last_prices.get(s) and abs((p - last_prices[s])/last_prices[s]) > 0.0001 else ("STABLE", "normal")
        label = f"{s} (Spread: ${spread:.2f})" if engine_type == "CEX" else f"Hyperliquid {s}"
        m_cols[i].metric(label=label, value=f"${p:,.2f}", delta=v_status, delta_color=v_color)
        last_prices[s] = p

    # --- 4. Liquidation Depth & CVD Charts ---
    lc1, lc2 = st.columns(2)
    with lc1:
        st.subheader(f"📊 {symbols[0]} Liquidity Depth")
        if not bids.empty:
            fig_depth = go.Figure()
            fig_depth.add_trace(go.Bar(y=asks['cluster'], x=asks['vol'], orientation='h', name='Short Risk', marker_color="#EF5350"))
            fig_depth.add_trace(go.Bar(y=bids['cluster'], x=bids['vol'], orientation='h', name='Long Risk', marker_color="#26A69A"))
            fig_depth.update_layout(height=250, barmode='overlay', paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#D1D4DC", margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_depth, use_container_width=True)

    with lc2:
        st.subheader(f"📈 {symbols[0]} CVD (Market Aggression)")
        if cvd_series:
            fig_cvd = go.Figure()
            line_color = '#26A69A' if cvd_series[-1] > cvd_series[0] else '#EF5350'
            fig_cvd.add_trace(go.Scatter(y=cvd_series, mode='lines', fill='tozeroy', name='CVD', line=dict(color=line_color)))
            fig_cvd.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#D1D4DC", margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
            fig_cvd.update_xaxes(visible=False)
            st.plotly_chart(fig_cvd, use_container_width=True)

    # --- 5. REKT Feeds ---
    st.subheader("🔥 Live REKT Feed")
    if not current_rekt.empty:
        r_cols = st.columns(3)
        for idx, row in current_rekt.head(3).iterrows():
            with r_cols[idx]:
                emoji = "🟢" if row['side'] == 'SELL' else "🔴"
                st.info(f"**{emoji} {row['symbol']}**\n\n{row['origQty']:.2f} Liq @ {row['price']:,.2f}")
    else: st.info("🛡️ Market calm... monitoring live exchange liquidations.")
    
    # --- 6. Ledgers & Logs ---
    st.subheader(f"📜 {engine_type} Historical Ledger")
    st.dataframe(st.session_state[history_key], width="stretch", hide_index=True)

    st.subheader("🤖 System Audit Log")
    st.dataframe(st.session_state[audit_key], width="stretch", hide_index=True)