# Revealing the True Indicators: Understanding and Improving IoC Extraction From Threat Reports

## Overview

This repository contains the artifacts and evaluation framework for the research paper on **LANCE** (LLM-Assisted Notation and Classification Engine) and **PRISM** (Processed and Reviewed Indicators from Security Media) dataset. The work presents a novel approach to automatically extract and label Indicators of Compromise (IoCs) from unstructured cybersecurity threat reports using Large Language Models (LLMs).

### Key Contributions

1. **LANCE Framework**: An LLM-assisted pipeline for automated IoC extraction and labeling from threat reports
2. **PRISM Dataset**: A high-quality ground truth dataset containing manually verified IoCs from 50 threat reports
3. **Interactive UI**: A web-based interface for analyst assistance in IoC labeling with two modes (BAP and GAP)
4. **Comprehensive Evaluation**: Comparison with state-of-the-art methods and multiple LLM implementations

## Repository Structure

```plaintext
├── artifact/                  # Core implementation and datasets
│   ├── LANCE/                 # LANCE framework implementation (with ChatGPT 4o as the underline LLM)
│   ├── LANCE_sota_LLMS/       # LANCE implemented with other state of the art LLMs
│   ├── UI/                    # Interactive web interface
│   ├── IoCMiner/              # IoCMiner implementation and evaluation on PRISM
│   ├── 500/                   # Extended dataset with LANCE-GPT generated labels (500 reports)
│   ├── Comparison/            # Baseline method comparisons
│   ├── Generalization/        # Multi-LLM evaluation results
│   ├── GT_analysis/           # PRISM analysis and statistics
│   ├── AnalystsData/          # Human analyst and LANCE-GPT evaluation and comparison data
│   └── GT.json/               # PRISM dataset 
├── claims/                    # Evaluation claims and experiments
│   ├── claim1/                # PRISM dataset verification
│   ├── claim2/                # UI functionality demonstration  
│   ├── claim3/                # Analyst efficiency improvement
│   ├── claim4/                # Analyst performance enhancement
│   ├── claim5/                # LANCE performance evaluation
│   ├── claim6/                # Multi-LLM reproducibility
│   ├── claim7/                # Comparison with baseline methods
│   ├── claim8/                # LLM generalization evaluation
│   └── claim9/                # IoC extraction model improvement
├── infrastructure/            # Infrastructure requirements
├── install.sh                 # Installation script
├── license.txt                # License information
├── tree.txt                   # A detailed directory tree of this repository
├── use.txt                    # Intended use and limitations
└── README.md                  # This file
```

## Quick Start

### Prerequisites

- **Anaconda/Miniconda**: Required for environment management
- **Python 3.10+**: For running the framework and evaluation
- **API Keys** (optional): OpenAI API key for LANCE-GPT, Google API key for Gemini
- **System Requirements**: Moderate CPU usage, GPU optional for local LLM inference

### Notebook

LANCE_paper_artifacts.ipynb contains all the necessary steps for a first look of the artifacts and claims.

The cells are executed so you can see the output of the claims.

