# 🛡️ Sats Trading Monitor v2.3 | Market Sentinel

An institutional-grade cryptocurrency market monitor and real-time dashboard. This project provides a "single-pane-of-glass" view for high-speed trading environments, featuring a flicker-free web interface and automated environment management.

## 🚀 Key Features
*   **Real-Time Web Dashboard:** A Streamlit-powered frontend for sub-second visual updates across BTC, ETH, and SOL.
*   **Fixed-Frame UI Architecture:** Utilizes master placeholders to ensure a stationary, professional dashboard experience without annoying page scrolling.
*   **Unified API Integration:** Connects to global exchanges via the CCXT library for reliable, real-time price fetching.
*   **Production-Ready Repository:** Optimized with a comprehensive `.gitignore` and `requirements.txt` for one-command deployment.
*   **Future-Proof Syntax:** Fully updated for 2026 library standards, utilizing the latest `width='stretch'` parameters for responsive design.

## 🛠 Tech Stack
*   **Frontend:** Streamlit (v2.x+)
*   **Backend:** Python 3.12+ & CCXT
*   **Data Handling:** Pandas for real-time audit logging
*   **Environment:** Arch Linux / GitHub Codespaces

## 📦 Quick Start
To get the Market Sentinel online in a fresh environment, run these commands:

1.  **Clone the Repository:**
    ```
    git clone https://github.com/srimadhavsats/sats-trading-monitor.git
    cd sats-trading-monitor
    ```

2.  **Initialize the Environment:**
    ```
    python3 -m venv .venv && source .venv/bin/activate
    ```

3.  **Automated Dependency Installation:**
    ```
    pip install -r requirements.txt
    ```

4.  **Launch the Dashboard:**
    ```
    streamlit run app.py
    ```

## 📊 Repository Structure
| File | Description |
|-----------|-------------|
| `app.py` | Main Streamlit dashboard with "fixed-frame" UI logic. |
| `monitor.py` | Original CLI-based market monitor with CSV logging. |
| `requirements.txt` | Automated list of necessary Python libraries. |
| `.gitignore` | Configured to block environment junk (13,000+ files) and CSVs. |

## 🛠 Future Roadmap
*   [ ] **Volatility Heatmaps:** Visual color triggers for 1% - 5% price swings.
*   [ ] **Multi-Exchange Aggregation:** Comparison of spreads between Binance and Coinbase.
*   [ ] **Telegram Webhooks:** Instant alerts sent directly to your mobile device.


