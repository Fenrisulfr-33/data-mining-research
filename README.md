# Research Question

## Question:
What Is GenAI Being Used For in Zephyr?

## Goal:
Identify the concrete software engineering activities for which Zephyr contributors explicitly use GenAI during development.

## Data:
You will mine the last 4 years of public Zephyr GitHub pull requests, review comments, issues, and discussions.

For each case, examine the surrounding conversation to understand what the contributor was trying to accomplish with GenAI. Possible activities may involve coding, debugging, testing, documentation, or review, but the final categories should come from the data rather than being fixed in advance. A conversation may include more than one use case.

You will need to explain your strategies to:
● Select which GitHub data to analyze and detect candidate GenAI signals
● Validate candidates and remove false positives
● Determine what contributors were using GenAI to accomplish
● Qualitatively derive a taxonomy of GenAI use cases and develop a codebook
● Scale the analysis when appropriate, with human validation of automated classification

## Expected analysis:
Develop a taxonomy of GenAI use cases in Zephyr and report how frequently each use case appears among the validated artifacts. Include representative examples for the identified categories.

Prepare a dataset of validated GenAI-related artifacts and a qualitative codebook containing the use-case categories and representative quotes. GenAI may be used to assist the analysis, but the final classifications must be human-validated.


# Data Mining Research

This repo mines the GitHub API for research analysis — specifically Zephyr pull requests, looking for
signals that GenAI was used and what it was used for.

Can also extend to already existing data sets that just require analysis.

## Running it

All the code lives in `src/`. From that directory:

```
python main.py                # 1. mine the raw data -> data/pull_requests.csv
python make_final_dataset.py  # 2. clean it          -> data/final_dataset.csv
```

Requires a `.env` file (anywhere at or above `src/`, e.g. the repo root) with `GITHUB_TOKEN=<your token>`,
and `pip install -r requirements.txt`. The cleaning step makes no API calls, but it still needs the `.env`
because it imports the keyword matcher from `main.py`, which loads `CONSTANTS.py`.

Cleaning re-reads every saved comment/discussion file, so on the full dataset it takes a few minutes.
It never modifies the raw CSV or the saved files - it only writes `data/final_dataset.csv` (overwritten
on each run).

Optional environment variables:
- `TESTING` - `true` (the default) mines just the past 4 months; `false` mines the full 4-year range
  starting `2022-08-24`. Set in `src/CONSTANTS.py`.
- `PR_LIMIT` - stop after this many PRs, e.g. `PR_LIMIT=20 python main.py`, for a quick test run.

# Steps

1. Open a `Session` in the python package `requests` (`src/api.py`), which retries transient failures and
   honors GitHub's rate limits.
2. For testing we mine the past 4 months (`TESTING=true`, the default); `else` mine the past 4 years
   starting Aug 24th 2022 (`TESTING=false`). PRs are paged newest-first and mining stops at the first PR
   created before `start_date`. Note: `end_date` (Aug 23rd 2026) is defined in `CONSTANTS.py` but not
   currently applied, so PRs created after it are also mined.
3. We page through `GET /pulls` in a single pass: for each `pr` returned, immediately fetch its
   comments/discussion/commits and write one completed row to the `.csv`, rather than collecting all
   `pr_numbers` first and doing a second pass. This way progress is saved as we go and the run can pick
   back up without redoing work if it's interrupted.
4. For each `pr_number` we extract additional data from `GET /pulls/{pr_number}/comments`,
   `GET /issues/{pr_number}/comments`, `GET /pulls/{pr_number}/reviews`, and
   `GET /pulls/{pr_number}/commits`.
