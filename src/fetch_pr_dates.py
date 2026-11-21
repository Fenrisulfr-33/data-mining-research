"""
Fetch the creation date of every Zephyr PR in the observation period.

The mining CSV does not store when each PR was created, so the observation
period filter in make_final_dataset.py needs this lookup. One pass over
GET /pulls (newest first, 100 per page) is enough - no per-PR requests.

Writes data/pr_created_at.csv with columns pr_number, created_at (UTC, as
returned by GitHub). Stops at the first PR created before PERIOD_START (always the full period).
"""

import csv
import os
from datetime import datetime

from api import fetch_all_pages, get_session
from CONSTANTS import DATA_DIR, PARAMS, PERIOD_START, PULLS_URL

PR_DATES_PATH = os.path.join(DATA_DIR, "pr_created_at.csv")
GITHUB_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    session = get_session()
    rows = []

    for page in fetch_all_pages(session, PULLS_URL, params=PARAMS):
        done = False
        for pr in page:
            created_at = datetime.strptime(pr["created_at"], GITHUB_TIME_FORMAT)
            if created_at < PERIOD_START:
                done = True
                break
            rows.append({"pr_number": pr["number"], "created_at": pr["created_at"]})
        print(f"{len(rows)} PR dates so far (oldest: {rows[-1]['created_at'] if rows else '-'})")
        if done:
            break

    with open(PR_DATES_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["pr_number", "created_at"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"PR creation dates: {len(rows)}")
    print(f"Written to: {PR_DATES_PATH}")


if __name__ == "__main__":
    main()
