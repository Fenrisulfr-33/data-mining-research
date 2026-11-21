# Research Question

## Funny Prs found during verification

- "Now your AI is truly hallucinating."
- "AI slop, please stop wasting people's time. https://github.com/microsoft/terminal"
- "ter the final division by 10, everything smaller than 10 rounds down to 0. Wtf, AI, please be more competent."
- Who am I to question our AI overlords?

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

All the code lives in `src/`; run every command from that directory. Outputs go to `src/data/`, which is
git-ignored. The files a re-run can't recreate are committed in `src/data_raw/`.

### Setup

1. `pip install -r requirements.txt`
2. Create a `.env` file (anywhere at or above `src/`, e.g. the repo root) containing
   `GITHUB_TOKEN=<your token>`. Every step needs it, because every script imports `CONSTANTS.py`, which
   reads it - even the steps that make no API calls.

### Reproducing the dataset and every table, in order

Commands are for Git Bash / macOS / Linux. In PowerShell, set the variable first instead:
`$env:TESTING = "false"; python main.py`.

| # | Command | Reads | Writes | Our checkpoint numbers |
|---:|---|---|---|---|
| 1 | `TESTING=false python main.py` | GitHub API | `data/pull_requests.csv` + the `descriptions/`, `comments/`, `discussions/`, `commits/`, `assisted_by_commits/` folders | 55,212 rows retrieved |
| 2 | `python fetch_pr_dates.py` | GitHub API | `data/pr_created_at.csv` | 59,480 PR dates (every PR since 2022-08-24, as of Nov 21st 2026) |
| 3 | `python make_final_dataset.py` | steps 1-2 | `data/final_dataset.csv` | 55,087 after duplicates → 51,716 in the observation period → 4,003 with an AI signal → **2,656** after ignoring bot comments |
| 4 | `python make_validation_sheet.py` | step 3 | `data/manual_validation.csv` (blank `decision`/`reason`) | **773** keyword-only PRs to check |
| 5 | Fill in `decision` (`keep`/`drop`/`unsure`) and `reason` for every row, save as `data/manual_validation_filled.csv` | step 4 | `data/manual_validation_filled.csv` | see [Manual validation](#manual-validation) |
| 6 | `python make_validated_dataset.py` | steps 3, 5 | `data/validated_dataset.csv` | 1,883 strong + 432 kept = **2,315** validated |
| 7 | `python make_results_tables.py` | steps 3, 5, 6 | `data/results_tables.md` (also printed) | every table under [Mining Results](#mining-results) |

**To reproduce our exact numbers, skip the hand work in step 5 and use our decisions:**

```
cp data_raw/manual_validation_filled.csv data/                # our filled sheet (step 5)
cp data_raw/manual_validation_second_review.csv data/         # optional: second-review agreement line
```

Our filled sheet has 868 rows because it was filled in before the end-date cutoff was applied. The 95 rows
outside the observation period are ignored by steps 6 and 7. You can also copy
`data_raw/pr_created_at.csv` into `data/` instead of running step 2. A PR's creation date never changes,
so the result is the same.

Notes:
- Without `TESTING=false`, step 1 mines only the past 4 months, which is a quick test run rather than the
  dataset. `PR_LIMIT=20` stops after 20 PRs, for an even quicker test.
- Step 1 takes many hours, and the API returns what GitHub holds on the day you run it. Comments edited or
  deleted since our run on Oct 3rd 2026 will differ slightly. `data_raw/pull_requests.csv` is our raw CSV,
  but the text and JSON files it points to (in `data/`) are not committed, so steps 3-4 need either a
  fresh step 1 or a copy of our `data/` folder.
- Step 3 always filters to the full observation period (`PERIOD_START` 2022-08-24 to `PERIOD_END`
  2026-08-24, exclusive, in `CONSTANTS.py`), whatever `TESTING` is set to. It re-reads every saved
  comment/discussion file, so it takes a few minutes. It never modifies the raw CSV or the saved files.
- Step 4 refuses to overwrite an existing `data/manual_validation.csv`, so it can't wipe out a sheet
  someone has started filling in. Move or delete the old one first.

# Steps

1. Open a `Session` in the python package `requests` (`src/api.py`), which retries transient failures and
   honors GitHub's rate limits.
2. For testing we mine the past 4 months (`TESTING=true`, the default); `else` mine the full 4-year
   observation period (`TESTING=false`): PRs created from Aug 24th 2022 00:00 UTC up to, but not including,
   Aug 24th 2026 00:00 UTC - i.e. through the end of Aug 23rd 2026. PRs are paged newest-first; PRs newer
   than `end_date` are skipped and mining stops at the first PR created before `start_date`.
   Our full run was done on Oct 3rd 2026, before the end-date check existed, so it also mined 3,371 PRs
   created after Aug 23rd 2026. The cleaning step removes them (see step 11).
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
    - **Observation-period filter** - keeps only PRs created in `[PERIOD_START, PERIOD_END)`, using each PR's
      `created_at` from `data/pr_created_at.csv` (written by `fetch_pr_dates.py`, since the mining CSV doesn't
      store it).
    - **Bot comments ignored** - `ai_keyword_comments` and `ai_keyword_discussion` are recalculated from
      the saved JSON files, skipping entries whose author ends in `[bot]` or is `zephyrbot`. Bot-authored
      PRs themselves are kept.
    - `ai_assisted`, `ai_keyword_desc`, `ai_keyword_commits`, `commit_assisted_by`, and `tags` are carried
      over unchanged from the mining stage.

    It prints the counts for each step (retrieved, after duplicate removal, after the observation-period
    filter, final), which feed the dataset-construction table in the paper. The current full run: 55,212
    retrieved, 125 duplicates removed (55,087), 3,371 created after the end date removed (51,716 in the
    period - every PR GitHub lists for the period), 2,656 with at least one AI signal.
12. Add additional data as necessary and update it HERE.

# Mining Results

Every table in this section, Manual validation and Tags on validated PRs comes from
`python make_results_tables.py` (step 7 above), which writes them to `src/data/results_tables.md`. The
funnel counts in the next line are the checkpoint lines that `make_final_dataset.py` prints.

**55,212** retrieved → **55,087** after removing duplicates → **51,716** in the observation period (Aug 24th 2022 - Aug 23rd 2026) → **2,656** with at least one AI signal

PRs flagged by each signal (one PR can hit several, so the counts add up to more than 2,656):

| Signal | Column | PRs flagged | |
|---|---|---:|---|
| `Assisted-by:` trailer | `commit_assisted_by` | **1,877** | `████████████████████` |
| Keyword in commit | `ai_keyword_commits` | **1,845** | `████████████████████` |
| Keyword in description | `ai_keyword_desc` | **528** | `██████` |
| Keyword in comments | `ai_keyword_comments` | **451** | `█████` |
| Keyword in review | `ai_keyword_discussion` | **396** | `████` |
| `AI-assisted` label | `ai_assisted` | **82** | `█` |

How strong the evidence is:

| Evidence | PRs | Meaning |
|---|---:|---|
| **Strong** | **1,883** | Has the `AI-assisted` label or an `Assisted-by:` trailer - the author disclosed it |
| **Keyword only** | **773** | Only a keyword match - needs a human check (see Manual validation below) |

![What the mining produced](Images/Results%20from%20mining.png)

> The image above was made before the Aug 23rd 2026 cutoff was applied, so its numbers are from the old, longer window. The tables here are current.

## Manual validation

The keyword-only PRs were checked by hand in `src/data/manual_validation_filled.csv` (`decision` = `keep` / `drop` / `unsure`, with a `reason`). The sheet has 868 rows because it was filled in before the end-date cutoff; **773** of them are in the observation period, and only those are used. All numbers below are for those 773. `python make_validated_dataset.py` combines those decisions with the strong PRs and writes `data/validated_dataset.csv`. `unsure` PRs are left out.

**How we decided.** A PR is `keep` when the text shows GenAI was actually used on that PR, by the author or by a reviewer. `drop` means the keyword meant something else (a board name, email domain, `cursor` in code, `LLMNR`, ...) or AI was only discussed, not used. `unsure` means there is a hint but not enough to call it. Two rules we applied across the sheet:

- **Copilot reviews count as GenAI use.** If anyone on the PR refers to a Copilot (or other AI) review that ran on it - addressing it, disagreeing with it, or saying it was wrong - the PR is `keep`. Asking `@copilot` to resolve conflicts or apply changes is also `keep`. Only *requesting* a Copilot review, with no sign it ran, is `unsure`.
- **We trust reviewers who suspect AI use.** When a Zephyr reviewer or maintainer says a PR looks AI-generated, or asks the author to follow the AI disclosure guidelines, the PR is `keep` even without a confirmation from the author. These rows have a reason starting with `Reviewer-suspected AI use:` (**51** PRs). If the author explicitly denied using AI, the PR stays `drop`.

**Second review.** A second, independent pass over the keyword-only PRs, done with an AI assistant (Claude), agreed with the first on **73.4%** of the 773 (Cohen's κ = **0.55**). We then reviewed the disagreements ourselves and settled them using the rules above, which changed 222 of the 773 rows. Both passes are side by side in `src/data/manual_validation_second_review.csv`.

| Decision | PRs | % of keyword-only |
|---|---:|---:|
| `keep` | 432 | 55.9% |
| `drop` | 322 | 41.7% |
| `unsure` | 19 | 2.5% |

**Validated dataset:**

| Evidence | PRs |
|---|---:|
| Strong (label or `Assisted-by:` trailer) | 1,883 |
| Keyword-only, kept after manual review | 432 |
| ...of which kept on reviewer suspicion alone | 51 |
| **Total validated** | **2,315** |

The 19 `unsure` PRs are the margin of error: the true total is somewhere between **2,315** and **2,334**. Without the reviewer-suspicion rule it would be **2,264**.

### How reliable each keyword was

For keyword-only PRs, how often a match turned out to be real GenAI use. A PR can match several keywords. Precision = `keep` / PRs matched.

| Keyword | PRs matched | `keep` | `drop` | `unsure` | Precision |
|---|---:|---:|---:|---:|---:|
| `ai` | 290 | 132 | 152 | 6 | 45.5% |
| `copilot` | 222 | 193 | 19 | 10 | 86.9% |
| `llm` | 119 | 41 | 72 | 6 | 34.5% |
| `claude` | 86 | 84 | 2 | 0 | 97.7% |
| `cursor` | 82 | 18 | 64 | 0 | 22.0% |
| `anthropic` | 36 | 36 | 0 | 0 | 100.0% |
| `assisted-by` | 25 | 21 | 4 | 0 | 84.0% |
| `gemini` | 23 | 12 | 11 | 0 | 52.2% |
| `chatgpt` | 19 | 15 | 3 | 1 | 78.9% |
| `ai tool` | 13 | 10 | 3 | 0 | 76.9% |
| `bard` | 12 | 1 | 11 | 0 | 8.3% |
| `ai generated` | 10 | 9 | 1 | 0 | 90.0% |
| `ai assistant` | 8 | 5 | 3 | 0 | 62.5% |
| `openai` | 7 | 5 | 2 | 0 | 71.4% |
| `used ai` | 7 | 5 | 2 | 0 | 71.4% |
| `using ai` | 7 | 5 | 2 | 0 | 71.4% |
| `gpt-5` | 4 | 4 | 0 | 0 | 100.0% |
| `ai-generated` | 2 | 1 | 1 | 0 | 50.0% |
| `gpt-4` | 1 | 0 | 1 | 0 | 0.0% |
| `written by ai` | 1 | 1 | 0 | 0 | 100.0% |

By where the keyword matched:

| Source | PRs matched | `keep` | `drop` | `unsure` | Precision |
|---|---:|---:|---:|---:|---:|
| Comments | 333 | 215 | 104 | 14 | 64.6% |
| Review | 289 | 190 | 92 | 7 | 65.7% |
| Description | 168 | 63 | 104 | 1 | 37.5% |
| Commit | 146 | 49 | 96 | 1 | 33.6% |

Most common reasons for dropping a PR:

| Reason | PRs |
|---|---:|
| reference to mouse/terminal cursor | 57 |
| keyword is a false positive (name/board/email/code) | 20 |
| s16s.ai | 11 |
| AI-64 | 10 |
| Bot PR | 9 |
| Gemini in email | 9 |
| BeagleY-AI | 8 |
| bard doesn't specific ai use | 8 |
| llm is part of utm_term | 8 |
| llm is part of a LLMNR | 7 |

## Tags on validated PRs

How often each PR label (`tags`) appears across the **2,315** validated PRs - a proxy for what part of Zephyr people were using GenAI on. A PR usually has several tags, so the counts add up to more than 2,315. **83** validated PRs have no tags. **352** distinct tags in total.

<details>
<summary>Show all tags, most to least</summary>

| # | Tag | PRs | % of validated PRs |
|---:|---|---:|---:|
| 1 | Tests | 619 | 26.7% |
| 2 | Boards/SoCs | 290 | 12.5% |
| 3 | Bluetooth | 287 | 12.4% |
| 4 | Networking | 272 | 11.7% |
| 5 | Samples | 253 | 10.9% |
| 6 | Devicetree Binding | 231 | 10.0% |
| 7 | Backport | 197 | 8.5% |
| 8 | Stale | 183 | 7.9% |
| 9 | Sensors | 163 | 7.0% |
| 10 | NXP | 137 | 5.9% |
| 11 | Release | 137 | 5.9% |
| 12 | Bluetooth Host | 135 | 5.8% |
| 13 | Kernel | 118 | 5.1% |
| 14 | Infineon | 111 | 4.8% |
| 15 | XS | 108 | 4.7% |
| 16 | Devicetree | 92 | 4.0% |
| 17 | Build System | 85 | 3.7% |
| 18 | AI-assisted | 82 | 3.5% |
| 19 | STM32 | 79 | 3.4% |
| 20 | Trivial | 77 | 3.3% |
| 21 | Continuous Integration | 73 | 3.2% |
| 22 | Bluetooth Audio | 70 | 3.0% |
| 23 | backport v4.4-branch | 68 | 2.9% |
| 24 | Bluetooth Classic | 63 | 2.7% |
| 25 | I2C | 63 | 2.7% |
| 26 | Wi-Fi | 61 | 2.6% |
| 27 | manifest | 56 | 2.4% |
| 28 | ADI | 55 | 2.4% |
| 29 | backport v4.3-branch | 53 | 2.3% |
| 30 | Sockets | 53 | 2.3% |
| 31 | Documentation | 52 | 2.2% |
| 32 | Ethernet | 51 | 2.2% |
| 33 | nRF | 47 | 2.0% |
| 34 | Clock Control | 46 | 2.0% |
| 35 | SPI | 43 | 1.9% |
| 36 | UART | 43 | 1.9% |
| 37 | backport v3.7-branch | 41 | 1.8% |
| 38 | ESP32 | 41 | 1.8% |
| 39 | MAINTAINER File | 41 | 1.8% |
| 40 | Architectures | 40 | 1.7% |
| 41 | ARM | 39 | 1.7% |
| 42 | Base OS | 38 | 1.6% |
| 43 | nRF BSIM | 38 | 1.6% |
| 44 | NXP MCU | 38 | 1.6% |
| 45 | USB | 38 | 1.6% |
| 46 | RISCV | 36 | 1.6% |
| 47 | ADC | 34 | 1.5% |
| 48 | Bluetooth Controller | 34 | 1.5% |
| 49 | Documentation Infrastructure | 34 | 1.5% |
| 50 | Linters | 34 | 1.5% |
| 51 | Hotfix | 32 | 1.4% |
| 52 | Display | 31 | 1.3% |
| 53 | Flash | 31 | 1.3% |
| 54 | Input | 31 | 1.3% |
| 55 | DMA | 30 | 1.3% |
| 56 | GPIO | 30 | 1.3% |
| 57 | Twister | 30 | 1.3% |
| 58 | Modem Drivers | 29 | 1.3% |
| 59 | Userspace | 29 | 1.3% |
| 60 | West | 28 | 1.2% |
| 61 | Audio | 27 | 1.2% |
| 62 | Bluetooth Mesh | 26 | 1.1% |
| 63 | I3C | 25 | 1.1% |
| 64 | Logging | 25 | 1.1% |
| 65 | I2S | 24 | 1.0% |
| 66 | MFD | 23 | 1.0% |
| 67 | Timer | 23 | 1.0% |
| 68 | Bluetooth HCI | 22 | 1.0% |
| 69 | Pinctrl | 22 | 1.0% |
| 70 | Silabs | 22 | 1.0% |
| 71 | Microchip SAM | 21 | 0.9% |
| 72 | Testsuite | 21 | 0.9% |
| 73 | Counter | 20 | 0.9% |
| 74 | ARM64 | 19 | 0.8% |
| 75 | bug | 19 | 0.8% |
| 76 | Disk Access | 19 | 0.8% |
| 77 | Interrupt Controller | 19 | 0.8% |
| 78 | Toolchains | 19 | 0.8% |
| 79 | Device Model | 16 | 0.7% |
| 80 | OpenThread | 16 | 0.7% |
| 81 | Release Notes | 16 | 0.7% |
| 82 | Architecture Review | 15 | 0.6% |
| 83 | Bluetooth Qualification | 15 | 0.6% |
| 84 | Debugging | 15 | 0.6% |
| 85 | LWM2M | 15 | 0.6% |
| 86 | native port | 15 | 0.6% |
| 87 | POSIX | 15 | 0.6% |
| 88 | Power Management | 15 | 0.6% |
| 89 | VIRTIO | 15 | 0.6% |
| 90 | Xtensa | 15 | 0.6% |
| 91 | CAN | 14 | 0.6% |
| 92 | IEEE 802.15.4 | 14 | 0.6% |
| 93 | ITE | 14 | 0.6% |
| 94 | llext | 14 | 0.6% |
| 95 | Microchip MEC | 14 | 0.6% |
| 96 | PTP | 14 | 0.6% |
| 97 | Shell | 14 | 0.6% |
| 98 | Tracing | 14 | 0.6% |
| 99 | DNM | 13 | 0.6% |
| 100 | mcumgr | 13 | 0.6% |
| 101 | Microchip PIC32 | 13 | 0.6% |
| 102 | Modem | 13 | 0.6% |
| 103 | X86 | 13 | 0.6% |
| 104 | Crypto / RNG | 12 | 0.5% |
| 105 | File System | 12 | 0.5% |
| 106 | HTTP | 12 | 0.5% |
| 107 | PWM | 12 | 0.5% |
| 108 | Renesas RA | 12 | 0.5% |
| 109 | Seeed Studio | 12 | 0.5% |
| 110 | TF-M | 12 | 0.5% |
| 111 | Watchdog | 12 | 0.5% |
| 112 | DNM (manifest) | 11 | 0.5% |
| 113 | Inclusive Language | 11 | 0.5% |
| 114 | LED | 11 | 0.5% |
| 115 | Mbed TLS | 11 | 0.5% |
| 116 | Raspberry Pi Pico | 11 | 0.5% |
| 117 | RTC | 11 | 0.5% |
| 118 | Storage | 11 | 0.5% |
| 119 | Benchmarks | 10 | 0.4% |
| 120 | Kconfig | 10 | 0.4% |
| 121 | manifest-hal_nxp | 10 | 0.4% |
| 122 | Realtek Bee | 10 | 0.4% |
| 123 | RTIO | 10 | 0.4% |
| 124 | Shields | 10 | 0.4% |
| 125 | SPDX Tooling | 10 | 0.4% |
| 126 | Fuel Gauge | 9 | 0.4% |
| 127 | IPC | 9 | 0.4% |
| 128 | LoRa | 9 | 0.4% |
| 129 | NXP MPU | 9 | 0.4% |
| 130 | Regulators | 9 | 0.4% |
| 131 | Renesas RZ | 9 | 0.4% |
| 132 | RFC | 9 | 0.4% |
| 133 | UpdateHub | 9 | 0.4% |
| 134 | WinChipHead | 9 | 0.4% |
| 135 | Bouffalo Lab | 8 | 0.3% |
| 136 | C Library | 8 | 0.3% |
| 137 | Linker Scripts | 8 | 0.3% |
| 138 | manifest-hal_infineon | 8 | 0.3% |
| 139 | Nuvoton NPCX | 8 | 0.3% |
| 140 | OCPP | 8 | 0.3% |
| 141 | Stepper | 8 | 0.3% |
| 142 | Cache | 7 | 0.3% |
| 143 | Comparator | 7 | 0.3% |
| 144 | manifest-hostap | 7 | 0.3% |
| 145 | manifest-trusted-firmware-m | 7 | 0.3% |
| 146 | Nuvoton Numicro Numaker | 7 | 0.3% |
| 147 | Override Required | 7 | 0.3% |
| 148 | PMCI | 7 | 0.3% |
| 149 | Realtek | 7 | 0.3% |
| 150 | Realtek Ameba | 7 | 0.3% |
| 151 | Utilities | 7 | 0.3% |
| 152 | Video | 7 | 0.3% |
| 153 | Ambiq | 6 | 0.3% |
| 154 | Aux display | 6 | 0.3% |
| 155 | CRC | 6 | 0.3% |
| 156 | Drivers | 6 | 0.3% |
| 157 | Intel ADSP | 6 | 0.3% |
| 158 | manifest-hal_espressif | 6 | 0.3% |
| 159 | manifest-hal_nordic | 6 | 0.3% |
| 160 | manifest-hal_realtek | 6 | 0.3% |
| 161 | manifest-mcuboot | 6 | 0.3% |
| 162 | manifest-nrf_wifi | 6 | 0.3% |
| 163 | mbox | 6 | 0.3% |
| 164 | NXP Drivers | 6 | 0.3% |
| 165 | Reset | 6 | 0.3% |
| 166 | TI SimpleLink | 6 | 0.3% |
| 167 | Andes Technology | 5 | 0.2% |
| 168 | ARC | 5 | 0.2% |
| 169 | Binary Blobs Added | 5 | 0.2% |
| 170 | Display Controller | 5 | 0.2% |
| 171 | HW Test | 5 | 0.2% |
| 172 | In progress | 5 | 0.2% |
| 173 | IPM | 5 | 0.2% |
| 174 | manifest-hal_bouffalolab | 5 | 0.2% |
| 175 | manifest-hal_silabs | 5 | 0.2% |
| 176 | manifest-hal_stm32 | 5 | 0.2% |
| 177 | MCUBoot | 5 | 0.2% |
| 178 | Microchip | 5 | 0.2% |
| 179 | Multimedia Pipeline | 5 | 0.2% |
| 180 | Networking Buffers | 5 | 0.2% |
| 181 | OpenRISC | 5 | 0.2% |
| 182 | PCI | 5 | 0.2% |
| 183 | PM CPU ops | 5 | 0.2% |
| 184 | Renesas RX | 5 | 0.2% |
| 185 | Security | 5 | 0.2% |
| 186 | Xen Platform | 5 | 0.2% |
| 187 | Authentication | 4 | 0.2% |
| 188 | Bluetooth ISO | 4 | 0.2% |
| 189 | Charger | 4 | 0.2% |
| 190 | Coding Guidelines | 4 | 0.2% |
| 191 | dap | 4 | 0.2% |
| 192 | False Positive | 4 | 0.2% |
| 193 | FIDO2 | 4 | 0.2% |
| 194 | GD32 | 4 | 0.2% |
| 195 | Haptics | 4 | 0.2% |
| 196 | hawkBit | 4 | 0.2% |
| 197 | HW Emulation | 4 | 0.2% |
| 198 | HWINFO | 4 | 0.2% |
| 199 | Key-Value Storage Systems | 4 | 0.2% |
| 200 | M5Stack | 4 | 0.2% |
| 201 | manifest-hal_renesas | 4 | 0.2% |
| 202 | manifest-net-tools | 4 | 0.2% |
| 203 | MEMC | 4 | 0.2% |
| 204 | MSPI | 4 | 0.2% |
| 205 | Renesas | 4 | 0.2% |
| 206 | Safety | 4 | 0.2% |
| 207 | SF32LB | 4 | 0.2% |
| 208 | Antmicro | 3 | 0.1% |
| 209 | Battery Backed RAM (bbram) | 3 | 0.1% |
| 210 | Binary Blobs Modified | 3 | 0.1% |
| 211 | Boards | 3 | 0.1% |
| 212 | Clocks | 3 | 0.1% |
| 213 | CMSIS-Core | 3 | 0.1% |
| 214 | Console | 3 | 0.1% |
| 215 | DAC | 3 | 0.1% |
| 216 | DAI | 3 | 0.1% |
| 217 | eSPI | 3 | 0.1% |
| 218 | Formatting Output | 3 | 0.1% |
| 219 | Intel | 3 | 0.1% |
| 220 | JSON | 3 | 0.1% |
| 221 | low | 3 | 0.1% |
| 222 | LVGL | 3 | 0.1% |
| 223 | manifest-hal_adi | 3 | 0.1% |
| 224 | manifest-hal_microchip | 3 | 0.1% |
| 225 | manifest-mbedtls | 3 | 0.1% |
| 226 | manifest-nrf_hw_models | 3 | 0.1% |
| 227 | Nuvoton NPCM | 3 | 0.1% |
| 228 | NVMEM | 3 | 0.1% |
| 229 | NXP S32 | 3 | 0.1% |
| 230 | Octavo Systems | 3 | 0.1% |
| 231 | Opamp | 3 | 0.1% |
| 232 | Process | 3 | 0.1% |
| 233 | Realtek EC | 3 | 0.1% |
| 234 | Renesas SmartBond | 3 | 0.1% |
| 235 | sensry | 3 | 0.1% |
| 236 | Settings | 3 | 0.1% |
| 237 | Sysbuild | 3 | 0.1% |
| 238 | TI | 3 | 0.1% |
| 239 | W1 | 3 | 0.1% |
| 240 | Arduino | 2 | <0.1% |
| 241 | Board/SoC configuration | 2 | <0.1% |
| 242 | Broadcom | 2 | <0.1% |
| 243 | camera | 2 | <0.1% |
| 244 | Clock Monitor | 2 | <0.1% |
| 245 | CMSIS-DSP | 2 | <0.1% |
| 246 | Coredump | 2 | <0.1% |
| 247 | CPU Frequency Scaling | 2 | <0.1% |
| 248 | DSA | 2 | <0.1% |
| 249 | DSP | 2 | <0.1% |
| 250 | ec_host_cmd | 2 | <0.1% |
| 251 | Enhancement | 2 | <0.1% |
| 252 | Firmware | 2 | <0.1% |
| 253 | GNSS | 2 | <0.1% |
| 254 | Hardware Spinlock | 2 | <0.1% |
| 255 | hash utils | 2 | <0.1% |
| 256 | manifest-babblesim_base | 2 | <0.1% |
| 257 | manifest-bsim | 2 | <0.1% |
| 258 | manifest-hal_ambiq | 2 | <0.1% |
| 259 | manifest-hal_ti | 2 | <0.1% |
| 260 | manifest-hal_wch | 2 | <0.1% |
| 261 | manifest-picolibc | 2 | <0.1% |
| 262 | manifest-reqmgmt | 2 | <0.1% |
| 263 | manifest-tf-psa-crypto | 2 | <0.1% |
| 264 | manifest-trusted-firmware-a | 2 | <0.1% |
| 265 | manifest-zephyr-lang-rust | 2 | <0.1% |
| 266 | Memory Management | 2 | <0.1% |
| 267 | Microchip RISC-V | 2 | <0.1% |
| 268 | modbus | 2 | <0.1% |
| 269 | Neural Networks | 2 | <0.1% |
| 270 | nRF IronSide SE | 2 | <0.1% |
| 271 | Release Notes Required | 2 | <0.1% |
| 272 | Renesas R-Car | 2 | <0.1% |
| 273 | Secure Storage | 2 | <0.1% |
| 274 | Sensor Subsystem | 2 | <0.1% |
| 275 | State Machine Framework | 2 | <0.1% |
| 276 | Synopsys | 2 | <0.1% |
| 277 | Task Watchdog | 2 | <0.1% |
| 278 | USB-C | 2 | <0.1% |
| 279 | wuc | 2 | <0.1% |
| 280 | Zbus | 2 | <0.1% |
| 281 | ACPI | 1 | <0.1% |
| 282 | Aesc Silicon | 1 | <0.1% |
| 283 | Alif Semiconductor | 1 | <0.1% |
| 284 | Ameba | 1 | <0.1% |
| 285 | ARM SiP SVC | 1 | <0.1% |
| 286 | Biometrics | 1 | <0.1% |
| 287 | Bluetooth Review | 1 | <0.1% |
| 288 | Bootloader | 1 | <0.1% |
| 289 | Breaking API Change | 1 | <0.1% |
| 290 | CMSIS API Layer | 1 | <0.1% |
| 291 | CMSIS-NN | 1 | <0.1% |
| 292 | DALI | 1 | <0.1% |
| 293 | Demand Paging | 1 | <0.1% |
| 294 | Devicetree Tooling | 1 | <0.1% |
| 295 | DFU | 1 | <0.1% |
| 296 | Emulation | 1 | <0.1% |
| 297 | Experimental | 1 | <0.1% |
| 298 | Instrumentation | 1 | <0.1% |
| 299 | Intel ISH | 1 | <0.1% |
| 300 | LiteX | 1 | <0.1% |
| 301 | manifest-babblesim_ext_2G4_phy_v1 | 1 | <0.1% |
| 302 | manifest-chre | 1 | <0.1% |
| 303 | manifest-cmsis_6 | 1 | <0.1% |
| 304 | manifest-dhara | 1 | <0.1% |
| 305 | manifest-hal_afbr | 1 | <0.1% |
| 306 | manifest-hal_altera | 1 | <0.1% |
| 307 | manifest-hal_atmel | 1 | <0.1% |
| 308 | manifest-hal_intel | 1 | <0.1% |
| 309 | manifest-hal_nuvoton | 1 | <0.1% |
| 310 | manifest-hal_rpi_pico | 1 | <0.1% |
| 311 | manifest-hal_st | 1 | <0.1% |
| 312 | manifest-hal_tdk | 1 | <0.1% |
| 313 | manifest-hal_wurthelektronik | 1 | <0.1% |
| 314 | manifest-hal_xtensa | 1 | <0.1% |
| 315 | manifest-libmctp | 1 | <0.1% |
| 316 | manifest-littlefs | 1 | <0.1% |
| 317 | manifest-lvgl | 1 | <0.1% |
| 318 | manifest-lz4 | 1 | <0.1% |
| 319 | manifest-mldsa-native | 1 | <0.1% |
| 320 | manifest-openthread | 1 | <0.1% |
| 321 | manifest-percepio | 1 | <0.1% |
| 322 | manifest-tflite-micro | 1 | <0.1% |
| 323 | manifest-uoscore-uedhoc | 1 | <0.1% |
| 324 | manifest-zephyr-xenlib | 1 | <0.1% |
| 325 | MCP | 1 | <0.1% |
| 326 | MCTP | 1 | <0.1% |
| 327 | Microchip SAM MCU | 1 | <0.1% |
| 328 | MIPI-DSI | 1 | <0.1% |
| 329 | MUX | 1 | <0.1% |
| 330 | net-review | 1 | <0.1% |
| 331 | NUCODE | 1 | <0.1% |
| 332 | Open AMP | 1 | <0.1% |
| 333 | OpenTitan | 1 | <0.1% |
| 334 | OSDP | 1 | <0.1% |
| 335 | OTP | 1 | <0.1% |
| 336 | picolibc | 1 | <0.1% |
| 337 | Portability | 1 | <0.1% |
| 338 | PS2 | 1 | <0.1% |
| 339 | Renode | 1 | <0.1% |
| 340 | Segger RTT | 1 | <0.1% |
| 341 | Silabs SiM3U | 1 | <0.1% |
| 342 | SMBus | 1 | <0.1% |
| 343 | Stats | 1 | <0.1% |
| 344 | Symtab | 1 | <0.1% |
| 345 | TF-A | 1 | <0.1% |
| 346 | TI AM13 | 1 | <0.1% |
| 347 | TI MSPM | 1 | <0.1% |
| 348 | treewide 🧹 | 1 | <0.1% |
| 349 | UUID | 1 | <0.1% |
| 350 | Waiting for response | 1 | <0.1% |
| 351 | Windows Support | 1 | <0.1% |
| 352 | Xilinx | 1 | <0.1% |

</details>

