from github import Github, Auth
from dotenv import dotenv_values
import pandas as pd
import json

config = dotenv_values(".env")
auth = Auth.Token(config["GITHUB_TOKEN"])

github = Github(auth=auth)

repos = pd.read_csv("./repos.csv")

for index, row in repos.iterrows():
    # download issues for each repo
    tool = row["tool"]
    repo = row["repo"]

    print(f"Downloading issues for {tool} - {repo}")

    issues = github.get_repo(repo).get_issues(state="all")

    for completed, issue in enumerate(issues, start=1):
        # check if the issue is already downloaded
        try:
            with open(f"./data/issues/{tool}_{issue.number}.json", "r") as f:
                print(f"Skipping {tool} - {issue.number} - {issue.title}")
                continue
        except FileNotFoundError:
            print(f"Downloading {tool} - {issue.number} - {issue.title}")
            # ITEMS WE NEED
            # 1. title
            # 2. body
            # 3. id
            # 4. state
            # 5. created_at
            # 6. closed_at
            # 7. comments
            # 8. html_url
            # 9. labels
            # 10. author
            # 11. repository
            # download the issue data
            issue_type = "pull_request" if issue.pull_request else "issue"
            issue_data = {
                "tool": tool,
                "title": issue.title,
                "body": issue.body,
                "id": issue.id,
                "number": issue.number,
                "state": issue.state,
                "created_at": issue.created_at.isoformat() if issue.created_at else None,
                "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                "comments": [
                    {
                        "id": comment.id,
                        "body": comment.body,
                        "created_at": comment.created_at.isoformat() if comment.created_at else None,
                        "updated_at": comment.updated_at.isoformat() if comment.updated_at else None,
                        "author": comment.user.login if comment.user else None,
                        "html_url": comment.html_url,
                    }
                    for comment in issue.get_comments()
                ],
                "html_url": issue.html_url,
                "labels": [label.name for label in issue.labels],
                "author": issue.user.login if issue.user else None,
                "repository": repo,
                "type": issue_type
            }

            # additional info if a pull request
            if issue_type == "pull_request":
                # PULL REQUEST SPECIFIC INFO
                # 1. merge state
                # 2. commits
                # 3. code_changes
                # 4. files_changed
                pr = issue.as_pull_request()
                issue_data["merge_state"] = pr.mergeable_state
                issue_data["commits"] = []
                for commit in pr.get_commits():
                    # For each commit we also need
                    # 1. list of commit sha
                    # 2. messages
                    # 3. list of changed files
                    # 4. actual code changes (patch file) 
                    files = []
                    for file_ in commit.files:
                        files.append({
                            "filename": file_.filename,
                            "patch": file_.patch,
                            "additions": file_.additions,
                            "deletions": file_.deletions,
                            "previous_filename": file_.previous_filename
                        })

                    issue_data["commits"].append({
                        "sha": commit.sha,
                        "message": commit.commit.message,
                        "author": commit.commit.author.name if commit.commit.author else None,
                        "date": commit.commit.author.date.isoformat() if commit.commit.author else None,
                        "files": files,
                        "html_url": commit.html_url
                    })

                issue_data["total_additions"] = pr.additions
                issue_data["total_deletions"] = pr.deletions
                issue_data["total_files_changed"] = pr.changed_files

            # save the data to a json file
            with open(f"./data/issues/{tool}_{issue.number}.json", "w") as f:
                json.dump(issue_data, f, indent=4)