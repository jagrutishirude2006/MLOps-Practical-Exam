# DVC Dataset Versioning Workflow

## 1. Local Remote Storage

DVC remote storage is configured as a local directory:

`~/dvc-remote-storage`

This directory stores the dataset versions pushed using DVC. Git tracks the DVC metadata files, while DVC stores the actual data files in its cache and remote storage.

## 2. Wine Dataset Versions

The Wine dataset was tracked and managed using DVC.

- **Version 1:** 178 rows
- **Version 2:** 198 rows

Version 2 was created by augmenting Version 1 with 20 additional records.

## 3. Dataset Tracking Workflow

The following commands were used to track and save dataset versions:

```bash
dvc add data/raw/wine_v1.csv
git add data/raw/wine_v1.csv.dvc data/raw/.gitignore
git commit -m "Track dataset version"
dvc push
```

The `dvc add` command tracks the dataset, `git add` stages the DVC metadata, `git commit` saves the version in Git, and `dvc push` uploads the dataset to the configured DVC remote.

## 4. Comparing Dataset Versions

The `dvc diff` command was used to compare the dataset versions and identify changes between Version 1 and Version 2.

```bash
dvc diff FIRST_COMMIT_ID
```

## 5. Restoring Dataset Versions

The `dvc checkout` command was used to restore the dataset corresponding to a selected Git version.

```bash
git checkout FIRST_COMMIT_ID -- data/raw/wine_v1.csv.dvc
dvc checkout data/raw/wine_v1.csv.dvc
```

This allows switching between dataset versions and restoring the required data.

## Conclusion

DVC was used to track, store, compare, and restore different versions of the Wine dataset. Git stores the version metadata and history, while DVC manages the dataset files and remote storage.
