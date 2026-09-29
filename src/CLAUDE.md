# mining_git_genAI

<!-- CS480 project: mining Git/GitHub repository data, likely paired with GenAI-based
     analysis. Fill in each section below as the project takes shape — this file is
     what future Claude sessions read first, so keep it current and terse. -->

## Project goal

- Goal: Identify the concrete software engineering activities for which Zephyr contributors explicitly use
GenAI during development.
- Research Question: For which software engineering activities do Zephyr contributors explicitly use GenAI?
- Deliver a research paper.
- Due Oct 18th.

## Target repository & data

- Repo under study: `zephyrproject-rtos/zephyr` (see `CONSTANTS.py`)
- Date range: 2022-08-24 to 2026-08-23
- Which GitHub entities are being mined? (issues, issue comments, PR comments, commits, ...)
- Fetched data will be stored in CSV files.

## Architecture

- `CONSTANTS.py` — API endpoints, headers, query params, date ranges
- `api.py` — thin wrapper around `requests` for hitting the GitHub API
- `main.py` — entry point; `mine_pull_requests()` runs the one-pass mining pipeline
- `data/` - comments/, discussions/, descriptions/, commits/, and pull_requests.csv live here (git-ignored, since it's fetched output not source). The CSV holds a file path in `pr_desc`/`pr_comments`/`pr_discussion`/`pr_commits` rather than the raw text, since PR bodies and commit messages can be long/multi-line and were breaking readability of the CSV.

## Environment & secrets

- GitHub token: loaded from a `.env` file via `python-dotenv` as `GITHUB_TOKEN`
  (`CONSTANTS.py` calls `load_dotenv()` and reads `os.environ["GITHUB_TOKEN"]`).
  `.env` is git-ignored; never hardcode tokens.
- Rate limits: authenticated requests get 5000/hr. `api.py` opens a `requests.Session`
  that retries transient 5xx errors with backoff, sleeps until reset on primary
  rate-limit exhaustion (403 + `X-RateLimit-Remaining: 0`), and sleeps on
  `Retry-After` for secondary (abuse-detection) limits.
- Dependencies: `pip install -r requirements.txt` (`requests`, `python-dotenv`).
- Python version / virtualenv setup:

## Conventions

- Preferred libraries for HTTP, data handling, GenAI calls?
- PEP8 styling convention.
- Using a Session to mine the data and can return to the same point on interruption.
- Single-pass mining: `main.py`'s `mine_pull_requests()` pages through `GET /pulls`
  and, for each PR, fetches comments/discussion/commits and writes the completed
  row to `data/pull_requests.csv` immediately (flushed per row) rather than
  collecting PR numbers first and filling in details in a second pass.

## GenAI component

- What is GenAI being used for here? (summarizing issues/PRs, classifying comments, generating commit messages, something else?)
- Claude, Sonnet 5
- `main.py` has `genai_keywords` / `comment_contains_ai()` as a first-pass keyword
  filter over mined comments; `mine_genai_comments()` and `check_genai_tag()` are
  still stubs.

## Status / open TODOs

- [x] `main.py` now implements the one-pass PR mining pipeline (`mine_pull_requests`)
- [x] GitHub token moved to `.env` (not committed) — each dev needs their own
- [x] Git repo initialized
- [ ] `mine_genai_comments()` / `check_genai_tag()` in `main.py` are still stubs
- [ ] `data/` (comments, discussions, CSV) doesn't exist until the first run
