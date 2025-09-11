The run.sh will go th the artifact/Generalization/ directory and execute the LLMs.py 

The directory contains all the outputs from LANCE using the 4 different state of the art models as underline LLMs.
The structure of the directory is the following:

Generalization
├── GT.json                 # The ground truth PRISM dataset
├── LLMs.py                 # The script that loads all the results and calculates Precision Recall and F1 Score and missing indicators per type for each of the methods.
├── Gemini                  # This directory contains the final indicators, labels and justifications for each report, as outputted by LANCE using **Gemini** as the underline LLM.
│   └── ReportNameA.csv     # Naming Convention*
├── Gemma                   # This directory contains the final indicators, labels and justifications for each report, as outputted by LANCE using **Gemma** as the underline LLM.
│   └── ReportNameA.csv     # Naming Convention*
├── Llama                   # This directory contains the final indicators, labels and justifications for each report, as outputted by LANCE using **Llama** as the underline LLM.
│   └── ReportNameA.csv     # Naming Convention*
└── Nemotron                # This directory contains the final indicators, labels and justifications for each report, as outputted by LANCE using **Nemotron** as the underline LLM.
    └── ReportNameA.csv     # Naming Convention*

*The naming convention for the files in this directory, where ReportNameA=the name of the report taken from the filename of the corresponding JSON file


