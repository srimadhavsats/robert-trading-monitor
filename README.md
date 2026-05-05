# 🛡️ Sats Trading Monitor v4.0 | Magnet Sentinel

An institutional-grade cryptocurrency market sentinel and predictive visualization suite. Version 4.0 marks the transition from a monolithic architecture to a **Decoupled Full-Stack System**, utilizing a **FastAPI** backend for high-frequency data processing and a **React** frontend for a high-performance, responsive trading interface.

## 🏗 Architecture & Efficiency

The suite has been rebuilt to ensure sub-second latency and system modularity, specifically optimized for **Arch Linux (Xfce)** environments.

*   **Decoupled Engine:** Complete separation of the "Brain" (Python/FastAPI) and the "Face" (React/Vite).
*   **Asynchronous Data Pipeline:** Utilizes `ccxt.async_support` for non-blocking, real-time market data aggregation.
*   **Modular Component Architecture:** Independent UI components (Price Cards, Liquidity Tables, Charts) that communicate via a standardized JSON API.
*   **Cloud & Native Ready:** Fully compatible with GitHub Codespaces for remote development and local Arch Linux setups for maximum performance.

## 🚀 Key Features

### **Market Intelligence**
*   **Liquidity Magnets:** Real-time detection of high-volume limit order clusters within a **1%** price range to identify potential "snap" points.
*   **CVD Aggression Tracking:** Monitoring aggressive market buying vs. selling pressure to identify absorption levels.
*   **Divergence Engine:** Proactive flagging of **Bullish Absorption** and **Bearish Fakeouts** by correlating order book depth with volume delta.

### **On-Chain Readiness (In Development)**
*   **Whale Signal Listeners:** Integration architecture for **Solidity/Foundry** events to monitor massive exchange inflows and outflows.
*   **Liquidation "Magnets":** Monitoring lending protocol health factors to identify high-probability liquidation zones on-chain.

## 🛠 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 18, Vite, Axios |
| **Backend** | FastAPI, Uvicorn, Python 3.12+ |
| **Market Data** | CCXT (Asynchronous Exchange API) |
| **Environment** | Arch Linux Xfce / GitHub Codespaces |

## 📦 Quick Start

### 1. Initialize Backend (The Engine)
```
cd backend
pip install -r ../requirements.txt
python main.py
```
*The API serves data at http://localhost:8000.*

### 2. Initialize Frontend (The Dashboard)
```
cd frontend
npm install
npm run dev
```
*The dashboard is accessible via http://localhost:5173.*

## 📊 Repository Structure

| Directory/File | Role | Description |
| :--- | :--- | :--- |
| **`backend/`** | **Data Engine** | FastAPI server handling CCXT integration and market logic. |
| **`frontend/`** | **UI Shell** | React application providing the visualization dashboard. |
| **`contracts/`** | **On-Chain Logic** | Foundry/Solidity workspace for whale and liquidity monitoring. |
| **`requirements.txt`**| **Dependencies** | Unified list of Python libraries for the backend. |

## 🛠 Strategic Roadmap

*   [x] **v4.0:** Migrate from Streamlit to React/FastAPI and integrate live CCXT data.
*   [ ] Implement **Tailwind CSS** for a professional Dark Mode UI.
*   [ ] Transition from polling to **WebSockets** for zero-latency updates.
*   [ ] **Solidity Signal Layer:** Integrating custom smart contracts to monitor whale wallet movements via on-chain events.
*   [ ] **One-Click Execution:** Direct exchange API integration for rapid trade entry from Magnet alerts.
*   [ ] **TUI Port:** A lightweight Terminal User Interface version for pure system-level terminal monitoring.

## ⚖️ License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### **Usage Terms:**
*   **Permissions:** You are free to use, modify, and distribute this software for personal or commercial purposes.
*   **Conditions:** You must include the original copyright notice and permission notice in any substantial portion of the software.
*   **Liability:** The software is provided "as is", without warranty of any kind. As this is a financial monitoring tool, the author is not responsible for any trading losses incurred.

> **Note:** This is a financial monitoring tool. The author is not responsible for any trading losses incurred. Always verify signals through multiple data points before execution.