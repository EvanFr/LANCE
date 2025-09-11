The run.sh script will do the following:
- Read the number of reports the user wants parsed (out of the 50 reports in PRIMS). This is so the reviewer(s) will not have to run LANCE for all 50 reports which would be time consuming and costly.
- Activate the anaconda environment for the open source LLMs. The environment was created from the install.sh .
- Run LANCE with Llama.
- Run LANCE with Nemotron.
- Run LANCE with Gemma.
- Activate the anaconda environment for Gemini, also created from the install.sh .
- Run LANCE with Gemini.

For each LLM the directories' structure looks like the one in LANCE (claim 5).
The only deference would be that they include a subdirectory: [LLM]_IoCs_copy.
These directories contain the output indicators, labels and justifications from LANCE from our run.

The approximate average run time per report is ~20 minutes for the open source models (Llama, Nemotron, and Gemma).
This depends on the GPUs used for running LANCE.

For Gemini the approximate average time per report is 2-3 minutes and the approximate average cost per report is $0.50.

The above were calculated during the original experiments.
They are subject to change and beyond the control of the authors.

