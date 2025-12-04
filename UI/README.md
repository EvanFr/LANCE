# IoC extraction 

Thank you for participating it this test!

## Target of this experiment

You mission, if you choose to accept it, is to label Indicators in Cyber Security Reports as either Indicators of Compromise (IoC) or not.

## Part 1: Baseline
For this task, you are provided with a web interface that will (hopefully) help you to execute the task in a more efficient way.
You have been assigned 10 reports. 
The Indicators in this reports have been extracted by our system.
You are requested to make sure you label all Indicators in each Report.
The interface will record the time you needed to complete the labeling of Indicators for each report. The timer will start automatically when you load the report and will stop and be stored automatically when the .json file is downloaded. You are requested to label all indicators of each report in one siting. You can take brakes between reports.




### Installation
```sh
# install the necessary packages from requirements.txt
$ pip install -r requirements.txt
```

### Setup
```sh
$ cd ./pyWeb1
$ python app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://XX.XX.XX.XX:XXXX
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```
You can access the web interface of the application in the "Running on" link that you see in the first lines of the output.
**Note:** Leave the python program running for as long as you are using the application.


### Usage

The interface has several features that can help you complete your task more efficiently.
A short demo/tutorial of the tool can be seen in the UI_tutorial_1 video.

### Indicators

The targeted indicators belong to one of the following categories:
CVE, domain, IP, URL, HASH

Each one of those can be either an IoC or nonIoC.
All of the instances of an indicator should have the same label at all times. This is ensured by the system, meaning, the changes that you make in one indicator (label, comments, etc.) are persistent to all of the instances of that Indicator

### Resources

You are **NOT** allowed to use the internet or other resources to help you determine whether an indicator is an IoC or not.
You should make this decision based **only** on the content of the report and your understanding of Indicators of Compromise.

### Labeling Output 

After the completion of the labeling of all indicators in a report, you should click the "Download JSON" button on the top of the web app and make sure you have downloaded the corresponding .json file.
This file for each of the 10 reports is what we will request from you at the end of the experiment


## Part 2: LLM Assisted Labeling.

For this task, you are provided with a web interface that will (hopefully) help you to execute the task in a more efficient way.
You have been assigned 10 reports. 
The Indicators in this reports have been extracted **and labeled** by our system and you will be provided with a suggested label and justification for that label for each Indicator.
Those labels might be false. You are requested to make sure you identify the false labels and correct them.
Ideally, a short comment for your correction should be provided in the corresponding field of the app.
The interface will record the time you needed to complete the labeling of Indicators for each report. The timer will start automatically when you load the report and will stop and be stored automatically when the .json file is downloaded. You are requested to label all indicators of each report in one siting. You can take brakes between reports.

### Installation
```sh
# install the necessary packages from requirements.txt
$ pip install -r requirements.txt
```

### Setup
```sh
$ cd ./pyWeb2
$ python app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://XX.XX.XX.XX:XXXX
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```
You can access the web interface of the application in the "Running on" link that you see in the first lines of the output.
**Note:** Leave the python program running for as long as you are using the application.


### Usage

The interface has several features that can help you complete your task more efficiently.
A short demo/tutorial of the tool can be seen in the UI_tutorial_2 video.

## Indicators

The targeted indicators belong to one of the following categories:
CVE, domain, IP, URL, HASH

Each one of those can be either an IoC or nonIoC.
Each detected indicator is labeled buy the system either as IoC or nonIoC. 
The system also provides a justification for it's choice of label. 
All of the instances of an indicator should have the same label at all times. This is ensured by the system, meaning, the changes that you make in one indicator (label, comments, etc.) are persistent to all of the instances of that Indicator

### Resources

You are **NOT** allowed to use the internet or other resources to help you determine whether an indicator is an IoC or not.
You should make this decision based on the content of the report, and your understanding of Indicators od Compromise

### Labeling Output 

After the completion of the labeling of all indicators in a report, you should click the "Download JSON" button on the top of the web app and make sure you have downloaded the corresponding .json file.
This file for each of the 10 reports is what we will request from you at the end of the experiment

