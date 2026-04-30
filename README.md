
# Sats Trading Monitor v1.4 | Live Execution Monitor

An institutional-grade cryptocurrency market monitor designed for high-speed trading environments. This tool provides real-time asset tracking across multiple symbols with integrated volatility alerting and automated CSV logging for audit compliance.

## 🚀 Features
- **Asynchronous Execution:** Built with `asyncio` for non-blocking, sub-second market data retrieval[cite: 1].
- **Unified API Integration:** Utilizes the CCXT library to connect seamlessly with global exchanges like Binance[cite: 1].
- **Proactive Volatility Alerts:** Real-time calculation of price change percentages with visual "High Volatility" triggers.
- **Flicker-Free Dashboard:** Custom UI implemented with ANSI escape sequences for a stationary, professional terminal experience.
- **Automated Audit Trail:** Real-time logging of every market tick to an Excel-compatible CSV format for accurate record-keeping.

## 🛠 Tech Stack
- **Language:** Python 3.10+
- **Library:** [CCXT (CryptoCurrency eXchange Trading Library)](https://github.com/ccxt/ccxt)[cite: 1]
- **Concurrency:** Python `asyncio`[cite: 1]
- **Environment:** GitHub Codespaces / Linux

## 📦 Prerequisites
Ensure you have Python 3 installed. The following library is required:
```bash
pip install ccxt
```

## 🚦 Usage
1. Clone this repository.
2. Launch your terminal.
3. Run the monitor:
   ```
   bash
   python3 monitor.py
   ```

## 📊 Data Structure
The monitor automatically generates `trading_records.csv` with the following schema:
| Timestamp | Asset | Price | Change % | Status |
|-----------|-------|-------|----------|--------|
| HH:MM:SS  | BTC/USDT| 76,000| +0.02%   | STABLE |

## 🛠 Future Roadmap
- [ ] Integration of Private API keys for real-time order tracking.
- [ ] Telegram/Discord Webhook integration for remote volatility alerts.
- [ ] Support for 10+ simultaneous asset "baskets."
