
# MLOps Practical Exam – Wine Classification

End-to-end collaborative MLOps pipeline developed

## Project Technologies

- Python
- SQLite
- DVC
- Parquet Feature Store
- MLflow
- Pytest
- Joblib

## Team Contributions

- Member 1: ML Pipeline
- Member 2: DVC
- Member 3: Data Preprocessing
- Member 4: Feature Store
- Member 5: Data Validation
- Member 6: Documentation and Integration Testing

## Installation

```bash
pip install -r requirements.txt
```

## Run the Pipeline

```bash
dvc repro
```

## Run Integration Tests

```bash
pytest -v tests/test_integration.py
```

## Run MLflow UI

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Open http://127.0.0.1:5000 in your browser.

## Member 6 Responsibilities

- Maintain project documentation.
- Develop modular pytest integration tests.
- Verify pipeline execution.
- Verify feature-store registry and Parquet schema.
- Verify MLflow SQLite tracking.
- Verify saved model predictions.

## Git Workflow

Branch: integration

Commit message:

`docs(integration): add README and end-to-end integration tests`
