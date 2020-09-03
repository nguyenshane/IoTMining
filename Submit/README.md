# IoTMining
This repo is a research project for the paper Incremental Learning from IoT for Smart Home Automation

## Prerequisite / Installation:
- Python 3.6 or install Anaconda for Python 3.6 (https://docs.anaconda.com/anaconda/user-guide/faq/#anaconda-faq-35), then import environment.yml to have the recommended environment
- Install efficient apriori library using `pip install efficient-apriori`

## Input:
- Data is stored in /dataset
- The full dataset for 36 weeks is located at https://github.com/nguyenshane/IoTMining/raw/master/IoTMining/dataset/data

## Usage:
- Execute `importData.py` to generate data and dataByWeek in numpy pickle
- Choose either `timeThresholdBasedAssociationRulesGenerator.py` or `durationPruning.py` to preprocess the pickled numpy data by week
- If pre-process data by `timeThresholdPruning.py`, run `timeThresholdBasedAssociationRulesGenerator.py` to generate the rules
- If pre-process data by `durationPruning.py`, run `durationBasedAssociationRulesGenerator.py` to generate the rules


## Outputs:
- All measurements are located in /ProgOutput
- All activities sets are stored in /ProgOutput
- All pickled numpy data are stored in /npy
- Matlab figures are generated to /matlabFig
- Time Threshold Based Association Rules are stored in /ttRules
- Duration Based Association Rules are stored in /dpRules
