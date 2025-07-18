# The Artifacts for "Mining Repositories to Understand User and Developer Challenges with Static Analysis Tools"

## Table of Contents
- [Purpose](#purpose)
- [Repository Structure](#repository-structure)
- [Setup](#setup)
    - [Requirements](#requirements)
    - [Download Data (From Google Drive) (Recommended)](#download-data-from-google-drive-recommended)
    - [Download Data (From GitHub/BitBucket)](#download-data-from-githubbitbucket)
- [General](#general)
    - [Generate General Statistics](#generate-general-statistics)
    - [Calculate LoC For Each Repository](#calculate-loc-for-each-repository)
- [RQ1. Common Properties and Patterns](#rq1-common-properties-and-patterns)
    - [Generate Common Properties (already included with Google Drive download)](#generate-common-properties-already-included-with-google-drive-download)
    - [Generate Category With Catiss (already included with Google Drive download)](#generate-category-with-catiss-already-included-with-google-drive-download)
    - [Format Tool Names](#format-tool-names)
    - [Common Properties Figures](#common-properties-figures)
    - [Interest Groups (already included with Google Drive download)](#generate-interest-groups-already-included-with-google-drive-download)
    - [Generate Interest Groups Figures](#interest-groups-figures)
- [RQ2. Common Challenges](#rq2-common-challenges)
    - [Topic Modeling with BERTopic (already included with Google Drive download)](#topic-modeling-with-bertopic-already-included-with-google-drive-download)
    - [Topic Modeling Figures](#topic-modeling-figures)
    - [Cross Comparison of Interest Groups and Topic Groups](#cross-comparison-of-interest-groups-and-topic-groups)
- [RQ3. Static Analysis Tools](#rq3-static-analysis-tools)

## Purpose
This artifact repository contains the code, data, and results for the paper *"Mining Repositories to Understand User and Developer Challenges with Static Analysis Tools"*.

## Repository Structure
- `analysis`: Contains the scripts and notebooks for all analyses performed in the paper.
- `download_data`: Contains scripts to download the data used in the analyses.
- `results`: Contains the results of the analyses, including figures and tables (csv)
- `utils`: Contains utility functions used across the different analyses (ex. constants, data loading functions, preprocessing functions).



## Setup
### Requirements
The evaluation of this artifact does not require specific hardware. However, the recommended specifications are as listed:
- **Python** 3.9.6 (version project was developed on)
- **Pip** 25.1.1 (version project was developed on)

First create a virtual enviornment using the commands:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
```
Then install the required packages. The requirements are listed in the `requirements.txt` file.
The packages used in this project can be install using the following command:
```bash
pip install -r requirements.txt
```

### Download Data (From Google Drive) (Recommended)
To get the data used in this project, download the data from the following link:
[MSR-Static-Analysis Data](https://drive.google.com/file/d/159g3vpngk6OmsKBZnDTJgNyrwETmhkAO/view?usp=sharing)
Save the data in the root directory of this repository and unzip it. The data should be in a folder named `data`.

#### `issues_metadata.csv`
This file contains the raw metadata of the issues collected from GitHub or BitBucket. It includes information such as issue ID, title, body, labels, etc..

#### `pull_requests_metadata.csv`
This file contains the raw metadata of the pull requests collected from GitHub or BitBucket. It includes information such as pull request ID, linked commits, etc.

#### `commits_metadata.csv`
This file contains the raw metadata of the commits collected from GitHub or BitBucket. It includes information such as commit ID, number of files changed, etc.

#### `issues_properties.csv`
This file contains the properties of the issues which are generated from this [notebook](./analysis/common_properties/generate_common_properties.ipynb). All the columns with the prefix `prop:` are considered properties. The columns with the prefix `ig:` are interest group information, having a boolean value indicating whether the corresponding issue is part of the interest group or not.

#### `repositories.csv`
This file contains the repositories used in the paper. It includes the repository name and host (GitHub or BitBucket).

### Download Data (From GitHub/BitBucket)
If you want to download the data directly from GitHub or BitBucket, you can use the scripts in the `download_data` folder.
First, get API keys from both Github and Atlassian and save them in a .env file in the root directory of this repository. The file should contain the following variables:
```GITHUB_TOKEN=your_github_token
ATLASSIAN_TOKEN=your_atlassian_token
```

Run the following command to download the issues and pull requests metadata from GitHub or BitBucket:
```bash
python download_data/download_issues.py
```
Run the following command to download the commits metadata from GitHub or BitBucket:
```bash
python download_data/download_commits.py
```
Then run the following command to generate the csv data files:
```bash
python download_data/generate_csv.py
```

## General
This section contains the generation of the general statistics of the repositories.
### Generate General Statistics
The general statistics of the repositories are generated from [subject_tools.ipynb](./analysis/general/subject_tools.ipynb). This notebook generates the general statistics of the repositories and saves them in the `results/csv/general` folder. The statistics include the number of stars and issues for each repository.
### Calculate LoC For Each Repository
The lines of code (LoC) for each repository is calculated from [loc.ipynb](./analysis/general/loc.ipynb). This notebook calculates the LoC with `cloc` for each repository and saves the results in the `results/csv/general/loc/` folder. Each repository has its own file.

## RQ1. Common Properties and Patterns
### Generate Common Properties (already included with Google Drive download)
The common properties of the issues are generated from [generate_common_properties.ipynb](./analysis/common_properties/generate_common_properties.ipynb). This notebook generates the common properties of the issues and saves them in the `issues_properties.csv` file in the `data` folder. The properties are identified by the prefix `prop:` in the column names.
### Generate Category With Catiss (already included with Google Drive download)
The Catiss model is used to classify all the issues into bug, question, and enhancement. To download the Catiss model, perform the following steps:
1. Clone the Catiss Repository in the current directory:
    ```bash
    git clone https://github.com/MalihehIzadi/catiss.git catiss
    ```
2. Download the catiss model (pytorch_model.bin) from https://drive.google.com/drive/folders/1jgV4U41-2acctpc6jH5DWL3fF5V6bKF8 and place in the `catiss/model/` directory.
3. Run the [catiss_classification.ipynb](./analysis/catiss_classification/catiss_classification.ipynb) notebook to classify the issues into bug, question, and enhancement. The results are saved in the `issues_properties.csv` file in the `data` folder. The category is identified by `prop:category` in the column names.
4. Verify the results by running [predictions_analysis.ipynb](./analysis/catiss_classification/predictions_analysis.ipynb). This notebook calculates the accuracy of the Catiss model against the issues with labels.

### Format Tool Names
The formatted tool names are generated from [set_tool_name.py](./analysis/general/set_tool_name.py). The script reads the `issues_properties.csv` file and generates the tool names for each issue from the constants in `utils/constants.py`. The tool names are saved in the `issues_properties.csv` file in the `data` folder in the column `tool_name`.

### Common Properties Figures
The common properties figures are generated from [common_properties_figures.ipynb](./analysis/common_properties/common_properties_figures.ipynb). This notebook generates the figures for the common properties of the issues and saves them in the `results/figures/common_properties` folder.

### Generate Interest Groups (already included with Google Drive download)
The next step of RQ1 is generating the interest groups. The interest groups are generated from [interest_groups.ipynb](./analysis/interest_groups/interest_groups.ipynb). This notebook generates the interest groups and saves them in the `issues_properties.csv` file in the `data` folder. The interest groups are identified by the prefix `ig:` in the column names.

### Interest Groups Figures
The interest groups figures are generated from [interest_groups_figures.ipynb](./analysis/interest_groups/interest_groups_figures.ipynb). This notebook generates the figures for the interest groups and saves them in the `results/figures/interest_groups` folder.

## RQ2. Common Challenges
### Topic Modeling with BERTopic (already included with Google Drive download)
The common challenges are identified through topic modeling with BERTopic. The clustering can found in the [clustering](./analysis/topic_modeling/clustering) folder. Each file in this folder clusters one of the issue categories (bug, question, enhancement). Run each of the notebooks in this folder to generate the clusters. The topics for each are generated in `results/csv/topic_modeling/manual_review` folder. These are the topics that we label during the *Topic Refinement* step in the paper.

**IMPORTANT: At this point, to recreate the results, you must use the `data` folder provided from the Google Drive link previously mentioned, as it contains the clustering results we generated.**

### Topic Modeling Figures
The topic modeling figures are generated from [topic_modeling_figures.ipynb](./analysis/topic_modeling/topic_modeling_figures.ipynb). This notebook generates the figures for the topic modeling and saves them in the `results/figures/topic_modeling` folder.

### Cross Comparison of Interest Groups and Topic Groups
The cross-comparison of interest groups and topic groups is performed to identify common patterns and relationships between the two. This analysis helps in understanding how different interest groups are associated with specific topics and vice versa. The cross-comparison is done in [interest_groups_per_group.ipynb](./analysis/cross_comparison/interest_groups_per_group.ipynb). This notebook generates the cross-comparison and saves the results in the `results/cross_comparison` folder.

## RQ3. Static Analysis Tools
The work in this section is performed manually.