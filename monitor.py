import ccxt.async_support as ccxt
import asyncio
import csv
from datetime import datetime

# 1. Configuration
exchange = ccxt.binance()
symbols = ['BTC/USDT', 'ETH/USDT']
log_file = 'trading_records.csv'
last_prices = {symbol: None for symbol in symbols}

async def fetch_price(symbol):
    ticker = await exchange.fetch_ticker(symbol)
    return ticker['last']

async def monitor_desk():
    print(f"--- Robert Trading Desk: Live Execution Monitor ---")
    print(f"Monitoring: {', '.join(symbols)} | Logging to: {log_file}\n")

    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Timestamp', 'Asset', 'Price', 'Change %', 'Status'])

        try:
            while True:
                for symbol in symbols:
                    current_price = await fetch_price(symbol)
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    status = 'STABLE'
                    change_pct = 0.0

                    # Calculate Volatility Logic
                    if last_prices[symbol] is not None:
                        change_pct = ((current_price - last_prices[symbol]) / last_prices[symbol]) * 100
                        
                        # Alert if movement is more than 0.01% (#Adjust accordingly)
                        if abs(change_pct) > 0.01:
                            status = '!! VOLATILE !!'

                    # Terminal Output
                    alert_color = "\033[91m" if status == '!! VOLATILE !!' else "\033[92m"
                    reset_color = "\033[0m"
                    print(f"[{timestamp}] {symbol}: ${current_price:,.2f} | {alert_color}{change_pct:+.4f}% [{status}]{reset_color}")

                    # Log to CSV
                    writer.writerow([timestamp, symbol, current_price, f"{change_pct:.4f}%", status])
                    last_prices[symbol] = current_price
                
                file.flush()
                await asyncio.sleep(2) # Refresh every 2 seconds

        except Exception as e:
            print(f"System Error: {e}")
        finally:
            await exchange.close()

if __name__ == "__main__":
    asyncio.run(monitor_desk())
