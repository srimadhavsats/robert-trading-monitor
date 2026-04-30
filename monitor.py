import ccxt.async_support as ccxt
import asyncio
import csv
from datetime import datetime

# 1. Setup the Exchange (Binance Public - No API keys needed for price monitoring)
exchange = ccxt.binance()
symbol = 'BTC/USDT'
log_file = 'trading_records.csv'

async def monitor_and_log():
    print(f"--- Robert Trading Assistant: Monitoring {symbol} ---")
    print(f"Logging data to: {log_file}")

    # Create the CSV file and write the header if it doesn't exist
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Check if file is new to write header
        if file.tell() == 0:
            writer.writerow(['Timestamp', 'Asset', 'Price', 'Status'])

        try:
            while True:
                # A. The "Waiter" Request (Non-blocking)
                ticker = await exchange.fetch_ticker(symbol)
                price = ticker['last']
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # B. Terminal Output (Visual Trend Monitoring)
                print(f"[{timestamp}] {symbol}: ${price:,.2f}")

                # C. The "Records" Logic (Excel-ready Logging)
                writer.writerow([timestamp, symbol, price, 'MONITORING'])
                file.flush() # Forces the data to save immediately

                # Wait 2 seconds before the next update
                await asyncio.sleep(2)

        except Exception as e:
            print(f"Connection Error: {e}")
        finally:
            await exchange.close()

if __name__ == "__main__":
    asyncio.run(monitor_and_log())