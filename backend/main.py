import asyncio

import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# 1. RESTORE ORIGINAL PROJECT LOGIC
try:
    from ui_layout import WHALE_THRESHOLDS
except ImportError:
    # Default fallback for SATS Sentinel v4.1
    WHALE_THRESHOLDS = {"BTC/USDT": 0.1, "ETH/USDT": 1.0, "1000SATS/USDT": 500000.0}

app = FastAPI()

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BYBIT_API = "https://api.bybit.com/v5/market/tickers"


# 1. Health check to verify server connectivity
@app.get("/")
async def health_check():
    """Verify the backend is live in the browser."""
    return {
        "status": "Sentinel v4.1 Active",
        "message": "Oracle is ready for data requests",
    }


# 2. Initialization log for the SATS Oracle
@app.on_event("startup")
async def startup_event():
    print("⚡ SATS Sentinel v4.1: Streaming Oracle Online", flush=True)


# 3. Main WebSocket stream for real-time market data
@app.websocket("/ws/price/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()

    # Format symbol: BTC-USDT -> BTCUSDT for Bybit API
    api_symbol = symbol.replace("-", "")
    if "SATS" in api_symbol and "1000" not in api_symbol:
        api_symbol = f"1000{api_symbol}"

    # Headers to mimic a browser and bypass regional ISP blocks
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    try:
        print(f"🔗 Polling Data for {api_symbol}...", flush=True)

        async with httpx.AsyncClient(
            timeout=10.0, headers=headers, trust_env=True
        ) as client:
            while True:
                response = await client.get(
                    BYBIT_API, params={"category": "spot", "symbol": api_symbol}
                )

                if response.status_code == 200:
                    data = response.json()
                    result = data.get("result", {}).get("list", [{}])[0]

                    if result:
                        price = float(result.get("lastPrice", 0))
                        clean_key = symbol.replace("-", "/")
                        threshold = WHALE_THRESHOLDS.get(clean_key, 0)

                        payload = {
                            "symbol": clean_key,
                            "price": price,
                            "high": float(result.get("highPrice24h", 0)),
                            "low": float(result.get("lowPrice24h", 0)),
                            "volume": float(result.get("turnover24h", 0)),
                            "change": float(result.get("price24hPcnt", 0)) * 100,
                            "is_whale": price > threshold,
                            "whale_alert": price > threshold,
                        }

                        await websocket.send_json(payload)
                        print(f"✅ Sent {clean_key}: ${price}", flush=True)

                else:
                    print(f"❌ API Error: {response.status_code}", flush=True)

                await asyncio.sleep(1.0)  # 1-second heartbeat

    except WebSocketDisconnect:
        print(f"ℹ️ Frontend disconnected from {symbol}.", flush=True)
    except Exception as e:
        print(f"❌ Backend Error: {e}", flush=True)
