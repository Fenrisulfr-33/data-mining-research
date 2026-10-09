"""
Clean the mined Zephyr PR data and create the final analysis-ready dataset.

The unit of analysis is one pull request.

Raw mined files are not modified. Duplicate PR rows are removed and
bot-authored comments/discussion items are ignored when recalculating
the corresponding GenAI keyword indicators.

The first commit message is used for ai_keyword_commits.

commit_assisted_by is preserved from the mining stage because it checks
all commits for Zephyr's Assisted-by: trailer.
"""

import csv
import json
import os

from CONSTANTS import CSV_FIELDS, CSV_PATH, DATA_DIR
from main import comment_contains_ai


FINAL_CSV_PATH = os.path.join(DATA_DIR, "final_dataset.csv")


def load_json(relative_path):
    """Load a JSON file using the relative path stored in the raw CSV."""
    if not relative_path:
        return []

    path = os.path.join(DATA_DIR, relative_path)

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def is_bot(name):
    """Return True when a GitHub login is a bot."""
    if not name:
        return False

    return name.lower().endswith("[bot]") or name.lower() == "zephyrbot"


def item_contains_ai(item):
    """Check the text stored in a normalized comment/discussion item."""
    text = item.get("comment", "")

    if not text:
        text = item.get("message", "")

    return comment_contains_ai(text)


def check_comments(row):
    """Recalculate the comment GenAI indicator while ignoring bots."""
    comments = load_json(row["pr_comments"])

    for comment in comments:
        if is_bot(comment.get("name")):
            continue

        if item_contains_ai(comment):
            return True

    return False


def check_discussion(row):
    """Recalculate the discussion GenAI indicator while ignoring bots."""
    discussion = load_json(row["pr_discussion"])

    for item in discussion:
        if is_bot(item.get("name")):
            continue

        if item_contains_ai(item):
            return True

    return False


def read_raw_data():
    """Read all rows from the raw mined CSV."""
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def remove_duplicate_prs(rows):
    """Keep one row for each PR number."""
    seen = set()
    unique_rows = []

    for row in rows:
        pr_number = row["pr_number"]

        if pr_number in seen:
            continue

        seen.add(pr_number)
        unique_rows.append(row)

    duplicates_removed = len(rows) - len(unique_rows)

    return unique_rows, duplicates_removed


def build_final_rows(rows):
    """Construct the final analysis-ready dataset."""
    final_rows = []
    positive_before_bot_check = 0

    for row in rows:
        # Count PRs with positive indicators before recalculating
        # the comment and discussion indicators.
        if (
            str(row["ai_assisted"]).lower() == "true"
            or str(row["ai_keyword_desc"]).lower() == "true"
            or str(row["ai_keyword_comments"]).lower() == "true"
            or str(row["ai_keyword_discussion"]).lower() == "true"
            or str(row["ai_keyword_commits"]).lower() == "true"
            or str(row["commit_assisted_by"]).lower() == "true"
        ):
            positive_before_bot_check += 1

        # Recalculate comment and discussion indicators,
        # ignoring bot-authored items.
        ai_keyword_comments = check_comments(row)
        ai_keyword_discussion = check_discussion(row)

        final_row = {
            "pr_number": row["pr_number"],
            "pr_creator": row["pr_creator"],
            "ai_assisted": row["ai_assisted"],
            "tags": row["tags"],
            "pr_desc": row["pr_desc"],
            "ai_keyword_desc": row["ai_keyword_desc"],
            "pr_comments": row["pr_comments"],
            "ai_keyword_comments": ai_keyword_comments,
            "pr_discussion": row["pr_discussion"],
            "ai_keyword_discussion": ai_keyword_discussion,
            "pr_commits": row["pr_commits"],
            "ai_keyword_commits": row["ai_keyword_commits"],
            "commit_assisted_by": row["commit_assisted_by"],
            "commit_assisted_by_file": row["commit_assisted_by_file"],
        }

        if (
            str(final_row["ai_assisted"]).lower() == "true"
            or str(final_row["ai_keyword_desc"]).lower() == "true"
            or ai_keyword_comments
            or ai_keyword_discussion
            or str(final_row["ai_keyword_commits"]).lower() == "true"
            or str(final_row["commit_assisted_by"]).lower() == "true"
        ):
            final_rows.append(final_row)

    print(
        "PRs with positive indicators before bot-filtered checks: "
        f"{positive_before_bot_check}"
    )
    print(
        "PRs remaining after bot-filtered checks and indicator filtering: "
        f"{len(final_rows)}"
    )

    return final_rows


def write_final_dataset(rows):
    """Write the final analysis-ready CSV."""
    with open(FINAL_CSV_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    raw_rows = read_raw_data()

    print(f"Artifacts retrieved: {len(raw_rows)}")

    unique_rows, duplicates_removed = remove_duplicate_prs(raw_rows)

    print(
        f"After duplicate exclusions: {len(unique_rows)} "
        f"({duplicates_removed} duplicates removed)"
    )

    final_rows = build_final_rows(unique_rows)

    write_final_dataset(final_rows)

    print(f"Final observations: {len(final_rows)}")
    print(f"Final dataset: {FINAL_CSV_PATH}")


if __name__ == "__main__":
    main()