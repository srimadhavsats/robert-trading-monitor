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
            
            # --- OPTIMIZATION: Parallel Fetching ---
            # Instead of waiting for one then the other, we fire both at once.
            ticker_task = exchange.fetch_ticker(clean_symbol)
            order_book_task = exchange.fetch_order_book(clean_symbol, limit=20) # Reduced from 50 to 20 for speed
            
            # Gather both results simultaneously
            ticker, order_book = await asyncio.gather(ticker_task, order_book_task)
            
            # Identify the "Supply Zones" (Top 5 largest Ask volumes)
            top_asks = sorted(order_book['asks'], key=lambda x: x[1], reverse=True)[:5]

            payload = {
                "symbol": ticker['symbol'],
                "price": ticker['last'],
                "walls": [{"price": wall[0], "volume": wall[1]} for wall in top_asks],
                "timestamp": ticker['timestamp']
            }
            
            await websocket.send_json(payload)
            
            # Keep the 1s sleep to match the smooth frontend flow
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")