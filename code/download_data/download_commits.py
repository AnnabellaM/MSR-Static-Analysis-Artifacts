from github import Github
from github import Auth
from dotenv import dotenv_values
import os
from tqdm import tqdm
import json
import pandas as pd
import requests
import sys
sys.path.append('../')
from utils.dataloader import get_repos

config = dotenv_values("../../.env")
auth = Auth.Token(config['GITHUB_TOKEN'])
gh = Github(auth=auth)
repos = get_repos()

if not os.path.exists('../../raw_data/commits'):
    os.makedirs('../../raw_data/commits')

# Github
for _, repo in repos[repos['Host'] == "Github"].iterrows():
    tqdm.write(f"Downloading commits for {repo['Repository']}")
    repository = gh.get_repo(repo['Repository'])
    commits = repository.get_commits()
    for commit in tqdm(commits, desc=repo['Repository'], total=commits.totalCount):
        if os.path.exists(f'../../raw_data/commits/Github_{repo["Repository"].split("/")[1]}_{commit.sha}.json'):
            tqdm.write(f"Skipping commit {commit.sha}")
            continue
        tqdm.write(f"Downloading commit {commit.sha}")
        # Save commit data to file
        raw_data = commit.raw_data
        raw_data['repo'] = repo['Repository']
        json.dump(commit.raw_data, open(f'../../raw_data/commits/Github_{repo["Repository"].split("/")[1]}_{commit.sha}.json', 'w')) 

# Bitbucket
for _, repo in repos[repos['Host'] == "Bitbucket"].iterrows():
    tqdm.write(f"Downloading commits for {repo['Repository']}")

    url = f"https://api.bitbucket.org/2.0/repositories/{repo['Repository']}/commits"
    while True:
        response = requests.get(url)

        commits = response.json()
        for commit in commits['values']:
            if os.path.exists(f'../../raw_data/commits/Bitbucket_{repo["Repository"].split("/")[1]}_{commit["hash"]}.json'):
                tqdm.write(f"Skipping commit {commit['hash']}")
                continue
            tqdm.write(f"Downloading commit {commit['hash']}")
            data = {}
            data['repo'] = repo['Repository']
            data['type'] = 'commit'
            data['sha'] = commit['hash']
            data['message'] = commit['message']
            data['author'] = {
                'uuid': commit['author']['user']['uuid'],
                'account_id': commit['author']['user']['account_id'],
            } if 'user' in commit['author'] else None
            data['date'] = commit['date']
            data['parent'] = [parent['hash'] for parent in commit['parents']]
            data['patch'] = commit['links']['diff']['href']

            json.dump(data, open(f'../../raw_data/commits/Bitbucket_{repo["Repository"].split("/")[1]}_{commit["hash"]}.json', 'w'))

        if 'next' in commits:
            url = commits['next']
        else:
            break