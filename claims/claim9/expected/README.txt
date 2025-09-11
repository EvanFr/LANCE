The run.sh will go the the artifact/IoCMiner/ directory and execute the CTI_classifier.py 

The CTI_classifier.py file is used as given in the original repository with minor changes in the input (so it is trained and tested on the created datasets)
The file creates and trains several (11) random forest classifiers on the vectorized sentences.
It then uses them to vote on the label of the indicator in the test sentences.

The datasets we used for training and testing where created by isolating sentences from the reports that contain indicators.
We then label the indicators using three different methods: 
- LANCE
- VirusTotal with threshold=1
- VirusTotal with threshold=5

The threshold for the VirusTotal dataset was used to determine weather an indicator was an IoC (votes >= threshold) or not.
The datasets created by VirusTotal have ~500 less sentences as the indicators included in those where not in the VirusTotal database.

Then the sentences where vectorized to a bag of words format, as it is the required input of the model.

The structure of the IoCMiner directory is as follows:

IoCMiner
├── CTI_classifier.py                    # File from the original repository. It trains and test the IoC classifiers.
├── CTI_expert_finder.py                # File from the original repository. Unused in our case.
├── LICENSE                             # License from the original repository.
├── README.md                           # README from the original repository.
├── dataset                             # Directory that contains the datasets for training and testing.
│   ├── dataset50GPT_processed.csv      # Dataset created with labels from LANCE using GPT as the underline LLM. Used for training.
│   ├── dataset50VT1_processed.csv      # Dataset created with RegEx + VirusTotal (threshold=1). Used for training.
│   ├── dataset50VT5_processed.csv      # Dataset created with RegEx + VirusTotal (threshold=5). Used for training.
│   └── datasetTest50GT_processed.csv   # Dataset created from PRISM. Used for testing.
├── environment.yaml                    # File used for the IoC_Miner environment. Used in install.sh .
├── main.py                             # File from the original repository. Unused in our case.
└── utility.py                          # File from the original repository. Unused in our case.


### Runtime

The first time the CTI_classifier is run it will download the necessary data from nltk. 
This might take a couple of minutes.

The models are retrained for every run but they are trained quickly and do not use GPU.
Given the rundowns of the training and the nature of random forests the results are different for each run.
That being said the general trend that the IoC_Miner trained on LANCE outperforms the other two is persistent.
