import pandas as pd
from pathlib import Path

# datafolder path is ../data relative to the current file make sure it is always regardless of where the file is called
data_folder_path = Path(__file__).resolve().parents[1] / 'data'

def get_repos():
    repos = pd.read_csv(f'{data_folder_path}/repositories.csv')
    return repos

def get_issues(filter=None):
    if filter == None:
        issues_metadata = pd.read_csv(f'{data_folder_path}/issues_metadata.csv')
        
        # check if exists
        if (data_folder_path / 'issues_properties.csv').exists():
            issues_properties = pd.read_csv(f'{data_folder_path}/issues_properties.csv')
            issues_properties.drop(columns=['html_url', 'repo', 'host', 'repo', 'url'], inplace=True)

            issues = issues_metadata.merge(issues_properties, on='id', how='left')
        else:
            issues = issues_metadata
    elif filter == 'metadata':
        issues = pd.read_csv(f'{data_folder_path}/issues_metadata.csv')
    elif filter == 'properties':
        issues = pd.read_csv(f'{data_folder_path}/issues_properties.csv')
    else:
        raise ValueError("Invalid filter. Use None or 'properties'.")

    return issues

def get_pull_requests():
    pull_requests = pd.read_csv(f'{data_folder_path}/processed/pull_requests_metadata.csv')

    return pull_requests

def get_commits():
    commits = pd.read_csv(f'{data_folder_path}/processed/commits_metadata.csv')

    return commits