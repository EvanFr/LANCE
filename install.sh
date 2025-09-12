###
# Install script for the project
###

echo "Starting installation..."

# Unzip the directories in the artifact/

echo "Unzipping all .tgz files in artifact/ directory..."

TARGET_DIR="./artifact/"

for file in "$TARGET_DIR"*.tgz; do
    # Check if any files matched
    [ -e "$file" ] || continue

    echo "Extracting: $file"
    tar -xvzf "$file" -C "$TARGET_DIR"
done

echo "Unzipping completed. [1/6]"

# minor fixes
cp ./artifact/LANCE_sota_LLMs/Llama/reports.txt ./artifact/LANCE_sota_LLMs/Gemini/reports.txt

sed -i '$d' ./artifact/LANCE_sota_LLMs/transformers_env.yml
echo "      - iocsearcher==2.4.3" >> artifact/LANCE_sota_LLMs/transformers_env.yml
# Making sure Anaconda is installed

if command -v conda &> /dev/null; then
    echo "Anaconda is already installed."
else
    echo "Anaconda is not installed. Please install Anaconda from https://www.anaconda.com/products/distribution and rerun this script."
    exit 1
fi

# Create UI conda environment
echo "Creating conda environment for UI (claim 2)..."
eval "$(conda shell.bash hook)"

conda env create -n UI_env python=3.12 -y
conda activate UI_env
pip install -r ./artifact/UI/requirements.txt
conda deactivate

echo "Conda environment for UI created. [2/6]"

# Create LANCE-GPT conda environment
echo "Creating conda environment for LANCE-GPT (claim 5)..."

conda env create -f ./artifact/LANCE/environment.yaml -y

echo "Conda environment for LANCE-GPT created. [3/6]"

# Create LANCE-OpenSource conda environment
echo "Creating conda environment for LANCE-OpenSource (claim 6)..."

conda env create -f ./artifact/LANCE_sota_LLMs/transformers_env.yml  -y
echo "Conda environment for LANCE-OpenSource created. [4/6]"

# Create LANCE-Gemini conda environment
echo "Creating conda environment for LANCE-Gemini (claim 6)..."

conda env create -f ./artifact/LANCE_sota_LLMs/Gemini/environment.yaml -y
echo "Conda environment for LANCE-Gemini created. [5/6]"

# Create IoC_Miner conda environment
echo "Creating conda environment for IoC_Miner (claim 9)..."

conda env create -f ./artifact/IoCMiner/environment.yaml -y

echo "Conda environment for IoC_Miner created. [6/6]"

echo "Installation completed successfully."
