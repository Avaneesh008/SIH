# SIH26182 - Crypto Wallet Attribution Engine

An intelligent on-chain analytics and machine learning system for attributing cryptocurrency wallet addresses to known entities, behavior clusters, and risk categories.

---

## 📌 Project Overview

**Problem Statement ID:** SIH26182  
**Theme:** Blockchain / Cyber Security / AI-ML  
**Goal:** Develop an end-to-end framework to analyze on-chain transaction graphs, extract temporal & structural graph features, and accurately attribute pseudonymous crypto wallets to real-world entities (Exchanges, Miners, Mixers/Tornadocash, Scam/Phishing, DeFi protocols, Darknet Markets, etc.).

---

## 📁 Repository Structure

```tree
.
├── backend/          # Backend API services, ingestion pipelines & graph query engine
├── data/             # Dataset specifications, preprocessing scripts & sample transaction graphs
├── docs/             # Technical specifications, architecture diagrams & API documentation
├── model/            # GNN / ML attribution models, feature extraction pipelines & training scripts
├── ui/               # Web dashboard & interactive graph visualization interface
├── .gitignore        # Git ignore rules for environments, data & build artifacts
└── README.md         # Project documentation
```

---

## 🚀 Key Modules

- **`/data`**: Handles on-chain data collection (Etherscan, Bitcoin RPC, Graph Protocol, Dune), parsing raw transaction ledgers, address label normalization, and sub-graph sampling.
- **`/model`**: Graph Neural Networks (e.g., RGCN, GraphSAGE, GAT), heuristics-based clustering, and behavioral feature engineering for entity resolution and risk scoring.
- **`/backend`**: High-performance REST / WebSocket APIs for querying wallet risk scores, trace paths, and real-time transaction monitoring.
- **`/ui`**: Modern, interactive visual graph explorer and investigative dashboard for forensic analysis.
- **`/docs`**: Solution architecture, mathematical formulations, API reference, and evaluation benchmarks.

---

## 🛠️ Getting Started & Integration Run Guide

### Prerequisites
- Python 3.10+
- Virtual environment with dependencies installed:
  ```bash
  pip install fastapi uvicorn streamlit requests pandas networkx scikit-learn joblib
  ```

### ⚙️ Environment Variables & Configuration

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `API_BASE_URL` / `BACKEND_API_URL` | `http://localhost:8000` | Base URL used by the Streamlit frontend to connect to the FastAPI backend. |
| `CORS_ORIGINS` | `*` | Allowed CORS origins for the backend (e.g. `http://localhost:8501,http://127.0.0.1:8501` for production). |

---

### 🚀 Running the System

#### 1. Start the FastAPI Backend
From the repository root:
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Health Check: `http://localhost:8000/health`
- Interactive API Docs (Swagger UI): `http://localhost:8000/docs`

#### 2. Start the Streamlit Frontend
In a separate terminal from the repository root:
```bash
streamlit run ui/app.py --server.port 8501
```
- Open your browser at `http://localhost:8501`

---

### 🧪 Local End-to-End Testing Steps

1. **Verify Valid Wallet Attribution:**
   - In the search bar on `http://localhost:8501`, enter a valid wallet address or dataset transaction ID (e.g., `0xd90e2f925da726b50c4ed8d0fb90ad053324f31b` or `230425980`).
   - Click **Analyze**.
   - Verify that the dashboard renders the **Risk Score**, **Risk Classification** (`Illicit` / `Licit`), **Nearest VASP Name**, **Graph Hops**, **Confidence Level**, and **Top Influencing Features**.

2. **Verify 404 Graceful Error Handling:**
   - In the search bar, enter a non-existent identifier such as `non_existent_wallet_99999`.
   - Click **Analyze**.
   - Verify that a clear, user-friendly 404 error banner is displayed without crashing the UI.

---

## 📄 License
This project is developed for Smart India Hackathon (SIH). All rights reserved.

