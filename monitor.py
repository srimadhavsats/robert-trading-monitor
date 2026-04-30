import ccxt.async_support as ccxt
import asyncio
import csv
import os
import sys
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
    # Initial setup
    os.system('clear')
    
    if not os.path.exists(log_file) or os.stat(log_file).st_size == 0:
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Asset', 'Price', 'Change %', 'Status'])

    try:
        while True:
            # Move cursor to top-left
            sys.stdout.write("\033[H")
            
            # \033[K is the magic "Clear to end of line" command
            clear_line = "\033[K"

            print(f"{'='*60}{clear_line}")
            print(f" ROBERT TRADING DESK | LIVE MONITOR | {datetime.now().strftime('%Y-%m-%d')}{clear_line}")
            print(f"{'='*60}{clear_line}")
            print(f"{'ASSET':<12} | {'PRICE':<12} | {'CHANGE':<10} | {'STATUS'}{clear_line}")
            print(f"{'-'*60}{clear_line}")

            with open(log_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                
                for symbol in symbols:
                    current_price = await fetch_price(symbol)
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    status = 'STABLE'
                    change_pct = 0.0

                    if last_prices[symbol] is not None:
                        change_pct = ((current_price - last_prices[symbol]) / last_prices[symbol]) * 100
                        if abs(change_pct) > 0.005: 
                            status = '!! VOLATILE !!'

                    color = "\033[91m" if status == '!! VOLATILE !!' else "\033[92m"
                    reset = "\033[0m"
                    
                    # Apply clear_line at the very end of the string, after the reset color
                    print(f"{symbol:<12} | ${current_price:<11,.2f} | {color}{change_pct:>+8.4f}%{reset} | {color}{status}{reset}{clear_line}")

                    writer.writerow([timestamp, symbol, current_price, f"{change_pct:.4f}%", status])
                    last_prices[symbol] = current_price
                
                file.flush()
            
            print(f"{'='*60}{clear_line}")
            print(f" Last Update: {datetime.now().strftime('%H:%M:%S')} | Logging Active...{clear_line}")
            
            sys.stdout.flush()
            await asyncio.sleep(2)

    except Exception as e:
        print(f"\n[!] System Error: {e}")
    finally:
        await exchange.close()

if __name__ == "__main__":
    asyncio.run(monitor_desk())