# ATTENTION: 
# Before running this script, please make sure to replace "your_api_key_here" 
# with your actual OpenAI API key.
OpenAI_API_KEY="your_api_key_here"

# assert that the API key has been replaced
if [ "$OpenAI_API_KEY" == "your_api_key_here" ]; then
  echo "Please replace 'your_api_key_here' with your actual OpenAI API key in run.sh"
  exit 1
fi

# navigate to the LANCE directory
cd ../../artifact/LANCE/

# activate the conda environment
# the conda environment must be created first by running install.sh
eval "$(conda shell.bash hook)"
conda activate LANCE_GPT

# Export the API key as an environment variable within this session
export OpenAI_API_KEY

# run the LANCE.py script with the API key as an environment variable
python LANCE.py
