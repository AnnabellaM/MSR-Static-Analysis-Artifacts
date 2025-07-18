import sys
sys.path.append('../../')

from utils.constants import TOOL_NAME_MAPPING
from utils.dataloader import get_issues

issues = get_issues(filter="properties")

# get repo name of every issues, take the second of the split / lowercase and map it to the tool name
new_tool_names = []
for index, issue in issues.iterrows():
    repo_name = issue['repo']
    tool_name = repo_name.split('/')[1].lower()
    if tool_name in TOOL_NAME_MAPPING:
        new_tool_names.append(TOOL_NAME_MAPPING[tool_name])
    else:
        new_tool_names.append(tool_name)

# add the new tool names to the issues dataframe
issues['tool_name'] = new_tool_names
issues.to_csv('../../data/issues_properties.csv', index=False)