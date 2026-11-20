
"""Integration tests for   Wine MLOps project."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PIPELINE_FILE = PROJECT_ROOT / "src" / "pipeline.py"
REGISTRY_PATH = PROJECT_ROOT / "feature_store" / "registry.json"
MLFLOW_DB_PATH = PROJECT_ROOT / "mlflow.db"
BEST_MODEL_PATH = PROJECT_ROOT / "models" / "best_wine_model.pkl"


@pytest.fixture(scope="module")
def pipeline_result():
    """Run the pipeline using the active Python interpreter."""

    if not PIPELINE_FILE.exists():
        pytest.skip("Pipeline not available yet: src/pipeline.py is missing")

    return subprocess.run(
        [sys.executable, "-m", "src.pipeline"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )


@pytest.fixture(scope="module")
def registry(pipeline_result):
    """Load the feature-store registry."""

    assert pipeline_result.returncode == 0, pipeline_result.stderr
    assert REGISTRY_PATH.exists(), "Feature-store registry missing"

    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_pipeline_exit_code_and_clean_output(pipeline_result):
    """Check successful pipeline execution."""

    assert pipeline_result.returncode == 0, pipeline_result.stderr
    assert "Traceback" not in pipeline_result.stderr
    assert "Traceback" not in pipeline_result.stdout


def test_registry_integrity(registry):
    """Check feature-store registry."""

    required_keys = {
        "feature_group",
        "version",
        "entity_key",
        "timestamp_key",
        "target",
        "features",
        "storage_path",
    }

    assert required_keys.issubset(registry.keys())
    assert registry["feature_group"] == "wine_classification_features"
    assert isinstance(registry["features"], list)
    assert len(registry["features"]) > 0
    assert (PROJECT_ROOT / registry["storage_path"]).exists()


def test_parquet_schema_and_row_count(registry):
    """Check Parquet schema and data."""

    import pandas as pd

    df = pd.read_parquet(PROJECT_ROOT / registry["storage_path"])

    assert len(df) > 0
    assert df.isnull().sum().sum() == 0

    expected_columns = set(
        registry["features"] + [registry["entity_key"], registry["target"]]
    )

    assert expected_columns.issubset(df.columns)
    assert df[registry["target"]].nunique() == 3


def test_mlflow_sqlite_tracking():
    """Check MLflow tracking database."""

    if not MLFLOW_DB_PATH.exists():
        pytest.skip("MLflow database not available yet")

    from mlflow.tracking import MlflowClient

    client = MlflowClient(tracking_uri="sqlite:///mlflow.db")

    experiment = client.get_experiment_by_name(
        "Wine_Classification_Team_G2"
    )

    assert experiment is not None

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id]
    )

    assert len(runs) >= 3

    for run in runs:
        assert run.info.status == "FINISHED"
        assert "accuracy" in run.data.metrics
        assert run.data.tags.get("team") == "Group_G2"


def test_saved_model_predictions(registry):
    """Check saved model and predictions."""

    if not BEST_MODEL_PATH.exists():
        pytest.skip("Saved model not available yet")

    import joblib
    import pandas as pd

    model = joblib.load(BEST_MODEL_PATH)

    df = pd.read_parquet(PROJECT_ROOT / registry["storage_path"])
    sample = df[registry["features"]].iloc[:5]

    predictions = model.predict(sample)

    assert len(predictions) == 5
    assert set(predictions).issubset({0, 1, 2})
