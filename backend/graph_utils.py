"""
graph_utils.py — shared by Duo A and Duo B.
Builds the transaction graph once and exposes get_nearest_vasp() for the /score endpoint.
"""
import os
from pathlib import Path
import random
import pandas as pd
import networkx as nx

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent

EDGELIST_CANDIDATE_PATHS = [
    REPO_ROOT / "data" / "elliptic_txs_edgelist.csv",
    BASE_DIR / "data" / "elliptic_txs_edgelist.csv",
    BASE_DIR / "elliptic_txs_edgelist.csv",
    REPO_ROOT / "elliptic_txs_edgelist.csv",
    Path("data") / "elliptic_txs_edgelist.csv",
    Path("elliptic_txs_edgelist.csv"),
]


def build_graph(edgelist_path=None):
    """Build and return the directed transaction graph from edgelist CSV."""
    target_path = None
    if edgelist_path and Path(edgelist_path).is_file():
        target_path = Path(edgelist_path)
    else:
        for p in EDGELIST_CANDIDATE_PATHS:
            if p.is_file():
                target_path = p
                break

    if not target_path:
        print("Warning: elliptic_txs_edgelist.csv not found.")
        return None

    try:
        edges_df = pd.read_csv(target_path)
        graph = nx.from_pandas_edgelist(
            edges_df,
            source=edges_df.columns[0],
            target=edges_df.columns[1],
            create_using=nx.DiGraph(),
        )
        # Precompute and cache undirected graph for fast shortest-path lookups
        graph._undirected = graph.to_undirected()
        print(f"Built transaction graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")
        return graph
    except Exception as e:
        print(f"Failed to build graph from {target_path}: {e}")
        return None


def build_known_vasps(graph, n=8, seed=42):
    """Generate deterministic placeholder VASP mapping from graph sample nodes."""
    if graph is None or graph.number_of_nodes() == 0:
        return {}
    random.seed(seed)
    sample_nodes = random.sample(list(graph.nodes()), min(n, graph.number_of_nodes()))
    return {node: f"known_vasp_{i+1}" for i, node in enumerate(sample_nodes)}


def get_nearest_vasp(wallet_id, graph, known_vasps):
    """
    Returns (nearest_vasp_name, hop_count, confidence) for wallet_id.
    confidence: 'high' if hops<=2, 'medium' if hops<=5, else 'low'.
    """
    if graph is None or known_vasps is None:
        return "unidentified", None, "low"

    # Handle type conversions if wallet_id is str and graph nodes are int (or vice versa)
    target_node = wallet_id
    if target_node not in graph:
        try:
            int_node = int(wallet_id)
            if int_node in graph:
                target_node = int_node
        except (ValueError, TypeError):
            pass
        if target_node not in graph:
            str_node = str(wallet_id)
            if str_node in graph:
                target_node = str_node

    if target_node not in graph:
        return "unidentified", None, "low"

    undirected = getattr(graph, "_undirected", None)
    if undirected is None:
        undirected = graph.to_undirected()
        graph._undirected = undirected

    best_name, best_hops = None, None
    for vasp_node, vasp_name in known_vasps.items():
        if vasp_node not in graph:
            continue
        try:
            hops = nx.shortest_path_length(undirected, source=target_node, target=vasp_node)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            continue
        if best_hops is None or hops < best_hops:
            best_hops, best_name = hops, vasp_name

    if best_name is None:
        return "unidentified", None, "low"

    confidence = "high" if best_hops <= 2 else ("medium" if best_hops <= 5 else "low")
    return best_name, best_hops, confidence
