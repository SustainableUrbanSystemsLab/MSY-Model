# Lake Victoria MSY Notebook

Interactive Jupyter notebook for Maximum Sustainable Yield (MSY) calculations using the Schaefer surplus production model.

## Open In Browser

- Colab: https://colab.research.google.com/github/SustainableUrbanSystemsLab/MSY-Model/blob/main/notebooks/lake_victoria_msy.ipynb
- Binder (JupyterLab): https://mybinder.org/v2/gh/SustainableUrbanSystemsLab/MSY-Model/HEAD?labpath=notebooks%2Flake_victoria_msy.ipynb

## Local Setup (uv + Python)

1. Install `uv` (if needed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Create the environment and install dependencies:
   ```bash
   uv sync
   ```
3. Start JupyterLab:
   ```bash
   uv run jupyter lab
   ```
4. Open:
   - `notebooks/lake_victoria_msy.ipynb`

## Files

- `notebooks/lake_victoria_msy.ipynb`: Main notebook with formulas, scenario analysis, and sample country calculation.
- `msy_math.py`: Core MSY calculations and table-building helpers.
- `msy_plotting.py`: Shared matplotlib styling and plotting functions used by the notebook.
- `pyproject.toml`: `uv` project configuration and dependencies.
- `requirements.txt`: Binder-compatible dependency list.
