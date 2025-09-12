# ATTENTION: 
# Before running this script, please make sure to replace "your_api_key_here" 
# with your actual Gemini API key.
Gemini_API_KEY="your_api_key_here"


# Get the number of reports from the command line argument, default to all 50 if not provided
if [ -z "$1" ]; then
    # No argument → set to 50
    rep_num=50
else
    # Check if argument is a positive integer
    if [[ "$1" =~ ^[0-9]+$ ]]; then
        rep_num=$1
    else
        echo "Error: Argument must be a positive integer."
        exit 1
    fi
fi

export rep_num



# navigate to the LANCE directory
cd ../../artifact/LANCE_sota_LLMs/


## Llama

# activate the conda environment
# the conda environment must be created first by running install.sh
eval "$(conda shell.bash hook)"
conda activate open_LLMs

cd ./Llama/

python extractor.py 

## Nemotron
cd ../nvidiaLama/

python extractor.py

## Gemma

cd ../gemma/

python extractor.py

## Gemini


# assert that the API key has been replaced
if [ "$Gemini_API_KEY" == "your_api_key_here" ]; then
  echo "Please replace 'your_api_key_here' with your actual Gemini API key in run.sh"
  exit 1
fi

export Gemini_API_KEY

conda deactivate
conda activate Gemini

cd ../Gemini/
python extractor.py
