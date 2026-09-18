from datetime import datetime

start_date = datetime(2022, 8, 24)
end_date = datetime(2026, 8, 23)

REPO = "zephyrproject-rtos/zephyr"
BASE_URL = f"https://api.github.com/repos/{REPO}"


ISSUES_URL = f"{BASE_URL}/issues"
ISSUES_COMMENTS_URL = f"{ISSUES_URL}/comments"
COMMENT_ID_URL = f"{ISSUES_COMMENTS_URL}/<comment_id>"

# List issue comments?
ISSUES_ID_URL = f"/repos/{owner}/{repo}/issues/{issue_number}/comments"

PULL_REQUESTS_COMMENTS_URL = f"{BASE_URL}/pulls/comments"

# Usually keep in a .env
# import github token from .env
# Header avoids low rate limit, prevents 404s
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
}
# August 24th, 2022 - August 23rd, 2026
QUERY_PARAMS = {
    "sha": "v3.7.0",
    "since": "2022-08-24T00:00:00Z",
    "until": "2026-08-23T23:59:59Z",
}

PARAMS = {
    "since": start_date,
    "sort": "created_at",
    "direction": "asc",
    "per_page": 100,
}

pull_requests_headers = [ "body", ]
