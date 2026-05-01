# 🛡️ Sats Trading Monitor v2.4 | Command Center

An institutional-grade cryptocurrency market sentinel and real-time visualization suite developed for high-precision monitoring. This version introduces a **Modular Architecture**, decoupling the high-speed data engine from the financial visualization layer to ensure maximum stability and maintainability.

## 🚀 Key Features
*   **Modular Architecture:** Separated into a core data engine (`monitor.py`) and a visualization library (`charts.py`) for clean, scalable development.
*   **Simultaneous Multi-Asset Dashboard:** Real-time, side-by-side view of BTC, ETH, and SOL without the need for manual tab switching.
*   **Integrated Technical Suite:** Automated injection of Moving Averages (EMA/SMA), RSI, and MACD indicators via industry-standard TradingView widgets.
*   **Persistent Live Audit Ledger:** A session-state persistent log that records every market movement, providing a verifiable "paper trail" for all price actions.
*   **2026 Standard Compliance:** Fully optimized for late-2026 library syntax, including `width='stretch'` responsive dataframes and secure HTML injection protocols.
*   **Built on Industry Experience:** Designed by a participant with cryptocurrency market experience dating back to 2012-2013.

## 🛠 Tech Stack
*   **Frontend:** Streamlit (v2.x+).
*   **Backend:** Python 3.12+ & CCXT (Unified Exchange API).
*   **Data Handling:** Pandas for real-time ledger management.
*   **Visuals:** TradingView Advanced Charts Integration.
*   **Environment:** Arch Linux - Xfce / GitHub Codespaces.

## 📦 Quick Start
To deploy the Command Center in a fresh environment, execute the following:

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
    streamlit run monitor.py
    ```

## 📊 Repository Structure
| File | Role | Description |
|-----------|-----------|-------------|
| **`monitor.py`** | **Engine** | Main entry point handling CCXT data streams, volatility logic, and state management. |
| **`charts.py`** | **Visuals** | Specialized module for rendering high-performance financial widgets and indicators. |
| `requirements.txt` | **Dependencies** | Automated list of production-ready Python libraries. |
| `.gitignore` | **Cleanliness** | Configured to exclude virtual environments, system junk, and local data logs. |

## 🛠 Strategic Roadmap
*   [ ] **FastAPI Integration:** Transition to a decoupled React/FastAPI stack for higher-frequency data throughput.
*   [ ] **On-Chain Signal Layer:** Integrating custom Solidity events to monitor specific whale wallet movements.
*   [ ] **Custom Price Alerts:** Triggering system notifications when volatility thresholds (1%+) are breached.
