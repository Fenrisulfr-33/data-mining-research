"""
Produce every results table shown in the README (and used in the paper).

Reads the pipeline outputs - it never modifies them:
  data/final_dataset.csv                     (make_final_dataset.py)
  data/manual_validation_filled.csv          (hand-filled validation sheet)
  data/validated_dataset.csv                 (make_validated_dataset.py)
  data/manual_validation_second_review.csv   (optional, second-review pass)

Only rows of the validation sheet whose PR is keyword-only in the final
dataset are counted, so PRs outside the observation period are ignored.

Writes data/results_tables.md and prints the same Markdown to stdout.
"""

import csv
import os
from collections import Counter, defaultdict

from CONSTANTS import DATA_DIR
from make_final_dataset import FINAL_CSV_PATH
from make_validated_dataset import (
    FILLED_CSV_PATH,
    VALIDATED_CSV_PATH,
    is_strong,
    is_true,
    normalize_decision,
)

SECOND_REVIEW_PATH = os.path.join(DATA_DIR, "manual_validation_second_review.csv")
RESULTS_PATH = os.path.join(DATA_DIR, "results_tables.md")

DECISIONS = ["keep", "drop", "unsure"]
REVIEWER_PREFIX = "Reviewer-suspected AI use:"

SIGNALS = [
    ("`Assisted-by:` trailer", "commit_assisted_by"),
    ("Keyword in commit", "ai_keyword_commits"),
    ("Keyword in description", "ai_keyword_desc"),
    ("Keyword in comments", "ai_keyword_comments"),
    ("Keyword in review", "ai_keyword_discussion"),
    ("`AI-assisted` label", "ai_assisted"),
]

SOURCES = [
    ("Comments", "comments"),
    ("Review", "discussion"),
    ("Description", "desc"),
    ("Commit", "commits"),
]

BAR_WIDTH = 20


def read_csv(path):
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def n(value):
    return f"{value:,}"


def pct(part, whole):
    value = part / whole * 100 if whole else 0
    return "<0.1%" if 0 < value < 0.1 else f"{value:.1f}%"


def bar(value, largest):
    blocks = round(value / largest * BAR_WIDTH) if largest else 0
    return "`" + ("█" * blocks if blocks else "▌") + "`"


def signal_tables(final_rows):
    counts = [(label, col, sum(is_true(r[col]) for r in final_rows)) for label, col in SIGNALS]
    largest = max(c for _, _, c in counts)
    strong = sum(is_strong(r) for r in final_rows)

    lines = [
        f"PRs with at least one AI signal: **{n(len(final_rows))}**",
        "",
        "| Signal | Column | PRs flagged | |",
        "|---|---|---:|---|",
    ]
    lines += [f"| {label} | `{col}` | **{n(c)}** | {bar(c, largest)} |" for label, col, c in counts]
    lines += [
        "",
        "| Evidence | PRs | Meaning |",
        "|---|---:|---|",
        f"| **Strong** | **{n(strong)}** | Has the `AI-assisted` label or an `Assisted-by:` "
        "trailer - the author disclosed it |",
        f"| **Keyword only** | **{n(len(final_rows) - strong)}** | Only a keyword match - "
        "needs a human check (see Manual validation below) |",
    ]
    return lines


def precision_table(sheet, keys_of, names=None, order=None):
    counts = defaultdict(Counter)
    for row in sheet:
        for key in keys_of(row):
            counts[key][row["d"]] += 1

    keys = order or sorted(counts, key=lambda k: (-sum(counts[k].values()), k))
    lines = []
    for key in keys:
        c = counts[key]
        total = sum(c.values())
        name = names[key] if names else f"`{key}`"
        lines.append(
            f"| {name} | {n(total)} | {n(c['keep'])} | {n(c['drop'])} | "
            f"{n(c['unsure'])} | {c['keep'] / total * 100:.1f}% |"
        )
    return lines