By following the instructions and running the cells yourself, you can see the output of the claims.

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/EvanFr/LANCE.git
```

**ATENTION** ⚠️
Due to limited budget on GitHub LFS, the .tgz files in the artifact directory will not be downloaded with the git clone.

Please use the following link to download them from OneDrive:
https://gtvault-my.sharepoint.com/:f:/g/personal/efroudakis3_gatech_edu/EjTHXFyANtNPvIWVYAptoHIBSiVEkeB9bcz1a56sBPkoAQ?e=WwdzUG

Using the following as password:
IoC-ACSAC

Unzip the artifact folder and use it to replace the one downloaded by the git clone.

2. **Navigate to the directory:**

```bash
cd LANCE
```

3. **Run the installation script:**

```bash
bash install.sh
```

This script will:

- Extract all compressed artifacts
- Create necessary conda environments:
  - `UI_env`: For the web interface
  - `LANCE_GPT`: For LANCE with GPT-4o
  - `open_LLMs`: For open-source LLMs
  - `Gemini`: For LANCE with Gemini
  - `IoC_Miner`: For the IoC extraction model

Approximate running time ~15 minutes

### Basic Usage

Each research claim can be independently evaluated. Navigate to any `claims/claimX/` directory and run:

```bash
./run.sh
```

**Note**: Some claims (5, 6) require API keys. See individual claim directories for specific requirements.

## Research Claims & Experiments

### Core Framework Claims

- **Claim 1**: PRISM dataset verification - Validates the ground truth dataset structure and statistics
- **Claim 5**: LANCE performance evaluation - Demonstrates LANCE's IoC extraction capabilities using GPT-4o
- **Claim 6**: Multi-LLM reproducibility - Shows LANCE works with various state-of-the-art LLMs

### Human-AI Collaboration Claims  

- **Claim 2**: Interactive UI demonstration - Shows the web interface for analyst assistance
- **Claim 3**: Analyst efficiency improvement - Proves 43% time reduction with GAP mode
- **Claim 4**: Analyst performance enhancement - Shows improved precision/recall with LANCE assistance

### Comparative Evaluation Claims

- **Claim 7**: Baseline method comparison - Compares LANCE against GoodFATR, VirusTotal, AlienVault
- **Claim 8**: LLM generalization - Evaluates LANCE with multiple LLMs (Llama, Gemma, Nemotron, Gemini) as the underline model
- **Claim 9**: Downstream model improvement - Shows IoC extraction models benefit from LANCE-generated data

## Key Features

### LANCE Framework

- **LLM-Powered Labeling**: Uses sophisticated prompting to classify indicators of compromise
- **Contextual Understanding**: Analyzes threat reports to distinguish true IoCs from noise
- **Multiple LLM Support**: Compatible with GPT-4o, Llama, Gemma, Nemotron, and Gemini
- **Justification Generation**: Provides explanations for each classification decision

### Interactive UI

- **BAP Mode**: Baseline analyst performance without AI assistance  
- **GAP Mode**: AI-assisted mode with LANCE predictions and justifications
- **Real-time Analysis**: Live timing and performance tracking
- **Report Management**: Easy loading and processing of threat reports

### PRISM Dataset

- **High Quality**: 50 manually verified threat reports with expert annotations
- **Comprehensive Coverage**: Multiple indicator types (IP, domain, URL, hash, CVE)
- **Rich Metadata**: Includes justifications and contextual information
- **Extended Version**: 500+ reports (not manually verified) for large-scale training and evaluation

## API Requirements

Some experiments require external API access:

- **OpenAI API** (Claims 5): For LANCE with GPT-4o
- **Google Gemini API** (Claims 6, 8): For LANCE with Gemini 2.0 Flash

If API access is not available, pre-computed results are provided in the corresponding artifact directories.

## Results Summary

Key findings from our evaluation:

- **Analyst Efficiency**: 43% reduction in analysis time with AI assistance
- **Analyst Accuracy**: Improved precision and recall when using LANCE predictions
- **Method Comparison**: LANCE outperforms existing automated methods
- **LLM Generalization**: Framework successfully works across multiple state-of-the-art LLMs
- **Downstream Impact**: Models trained on LANCE-generated data show improved performance

## Citation

If you use this work in your research, please cite our paper:

```bibtex
[Citation information will be provided upon paper publication]
```

## Support & Troubleshooting

- **Installation Issues**: Ensure Anaconda is properly installed and accessible
- **API Errors**: Verify API keys are correctly set in run.sh files
- **Environment Problems**: Use `conda info --envs` to verify environment creation
- **Missing Dependencies**: Ensure all .tgz files are properly extracted by install.sh

For additional support, please refer to the individual claim.txt files in each claim directory or submit an issue in the repository.

## License

This project is licensed under the terms specified in `license.txt`. Please refer to that file for detailed licensing information.
