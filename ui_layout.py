import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from charts import render_tv_chart

def detect_divergence(current_price, magnets, cvd_series):
    if not cvd_series or len(cvd_series) < 5:
        return None
    threshold = 0.001 
    cvd_slope = cvd_series[-1] - cvd_series[-5]
    
    # Bearish Divergence
    upper_mag = magnets['short_risk'][0]
    if upper_mag > 0 and abs(current_price - upper_mag) / upper_mag < threshold:
        if cvd_slope < 0:
            return "⚠️ BEARISH DIVERGENCE: Price at Upper Magnet but CVD dropping. Possible Fakeout."

    # Bullish Divergence
    lower_mag = magnets['long_risk'][0]
    if lower_mag > 0 and abs(current_price - lower_mag) / lower_mag < threshold:
        if cvd_slope > 0:
            return "🚀 BULLISH DIVERGENCE: Price at Lower Magnet but CVD rising. Possible Absorption."
    return None

def render_sentinel_dashboard(page_title, engine_type, symbols, market_data, current_rekt, bids, asks, magnets, cvd_series, history_key, audit_key, last_prices):
    st.title(f"🛡️ {page_title}")

    # --- 1. Top Charts (TradingView) ---
    c_charts = st.columns(3)
    for i, s in enumerate(symbols):
        with c_charts[i]:
            render_tv_chart(s)

    st.markdown("---")

    # --- 2. Divergence & Magnet Alerts ---
    current_btc_price = market_data[symbols[0]]['price']
    divergence_msg = detect_divergence(current_btc_price, magnets, cvd_series)
    if divergence_msg:
        st.warning(divergence_msg)

    a1, a2 = st.columns(2)
    with a1:
        if magnets['short_risk'][1] > 0:
            dist = ((magnets['short_risk'][0] - current_btc_price) / current_btc_price) * 100
            st.error(f"🧲 **{engine_type} Upper Magnet:** ${magnets['short_risk'][0]:,.0f} ({dist:.2f}% away)")
    with a2:
        if magnets['long_risk'][1] > 0:
            dist = ((current_btc_price - magnets['long_risk'][0]) / current_btc_price) * 100
            st.warning(f"🧲 **{engine_type} Lower Magnet:** ${magnets['long_risk'][0]:,.0f} ({dist:.2f}% away)")

    # --- 3. Price Metrics ---
    m_cols = st.columns(3)
    for i, s in enumerate(symbols):
        p = market_data[s]['price']
        spread = market_data[s]['spread']
        v_status, v_color = ("!! VOLATILE !!", "inverse") if last_prices.get(s) and abs((p - last_prices[s])/last_prices[s]) > 0.0001 else ("STABLE", "normal")
        label = f"{s} (Spread: ${spread:.2f})" if engine_type == "CEX" else f"Hyperliquid {s}"
        m_cols[i].metric(label=label, value=f"${p:,.2f}", delta=v_status, delta_color=v_color)
        last_prices[s] = p

    # --- 4. Analytics (Liquidity & CVD) ---
    lc1, lc2 = st.columns(2)
    with lc1:
        st.subheader(f"📊 {symbols[0]} Liquidity Depth")
        if not bids.empty:
            fig_depth = go.Figure()
            fig_depth.add_trace(go.Bar(y=asks['cluster'], x=asks['vol'], orientation='h', name='Short Risk', marker_color="#EF5350"))
            fig_depth.add_trace(go.Bar(y=bids['cluster'], x=bids['vol'], orientation='h', name='Long Risk', marker_color="#26A69A"))
            fig_depth.update_layout(height=300, barmode='overlay', paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#D1D4DC", margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_depth, use_container_width=True)

    with lc2:
        st.subheader(f"📈 {symbols[0]} CVD (Aggression)")
        if cvd_series:
            fig_cvd = go.Figure()
            line_color = '#26A69A' if cvd_series[-1] > cvd_series[0] else '#EF5350'
            fig_cvd.add_trace(go.Scatter(y=cvd_series, mode='lines', fill='tozeroy', name='CVD', line=dict(color=line_color)))
            fig_cvd.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#D1D4DC", margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
            fig_cvd.update_xaxes(visible=False)
            st.plotly_chart(fig_cvd, use_container_width=True)

    # --- 5. Live Feed (REKT Alerts) ---
    st.subheader("🔥 Live REKT Alerts")
    if not current_rekt.empty:
        r_cols = st.columns(3)
        for idx, row in current_rekt.head(3).iterrows():
            with r_cols[idx]:
                emoji = "🟢" if row['side'] == 'SELL' else "🔴"
                st.info(f"**{emoji} {row['symbol']}**\n\n{row['origQty']:.2f} Liquidated @ {row['price']:,.2f}")
    else:
        st.info("🛡️ Market calm... monitoring live exchange liquidations.")

    # --- 6. Session Logs ---
    col_log1, col_log2 = st.columns(2)
    with col_log1:
        st.subheader("🤖 System Audit Log")
        st.dataframe(st.session_state[audit_key], use_container_width=True, hide_index=True)
    with col_log2:
        st.subheader(f"📜 {engine_type} Historical Ledger")
        st.dataframe(st.session_state[history_key], use_container_width=True, hide_index=True)