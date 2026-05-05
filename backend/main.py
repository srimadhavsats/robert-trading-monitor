from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import time

# Initialize the FastAPI application instance.
app = FastAPI()

# Configure Cross-Origin Resource Sharing (CORS).
# This allows the React frontend to communicate with this API 
# across different ports or domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Root endpoint to verify that the API server is active.
    """
    return {"message": "Sats Trading Monitor API is online"}

@app.get("/api/v1/sentinel/price")
async def get_btc_price():
    """
    Endpoint to retrieve simulated real-time market data.
    Returns a JSON object containing asset details and volatility status.
    """
    # Generates a randomized price within a specific range for testing.
    # This simulates price movement without an external API connection.
    mock_price = 78000 + random.uniform(-50, 50)
    
    # Determines volatility status based on a random threshold.
    status = "STABLE" if random.random() > 0.2 else "!! VOLATILE !!"
    
    return {
        "symbol": "BTC/USDT",
        "price": round(mock_price, 2),
        "timestamp": time.time(),
        "status": status
    }

if __name__ == "__main__":
    import uvicorn
    # Launches the server on port 8000.
    # The host '0.0.0.0' ensures visibility within cloud environments like Codespaces.
    uvicorn.run(app, host="0.0.0.0", port=8000)