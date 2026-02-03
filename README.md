# Integrated Framework for Stock Estimation (MEP-focused)

This repository contains an integrated, notebook-driven workflow to estimate building-service (MEP) stocks when data are fragmented or incomplete. The pipeline combines:
- **database connection & enrichment**
- **imputation / predictive modeling**
- **parametric (rule-based) subsystem logic** (HVAC / plumbing / electrical)
- optional **visualization outputs** (e.g., Sankey-style summaries)

It is primarily organized as a set of **Jupyter notebooks** plus a few Python modules that hold the reusable calculation logic.

> Note: The repo is currently code-first (minimal packaging). Most steps are executed via notebooks.

## What’s inside (high-level)

Main notebooks/scripts in the repo include (names as in the repository):
- `database_connection.ipynb` – connect to the source database and pull tables
- `Database_Enrichment_Imputation_Clean.ipynb` – enrichment + imputation workflow
- `feature selection.ipynb` – feature selection experiments
- `database prediction.ipynb` – prediction/model runs
- `validation_data_model_tuning.ipynb` – model tuning / validation
- `discussion.ipynb` – result checks / discussion playground
- `Connected_Database_Mathematical_Model.ipynb` – an integrated notebook tying model + DB together

Reusable subsystem logic:
- `HVAC.py` – HVAC / heating-related parametric logic (e.g., radiator calculation refactor + cross-validation notes)
- `plumbing.py` – plumbing-related logic and updates for fixtures
- `electrical.py` – electrical-related logic
- `genSankey.py` – helper to generate Sankey-style summaries

Configuration / mappings / intermediate data:
- `building_category_building_system_matrix.csv` – mapping between building categories and system assumptions
- `df3.csv` – calculated / intermediate data snapshot (example)
- `.gitignore`, `.vscode/`, `__pycache__/`

## Typical workflow

A typical run looks like:

1) **Connect & extract**
- Open `database_connection.ipynb`
- Configure credentials / host (see “Configuration” below)
- Pull raw tables / export intermediate files (depending on your setup)

2) **Enrich + impute missing attributes**
- Run `Database_Enrichment_Imputation_Clean.ipynb`
- This step is where you bring fragmented building/system attributes into a structured table usable by later models.

3) **Feature selection (optional but recommended)**
- Run `feature selection.ipynb` to test candidate predictors and reduce noise.

4) **Predictive modeling**
- Run `database prediction.ipynb` (and/or `validation_data_model_tuning.ipynb`)
- Output: predicted parameters used for subsystem-level stock estimation.

5) **Subsystem stock estimation (parametric rules)**
- The notebooks call into `HVAC.py`, `plumbing.py`, `electrical.py`
- Output: component/system quantities and material stock estimates.

6) **Summaries / visualization**
- Use `genSankey.py` (or notebook cells that call it) to generate Sankey-ready tables/figures.

## Setup

### Environment
Recommended: create a clean Python environment (conda or venv).

Minimal packages you’ll likely need:
- `pandas`, `numpy`
- `scikit-learn`
- `jupyter` / `jupyterlab`
- any database driver you use (e.g., `sqlalchemy`, `psycopg2`, `pyodbc`, etc.)

Because different users will connect to different databases, the exact DB packages are not pinned here yet.

### Configuration (important)
This repo connects to a database in notebooks. **Do not hardcode credentials.**

Suggested pattern:
- Create a local `.env` file (not committed), e.g.
  - `DB_HOST=...`
  - `DB_NAME=...`
  - `DB_USER=...`
  - `DB_PASSWORD=...`
- Load it in notebooks via `python-dotenv`, or read from your OS environment variables.

If you prefer a simpler setup, create a local `config.py` (gitignored) and import it in notebooks.

## Data availability

The repository includes some example/intermediate files (e.g., `df3.csv`), but the full underlying database and raw source data are typically **not** committed due to size and privacy constraints.

If you want others to reproduce results, consider adding:
- a small anonymized sample dataset, or
- a “schema + toy data generator”, or
- a clear export format (CSV/Parquet) with column definitions.

## Output conventions (suggested)

To keep things tidy, consider writing outputs to:
- `data/raw/` (gitignored)
- `data/processed/`
- `outputs/tables/`
- `outputs/figures/`

Right now outputs may be produced wherever the notebook is executed.

## How to cite / credit

If you use or adapt this workflow, please cite the related research outputs (paper/thesis) that describe the Integrated Framework for Stock Estimation and the parametric subsystem logic.

## Contact

Maintainer: Shuyan (repo owner)

If you open issues, it helps to include:
- which notebook you ran
- the exact error message
- OS + Python version
- whether you used DB connection or local exported files
