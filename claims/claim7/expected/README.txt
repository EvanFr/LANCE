The run.sh will go th the artifact/Comparison/ directory and execute the prominent_methods.py 

The directory contains all the outputs from the 5 different ground truth creation methods.
The structure of the directory is the following:

Comparison
├── AlienVault                                  # AlienVut evaluation on PRISM
│   ├── Results                                 # Results of the evaluation
│   │   ├── AV_FN.txt                           # All the false negatives (FN) per report
│   │   ├── AV_FP.txt                           # All the false positives (FP) per report
│   │   ├── AV_TP.txt                           # All the true positives (TP) per report
│   │   └── Results_AlienVault.json             # The results per indicator type
│   └── pulse2AV.json                           # All the IoC (active and inactive) related to the report as given from AlienVault at the time of the experiments
├── GoodFATR                                    # GoodFATR evaluation on PRISM
│   ├── GF_tester.py                            # The code that implements the methodology proposed in GoodFATR (it is already run, no need to rerun it)
│   └── Results                                 # Results of the evaluation
│       ├── GFM_FN.txt                          # All the false negatives (FN) per report
│       ├── GFM_FP.txt                          # All the false positives (FP) per report
│       ├── GFM_TP.txt                          # All the true positives (TP) per report
│       └── ResultsIoC_searcher_cleared.json    # The results per indicator type
├── PlainGPT                                    # Plain GPT evaluation on PRISM
│   ├── IoCs                                    # Results of the evaluation
│   │   ├── CVE                                 # All IoC CVEs given by naively prompted GPT per report
│   │   │   └── ReportNameA.txt                 # Naming Convention*
│   │   ├── Domain                              # All IoC Domains given by naively prompted GPT per report
│   │   │   └── ReportNameA.txt                 # Naming Convention*
│   │   ├── Hash                                # All IoC Hashes given by naively prompted GPT per report
│   │   │   └── ReportNameA.txt                 # Naming Convention*
│   │   ├── IP                                  # All IoC IPs given by naively prompted GPT per report
│   │   │   └── ReportNameA.txt                 # Naming Convention*
│   │   └── URL                                 # All IoC URLs given by naively prompted GPT per report
│   └── stats                                   # Results of the evaluation
│       ├── GPT_FN.txt                          # All the false negatives (FN) per report
│       ├── GPT_FP.txt                          # All the false positives (FP) per report
│       ├── GPT_TP.txt                          # All the true positives (TP) per report
│       └── Results.json                        # The results per indicator type
├── ReportsJSON                                 # All the reports' JSON files
│   └── ReportNameA.json                        # Naming Convention*
├── VirusTotal                                  # AlienVut evaluation on PRISM
│   ├── Results                                 # Results of the evaluation
│   │   ├── VT_th1_FN.txt                       # All the false negatives (FN) per report for threshold 1
│   │   ├── VT_th1_FP.txt                       # All the false positives (FP) per report for threshold 1
│   │   ├── VT_th1_TP.txt                       # All the true positives (TP) per report for threshold 1
│   │   ├── VT_th1_results.json                 # The results per indicator type for threshold 1
│   │   ├── VT_th5_FN.txt                       # All the false negatives (FN) per report for threshold 5
│   │   ├── VT_th5_FP.txt                       # All the false positives (FP) per report for threshold 5
│   │   ├── VT_th5_TP.txt                       # All the true positives (TP) per report for threshold 5
│   │   └── VT_th5_results.json                 # The results per indicator type for threshold 5
│   ├── ReportNameA_IoCs.txt                    # All the extracted indicators from the report using IoC searcher. Naming Convention*
│   └── ReportNameA_VT_results.csv              # The "votes" for each indicator of the report as given by VirusTotal at the time of the experiments. Naming Convention*
└── prominent_methods.py                        # The script that loads all the results and calculates Precision Recall and F1 Score per type for each of the methods.


*The naming convention for the files in this directory, where ReportNameA=the name of the report taken from the filename of the corresponding JSON file


### AlienVault:
For the evaluation of AlienVault we get all the indicators related to the report and assume these are labeled as IoCs while the rest of the extracted (by IoC searcher) indicators are labeled as nonIoCs.
We take active and inactive indicators as the "inactive" label indicates that the indicator is no longer active or malicious but was at the time of the attack.

### VirusTotal:
To evaluate the creation of ground truth using VirusTotal we extract all the indicators using IoC Searcher. 
We then get the number of malicious votes each indicator gets when queried on VirusTotal. 
We label as IoCs all the indicators that get number of votes greater than or equal the threshold.
We label as nonIoCs all the indicators that get number of votes less than the threshold or do not exist in the VirusTotal database.

### GoodFATR methodology:
We implement the methodology proposed by the Caballero et al. at the paper: "The Rise of GoodFATR: A Novel Accuracy Comparison Methodology for Indicator Extraction Tools".
We do that by first extracting all indicators using IoC Searcher (presented in the same paper). 
We then filter the resulting indicators by:
    a) Removing all domains that appear in the top 100k domains from the Tranco list.
    b) Removing all URLs that their domain appear in the top 100k domains from the Tranco list.
    c) Removing all privet IPs.

### Naive GPT:
To evaluate how ChatGPT 4o would perform in the IoC extraction and labeling task with a naive prompt and pipeline we generated a naive prompt and together with the text of the report we used it to request the IoCs of each of the 50 reports.
All return indicators were considered as labeled IoCs whereas all indicators extracted from the report (by IoC searcher) that where not returned where considered nonIoCs.
The naive prompt is as follows:
'''
Extract all IoC [indicator_type] from the following report. Make sure you extracted ALL IoC [indicator_type], but you did not include any false positives. Give me all IoC [indicator_type] in a csv format:
'''
