from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import ccxt.async_support as ccxt
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

exchange = ccxt.binance()

WHALE_THRESHOLDS = {
    "BTC/USDT": 0.1,
    "ETH/USDT": 5.0,
    "SATS/USDT": 1000000.0
}

async def get_mempool_fees():
    """Fetch Bitcoin network fees from mempool.space API"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://mempool.space/api/v1/fees/recommended", timeout=2.0)
            return response.json()
        except Exception:
            return {"fastestFee": 0, "halfHourFee": 0, "hourFee": 0}

@app.websocket("/ws/price/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()
    
    clean_symbol = symbol.replace("-", "/")
    threshold = WHALE_THRESHOLDS.get(clean_symbol, 0.1)
    
    try:
        while True:
            ticker_task = exchange.fetch_ticker(clean_symbol)
            order_book_task = exchange.fetch_order_book(clean_symbol, limit=20)
            trades_task = exchange.fetch_trades(clean_symbol, limit=10)
            mempool_task = get_mempool_fees()
            
            ticker, order_book, trades, fees = await asyncio.gather(
                ticker_task, order_book_task, trades_task, mempool_task
            )
            
            # Calculate Order Book Imbalance (Bid vs Ask Volume)
            total_bid_vol = sum(bid[1] for bid in order_book['bids'])
            total_ask_vol = sum(ask[1] for ask in order_book['asks'])
            imbalance = (total_bid_vol / (total_bid_vol + total_ask_vol)) * 100 if (total_bid_vol + total_ask_vol) > 0 else 50

            whale_trades = [
                {"amount": t['amount'], "side": t['side'], "price": t['price']} 
                for t in trades if t['amount'] >= threshold
            ]

            top_asks = sorted(order_book['asks'], key=lambda x: x[1], reverse=True)[:5]

            payload = {
                "symbol": ticker['symbol'],
                "price": ticker['last'],
                "walls": [{"price": wall[0], "volume": wall[1]} for wall in top_asks],
                "trades": whale_trades,
                "fees": fees,
                "imbalance": round(imbalance, 2), # New imbalance percentage
                "timestamp": ticker['timestamp']
            }
            
            await websocket.send_json(payload)
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected: {clean_symbol}")
    except Exception as e:
        print(f"Error: {e}")