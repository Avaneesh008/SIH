"""
graph_utils.py — shared by Duo A and Duo B.
Builds the transaction graph once and exposes get_nearest_vasp() for the /score endpoint.
"""
import pandas as pd
import networkx as nx
import random

def build_graph(edgelist_path="elliptic_txs_edgelist.csv"):
    edges_df = pd.read_csv(edgelist_path)
    graph = nx.from_pandas_edgelist(
        edges_df,
        source=edges_df.columns[0],
        target=edges_df.columns[1],
        create_using=nx.DiGraph(),
    )
    return graph


def build_known_vasps(graph, n=8, seed=42):
    random.seed(seed)
    sample_nodes = random.sample(list(graph.nodes()), n)
    return {node: f"known_vasp_{i+1}" for i, node in enumerate(sample_nodes)}


def get_nearest_vasp(wallet_id, graph, known_vasps):
    """
    Returns (nearest_vasp_name, hop_count, confidence) for wallet_id.
    confidence: 'high' if hops<=2, 'medium' if hops<=5, else 'low'.
    """
    if wallet_id not in graph:
        return "unidentified", None, "low"

    best_name, best_hops = None, None
    undirected = graph.to_undirected()
    for vasp_node, vasp_name in known_vasps.items():
        if vasp_node not in graph:
            continue
        try:
            hops = nx.shortest_path_length(undirected, source=wallet_id, target=vasp_node)
        except nx.NetworkXNoPath:
            continue
        if best_hops is None or hops < best_hops:
            best_hops, best_name = hops, vasp_name

    if best_name is None:
        return "unidentified", None, "low"

    confidence = "high" if best_hops <= 2 else ("medium" if best_hops <= 5 else "low")
    return best_name, best_hops, confidence
