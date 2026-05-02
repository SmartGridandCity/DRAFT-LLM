"""
Image / video statistics and diagnostics for Support Protocol 2.

This module:
- reads an image metadata table (paths, labels, etc.),
- samples images up to a maximum count,
- computes:
  - global image/video statistics (counts, label distribution, resolutions),
  - entropy-based diagnostics (global, local patch, spectral) on the sample.
"""

from typing import Dict, Any

import numpy as np
import pandas as pd
from pathlib import Path

from PIL import Image
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.util import view_as_blocks
from utils_io import load_table


def _compute_entropy_from_histogram(hist: np.ndarray) -> float:
    """Compute Shannon entropy (base 2) from a histogram."""
    p = hist / hist.sum()
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def image_entropy_stats(path: Path, patch_size: int = 16) -> Dict[str, float]:
    """
    Compute global, local patch, and spectral entropy for a single image.

    Parameters
    ----------
    path : Path
        Path to an image file.
    patch_size : int
        Patch size (square) for local entropy.

    Returns
    -------
    dict
        {
          "H_global": ...,
          "H_local_mean": ...,
          "H_local_std": ...,
          "H_spectral": ...
        }
    """
    img = Image.open(path).convert("L")  # grayscale
    arr = np.asarray(img, dtype=float)

    # Normalize to [0, 1]
    arr_norm = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)

    # Global intensity entropy
    hist, _ = np.histogram(arr_norm, bins=64, range=(0.0, 1.0))
    H_global = _compute_entropy_from_histogram(hist)

    # Local patch entropy
    h, w = arr_norm.shape
    ph = (h // patch_size) * patch_size
    pw = (w // patch_size) * patch_size
    arr_crop = arr_norm[:ph, :pw]
    blocks = view_as_blocks(arr_crop, block_shape=(patch_size, patch_size))
    local_entropies = []
    for i in range(blocks.shape[0]):
        for j in range(blocks.shape[1]):
            block = blocks[i, j].ravel()
            hist_block, _ = np.histogram(block, bins=32, range=(0.0, 1.0))
            if hist_block.sum() > 0:
                local_entropies.append(_compute_entropy_from_histogram(hist_block))
    H_local_mean = float(np.mean(local_entropies)) if local_entropies else 0.0
    H_local_std = float(np.std(local_entropies)) if local_entropies else 0.0

    # Spectral entropy via 2D FFT
    spectrum = np.fft.fft2(arr_norm)
    mag = np.abs(spectrum)
    hist_spec, _ = np.histogram(mag, bins=64, range=(0.0, np.percentile(mag, 99)))
    H_spectral = _compute_entropy_from_histogram(hist_spec)

    return {
        "H_global": H_global,
        "H_local_mean": H_local_mean,
        "H_local_std": H_local_std,
        "H_spectral": H_spectral,
    }


def build_image_datamart(config: Dict[str, Any], dataset_card: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute global image/video statistics and entropy-based diagnostics.

    Parameters
    ----------
    config : dict
        SP2 configuration dictionary.
    dataset_card : dict
        Dataset card from Support Protocol 1 (unused but kept for symmetry).

    Returns
    -------
    dict
        Image datamart for inclusion under eda_datamarts["image"].
    """
    img_cfg = config.get("modalities", {}).get("image", {})
    data_root = Path(config.get("data_root", "."))
    metadata_table_path = img_cfg.get("metadata_table")
    if not metadata_table_path:
        raise ValueError("Image modality enabled but 'metadata_table' not provided in config.")

    df_meta = load_table(data_root, metadata_table_path)

    path_col = img_cfg.get("path_column", "path")
    label_col = img_cfg.get("label_column", None)

    # Global counts
    n_items = int(df_meta.shape[0])

    label_dist = {}
    if label_col and label_col in df_meta.columns:
        vc = df_meta[label_col].value_counts(normalize=True, dropna=False)
        label_dist = {str(k): float(v) for k, v in vc.items()}

    # Resolution/aspect ratio stats (sampled to reduce I/O)
    max_samples = int(config.get("sampling", {}).get("image_max_samples", 200))
    sample_df = df_meta.sample(
        n=min(max_samples, len(df_meta)),
        random_state=config.get("sampling", {}).get("random_state", 42),
    )

    heights = []
    widths = []
    aspects = []
    entropy_records = []

    for _, row in sample_df.iterrows():
        img_path = data_root / str(row[path_col])
        try:
            with Image.open(img_path) as im:
                w, h = im.size
            widths.append(w)
            heights.append(h)
            aspects.append(w / (h + 1e-6))
            entropy_records.append(image_entropy_stats(img_path))
        except Exception:
            continue

    resolution_stats = {
        "height_summary": pd.Series(heights).describe().to_dict() if heights else {},
        "width_summary": pd.Series(widths).describe().to_dict() if widths else {},
        "aspect_ratio_summary": pd.Series(aspects).describe().to_dict() if aspects else {},
    }

    if entropy_records:
        H_global = [rec["H_global"] for rec in entropy_records]
        H_local_mean = [rec["H_local_mean"] for rec in entropy_records]
        H_local_std = [rec["H_local_std"] for rec in entropy_records]
        H_spectral = [rec["H_spectral"] for rec in entropy_records]
        entropy_summary = {
            "H_global_mean": float(np.mean(H_global)),
            "H_global_std": float(np.std(H_global)),
            "H_local_mean_mean": float(np.mean(H_local_mean)),
            "H_local_mean_std": float(np.std(H_local_mean)),
            "H_local_std_mean": float(np.mean(H_local_std)),
            "H_local_std_std": float(np.std(H_local_std)),
            "H_spectral_mean": float(np.mean(H_spectral)),
            "H_spectral_std": float(np.std(H_spectral)),
        }
    else:
        entropy_summary = {}

    return {
        "n_items": n_items,
        "label_distribution": label_dist,
        "resolution_stats": resolution_stats,
        "entropy_summary": entropy_summary,
    }
