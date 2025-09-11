cd ../../artifact/IoCMiner/

# activate the conda environment
# the conda environment must be created first by running install.sh
eval "$(conda shell.bash hook)"
conda activate IoC_Miner

python CTI_classifier.py