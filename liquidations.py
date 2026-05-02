import ccxt
import pandas as pd

class LiquidationEngine:
    def __init__(self):
        # CEX Exchanges
        self.binance = ccxt.binance({'options': {'defaultType': 'future'}})
        self.kraken = ccxt.kraken()
        # DEX Exchange
        self.hyperliquid = ccxt.hyperliquid()
        
    def get_market_data(self, symbols, exchange_type="CEX"):
        data = {}
        for symbol in symbols:
            try:
                if exchange_type == "CEX":
                    b_ticker = self.binance.fetch_ticker(symbol)
                    try:
                        k_ticker = self.kraken.fetch_ticker(symbol)
                        spread = b_ticker['last'] - k_ticker['last']
                    except: spread = 0.0
                    data[symbol] = {'price': b_ticker['last'], 'spread': spread}
                else: # DEX
                    hl_ticker = self.hyperliquid.fetch_ticker(symbol)
                    data[symbol] = {'price': hl_ticker['last'], 'spread': 0.0}
            except:
                data[symbol] = {'price': 0.0, 'spread': 0.0}
        return data

    def get_liquidity_depth(self, symbol, exchange_type="CEX"):
        try:
            ex = self.binance if exchange_type == "CEX" else self.hyperliquid
            ob = ex.fetch_order_book(symbol, limit=1000)
            bids = pd.DataFrame(ob['bids'], columns=['price', 'vol'])
            asks = pd.DataFrame(ob['asks'], columns=['price', 'vol'])
            
            cluster_size = 500 if "BTC" in symbol else 10 # Dynamic clustering
            bids['cluster'] = (bids['price'] // cluster_size) * cluster_size
            asks['cluster'] = (asks['price'] // cluster_size) * cluster_size
            
            b_grouped = bids.groupby('cluster')['vol'].sum().reset_index().tail(10)
            a_grouped = asks.groupby('cluster')['vol'].sum().reset_index().head(10)
            return b_grouped, a_grouped
        except: return pd.DataFrame(), pd.DataFrame()

    def get_liquidity_magnets(self, symbol, current_price, exchange_type="CEX"):
        try:
            ex = self.binance if exchange_type == "CEX" else self.hyperliquid
            ob = ex.fetch_order_book(symbol, limit=1000)
            up, low = current_price * 1.015, current_price * 0.985
            asks = [a for a in ob['asks'] if a[0] <= up]
            bids = [b for b in ob['bids'] if b[0] >= low]
            top_ask = max(asks, key=lambda x: x[1]) if asks else [0, 0]
            top_bid = max(bids, key=lambda x: x[1]) if bids else [0, 0]
            return {"short_risk": top_ask, "long_risk": top_bid}
        except: return {"short_risk": [0,0], "long_risk": [0,0]}

    def get_rekt_feed(self, exchange_type="CEX"):
        try:
            if exchange_type == "CEX":
                liquidations = self.binance.fapiPublicGetAllForceOrders()
                df = pd.DataFrame(liquidations)
            else: # Hyperliquid DEX
                trades = self.hyperliquid.fetch_trades('BTC/USDT', limit=50)
                df = pd.DataFrame(trades) # Note: HL requires specific info parsing for liqs
            
            if not df.empty:
                df['price'] = df['price'].astype(float)
                df['origQty'] = df.get('origQty', df.get('amount')).astype(float)
                return df[['symbol', 'side', 'price', 'origQty', 'time']].head(5)
            return pd.DataFrame()
        except: return pd.DataFrame()