def validation_tables(sheet, strong_count, validated_count):
    decisions = Counter(r["d"] for r in sheet)
    total = len(sheet)
    reviewer = sum(1 for r in sheet if r["d"] == "keep" and r["reason"].startswith(REVIEWER_PREFIX))

    lines = [
        f"Keyword-only PRs checked by hand: **{n(total)}**",
        "",
        "| Decision | PRs | % of keyword-only |",
        "|---|---:|---:|",
    ]
    lines += [f"| `{d}` | {n(decisions[d])} | {decisions[d] / total * 100:.1f}% |" for d in DECISIONS]
    lines += [
        "",
        "| Evidence | PRs |",
        "|---|---:|",
        f"| Strong (label or `Assisted-by:` trailer) | {n(strong_count)} |",
        f"| Keyword-only, kept after manual review | {n(decisions['keep'])} |",
        f"| ...of which kept on reviewer suspicion alone | {n(reviewer)} |",
        f"| **Total validated** | **{n(validated_count)}** |",
        "",
        f"`unsure` PRs (margin of error): {n(decisions['unsure'])} - true total between "
        f"**{n(validated_count)}** and **{n(validated_count + decisions['unsure'])}**. "
        f"Without the reviewer-suspicion rule: **{n(validated_count - reviewer)}**.",
    ]

    lines += [
        "",
        "### How reliable each keyword was",
        "",
        "| Keyword | PRs matched | `keep` | `drop` | `unsure` | Precision |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    lines += precision_table(sheet, lambda r: [k for k in r["matched_keywords"].split(";") if k])

    lines += [
        "",
        "By where the keyword matched:",
        "",
        "| Source | PRs matched | `keep` | `drop` | `unsure` | Precision |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    lines += precision_table(
        sheet,
        lambda r: [s for s in r["matched_sources"].split(";") if s],
        names=dict((key, label) for label, key in SOURCES),
        order=[key for _, key in SOURCES],
    )

    # Group reasons case-insensitively, shown with their first spelling.
    drop_reasons = Counter()
    shown_as = {}
    for row in sheet:
        if row["d"] == "drop":
            key = row["reason"].strip().lower()
            drop_reasons[key] += 1
            shown_as.setdefault(key, row["reason"].strip())
    lines += ["", "Most common reasons for dropping a PR:", "", "| Reason | PRs |", "|---|---:|"]
    lines += [f"| {shown_as[k]} | {v} |" for k, v in drop_reasons.most_common(10)]
    return lines


def second_review_lines(keyword_only):
    if not os.path.exists(SECOND_REVIEW_PATH):
        return []
    rows = [r for r in read_csv(SECOND_REVIEW_PATH) if r["pr_number"] in keyword_only]
    total = len(rows)
    agree = sum(r["team_decision"] == r["second_decision"] for r in rows)
    expected = sum(
        (sum(r["team_decision"] == d for r in rows) / total)
        * (sum(r["second_decision"] == d for r in rows) / total)
        for d in DECISIONS
    )
    kappa = (agree / total - expected) / (1 - expected)
    return [
        "",
        f"Second review: agreed on **{agree / total * 100:.1f}%** of {n(total)} PRs "
        f"(Cohen's κ = **{kappa:.2f}**) before disagreements were reconciled.",
    ]


def tag_table(validated_rows):
    # A PR can list the same tag twice; count each PR once per tag.
    tags = Counter(t for r in validated_rows for t in set(r["tags"].split(";")) if t.strip())
    untagged = sum(1 for r in validated_rows if not r["tags"].strip())
    total = len(validated_rows)

    lines = [
        f"Validated PRs: **{n(total)}**, with no tags: **{n(untagged)}**, "
        f"distinct tags: **{n(len(tags))}**",
        "",
        "| # | Tag | PRs | % of validated PRs |",
        "|---:|---|---:|---:|",
    ]
    ranked = sorted(tags.items(), key=lambda kv: (-kv[1], kv[0].lower()))
    lines += [f"| {i} | {tag} | {n(c)} | {pct(c, total)} |" for i, (tag, c) in enumerate(ranked, 1)]
    return lines


def main():
    final_rows = read_csv(FINAL_CSV_PATH)
    validated_rows = read_csv(VALIDATED_CSV_PATH)
    keyword_only = {r["pr_number"] for r in final_rows if not is_strong(r)}

    sheet = [r for r in read_csv(FILLED_CSV_PATH) if r["pr_number"] in keyword_only]
    for row in sheet:
        row["d"] = normalize_decision(row["decision"])
        row["reason"] = row["reason"].strip()

    strong_count = len(final_rows) - len(keyword_only)

    lines = ["# Results tables", "", "## Mining results", ""]
    lines += signal_tables(final_rows)
    lines += ["", "## Manual validation", ""]
    lines += validation_tables(sheet, strong_count, len(validated_rows))
    lines += second_review_lines(keyword_only)
    lines += ["", "## Tags on validated PRs", ""]
    lines += tag_table(validated_rows)

    text = "\n".join(lines) + "\n"
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    print(f"Written to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
