import ccxt.async_support as ccxt
import asyncio
import csv
import os  # Added to clear the terminal
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
    # Write header only if file is brand new
    if not os.path.exists(log_file) or os.stat(log_file).st_size == 0:
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Asset', 'Price', 'Change %', 'Status'])

    try:
        while True:
            # --- DASHBOARD HEADER ---
            os.system('clear') # Clears the terminal screen
            print("="*60)
            print(f" ROBERT TRADING DESK | LIVE MONITOR | {datetime.now().strftime('%Y-%m-%d')}")
            print("="*60)
            print(f"{'ASSET':<12} | {'PRICE':<12} | {'CHANGE':<10} | {'STATUS'}")
            print("-"*60)

            with open(log_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                
                for symbol in symbols:
                    current_price = await fetch_price(symbol)
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    status = 'STABLE'
                    change_pct = 0.0

                    if last_prices[symbol] is not None:
                        change_pct = ((current_price - last_prices[symbol]) / last_prices[symbol]) * 100
                        if abs(change_pct) > 0.005: # Sensitivity set to 0.005% for testing
                            status = '!! VOLATILE !!'

                    # Formatting for the Dashboard
                    color = "\033[91m" if status == '!! VOLATILE !!' else "\033[92m"
                    reset = "\033[0m"
                    
                    # Print Dashboard Row
                    print(f"{symbol:<12} | ${current_price:<11,.2f} | {color}{change_pct:>+8.4f}%{reset} | {color}{status}{reset}")

                    # Log to CSV
                    writer.writerow([timestamp, symbol, current_price, f"{change_pct:.4f}%", status])
                    last_prices[symbol] = current_price
                
                file.flush()
            
            print("="*60)
            print(f" Last Update: {datetime.now().strftime('%H:%M:%S')} | Logging Active...")
            await asyncio.sleep(2)

    except Exception as e:
        print(f"\n[!] System Error: {e}")
    finally:
        await exchange.close()

if __name__ == "__main__":
    asyncio.run(monitor_desk())
