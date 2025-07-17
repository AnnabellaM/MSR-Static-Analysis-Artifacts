from github import Github
from github import Auth
from dotenv import dotenv_values
import os
import json
from tqdm import tqdm
import pandas as pd
import requests
import json

config = dotenv_values("../.env")
auth = Auth.Token(config['GITHUB_TOKEN'])
gh = Github(auth=auth)

# repos = pd.read_csv('./repositories.csv')
repos = [
    {'Repository': 'phpstan/phpstan-src', 'Host': 'Github'},
]

repos = pd.DataFrame(repos)

output_dir = '../data'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    os.makedirs(os.path.join(output_dir, 'issues'))
    os.makedirs(os.path.join(output_dir, 'pull_requests'))

# github issues
for _, repo_name in repos[repos['Host'] == "Github"].iterrows():
    tqdm.write(f"Downloading issues for {repo_name['Repository']} (Github)")

    repository = gh.get_repo(repo_name['Repository'])

    repo_items = repository.get_issues(state='all')

    for repo_item in tqdm(repo_items, desc=repo_name['Repository'], total=repository.get_issues(state='all').totalCount):
        if repo_item.pull_request:
            # pull request
            if os.path.exists(os.path.join(output_dir, 'pull_requests', f"Github_{repo_name['Repository'].split('/')[1]}_{repo_item.id}.json")):
                tqdm.write(f"Skipping {repo_item.id}")
                continue
            pull_request = repo_item.as_pull_request()

            data = {}
            data['repo'] = repo_name['Repository']
            data['host'] = "Github"
            data['type'] = "pull_request"
            data['id'] = pull_request.id
            data['user'] = pull_request.user.login,
            data['head'] = {
                'label': pull_request.head.label,
                'ref': pull_request.head.ref,
                'sha': pull_request.head.sha,
            }
            data['title'] = pull_request.title
            data['body'] = pull_request.body
            data['html_url'] = pull_request.html_url
            data['state'] = pull_request.state
            data['created_at'] = str(pull_request.created_at)
            data['closed_at'] = str(pull_request.closed_at)
            data['merged'] = pull_request.merged
            data['mergeable'] = pull_request.mergeable
            data['mergeable_state'] = pull_request.mergeable_state
            data['merged_at'] = str(pull_request.merged_at)
            data['merge_commit_sha'] = pull_request.merge_commit_sha
            data['labels'] = [label.name for label in pull_request.labels]
            data['timeline'] = [
                {
                    'actor': {
                        'login': event.actor.login,
                    } if event.actor else None,
                    'event': event.event,
                    'commit_id': event.commit_id,
                    'commit_url': event.commit_url,
                    'source': {
                        'type': event.source.type,
                        'issue': {
                            'id': event.source.issue.id,
                            'html_url': event.source.issue.html_url,
                        },
                    } if event.source else None,
                    'body': event.body,
                    'author_association': event.author_association,
                    'created_at': str(event.created_at),
                    'url': event.url,
                }
                for event in repo_item.get_timeline()
            ]
            data['commits'] = [
                {
                    'sha': commit.sha,
                    'html_url': commit.html_url,
                }
                for commit in pull_request.get_commits()
            ]
            with open(os.path.join(output_dir, 'pull_requests', f"Github_{repo_name['Repository'].split('/')[1]}_{repo_item.id}.json"), 'w') as f:
                json.dump(data, f)
        else:
            if os.path.exists(os.path.join(output_dir, 'issues', f"Github_{repo_name['Repository'].split('/')[1]}_{repo_item.id}.json")):
                tqdm.write(f"Skipping {repo_item.id}")
                continue
            # issue
            data = {}
            data['repo'] = repo_name['Repository']
            data['id'] = repo_item.id
            data['host'] = "Github"
            data['type'] = "issue"
            data['title'] = repo_item.title
            data['body'] = repo_item.body
            data['html_url'] = repo_item.html_url
            data['created_at'] = str(repo_item.created_at)
            data['closed_at'] = str(repo_item.closed_at)
            data['state'] = repo_item.state
            data['user'] = repo_item.user.login,
            data['labels'] = [label.name for label in repo_item.labels]
            data['timeline'] = [
                {
                    'actor': {
                        'login': event.actor.login,
                    } if event.actor else None,
                    'event': event.event,
                    'commit_id': event.commit_id,
                    'commit_url': event.commit_url,
                    'source': {
                        'type': event.source.type,
                        'issue': {
                            'id': event.source.issue.id,
                            'html_url': event.source.issue.html_url,
                        },
                    } if event.source else None,
                    'body': event.body,
                    'author_association': event.author_association,
                    'created_at': str(event.created_at),
                    'url': event.url,
                }
                for event in repo_item.get_timeline()
            ]
            with open(os.path.join(output_dir, 'issues', f"Github_{repo_name['Repository'].split('/')[1]}_{repo_item.id}.json"), 'w') as f:
                json.dump(data, f)

