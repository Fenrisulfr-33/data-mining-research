"""
Build the validated dataset: strong-signal PRs plus the keyword-only PRs a
human marked `keep` in data/manual_validation_filled.csv.

- Strong PRs (AI-assisted label or Assisted-by: trailer) are kept as-is; the
  author disclosed GenAI use, so they are not hand-checked.
- Keyword-only PRs are kept only when `decision` is `keep`. `drop` and
  `unsure` are excluded (common typos like `usnure` are normalized).

Writes data/validated_dataset.csv with the final dataset's columns plus:
  evidence           - `strong` or `keyword_validated`
  validation_reason  - the reviewer's reason (keyword_validated rows only)

Never modifies its inputs.
"""

import csv
import os
from collections import Counter

from CONSTANTS import CSV_FIELDS, DATA_DIR
from make_final_dataset import FINAL_CSV_PATH

FILLED_CSV_PATH = os.path.join(DATA_DIR, "manual_validation_filled.csv")
VALIDATED_CSV_PATH = os.path.join(DATA_DIR, "validated_dataset.csv")

FIELDS = CSV_FIELDS + ["evidence", "validation_reason"]

DECISION_FIXES = {"usnure": "unsure"}


def is_true(value):
    return str(value).lower() == "true"


def is_strong(row):
    return is_true(row["ai_assisted"]) or is_true(row["commit_assisted_by"])


def normalize_decision(value):
    value = value.strip().lower()
    return DECISION_FIXES.get(value, value)


def load_decisions():
    with open(FILLED_CSV_PATH, "r", newline="", encoding="utf-8-sig") as f:
        return {
            r["pr_number"]: (normalize_decision(r["decision"]), r["reason"].strip())
            for r in csv.DictReader(f)
        }


def main():
    with open(FINAL_CSV_PATH, "r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    decisions = load_decisions()

    validated = []
    keyword_counts = Counter()
    for row in rows:
        if is_strong(row):
            validated.append({**row, "evidence": "strong", "validation_reason": ""})
            continue
        decision, reason = decisions.get(row["pr_number"], ("", ""))
        keyword_counts[decision or "not reviewed"] += 1
        if decision == "keep":
            validated.append(
                {**row, "evidence": "keyword_validated", "validation_reason": reason}
            )

    with open(VALIDATED_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(validated)

    strong = sum(1 for r in validated if r["evidence"] == "strong")
    print(f"Final dataset PRs: {len(rows)}")
    print(f"Strong (not hand-checked): {strong}")
    print(f"Keyword-only decisions: {dict(keyword_counts)}")
    print(f"Validated PRs: {len(validated)}")
    print(f"Validated dataset: {VALIDATED_CSV_PATH}")


if __name__ == "__main__":
    main()
