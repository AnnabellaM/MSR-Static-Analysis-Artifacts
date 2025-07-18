# The Artifacts for "Mining Repositories to Understand User and Developer Challenges with Static Analysis Tools"

## Table of Contents
- [Purpose](#purpose)
- [Repository Structure](#repository-structure)
- [Setup](#setup)
    - [Requirements](#requirements)
    - [Data](#data)
- [Detailed Description](#detailed-description)
    - [Data](#data)
        - [data.zip](#datazip)
        - [RQ2](#rq2)
        - [RQ3](#rq3)
    - [Code](#code)
        - [Download Data](#download-data)
        - [Analysis](#analysis)    
            - [Subject Tools](#subject-tools)
            - [Common Properties](#common-properties)
            - [Figures](#figures)
            - [Interest Groups](#interest-groups)
        - [Topic Modeling](#topic-modeling)
        - [Download Data](#download-data)
        - [Utils](#utils)

## Purpose
This artifact repository contains the code, data, and results for the paper *"Mining Repositories to Understand User and Developer Challenges with Static Analysis Tools"*.

## Repository Structure
- `code/`: Contains the code of the project.
    - `analysis/`: Contains the various analysis performed in the paper.
        - `subject_tools/`: Contains the code to provide the general statistics of the subject tools.
        - `common_properties/`: Contains the code to generate the common properties of issues (RQ1).
            - `catiss_classification/`: Contains the code to classify issues into bugs, questions, and enhancements using CatISS.
        - `interest_groups/`: Contains the code to generate the interest groups (RQ1).
        - `figures/`: Contains the code to generate the figures in the paper.
    - `topic_modeling/`: Contains the code for topic modeling using BERTopic (RQ2).
    - `download_data/`: Contains scripts to download the data from GitHub and BitBucket.
    - `utils/`: Contains utility functions and constants used throughout the code.
- `data/`: Contains the data used in the project.
    - `data.zip`: Zip file containing all issues used in the project.
    - `RQ2/`: Contains the full list of original and refined topics.
        - `RQ2_Topic_List.pdf`: Contains the full list of the refined topics.
        - `RQ2_Raw_Topic_Bugs.csv`: Contains the original topics for bugs.
        - `RQ2_Raw_Topic_Questions.csv`: Contains the original topics for questions.
        - `RQ2_Raw_Topic_Enhancements.csv`: Contains the original topics for enhancements.
    - `RQ3/`: Contains the results of the manual analysis performed on the 60 issues.

## Setup
### Requirements
The evaluation of this artifact does not require specific hardware. However, the recommended specifications are as listed:
- **Python** 3.9.6 (version project was developed on)
- **Pip** 25.1.1 (version project was developed on)

## Detailed Description
### Data
#### data.zip
The full dataset of all issues used in this project are located in the `data/data.zip` file of this repository. Details regarding each of the files inside the zipped data file are provided below:

- `issues_metadata.csv`
This file contains the raw metadata of the issues collected from GitHub or BitBucket. It includes information such as issue ID, title, body, labels, etc..

- `pull_requests_metadata.csv`
This file contains the raw metadata of the pull requests collected from GitHub or BitBucket. It includes information such as pull request ID, linked commits, etc.

- `commits_metadata.csv`
This file contains the raw metadata of the commits collected from GitHub or BitBucket. It includes information such as commit ID, number of files changed, etc.

- `issues_properties.csv`
This file contains the properties of the issues which are generated from this [notebook](./code/analysis/common_properties/generate_common_properties.ipynb). All the columns with the prefix `prop:` are considered properties. The columns with the prefix `ig:` are interest group information, having a boolean value indicating whether the corresponding issue is part of the interest group or not.

- `repositories.csv`
This file contains the repositories used in the paper. It includes the repository name and host (GitHub or BitBucket).

### Code
#### Download Data
The data is downloaded from GitHub and BitBucket in the scripts located in the `code/download_data/` directory. The scripts are as follows:
- [download_issues.py](./code/download_data/download_issues.py): This script downloads issues and pull requests from GitHub and BitBucket. These are saved into json files in a `raw_data/` directory.
- [download_commits.py](./code/download_data/download_commits.py): This script downloads commits from GitHub and BitBucket. These are saved into json files in a `raw_data/` directory.
- [generate_dataset.py](./code/download_data/generate_dataset.py): This script generates the dataset from the raw data downloaded from GitHub and BitBucket. It processes the raw data and saves it into CSV files in the `data/` directory. Specifically, it generates the `issues_metadata.csv`, `pull_requests_metadata.csv`, and `commits_metadata.csv`.
#### Analysis
The analysis performed in the paper is located in the `code/analysis/` directory. They answer RQ1 of the paper. The analysis is divided into the following subdirectories:

##### Subject Tools
Contains the code to provide the general statistics of the subject tools. This answers Section 3 of the paper (Research Questions and Study Objects). It identifies the number of stars, issues, and LoC of the subject tools (using cloc).

- [subject_tools.ipynb](./code/analysis/subject_tools/subject_tools.ipynb)
This notebook contains the code to provide the general statistics of the subject tools. It collects the number of stars and issues from each repository.

- [loc.ipynb](./code/analysis/subject_tools/loc.ipynb)
This notebook contains the code to calculate the lines of code (LoC) of the subject tools using the `cloc` tool. It runs `cloc` on each repository and collects the LoC information.

- [set_tool_name.py](./code/analysis/subject_tools/set_tool_name.py)
This script is used to set the formatted names of the subject tools in the issue data.

##### Common Properties
- [generate_common_properties.ipynb](./code/analysis/common_properties/generate_common_properties.ipynb)
Contains the code to generate the common properties of the issues. The properties are listed as follows:
    - *state*: whether the issue is open or closed
    - *category*: whether the issue is a bug, question, or enhancement
    - *resolution time*: the time taken to resolve the issue (if closed)
    - *number of comments*: the number of comments on the issue
    - *number of unique users*: the number of unique users who commented on the issue
    - *number of files changed*: the number of files changed in the issue (from linked pull requests and commits)
    - *number of lines changed*: the number of lines changed in the issue (from linked pull requests and commits)

Each of these properties is calculated for each issue in the dataset. The results of this analysis are stored in the `issues_properties.csv` file in the zipped data file.

- [collect_specific_datapoints.ipynb](./code/analysis/common_properties/collect_specific_datapoints.ipynb)
Contains the code used to collect specific datapoints from the issues mentioned throughout the paper. This includes various distributions of the properties of the issues.

- [investigation.ipynb](./code/analysis/common_properties/investigation.ipynb)
Contains the code to investigate the specific case or a large amount of files and LoC in PMD and SootUp issues.

- `analysis/catiss_classification/`
While all of the other properties can be easily extracted from the datasets, the category property requires additional processing, as it is not directly provided from metadata. This directory contains the code to classify issues into bugs, questions, and enhancements using CatISS.

- [catiss_classification.ipynb](./code/analysis/catiss_classification/catiss_classification.ipynb)
This notebook contains the code to classify issues into bugs, questions, and enhancements using CatISS. It uses the CatISS model to classify the issues based on their title and body. The results are stored in the `issues_properties.csv` file in the zipped data file.

    - [predictions_analysis.ipynb](./code/analysis/catiss_classification/predictions_analysis.ipynb) 
This notebook contains the code to analyze the accuracy of the CatISS model predictions. It compares the predictions with the existing labels in the dataset and calculates the accuracy of the model.

##### Figures
The figures in the paper are generated using the code in the `code/analysis/figures/` directory. These figure notebooks are calculated from the results of the analysis. The figures are as follows:
- *Figure 2*: Distribution of properties of static analysis issues across all tools. ([common_properties_figures.ipynb](./code/analysis/figures/common_properties_figures.ipynb))
- *Figure 3*: Distribution of interest groups by tool. ([interest_groups_figures.ipynb](./code/analysis/figures/interest_groups_figures.ipynb))
- *Figure 4*: Distribution of interest groups by topic groups. ([interest_groups_per_group_figures.ipynb](./code/analysis/figures/interest_groups_per_group_figures.ipynb))

##### Interest Groups
Contains the code to generate the interest groups (RQ1).

- [interest_groups.ipynb](./code/analysis/interest_groups/interest_groups.ipynb)
This notebook contains the code to generate the interest groups from the issues. The interest groups are as follows: quick resolution, slow resolution, easy fix, hard fix, hot topic, and ignored. It defines the interest group conditions, and then applies these conditions to these issues. The results are stored in the `issues_properties.csv` file in the zipped data file.

#### Topic Modeling
The topic modeling is performed using BERTopic and is located in the `code/topic_modeling/` directory. This answers RQ2 of the paper. Each of the notebooks in this directory contains code to perform topic modeling on the three categories of issues: bugs, questions, and enhancements independently ([cluster_bugs.ipynb](./code/topic_modeling/cluster_bugs.ipynb), [cluster_questions.ipynb](./code/topic_modeling/cluster_questions.ipynb), [cluster_enhancements.ipynb](./code/topic_modeling/cluster_enhancements.ipynb)). The results of the topic modeling are stored in the `issues_properties.csv` file in the zipped data file.

#### Utils
The utility functions and constants used throughout the code are located in the `code/utils/` directory. This includes functions to read and write data, process data, and constants used in the code.

- [constants.py](./code/utils/constants.py)
The constants used in the code are located in the `code/utils/constants.py` file. They include stop words, formatted names, and other constants used in the code.

- [dataloader.py](./code/utils/dataloader.py)
The dataloader is responsible for loading issue, pull request, commit, and repository data from the CSV files and providing it to the analysis code.

- [diamantopoulos_preprocessor.py](./code/utils/diamantopoulos_preprocessor.py)
The `diamantopoulos_preprocessor.py` file contains functions to preprocess the issue data using steps by Diamantopoulos et al. This includes text cleaning, tokenization, and other preprocessing steps to prepare the data for analysis.