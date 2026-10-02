import calendar
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


def _months_ago(dt, months):
    total = dt.year * 12 + (dt.month - 1) - months
    year, month = divmod(total, 12)
    month += 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


# TESTING=false mines the full 4-year range; anything else (including unset)
# mines just the past 4 months, for a quick end-to-end run.
TESTING = os.environ.get("TESTING", "true").lower() != "false"

start_date = _months_ago(datetime.now(), 4) if TESTING else datetime(2022, 8, 24)
end_date = datetime(2026, 8, 23)

REPO = "zephyrproject-rtos/zephyr"
BASE_URL = f"https://api.github.com/repos/{REPO}"

PULLS_URL = f"{BASE_URL}/pulls"

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

# Header avoids low rate limit, prevents 404s
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
}

# PRs newest-first so we can stop paging once we pass start_date.
PARAMS = {
    "state": "all",
    "sort": "created",
    "direction": "desc",
    "per_page": 100,
}

# Anchored to this file's directory (src/), so data/ lands in the same place
# no matter what directory main.py is invoked from.
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SRC_DIR, "data")
COMMENTS_DIR = os.path.join(DATA_DIR, "comments")
DISCUSSIONS_DIR = os.path.join(DATA_DIR, "discussions")
DESCRIPTIONS_DIR = os.path.join(DATA_DIR, "descriptions")
COMMITS_DIR = os.path.join(DATA_DIR, "commits")
CSV_PATH = os.path.join(DATA_DIR, "pull_requests.csv")

AI_ASSISTED_LABEL = "AI-assisted"

CSV_FIELDS = [
    "pr_number",
    "pr_creator",
    "ai_assisted",
    "pr_desc",
    "ai_keyword_desc",
    "pr_comments",
    "ai_keyword_comments",
    "pr_discussion",
    "ai_keyword_discussion",
    "pr_commits",
    "ai_keyword_commits",
]


def pr_comments_url(pr_number):
    """Conversation comments (PRs are issues in GitHub's API)."""
    return f"{BASE_URL}/issues/{pr_number}/comments"


def pr_review_comments_url(pr_number):
    """Inline code review comments."""
    return f"{BASE_URL}/pulls/{pr_number}/comments"


def pr_reviews_url(pr_number):
    """Review verdicts, each with an optional summary comment."""
    return f"{BASE_URL}/pulls/{pr_number}/reviews"


def pr_commits_url(pr_number):
    return f"{BASE_URL}/pulls/{pr_number}/commits"