# bitbucket issues
for _, repo in tqdm(repos[repos['Host'] == "Bitbucket"].iterrows(), desc="Bitbucket Repositories", total=len(repos[repos['Host'] == "Bitbucket"])):
    tqdm.write(f"Downloading issues for {repo['Repository']} (Bitbucket)")
    url = f"https://api.bitbucket.org/2.0/repositories/{repo['Repository']}/issues"

    # download issues
    while True:
        issues = requests.get(url).json()

        # process issues
        for issue in issues['values']:
            if os.path.exists(os.path.join(output_dir, 'issues', f"Bitbucket_{repo['Repository'].split('/')[1]}_{issue['id']}.json")):
                tqdm.write(f"Skipping {issue['id']}")
                continue
            tqdm.write(issue['id'])
            data = {}
            data['repo'] = repo['Repository']
            data['host'] = "Bitbucket"
            data['type'] = "issue"
            data['id'] = issue['id']
            data['title'] = issue['title']
            data['body'] = issue['content']['raw']
            data['html_url'] = issue['links']['html']['href']
            data['created_at'] = issue['created_on']
            data['state'] = issue['state']
            data['user'] = {
                'uuid': issue['reporter']['uuid'],
                'account_id': issue['reporter']['account_id'],
            } if issue['reporter'] else None
            data['updated_on'] = issue['updated_on']
            data['comments'] = []

            comments_url = issue['links']['comments']['href']
            while True:
                comments = requests.get(comments_url).json()
                for comment in comments['values']:
                    data['comments'].append({
                        'id': comment['id'],
                        'user': {
                            'uuid': comment['user']['uuid'],
                            'account_id': comment['user']['account_id'],
                        },
                        'body': comment['content']['raw'],
                        'created_at': comment['created_on'],
                    })

                if 'next' in comments:
                    comments_url = comments['next']
                else:
                    break

            with open(os.path.join(output_dir, 'issues', f"Bitbucket_{repo['Repository'].split('/')[1]}_{issue['id']}.json"), 'w') as f:
                json.dump(data, f)

        if 'next' in issues:
            url = issues['next']
        else:
            break
    
    # download pull requests
    url = f"https://api.bitbucket.org/2.0/repositories/{repo['Repository']}/pullrequests/?state=ALL"
    while True:
        pull_requests = requests.get(url).json()

        for pull_request in pull_requests['values']:
            if os.path.exists(os.path.join(output_dir, 'pull_requests', f"Bitbucket_{repo['Repository'].split('/')[1]}_{pull_request['id']}.json")):
                print(f"Skipping {pull_request['id']}")
                continue

            print(f"Downloading {pull_request['id']}")

            data = {}
            data['repo'] = repo['Repository']
            data['host'] = "Bitbucket"
            data['type'] = "pull_request"
            data['id'] = pull_request['id']
            data['title'] = pull_request['title']
            data['body'] = pull_request['description']
            data['html_url'] = pull_request['links']['html']['href']
            data['created_at'] = pull_request['created_on']
            data['state'] = pull_request['state']
            data['user'] = {
                'uuid': pull_request['author']['uuid'],
                'account_id': pull_request['author']['account_id'],
            } if pull_request['author'] else None
            data['updated_on'] = pull_request['updated_on']
            data['destination'] = {
                'branch': pull_request['destination']['branch']['name'],
                'commit': pull_request['destination']['commit']['hash'],
            }
            data['comments'] = []
            comments_url = pull_request['links']['comments']['href']
            while True:
                comments = requests.get(comments_url).json()
                for comment in comments['values']:
                    data['comments'].append({
                        'id': comment['id'],
                        'user': {
                            'uuid': comment['user']['uuid'],
                            'account_id': comment['user']['account_id'],
                        },
                        'body': comment['content']['raw'],
                        'created_at': comment['created_on'],
                    })

                if 'next' in comments:
                    comments_url = comments['next']
                else:
                    break

            with open(os.path.join(output_dir, 'pull_requests', f"Bitbucket_{repo['Repository'].split('/')[1]}_{pull_request['id']}.json"), 'w') as f:
                json.dump(data, f)

        if 'next' in pull_requests:
            url = pull_requests['next']

        else:
            break