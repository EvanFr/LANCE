LANCE — Detecting True Indicators from LLM Outputs
===============================================

Summary
-------
This repository contains the final release of artifacts, code, and instructions supporting the paper: "Revealing the True Indicators: Understanding and Improving IoC Extraction From Threat Reports". This repository contains the final LANCE release: the LANCE framework for IoC extraction, the PRISM ground‑truth dataset (50 hand‑annotated reports), and an interactive UI for manual analysis and IoC labeling.


Contents
--------
- `LANCE/` — Primary code and artifacts used for the experiments in the paper (environment spec, `LANCE.py`, prompts, and `Reports*` directories).
- `PRISM/` — Ground-truth dataset (PRISM). This folder contains the GT dataset contributed with the paper and the associated report artifacts used in evaluation.
- `UI/` — UI code and requirements for interactive components used during analyst studies (requires a separate environment or installation from the LANCE environment).
- `README.md` — This file.
- `license.txt` — Repository license.


Quick Start
-----------

Setup & run LANCE
-----------------
These steps show a minimal setup to run the core LANCE experiments.

1. Create and activate the Conda environment for LANCE (recommended):

```bash
conda env create -f LANCE/environment.yaml -n lance
conda activate lance
```

2. Run the core LANCE pipeline (example):

```bash
python LANCE/LANCE.py
```

Notes:
- LANCE experiments require API keys or external models. Set environment variables (`OPENAI_API_KEY`) before running those scripts.



Setup & run UI
-------------------------
The UI components use different dependencies from the core LANCE code and should be installed in a separate environment to avoid conflicts.

1. Create and activate a dedicated environment for the UI, then install UI requirements:

```bash
conda create -n lance-ui python=3.12 -y
conda activate lance-ui
pip install -r UI/requirements.txt
```

2. Run the UI

Follow the instructions in `UI/README.md` for starting the UI components and any additional setup steps. Installing the UI into an existing LANCE environment is possible but not recommended for reproducibility.


Outputs & Where to Look
-----------------------
- Model-generated IoC CSVs are in `LANCE/GPT_IoCs/`.
- Model-anotated Report PDFs are in `LANCE/output_PDF`

Citation
--------
Please cite the accompanying paper when using these artifacts.

```bibtex
@article{froudakisrevealing,
  title={Revealing the True Indicators: Understanding and Improving IoC Extraction From Threat Reports},
  author={Froudakis, Evangelos and Avgetidis, Athanasios and Frankum, Sean Tyler and Perdisci, Roberto and Antonakakis, Manos and Keromytis, Angelos D}
}
```

License
-------
The repository license is included in `license.txt`.

Reproducibility Notes & Tips
----------------------------
- Determinism: some experiments rely on stochastic models or remote LLM APIs — outputs may vary across runs.
- APIs & Keys: set required API keys as environment variables if experiments call external services (for example, `OPENAI_API_KEY`, or other provider keys).

Contributing & Contact
----------------------
For bugs or improvements, open an issue or a pull request in the original repository. For substantial changes, include a reproducible example.

Acknowledgments
---------------
This folder packages the contributions as stated in the paper for easy archival and artifact evaluation.

---