5. The data collected, one row per PR in `data/pull_requests.csv`:

   | Column | Meaning |
   |---|---|
   | `pr_number` | PR/issue number |
   | `pr_creator` | GitHub username of the PR author |
   | `ai_assisted` | boolean - `true` if the PR has the `AI-assisted` label |
   | `tags` | the PR's labels (`;`-joined, category prefix like `area:`/`platform:` stripped off), but only filled in when some AI signal was found for that PR (`ai_assisted`, any `ai_keyword_*` column, or `commit_assisted_by`) - otherwise blank, since the point is to see what people were working on specifically when AI use was detected |
   | `pr_desc` | path to the PR body, saved as text |
   | `ai_keyword_desc` | boolean - the PR body matched a GenAI keyword |
   | `pr_comments` | path to the PR's conversation comments, saved as JSON |
   | `ai_keyword_comments` | boolean - any conversation comment matched a GenAI keyword |
   | `pr_discussion` | path to the PR's inline review comments + review summaries, saved as JSON |
   | `ai_keyword_discussion` | boolean - any discussion item matched a GenAI keyword |
   | `pr_commits` | path to the PR's first commit message, saved as text |
   | `ai_keyword_commits` | boolean - the first commit message matched a GenAI keyword |
   | `commit_assisted_by` | boolean - any commit on the PR carries an `Assisted-by:` trailer |
   | `commit_assisted_by_file` | path to the flagged commit(s)' SHA + full message, saved as text |

6. `pr_comments` and `pr_discussion` are each saved as one `.json` file per PR, in `comments/` and
   `discussions/` respectively, in the order they happened, with each entry's `id`, `name`, `created_at`,
   and either `comment`/`message`. The `FILE_NAME` is `{pr_number}.json`, and the `.csv` column holds that
   path (relative to `data/`, e.g. `comments/120576.json`) as a link to the file.
```json
// Comment
[
	{
		"id": 1234,
		"name": "John",
		"created_at": "date_time",
		"comment": "body..."
	},
	{
		"id": 1235,
		"name": "Susan",
		"created_at": "date_time",
		"comment": "body..."

	}
]

```
```json
// Discussion
[
	{
		"id": 1234,
		"name": "John",
		"created_at": "date_time",
		"message": "body..."
	},
	{
		"id": 1235,
		"name": "Susan",
		"created_at": "date_time",
		"message": "body..."

	}
]
```

7. `pr_desc`, `pr_commits`, and `commit_assisted_by_file` are large free-text blobs too, so they're saved
   the same way - one `.txt` per PR - in `descriptions/`, `commits/`, and `assisted_by_commits/`
   respectively, with the `.csv` column holding the file path rather than the raw text.
8. Note that PR-level conversation comments (`pr_comments`) come from `GET /issues/{pr_number}/comments`,
   since GitHub treats every PR as an issue, while inline code review comments (part of `pr_discussion`)
   come from `GET /pulls/{pr_number}/comments`.
9. `ai_keyword_*` columns are a cheap first-pass heuristic: a simple keyword/phrase match (see
   `genai_keywords` in `main.py`) over the relevant text. Not a substitute for human validation - just a
   way to flag candidates.
10. `commit_assisted_by` is the stronger, more precise signal: Zephyr's own contribution guidelines ask
    contributors to add an `Assisted-by: [Agent Name]:[Model Version]` trailer to any commit that used AI
    assistance, the same way `Signed-off-by:` works. We scan **every** commit on the PR for this trailer,
    not just the first, since the guidelines don't say it has to be on the first commit.
11. Cleaning (`make_final_dataset.py`) turns `data/pull_requests.csv` into `data/final_dataset.csv`, the
    analysis dataset. One row per PR, same columns as above:
    - **Duplicate PRs removed** - keeps the first row for each `pr_number` (duplicates can appear when a
      run is resumed after an interruption).
    - **Bot comments ignored** - `ai_keyword_comments` and `ai_keyword_discussion` are recalculated from
      the saved JSON files, skipping entries whose author ends in `[bot]` or is `zephyrbot`. Bot-authored
      PRs themselves are kept.
    - `ai_assisted`, `ai_keyword_desc`, `ai_keyword_commits`, `commit_assisted_by`, and `tags` are carried
      over unchanged from the mining stage.

    It prints the counts for each step (retrieved, after duplicate removal, final), which feed the
    dataset-construction table in the paper. The current full run: 55,212 retrieved, 125 duplicates
    removed, 55,087 final.
12. Add additional data as necessary and update it HERE.
