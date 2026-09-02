# Run this with: uvicorn main:app --reload --port 8000
# Then visit http://localhost:8000/health in your browser

import os
import sys
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent

# Ensure local backend and model directories are importable
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(REPO_ROOT / "model") not in sys.path:
    sys.path.append(str(REPO_ROOT / "model"))

from graph_utils import build_graph, build_known_vasps, get_nearest_vasp

app = FastAPI(title="SIH26182 Crypto Wallet Risk Attribution API")

# Allow the Streamlit UI (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Candidate locations for model files (prefer model_v2.pkl if available, else model.pkl)
MODEL_V2_CANDIDATE_PATHS = [
    BASE_DIR / "model_v2.pkl",
    REPO_ROOT / "model" / "model_v2.pkl",
    REPO_ROOT / "model_v2.pkl",
    Path("model_v2.pkl"),
    Path("model") / "model_v2.pkl",
]

MODEL_CANDIDATE_PATHS = [
    BASE_DIR / "model.pkl",
    REPO_ROOT / "model" / "model.pkl",
    REPO_ROOT / "model.pkl",
    Path("model.pkl"),
    Path("model") / "model.pkl",
]

# Candidate locations for merged dataset
DATA_CANDIDATE_PATHS = [
    BASE_DIR / "merged_data.csv",
    REPO_ROOT / "data" / "merged_data.csv",
    REPO_ROOT / "model" / "merged_data.csv",
    REPO_ROOT / "merged_data.csv",
    Path("merged_data.csv"),
    Path("data") / "merged_data.csv",
    Path("model") / "merged_data.csv",
    # Fallback to merged_data_v2.csv if merged_data.csv is not found
    BASE_DIR / "merged_data_v2.csv",
    REPO_ROOT / "data" / "merged_data_v2.csv",
    REPO_ROOT / "model" / "merged_data_v2.csv",
    REPO_ROOT / "merged_data_v2.csv",
    Path("merged_data_v2.csv"),
    Path("data") / "merged_data_v2.csv",
    Path("model") / "merged_data_v2.csv",
]


def load_model():
    """Load model_v2.pkl if available, otherwise model.pkl using joblib."""
    for path in MODEL_V2_CANDIDATE_PATHS:
        if path.is_file():
            try:
                loaded = joblib.load(path)
                print(f"Loaded model_v2 from {path}")
                return loaded
            except Exception as e:
                print(f"Failed to load model from {path}: {e}")

    for path in MODEL_CANDIDATE_PATHS:
        if path.is_file():
            try:
                loaded = joblib.load(path)
                print(f"Loaded model from {path}")
                return loaded
            except Exception as e:
                print(f"Failed to load model from {path}: {e}")

    return None


def load_dataset():
    """Load merged_data.csv so features can be indexed and looked up by txId."""
    for path in DATA_CANDIDATE_PATHS:
        if path.is_file():
            try:
                df = pd.read_csv(path)
                if "txId" in df.columns:
                    df["txId"] = df["txId"].astype(str)
                    df = df[~df["txId"].duplicated(keep="first")]
                    df.set_index("txId", inplace=True)
                print(f"Loaded dataset from {path} with {len(df)} records.")
                return df
            except Exception as e:
                print(f"Failed to load dataset from {path}: {e}")
    return None


# Startup loading
model = load_model()
merged_df = load_dataset()
graph = build_graph()
known_vasps = build_known_vasps(graph) if graph is not None else {}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/score/{wallet_id}")
def get_score(wallet_id: str):
    global model, merged_df, graph, known_vasps

    # Attempt lazy re-load if files were added after process start
    if merged_df is None:
        merged_df = load_dataset()
    if model is None:
        model = load_model()
    if graph is None:
        graph = build_graph()
        if graph is not None:
            known_vasps = build_known_vasps(graph)

    if merged_df is None:
        raise HTTPException(
            status_code=500,
            detail="Dataset merged_data.csv is not loaded.",
        )

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Model is not loaded.",
        )

    wallet_key = str(wallet_id).strip()
    if wallet_key not in merged_df.index:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet ID '{wallet_id}' not found in dataset.",
        )

    wallet_row = merged_df.loc[wallet_key]
    if isinstance(wallet_row, pd.DataFrame):
        wallet_row = wallet_row.iloc[0]

    # Align input features with what the model expects
    if hasattr(model, "feature_names_in_"):
        feature_cols = list(model.feature_names_in_)
        features = wallet_row.reindex(feature_cols, fill_value=0.0)
        X = pd.DataFrame([features], columns=feature_cols)
    else:
        feature_cols = [c for c in wallet_row.index if c.startswith("feat_") or c == "time_step"]
        X = pd.DataFrame([wallet_row[feature_cols]])

    X = X.astype(float)

    # Predict class probabilities
    probs = model.predict_proba(X)[0]

    # Determine probability of illicit class
    classes = list(model.classes_)
    if "illicit" in classes:
        illicit_idx = classes.index("illicit")
    elif 1 in classes:
        illicit_idx = classes.index(1)
    elif "1" in classes:
        illicit_idx = classes.index("1")
    else:
        illicit_idx = 1 if len(probs) > 1 else 0

    illicit_prob = float(probs[illicit_idx])
    risk_score = round(illicit_prob, 3)
    risk_label = "illicit" if risk_score > 0.5 else "licit"

    # Nearest VASP attribution via graph BFS
    nearest_vasp_name, graph_hops, confidence = get_nearest_vasp(wallet_id, graph, known_vasps)
    if graph_hops is not None:
        confidence = "high" if graph_hops <= 2 else ("medium" if graph_hops <= 5 else "low")
    else:
        confidence = "low"

    # Top 3 most important features by model.feature_importances_
    top_features = []
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        if hasattr(model, "feature_names_in_"):
            feat_names = list(model.feature_names_in_)
        else:
            feat_names = feature_cols

        top_indices = importances.argsort()[::-1][:3]
        top_features = [str(feat_names[i]) for i in top_indices if i < len(feat_names)]

    # Match Step 0 JSON contract exactly
    return {
        "wallet_address": str(wallet_id),
        "risk_score": risk_score,
        "risk_label": risk_label,
        "graph_hops_to_nearest_vasp": graph_hops,
        "nearest_vasp_name": nearest_vasp_name,
        "attribution_confidence": confidence,
        "top_features": top_features,
    }