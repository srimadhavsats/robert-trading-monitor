# 🛡️ SATS Sentinel v4.1 | High-Frequency Market Monitor

A professional-grade cryptocurrency market sentinel and predictive visualization suite. Version 4.1 represents a critical advancement in data availability, transitioning from monolithic polling to a **Real-Time WebSocket Stream** with a custom **Stealth Oracle** designed for resilient global data access.

## 🏗 Architecture & Efficiency

The system is engineered for sub-second latency and high uptime, optimized for high-performance development environments like **Arch Linux**.

* **Decoupled High-Frequency Engine:** Complete separation of the data processing backbone (FastAPI) and the high-performance visualization layer (React).
* **Stealth Oracle Pipeline:** Implemented a custom `httpx` polling mechanism with browser-mimicking headers to access global exchange mirrors, ensuring uninterrupted data flow even in restricted network regions.
* **State-Aware Frontend:** React components are built with rigorous mount guards and cleanup routines to manage WebSocket lifecycles, preventing memory leaks and connection instability.
* **Standardized Local Infrastructure:** Services are strictly mapped to `127.0.0.1` and dedicated ports (8000 for Backend, 5174 for Frontend) to eliminate DNS overhead and ensure secure local communication.

## 🚀 Key Features

### **Market Intelligence**

* **Whale Impulse Tracking:** Real-time monitoring of BTC and major asset price movements against institutional volume thresholds.
* **Resilient Data Uplink:** Fail-safe connection logic that automatically identifies and switches to optimal global mirrors if primary endpoints face latency or restrictions.
* **Live Session Analytics:** Dynamic tracking of session-specific highs, lows, and price velocity directly within the streaming feed.

### **Advanced Visualizations**

* **Liquid Momentum Charts:** Predictive SVG-based charting that visualizes price trends with sub-second responsiveness.
* **Network Friction Monitoring:** Integrated tracking of network fees and synchronization latency to ensure data integrity.

## 🛠 Tech Stack

| Layer | Technology |
| --- | --- |
| **Frontend** | React 19, Vite, Tailwind CSS 4.0 |
| **Backend** | FastAPI, Uvicorn, Python 3.12+, httpx |
| **Data Oracle** | Bybit Global Mirror API |
| **Environment** | Arch Linux Xfce / Zed Editor |

## 📦 Quick Start

### 1. Initialize Backend (The Oracle)

```bash
cd backend
pip install -r ../requirements.txt
fastapi dev main.py --reload-dir .

```

*The API serves data via WebSockets at ws://127.0.0.1:8000.*

### 2. Initialize Frontend (The Dashboard)

```bash
cd frontend
npm install
npm run dev

```

*The dashboard is standardized to [http://127.0.0.1:5174](https://www.google.com/search?q=http://127.0.0.1:5174).*

## 📊 Repository Structure

| Directory/File | Role | Description |
| --- | --- | --- |
| **`backend/`** | **Data Engine** | FastAPI server handling asynchronous API polling and WebSocket streams. |
| **`frontend/`** | **UI Shell** | React dashboard with high-frequency charting and mount-guarded components. |
| **`.env.example`** | **Config Map** | Template for standardizing environment variables and port mappings. |
| **`requirements.txt`** | **Dependencies** | Optimized backend library list including `fastapi` and `httpx`. |

## 🛠 Strategic Roadmap

* [x] **v4.0:** Migrate from Streamlit to React/FastAPI decoupled architecture.
* [x] **v4.1:** Implementation of WebSockets, Stealth Oracle, and Frontend mount-guards.
* [ ] **Institutional Signal Layer:** Integration of custom smart contract event listeners for on-chain whale movement detection.
* [ ] **TUI Port:** A lightweight Terminal User Interface version for pure system-level terminal monitoring.

## ⚖️ License

This project is licensed under the **MIT License** - see the [LICENSE](https://github.com/srimadhavsats/sats-trading-monitor/blob/main/LICENSE) file for details.

> **Disclaimer:** This is a financial monitoring tool designed for technical analysis and market observation. Trading involves significant risk, and the author is not responsible for any financial losses incurred through the use of this software. Always verify market signals through multiple independent data points.
