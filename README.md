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

This repo is meant to provide the framework for mining the GitHub API for research analysis.

Can also extend to already existing data sets that just require analysis.

# Steps

1. Open a `Session` in the python package `requests`
2. For testing we mine the past 4 months, `else` mine the past 4 years from Aug 24th 2022 - August 24th 2026
3. We page through `GET /pulls` in a single pass: for each `pr` returned, immediately fetch its comments/discussion/commits and write one completed row to the `.csv`, rather than collecting all `pr_numbers` first and doing a second pass. This way progress is saved as we go and the run can pick back up without redoing work if it's interrupted.
4. For each `pr_number` we extract additional data from `GET /pulls/{pr_number}/comments`, `GET /issues/{pr_number}/comments`, `GET /pulls/{pr_number}/reviews`, and `GET /pulls/{pr_number}/commits`.
5. The data collected will be, `pr_creator`, `ai_assisted`, `pr_desc`, `pr_comments`, `pr_discussion`, `pr_commits`. `ai_assisted` is a boolean: `true` if the PR has the `AI-assisted` label, `false` otherwise.
6. `pr_discussion`, and/or `pr_comments` should be saved in their respective folder either, `discussions` and `comments`. Each file will be a `.json` of the respective discussion/comment in order they happen with the persons `id`, `name`, `created_at`, and either `comment`/`message`. The `FILE_NAME` should be the `{pr_number}.json` so it can be saved in the `.csv` column as a link to that `discussion`/`comment`. `pr_desc` and `pr_commits` are large free-text blobs too, so they're saved the same way, one per PR, as `descriptions/{pr_number}.txt` and `commits/{pr_number}.txt`, with the `.csv` column holding the file path rather than the raw text.
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

7. `pr_commits` is pulled from the endpoint `GET /pulls/{pr_number}/commits` so we can get the initial commit message. This is because the initial commit message contains information if they used `AI` or an `AI tool`. Note that PR-level conversation comments (`pr_comments`) come from `GET /issues/{pr_number}/comments`, since GitHub treats every PR as an issue, while inline code review comments (`pr_discussion`) come from `GET /pulls/{pr_number}/comments`.
8. Add addition data as necessary and update it HERE.