"""
Graph statistics and diagnostics for Support Protocol 2.

This module:
- loads an edge list (and optionally node attributes),
- constructs an undirected graph,
- computes:
  - global stats (nodes, edges, density, components),
  - degree distribution summaries,
  - clustering coefficients.

More advanced diagnostics (communities, assortativity) can be added as needed.
"""

from typing import Dict, Any

import pandas as pd
import networkx as nx
from pathlib import Path

from utils_io import load_table


def build_graph_datamart(config: Dict[str, Any], dataset_card: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute graph-level statistics.

    Parameters
    ----------
    config : dict
        SP2 configuration dictionary.
    dataset_card : dict
        Dataset card (unused here but kept for symmetry).

    Returns
    -------
    dict
        Graph datamart for inclusion under eda_datamarts["graph"].
    """
    graph_cfg = config.get("modalities", {}).get("graph", {})
    data_root = Path(config.get("data_root", "."))

    edge_list_path = graph_cfg.get("edge_list_path")
    if not edge_list_path:
        raise ValueError("Graph modality enabled but 'edge_list_path' not provided in config.")

    src_col = graph_cfg.get("source_column", "source")
    tgt_col = graph_cfg.get("target_column", "target")

    df_edges = load_table(data_root, edge_list_path)
    if src_col not in df_edges.columns or tgt_col not in df_edges.columns:
        raise ValueError(f"Edge list must contain columns '{src_col}' and '{tgt_col}'.")

    G = nx.from_pandas_edgelist(df_edges, source=src_col, target=tgt_col)

    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()

    if n_nodes > 1:
        density = nx.density(G)
    else:
        density = 0.0

    # Connected components
    components = list(nx.connected_components(G))
    n_components = len(components)
    component_sizes = [len(c) for c in components]

    # Degree stats
    degrees = [deg for _, deg in G.degree()]
    degree_series = pd.Series(degrees)
    degree_summary = degree_series.describe().to_dict()

    # Clustering coefficients
    clustering_vals = list(nx.clustering(G).values())
    clustering_series = pd.Series(clustering_vals)
    clustering_summary = clustering_series.describe().to_dict()

    return {
        "global_stats": {
            "n_nodes": int(n_nodes),
            "n_edges": int(n_edges),
            "density": float(density),
            "n_components": int(n_components),
            "component_size_summary": pd.Series(component_sizes).describe().to_dict()
            if component_sizes
            else {},
        },
        "degree_summary": degree_summary,
        "clustering_summary": clustering_summary,
        # Placeholders for more advanced metrics if desired
        "communities": {},
        "assortativity": {},
    }
