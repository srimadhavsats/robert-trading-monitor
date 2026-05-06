from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import ccxt.async_support as ccxt
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Add a Health Check to verify the URL is reachable
@app.get("/")
async def health_check():
    return {"status": "Backend is Online"}

exchange = ccxt.binance()

@app.websocket("/ws/price/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()
    print(f"✅ Client connected for {symbol}")
    try:
        while True:
            clean_symbol = symbol.replace("-", "/")
            ticker = await exchange.fetch_ticker(clean_symbol)
            
            payload = {
                "symbol": ticker['symbol'],
                "price": ticker['last'],
                "high": ticker['high'],
                "low": ticker['low']
            }
            
            await websocket.send_json(payload)
            await asyncio.sleep(0.1) # Slowed down to 1s for initial stability
            
    except WebSocketDisconnect:
        print(f"❌ Client disconnected")

# 2. Force Uvicorn to listen on 0.0.0.0
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)