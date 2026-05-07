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
            
            # 1. Fetch Ticker and Deep Order Book
            ticker = await exchange.fetch_ticker(clean_symbol)
            order_book = await exchange.fetch_order_book(clean_symbol, limit=50)
            
            # 2. Identify the "Supply Zones" (Top 5 largest Ask volumes)
            # We sort the 'asks' by volume (index 1) and take the top 5
            top_asks = sorted(order_book['asks'], key=lambda x: x[1], reverse=True)[:5]

            payload = {
                "symbol": ticker['symbol'],
                "price": ticker['last'],
                # Map walls to a simple list of price and volume
                "walls": [{"price": wall[0], "volume": wall[1]} for wall in top_asks],
                "timestamp": ticker['timestamp']
            }
            
            await websocket.send_json(payload)
            
            # 3. Match sleep to Frontend transition (1 second)
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")