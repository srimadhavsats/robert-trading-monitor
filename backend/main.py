from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ccxt.async_support as ccxt
import time
from contextlib import asynccontextmanager

# Global variable to hold the exchange instance
exchange = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the lifecycle of the FastAPI application.
    Initializes the exchange connection on startup and closes it on shutdown.
    """
    global exchange
    # Initialize the Binance exchange instance with rate limiting enabled.
    exchange = ccxt.binance({
        'enableRateLimit': True,
    })
    yield
    # Closes the exchange connection to release resources.
    await exchange.close()

# Initialize the FastAPI application with the lifecycle manager.
app = FastAPI(lifespan=lifespan)

# Configure Cross-Origin Resource Sharing (CORS).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Root endpoint to verify server connectivity.
    """
    return {"message": "Sats Trading Monitor API is online"}

@app.get("/api/v1/sentinel/price")
async def get_btc_price():
    """
    Endpoint to retrieve live market data for BTC/USDT.
    Uses CCXT to fetch the current ticker from Binance.
    """
    try:
        # Fetches the current ticker data for the specified symbol.
        ticker = await exchange.fetch_ticker('BTC/USDT')
        
        # Extracts relevant fields from the unified CCXT response.
        return {
            "symbol": ticker['symbol'],
            "price": ticker['last'],
            "timestamp": ticker['timestamp'] / 1000, # Converts ms to seconds
            "status": "LIVE",
            "high": ticker['high'],
            "low": ticker['low'],
            "volume": ticker['quoteVolume']
        }
    except Exception as e:
        # Returns a 503 error if the exchange connection fails.
        raise HTTPException(status_code=503, detail=f"Exchange Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)