# ====================================================================
# SATS Sentinel v4.1 - Telemetry & System Logging Utility
# ====================================================================


class SentinelLogger:
    @staticmethod
    def startup(message: str):
        """Logs system initialization sequences."""
        print(f"⚡ SYSTEM STARTUP: {message}", flush=True)

    @staticmethod
    def broadcast(symbol: str, price: float):
        """Logs successful WebSocket payload dispatches."""
        print(f"✅ BROADCAST [{symbol}]: ${price:,.2f}", flush=True)

    @staticmethod
    def info(message: str):
        """Logs standard network and lifecycle events."""
        print(f"ℹ️ TELEMETRY INFO: {message}", flush=True)

    @staticmethod
    def error(message: str):
        """Logs internal pipeline telemetry exceptions and edge connection errors."""
        print(f"❌ PIPELINE ERROR: {message}", flush=True)
