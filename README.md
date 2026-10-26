# Artifacts for "Mining Repositories to Understand Common Challenges with Static Analysis Frameworks"

This repository contains the code and data for the paper. We study the GitHub issues and pull requests of six static analysis frameworks (Soot, WALA, OPAL, DOOP, PhASAR, and SVF):

1. We summarize all 7,473 items with an LLM agent.
2. A second LLM agent groups the items into challenge topics.
3. We manually validate 669 sampled items.
4. We analyze 229 validated cases in depth to label their symptoms, causes, fixes, and layers.

## Table of Contents
- [Repository Structure](#repository-structure)
- [Code](#code)
- [Data](#data)
  - [All Items with Summaries and Topics](#all-items-with-summaries-and-topics)
  - [Topic Validation](#topic-validation)
  - [In-depth Manual Analysis](#in-depth-manual-analysis)
  - [Appendix: Full List of Cause Categories](#appendix-full-list-of-cause-categories)

## Repository Structure
```
code/
  agents/prompts.pdf                 prompts of the two LLM agents (summarizer and categorizer)
  agents/validate_summary.py         validation script for the summaries (schema and quoted evidence)
  download_data/download_issues.py   download issues/PRs from GitHub
  download_data/repos.csv            the six studied repositories (input of download_issues.py)
data/
  full_list_7473.csv                 7,473 items with LLM summaries and topics
  validation_669.csv                 669 validated samples with final labels
  manual_analysis_229.csv            229 analyzed cases with final summaries and labels
  full_list_causes.pdf               appendix: full list of cause categories
```

## Code
- [prompts.pdf](./code/agents/prompts.pdf) shows the prompts of our two LLM agents.
  - **Summarizer** (Claude Sonnet 5.5) summarizes each issue or pull request from its title, body and comments. It records the item's type, problem, cause and references to other items, and backs every answer with evidence: a verbatim quote and the field it comes from (`TITLE`, `BODY` or `COMMENT_NN`).
  - **Categorizer** derives challenge topics from the summaries and assigns each item to one to three topics, or to `NOT_A_CHALLENGE`. Each topic has a name, a definition, inclusion and exclusion criteria, and up to three example items. In **SEED** mode (Claude Opus 5.5), it processed 300 seed summaries in 12 batches of 25 and created, broadened, merged or sharpened the topics. In **CLASSIFY** mode (Claude Sonnet 5.5), it assigned each remaining item to the frozen topics and proposed a new topic (`NEW`) if none fit.
- [validate_summary.py](./code/agents/validate_summary.py) is **the validation script** for the summarizer. It checks the schema of a summary and rejects it if any quote is not a substring of the cited field (after whitespace normalization). The agent revises the summary until it passes. 
- [download_issues.py](./code/download_data/download_issues.py) uses PyGithub to download every open and closed issue and pull request of the studied repositories to `data/issues/<tool>_<number>.json`. Each file holds the title, body, state, creation and closing dates, labels, URL and all comments. For a pull request, it also holds every commit with its message and per-file patch, and the PR-level totals of additions, deletions and changed files. It reads the repositories from [repos.csv](./code/download_data/repos.csv). 
Items that are already downloaded are skipped, so the script can be restarted. To run it, install `PyGithub python-dotenv pandas`, put a GitHub token in `code/download_data/.env` (`GITHUB_TOKEN=...`), and run from `code/download_data/`:

## Data

### All Items with Summaries and Topics
[`data/full_list_7473.csv`](./data/full_list_7473.csv) has one row for each of the 7,473 items (2,724 issues and 4,749 pull requests).
Each evidence column has one `FIELD: quote` per line. The quote is copied verbatim from the cited field of the original item.

### Topic Validation
[`data/validation_669.csv`](./data/validation_669.csv) holds the 669 sampled items: 619 from the challenge topics and 50 from the `NOT_A_CHALLENGE` pool. 

### In-depth Manual Analysis
[`data/manual_analysis_229.csv`](./data/manual_analysis_229.csv) holds the 229 cases we analyzed in depth: 150 core, 55 framework usage, and 24 general software engineering.

The codes are:
- **Symptoms:** F1 crash/exception, F2 missing results, F3 wrong or imprecise results, F4 inconsistent/nondeterministic results, F5 performance/timeout, F6 invalid output, F7 build/install failure; N1 unsupported feature/limitation, N2 usage question, N3 maintenance/design request.
- **Causes:** C1–C12 and their subcategories, listed in the [appendix](#appendix-full-list-of-cause-categories).
- **Fix strategies:** X1 local code fix, X2 extend a model or add support, X3 change an interface or contract, X4 redesign, X5 defensive check or assertion, X6 configuration or workaround answer, X7 explanation or documentation, X8 rejected / won't fix, X9 unresolved, X10 infrastructure or process change.
- **Layers:** L1 input and front end, L2 program representation, L3 modeling, L4 core analyses, L5 clients and output, L6 configuration and driver, L7 infrastructure.

### Appendix: Full List of Cause Categories
[`data/full_list_causes.pdf`](./data/full_list_causes.pdf) lists all 12 cause categories and their subcategories. 

