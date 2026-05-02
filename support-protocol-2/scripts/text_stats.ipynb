"""
Text statistics and diagnostics for Support Protocol 2.

This module:
- reads a text table (documents, labels, etc.),
- computes:
  - global counts and length distributions,
  - vocabulary and top term summaries,
  - simple lexical richness indicators.

Full embedding-based diagnostics can be added as needed, but are left
lightweight here to minimize dependencies.
"""

from typing import Dict, Any

import numpy as np
import pandas as pd
from pathlib import Path

from collections import Counter
from utils_io import load_table


def _simple_tokenize(text: str) -> list:
    """Very simple whitespace-based tokenizer; replace with spaCy or similar if needed."""
    return [t for t in str(text).strip().split() if t]


def build_text_datamart(config: Dict[str, Any], dataset_card: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute global and lexical statistics for text data.

    Parameters
    ----------
    config : dict
        SP2 configuration dictionary.
    dataset_card : dict
        Dataset card (unused here but kept for symmetry).

    Returns
    -------
    dict
        Text datamart for inclusion under eda_datamarts["text"].
    """
    txt_cfg = config.get("modalities", {}).get("text", {})
    data_root = Path(config.get("data_root", "."))
    table_path = txt_cfg.get("table")
    if not table_path:
        raise ValueError("Text modality enabled but 'table' not provided in config.")

    df_text = load_table(data_root, table_path)

    text_col = txt_cfg.get("text_column", "text")
    label_col = txt_cfg.get("label_column", None)

    # Global counts
    n_docs = int(df_text.shape[0])

    # Length distributions
    lengths = df_text[text_col].fillna("").apply(lambda s: len(_simple_tokenize(s)))
    length_stats = lengths.describe().to_dict()

    # Vocabulary and term frequency
    vocab_counter = Counter()
    for txt in df_text[text_col].fillna(""):
        vocab_counter.update(_simple_tokenize(txt))

    vocab_size = len(vocab_counter)
    top_terms = dict(vocab_counter.most_common(50))

    # Lexical richness: type-token ratio (TTR) and approximate Zipf-ness
    total_tokens = sum(vocab_counter.values())
    ttr = float(vocab_size / (total_tokens + 1e-8))

    freq_values = np.array(sorted(vocab_counter.values(), reverse=True), dtype=float)
    ranks = np.arange(1, len(freq_values) + 1)
    # Log-log slope as crude Zipf indicator
    if len(freq_values) > 1:
        slope, _ = np.polyfit(np.log(ranks), np.log(freq_values + 1e-8), 1)
        zipf_slope = float(slope)
    else:
        zipf_slope = 0.0

    lexical_metrics = {
        "type_token_ratio": ttr,
        "zipf_loglog_slope": zipf_slope,
        "vocab_size": int(vocab_size),
        "total_tokens": int(total_tokens),
    }

    # Label-wise term frequencies (optional, only if label_col exists)
    label_term_usage = {}
    if label_col and label_col in df_text.columns:
        for label, group in df_text.groupby(label_col):
            label_counter = Counter()
            for txt in group[text_col].fillna(""):
                label_counter.update(_simple_tokenize(txt))
            label_term_usage[str(label)] = dict(label_counter.most_common(30))

    global_stats = {
        "n_docs": n_docs,
        "length_stats": length_stats,
        "vocab_summary": {
            "vocab_size": int(vocab_size),
            "top_terms": top_terms,
        },
    }

    return {
        "global_stats": global_stats,
        "lexical_metrics": lexical_metrics,
        "label_term_usage": label_term_usage,
        # Embedding structure and topic structure can be added as needed
        "embedding_summary": {},
        "topic_summary": {},
    }
