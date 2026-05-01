import streamlit as st
import streamlit.components.v1 as components

def render_tv_chart(symbol):
    """
    Renders a high-performance TradingView candlestick chart widget.
    
    Note: We use components.html because st.html strips script tags 
    for security reasons in current Streamlit versions.
    """
    clean_symbol = symbol.replace('/', '')
    tv_symbol = f"BINANCE:{clean_symbol}"
    
    html_content = f"""
    <div id="tv_{clean_symbol}"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "width": "100%",
      "height": 400,
      "symbol": "{tv_symbol}",
      "interval": "60",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "withdateranges": true,
      "hide_side_toolbar": false,
      "allow_symbol_change": true,
      "details": true,
      "studies": [
        "MASimple@tv-basicstudies",
        "MAExp@tv-basicstudies",
        "RSI@tv-basicstudies",
        "MACD@tv-basicstudies"
      ],
      "container_id": "tv_{clean_symbol}"
    }});
    </script>
    """
    # Using v1 component to ensure scripts execute properly
    components.html(html_content, height=410)