# 🛡️ Sats Trading Monitor v3.0 | Magnet Sentinel

An institutional-grade cryptocurrency market sentinel and predictive visualization suite. Developed for high-precision monitoring, this version transitions from reactive charting to a proactive **Divergence Engine**, utilizing **Liquidity Magnets** and **CVD (Cumulative Volume Delta)** to identify market traps in real-time.

## 🚀 Key Features

### **Architecture & Efficiency**
*   **Multi-Page Sentinel System:** Dedicated environments for Institutional (CEX) and On-Chain (DEX) liquidity monitoring.
*   **Shared UI Engine (DRY):** A unified component architecture that ensures visual consistency and high maintainability across all exchange pages.
*   **Arch Linux Native:** Fully optimized for high-speed performance on **Arch Linux (Xfce)** with minimal system overhead.

### **Market Intelligence**
*   **Liquidity Magnets:** Real-time detection of high-volume limit order clusters within a **1%** price range to identify potential "snap" points.
*   **CVD Aggression Tracking:** Integrated volume delta visualization to monitor aggressive market buying vs. selling pressure.
*   **Divergence Alert System:** Proactive flagging of **Bullish Absorption** (limit order absorption) and **Bearish Fakeouts**.

### **Operational Logging**
*   **System Audit Log:** Persistent real-time record of all price actions, volatility status, and system ticks.
*   **Past Liquidations Ledger:** Session-based historical tracking of every detected liquidation event (REKT trades).

## 🛠 Tech Stack
*   **Frontend:** Streamlit with multi-page routing.
*   **Backend:** Python 3.12+ & CCXT (Unified Exchange API).
*   **Analytics:** Plotly for high-fidelity Liquidity Depth and Volume Delta charts.
*   **Indicators:** Integrated TradingView suite for EMA, SMA, RSI, and MACD analysis.

## 📦 Quick Start
1.  **Clone the Repository:**
    ```
    git clone https://github.com/srimadhavsats/sats-trading-monitor.git
    cd sats-trading-monitor
    ```
2.  **Initialize Virtual Environment:**
    ```
    python3 -m venv .venv && source .venv/bin/activate
    ```
3.  **Install Production Dependencies:**
    ```
    pip install -r requirements.txt
    ```
4.  **Launch the Suite:**
    ```
    streamlit run cex.py
    ```

## 📊 Repository Structure
| File | Role | Description |
| :--- | :--- | :--- |
| **`cex.py`** | **CEX Gateway** | Main entry point for Institutional Sentinel (Binance/Kraken). |
| **`pages/dex.py`** | **DEX Gateway** | Specialized monitoring for Hyperliquid L1 order flow. |
| **`ui_layout.py`** | **Shared UI** | Unified component rendering charts, magnets, and analytics. |
| **`liquidations.py`** | **Data Engine** | Core logic for fetching order books, trades, and liquidation feeds. |
| **`charts.py`** | **Visualizer** | Specialized module for high-performance financial widgets. |

## 🛠 Strategic Roadmap
*   [ ] **Solidity Signal Layer:** Integrating custom smart contracts to monitor whale wallet movements via on-chain events.
*   [ ] **One-Click Execution:** Direct exchange API integration for rapid trade entry from Magnet alerts.
*   [ ] **TUI Port:** A lightweight Terminal User Interface version for pure system-level terminal monitoring.

## ⚖️ License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### **Usage Terms:**
*   **Permissions:** You are free to use, modify, and distribute this software for personal or commercial purposes.
*   **Conditions:** You must include the original copyright notice and permission notice in any substantial portion of the software.
*   **Liability:** The software is provided "as is", without warranty of any kind. As this is a financial monitoring tool, the author is not responsible for any trading losses incurred.