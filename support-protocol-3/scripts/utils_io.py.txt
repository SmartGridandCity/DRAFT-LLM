"""
Utility functions for Support Protocol 3.

Provides simple JSON/YAML loading and saving, with lightweight
error handling suitable for command-line usage.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


def load_json(path: str | Path) -> Dict[str, Any]:
    path = Path(path)
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] JSON file not found: {path}", file=sys.stderr)
        raise
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON at {path}: {e}", file=sys.stderr)
        raise


def save_json(data: Dict[str, Any], path: str | Path, indent: int = 2) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, sort_keys=True, ensure_ascii=False)


def load_yaml(path: str | Path) -> Optional[Dict[str, Any]]:
    if yaml is None:
        print(
            "[WARN] PyYAML is not installed; YAML configuration will be ignored.",
            file=sys.stderr,
        )
        return None

    path = Path(path)
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[ERROR] YAML file not found: {path}", file=sys.stderr)
        raise
    except yaml.YAMLError as e:  # type: ignore[attr-defined]
        print(f"[ERROR] Failed to parse YAML at {path}: {e}", file=sys.stderr)
        raise
