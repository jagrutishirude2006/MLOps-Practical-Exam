"""Data and schema validation gate for the Wine feature store.

Validates the materialized Parquet feature store against
``feature_store/registry.json``: zero nulls, schema alignment, non-empty
row count, and exactly 3 target classes. All failures raise explicit
``ValueError`` / ``RuntimeError`` (never bare ``assert``, which is stripped
under ``python -O``).

Run from the repository root with::

    python -m src.validation
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# Paths & constants
PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
REGISTRY_PATH: Path = PROJECT_ROOT / "feature_store" / "registry.json"
EXPECTED_N_CLASSES: int = 3


def _load_registry() -> dict[str, Any]:
    """Load and return the feature-store registry.

    Raises:
        RuntimeError: If the registry file is missing or malformed.
    """
    if not REGISTRY_PATH.exists():
        raise RuntimeError(
            f"Feature-store registry not found at {REGISTRY_PATH}. "
            "Run 'python -m src.feature_engineering' first."
        )
    try:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Registry at {REGISTRY_PATH} is not valid JSON: {exc}") from exc


def run_validation() -> None:
    """Validate the Parquet feature store against the registry contract.

    Raises:
        ValueError: If nulls, schema drift, empty data, or wrong class
            count are detected.
    """
    registry = _load_registry()
    storage_path = PROJECT_ROOT / registry["storage_path"]
    if not storage_path.exists():
        raise RuntimeError(f"Parquet feature file not found at {storage_path}.")

    df: pd.DataFrame = pd.read_parquet(storage_path)
    logger.info("Loaded feature store with shape %s", df.shape)

    if df.empty:
        raise ValueError("Feature store is empty (0 rows).")

    n_nulls = int(df.isnull().sum().sum())
    if n_nulls != 0:
        raise ValueError(f"Null values detected in feature store: {n_nulls} null cells.")

    expected_cols = set(registry["features"] + [registry["entity_key"], registry["target"]])
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Feature-store schema mismatch. Missing columns: {sorted(missing)}")

    n_classes = int(df[registry["target"]].nunique())
    if n_classes != EXPECTED_N_CLASSES:
        raise ValueError(
            f"Expected {EXPECTED_N_CLASSES} wine classes (0, 1, 2), found {n_classes}."
        )

    logger.info("All Wine schema and quality checks PASSED.")


def main() -> None:
    """CLI entry point."""
    run_validation()


if __name__ == "__main__":
    main()