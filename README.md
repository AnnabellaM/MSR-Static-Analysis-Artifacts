# MSR-Static-Analysis-Artifacts
This repository contains the code for the paper "Mining Repositories to Understand User and Developer Challenges with Static Analysis Tools".

## Code Structure
- 'analysis': Contains the scripts and notebooks for all analyses performed in the paper.
- 'download_data': Contains scripts to download the data used in the analyses.
- 'utils': Contains utility functions used across the different analyses (ex. constants, data loading functions, preprocessing functions).

## Data
The get the data used in this project, download the data from the following link:
[MSR-Static-Analysis Data](https://drive.google.com/file/d/12cIILySkvsyZYdkrPSwRWKQaI0dDLTKq/view?usp=sharing)
Save the data in the root directory of this repository and unzip it. The data should be in a folder named `data`.

## Requirements
The python requirements for the project can be found in the `requirements.txt` file. You can install them using pip:

```bash
pip install -r requirements.txt
```