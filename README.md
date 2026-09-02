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

## 🛠️ Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ (for UI)
- Graph database / storage (e.g., Neo4j, PostgreSQL, DuckDB)

### Setup
*(Detailed setup instructions will be updated as modules are developed)*

```bash
# Clone the repository
git clone https://github.com/Avaneesh008/SIH.git
cd SIH

# Setup backend & model dependencies
# cd backend && pip install -r requirements.txt
```

---

## 📄 License
This project is developed for Smart India Hackathon (SIH). All rights reserved.
