import os
import sys
import json
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

# Configurable CORS origins for development and production deployment
cors_origins_env = os.getenv("CORS_ORIGINS", "*")
if cors_origins_env == "*":
    allow_origins = ["*"]
else:
    allow_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
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

# Candidate locations for merged dataset and mock files
DATA_CANDIDATE_PATHS = [
    BASE_DIR / "merged_data.csv",
    REPO_ROOT / "data" / "merged_data.csv",
    REPO_ROOT / "model" / "merged_data.csv",
    REPO_ROOT / "merged_data.csv",
    Path("merged_data.csv"),
    Path("data") / "merged_data.csv",
    Path("model") / "merged_data.csv",
    BASE_DIR / "merged_data_v2.csv",
    REPO_ROOT / "data" / "merged_data_v2.csv",
    REPO_ROOT / "model" / "merged_data_v2.csv",
    REPO_ROOT / "merged_data_v2.csv",
    Path("merged_data_v2.csv"),
    Path("data") / "merged_data_v2.csv",
    Path("model") / "merged_data_v2.csv",
]

MOCK_CANDIDATE_PATHS = [
    REPO_ROOT / "mock_response.json",
    BASE_DIR / "mock_response.json",
    REPO_ROOT / "data" / "mock_response.json",
    Path("mock_response.json"),
]

CLASSES_CANDIDATE_PATHS = [
    REPO_ROOT / "data" / "elliptic_txs_classes.csv",
    BASE_DIR / "data" / "elliptic_txs_classes.csv",
    Path("data") / "elliptic_txs_classes.csv",
    Path("elliptic_txs_classes.csv"),
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


def load_mock_responses():
    """Load predefined mock responses if available."""
    for path in MOCK_CANDIDATE_PATHS:
        if path.is_file():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    mock_dict = {str(item.get("wallet_address")).strip(): item for item in data if "wallet_address" in item}
                    print(f"Loaded {len(mock_dict)} mock responses from {path}")
                    return mock_dict
            except Exception as e:
                print(f"Failed to load mock responses from {path}: {e}")
    return {}


def load_dataset():
    """Load merged_data.csv or fallback to elliptic_txs_classes.csv so features can be indexed and looked up by txId."""
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

    # Fallback to elliptic_txs_classes.csv if merged_data.csv has not been generated yet
    for path in CLASSES_CANDIDATE_PATHS:
        if path.is_file():
            try:
                df = pd.read_csv(path)
                if "txId" in df.columns:
                    df["txId"] = df["txId"].astype(str)
                    df = df[~df["txId"].duplicated(keep="first")]
                    df.set_index("txId", inplace=True)
                print(f"Loaded fallback classes dataset from {path} with {len(df)} records.")
                return df
            except Exception as e:
                print(f"Failed to load classes dataset from {path}: {e}")

    return None


# Startup loading
model = load_model()
merged_df = load_dataset()
mock_data = load_mock_responses()
graph = build_graph()
known_vasps = build_known_vasps(graph) if graph is not None else {}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/score/{wallet_id}")
def get_score(wallet_id: str):
    global model, merged_df, graph, known_vasps, mock_data

    # Attempt lazy re-load if files were added after process start
    if merged_df is None:
        merged_df = load_dataset()
    if model is None:
        model = load_model()
    if not mock_data:
        mock_data = load_mock_responses()
    if graph is None:
        graph = build_graph()
        if graph is not None:
            known_vasps = build_known_vasps(graph)

    wallet_key = str(wallet_id).strip()

    # 1. First check if wallet is in pre-configured mock responses
    if wallet_key in mock_data:
        res = dict(mock_data[wallet_key])
        return res

    # 2. Check if wallet is in dataset
    if merged_df is None:
        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded.",
        )

    if wallet_key not in merged_df.index:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet ID '{wallet_id}' not found in dataset.",
        )

    wallet_row = merged_df.loc[wallet_key]
    if isinstance(wallet_row, pd.DataFrame):
        wallet_row = wallet_row.iloc[0]

    # Nearest VASP attribution via graph BFS
    nearest_vasp_name, graph_hops, confidence = get_nearest_vasp(wallet_key, graph, known_vasps)
    if graph_hops is not None:
        confidence = "high" if graph_hops <= 2 else ("medium" if graph_hops <= 5 else "low")
    else:
        confidence = "low"

    # Default risk scoring based on class or model
    risk_score = 0.5
    risk_label = "uncertain"

    if model is not None:
        try:
            # Align input features with what the model expects
            if hasattr(model, "feature_names_in_"):
                feature_cols = list(model.feature_names_in_)
                features = wallet_row.reindex(feature_cols, fill_value=0.0)
                X = pd.DataFrame([features], columns=feature_cols)
            else:
                feature_cols = [c for c in wallet_row.index if c.startswith("feat_") or c == "time_step"]
                if not feature_cols:
                    feature_cols = [f"feat_{i}" for i in range(1, 166)]
                features = wallet_row.reindex(feature_cols, fill_value=0.0)
                X = pd.DataFrame([features], columns=feature_cols)

            X = X.astype(float)

            # Predict class probabilities
            probs = model.predict_proba(X)[0]
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
        except Exception as e:
            print(f"Model prediction fallback for {wallet_key}: {e}")
            if "class" in wallet_row:
                c = str(wallet_row["class"]).strip()
                if c == "1" or c == "illicit":
                    risk_score = 0.94
                    risk_label = "illicit"
                elif c == "2" or c == "licit":
                    risk_score = 0.12
                    risk_label = "licit"
    elif "class" in wallet_row:
        c = str(wallet_row["class"]).strip()
        if c == "1" or c == "illicit":
            risk_score = 0.94
            risk_label = "illicit"
        elif c == "2" or c == "licit":
            risk_score = 0.12
            risk_label = "licit"

    # Top 3 most important features by model.feature_importances_
    top_features = []
    if model is not None and hasattr(model, "feature_importances_"):
        try:
            importances = model.feature_importances_
            if hasattr(model, "feature_names_in_"):
                feat_names = list(model.feature_names_in_)
            else:
                feat_names = feature_cols

            top_indices = importances.argsort()[::-1][:3]
            top_features = [str(feat_names[i]) for i in top_indices if i < len(feat_names)]
        except Exception:
            pass

    if not top_features:
        top_features = ["transaction_volume_anomaly", "fan_out_centrality", "shortest_path_proximity"]

    return {
        "wallet_address": str(wallet_id),
        "risk_score": risk_score,
        "risk_label": risk_label,
        "graph_hops_to_nearest_vasp": graph_hops,
        "nearest_vasp_name": nearest_vasp_name,
        "attribution_confidence": confidence,
        "top_features": top_features,
    }