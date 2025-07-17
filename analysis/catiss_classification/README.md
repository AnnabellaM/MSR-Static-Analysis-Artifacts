# Catiss Classification (RQ1)

This directory contains notebooks for classification of issues into bugs, questions, and enhancements, which is a subsection of the common properties section of the work (RQ1). They provide the results for the category property which is found in Figure 2(a) of the paper.

## Notebooks
- 'catiss_classification.ipynb': Contains the classification of issues into bugs, questions, and enhancements using the Catiss model.
- 'predictions_analysis.ipynb': Analyzes the predictions made by the Catiss model, providing insights into the classification results.

## Download the Catiss Model
To download the Catiss model, perform the following steps:
1. Clone the Catiss Repository in the current directory:
    ```bash
    git clone https://github.com/MalihehIzadi/catiss.git catiss
    ```
2. Download the catiss model (pytorch_model.bin) from https://drive.google.com/drive/folders/1jgV4U41-2acctpc6jH5DWL3fF5V6bKF8 and place in the `catiss/model/` directory.