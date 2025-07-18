import os
import pandas as pd
import json

raw_issue_data = []
raw_pull_request_data = []
raw_commit_data = []

for file in os.listdir('./raw_data/issues'):
    if file.endswith('.json'):
        issue_data = json.load(open(os.path.join('./raw_data/issues', file), 'r'))
        raw_issue_data.append(issue_data)

for file in os.listdir('./raw_data/pull_requests'):
    if file.endswith('.json'):
        pull_request_data = json.load(open(os.path.join('./raw_data/pull_requests', file), 'r'))
        raw_pull_request_data.append(pull_request_data)

for file in os.listdir('./raw_data/commits'):
    if file.endswith('.json'):
        commit_data = json.load(open(os.path.join('./raw_data/commits', file), 'r'))
        raw_commit_data.append(commit_data)

# Convert raw issue data to DataFrame
issues_df = pd.DataFrame(raw_issue_data)
pull_requests_df = pd.DataFrame(raw_pull_request_data)
commits_df = pd.DataFrame(raw_commit_data)


issues_df = issues_df[['id', 'title', 'body', 'user', 'state', 'created_at', 'closed_at', 'updated_on', 'timeline', 'html_url', 'labels', 'repo', 'host']]
pull_requests_df = pull_requests_df[['id', 'html_url', 'repo', 'host', 'commits']]

commits_df = commits_df[['sha', 'files']]
new_commits = []

for i, row in commits_df.iterrows():
    if isinstance(row['files'], list):
        files = row['files']
        new_files = []
        for file in files:
            # Process each file
            # only keep the file name and changes count
            file_name = file['filename']
            changes = file['changes']
            new_files.append({'filename': file_name, 'changes': changes})
    new_commits.append({'sha': row['sha'], 'files': new_files})

new_commits_df = pd.DataFrame(new_commits)

# create folder if it does not exist
if not os.path.exists('./data'):
    os.makedirs('./data')
# Save the processed data to CSV files
issues_df.to_csv('./data/issues_metadata.csv', index=False)
pull_requests_df.to_csv('./data/pull_requests_metadata.csv', index=False)
commits_df.to_csv('./data/commits_metadata.csv', index=False)