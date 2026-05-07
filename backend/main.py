from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import ccxt.async_support as ccxt
import time

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

exchange = ccxt.binance()

@app.websocket("/ws/price/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        while True:
            clean_symbol = symbol.replace("-", "/")
            
            # Fire THREE tasks at once now
            ticker_task = exchange.fetch_ticker(clean_symbol)
            order_book_task = exchange.fetch_order_book(clean_symbol, limit=20)
            trades_task = exchange.fetch_trades(clean_symbol, limit=10) # Get last 10 trades
            
            ticker, order_book, trades = await asyncio.gather(ticker_task, order_book_task, trades_task)
            
            # Filter for "Whale" trades (e.g., > 0.5 BTC or $40,000)
            # You can adjust this '0.5' based on the asset
            whale_trades = [
                {"amount": t['amount'], "side": t['side'], "price": t['price']} 
                for t in trades if t['amount'] >= 0.1 # Lowered to 0.1 BTC to see more activity for testing
            ]

            payload = {
                "symbol": ticker['symbol'],
                "price": ticker['last'],
                "walls": [{"price": wall[0], "volume": wall[1]} for wall in sorted(order_book['asks'], key=lambda x: x[1], reverse=True)[:5]],
                "trades": whale_trades, # New field for the Whale Tape
                "timestamp": ticker['timestamp']
            }
            
            await websocket.send_json(payload)
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")