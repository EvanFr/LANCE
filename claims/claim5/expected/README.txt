The run.sh will:
- Change directory to artifact/LANCE/
- Activate a conda environment with the necessary packages (the environment was created trough the install.sh)
- run the artifact/LANCE/LANCE.py

LANCE.py will iterate through the 50 reports from PRISM that are preloaded in the directories:
artifact/LANCE/ReportsJSON : contains the JSON file provided by ORKL.eu that includes information about the report (including the original text)
artifact/LANCE/ReportsPDF : contains the original PDF of the report or a PDF version of the website of the report (also provided by ORKL.eu)

The code will do the following for all 50 reports iteratively:

1. Get the text of the report from the JSON
2. Use IoC searcher to extract all indicators
3. Store all the appearances of each indicator
4. Use ChatGPT 4o to label all the indicators as described in Section 3.2.2 of the paper
5. Generate the PDF that can be then inputted to the UI (claim 2)

The intended output is a directory with the following structure:
LANCE
├── environment.yaml                # Environment setup file used in install.sh to create LANCE_GPT conda env
├── LANCE.py                        # Core implementation of LANCE with GPT
├── logs.txt                        # Logs output from LANCE.py
├── prompts.txt                     # The prompts used for each indicator type 
├── GPT_IoCs/                       # This directory contains all the indicator labels from LANCE
│   ├── CVE/                        # The extracted CVEs labeled for each report, before filtering. The directory contains a .txt file for each report
│   │   └── ReportNameA.txt         # Naming Convention*
│   ├── domain/                     # The extracted domains labeled for each report, before filtering. The directory contains a .txt file for each report
│   │   └── ReportNameA.txt         # Naming Convention*
│   ├── HASH/                       # The extracted hashes labeled for each report, before filtering. The directory contains a .txt file for each report
│   │   └── ReportNameA.txt         # Naming Convention*
│   ├── IP/                         # The extracted IPs labeled for each report, before filtering. The directory contains a .txt file for each report
│   │   └── ReportNameA.txt         # Naming Convention*
│   ├── URL/                        # The extracted URLs labeled for each report, before filtering. The directory contains a .txt file for each report
│   │   └── ReportNameA.txt         # Naming Convention*
│   └── ReportNameA.csv             # ** The .csv files contain the final extracted indicators of all types, their label and the justification provided by LANCE. Naming Convention* **
├── IoC_searcher_IoC_dict/          # The directory contains a json file for each report that contains all the extracted indicators and their deferent (de-fanged) appearances  
│   └── ReportNameA.json            # Naming Convention*
├── IoC_searcher_IoCs/              # The directory contains all the indicators extracted from each report by IoC searcher
│   └── ReportNameA.csv             # Naming Convention*
├── output_PDFs/                    # ** The output pdf with the indicators annotated. These PDFs can be inputted to the provided UI in claim 2 **
│   └── ReportNameA_Highlighter.pdf # Naming Convention*
├── ReportsJSON/                    # The report JSON files as provided by ORKL.eu
│   └── ReportNameA.json            # Naming Convention*
├── ReportsPDF/                     # The report PDF files as provided by ORKL.eu
│   └── ReportNameA.pdf             # Naming Convention*
└── ReportsTXT/                     # The text of each report extracted by the corresponding JSON in ReportsJSON/
    └── ReportNameA.txt             # Naming Convention*


*The naming convention for the files in this directory, where ReportNameA=the name of the report taken from the filename of the corresponding JSON file


The directory structure gets automatically created by LANCE.py

We have left the actual output of one report for reference (b299f3685100e68d79d30b8949428b0f954d3cc9).
This is for demonstration prepuces in case the reviewer(s) are not able to run LANCE.py

The approximate average run time per report is 2-3 minutes.
The approximate average cost per report is $0.50.

The above were calculated during the original experiments.
They are subject to change and beyond the control of the authors.

The main areas of interest are the directories:
- LANCE/GPT_IoCs : Where the final labels and justifications for each indicator (by LANCE) of each report can be seen in the corresponding CSV file
- LANCE/output_PDFs : Where the final PDF of each report can be seen. The annotations in the reports are invisible but can still be seen by hovering the mouse over the indicators and in the meta data of the PDF. That being said the optimal way to visualize the PDFs is the provided UI (claim 2)

