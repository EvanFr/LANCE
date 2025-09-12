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

    # Remove any macOS metadata files like ._Report10.pdf etc.
    find "$TARGET_DIR" -type f -name '._*' -delete
done


echo "[1/7] Unzipping completed."

# minor fixes
cp ./artifact/LANCE_sota_LLMs/Llama/reports.txt ./artifact/LANCE_sota_LLMs/Gemini/reports.txt

sed -i '$d' ./artifact/LANCE_sota_LLMs/transformers_env.yml
echo "      - iocsearcher==2.4.3" >> artifact/LANCE_sota_LLMs/transformers_env.yml
echo "      - pymupdf==1.25.3" >> artifact/LANCE_sota_LLMs/transformers_env.yml
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

conda create -n UI_env python=3.12 -y
conda activate UI_env
pip install -r ./artifact/UI/requirements.txt
conda deactivate

echo "[2/7] Conda environment for UI created."

# Create LANCE-GPT conda environment
echo "Creating conda environment for LANCE-GPT (claim 5)..."

conda env create -f ./artifact/LANCE/environment.yaml -y

echo "[3/7] Conda environment for LANCE-GPT created."

# Create LANCE-OpenSource conda environment
echo "Creating conda environment for LANCE-OpenSource (claim 6)..."

conda env create -f ./artifact/LANCE_sota_LLMs/transformers_env.yml  -y
echo "[4/7] Conda environment for LANCE-OpenSource created."

# Create LANCE-Gemma conda environment
echo "Creating conda environment for LANCE-Gemma (claim 6)..."

conda env create -n LANCE-Gemma -f ./artifact/LANCE_sota_LLMs/transformers_env.yml  -y
conda activate LANCE-Gemma
pip uninstall transformers -y
pip install git+https://github.com/huggingface/transformers@v4.49.0-Gemma-3
echo "[5/7] Conda environment for LANCE-Gemma created."


# Create LANCE-Gemini conda environment
echo "Creating conda environment for LANCE-Gemini (claim 6)..."

conda env create -f ./artifact/LANCE_sota_LLMs/Gemini/environment.yaml -y
echo "[6/7] Conda environment for LANCE-Gemini created."

# Create IoC_Miner conda environment
echo "Creating conda environment for IoC_Miner (claim 9)..."

conda env create -f ./artifact/IoCMiner/environment.yaml -y

echo "[7/7] Conda environment for IoC_Miner created."

echo "Installation completed successfully."
