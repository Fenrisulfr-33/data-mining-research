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
- `main.py` — currently empty; entry point once the pipeline exists
- `data/` - The folder where the CSV files will live

## Environment & secrets

- GitHub token: move out of `CONSTANTS.py` into a `.env` file (loaded via
  `python-dotenv` or similar) and add `.env` to `.gitignore`. Never hardcode tokens.
- Rate limits: authenticated requests get 5000/hr. `api.py` opens a `requests.Session`
  that retries transient 5xx errors with backoff, sleeps until reset on primary
  rate-limit exhaustion (403 + `X-RateLimit-Remaining: 0`), and sleeps on
  `Retry-After` for secondary (abuse-detection) limits.
- Dependencies: `pip install -r requirements.txt` (currently just `requests`).
- Python version / virtualenv setup:

## Conventions

- Preferred libraries for HTTP, data handling, GenAI calls?
- PEP8 styling convention.
- Using a Session to mine the data and can return to the same point on interruption.

## GenAI component

- What is GenAI being used for here? (summarizing issues/PRs, classifying comments, generating commit messages, something else?)
- Claude, Sonnet 5

## Status / open TODOs

- [ ] Not yet a git repo — initialize with `git init` when ready
- [ ] `main.py` is empty
- [ ] Rotate the GitHub token currently hardcoded in `CONSTANTS.py`
