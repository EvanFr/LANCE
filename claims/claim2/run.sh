
cd ../../artifact/UI/

# open conda environment
eval "$(conda shell.bash hook)"
conda activate UI_env

# run the GAP (pyWeb2) UI with python
cd pyWeb2/


# for inspection of the BAP version of the UI please uncomment the following line
# cd ../pyWeb1/

python ./app.py
