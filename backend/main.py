from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import ccxt.async_support as ccxt
import httpx

app = FastAPI()

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize exchange client
exchange = ccxt.binance()

# Define asset-specific volume thresholds for whale trade filtering
WHALE_THRESHOLDS = {
    "BTC/USDT": 0.1,
    "ETH/USDT": 2.0,
    "SATS/USDT": 1000000.0
}

async def get_mempool_fees():
    """Fetch recommended Bitcoin network fees from mempool.space API"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://mempool.space/api/v1/fees/recommended", timeout=2.0)
            return response.json()
        except Exception:
            return {"fastestFee": 0, "halfHourFee": 0, "hourFee": 0}

@app.websocket("/ws/price/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()
    
    # Format symbol and identify corresponding whale threshold
    clean_symbol = symbol.replace("-", "/")
    threshold = WHALE_THRESHOLDS.get(clean_symbol, 0.1)
    
    try:
        while True:
            # Define concurrent data fetching tasks
            ticker_task = exchange.fetch_ticker(clean_symbol)
            order_book_task = exchange.fetch_order_book(clean_symbol, limit=20)
            trades_task = exchange.fetch_trades(clean_symbol, limit=10)
            mempool_task = get_mempool_fees()
            
            # Execute tasks concurrently
            ticker, order_book, trades, fees = await asyncio.gather(
                ticker_task, 
                order_book_task, 
                trades_task, 
                mempool_task
            )
            
            # Filter trades using asset-specific threshold
            whale_trades = [
                {"amount": t['amount'], "side": t['side'], "price": t['price']} 
                for t in trades if t['amount'] >= threshold
            ]

            # Extract top 5 sell orders by volume
            top_asks = sorted(order_book['asks'], key=lambda x: x[1], reverse=True)[:5]

            # Prepare data payload
            payload = {
                "symbol": ticker['symbol'],
                "price": ticker['last'],
                "walls": [{"price": wall[0], "volume": wall[1]} for wall in top_asks],
                "trades": whale_trades,
                "fees": fees,
                "timestamp": ticker['timestamp']
            }
            
            # Transmit payload to client
            await websocket.send_json(payload)
            
            # Sync with frontend transition interval
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for {clean_symbol}")
    except Exception as e:
        print(f"Error encountered on {clean_symbol}: {e}")