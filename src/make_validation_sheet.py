"""
Build the manual-validation sheet: the keyword-only PRs from the final dataset.

A PR is "keyword-only" when it has no AI-assisted label and no Assisted-by:
commit trailer, so the only evidence of GenAI use is a keyword match in its
description, comments, review discussion, or first commit message. These are
the candidates most likely to be false positives and must be checked by hand.

For each PR the sheet lists which sources matched, which keywords matched, and
a short snippet around the first hit, plus empty `decision` (keep/drop) and
`reason` columns for the reviewer to fill in.
"""

import csv
import os
import re

from CONSTANTS import DATA_DIR
from main import genai_keywords
from make_final_dataset import FINAL_CSV_PATH, is_bot, load_json

VALIDATION_CSV_PATH = os.path.join(DATA_DIR, "manual_validation.csv")

KEYWORD_SOURCES = [
    "ai_keyword_desc",
    "ai_keyword_comments",
    "ai_keyword_discussion",
    "ai_keyword_commits",
]

FIELDS = [
    "pr_number",
    "pr_desc",
    "pr_comments",
    "pr_discussion",
    "pr_commits",
    "pr_creator",
    "tags",
    "matched_sources",
    "matched_keywords",
    "snippet",
    "decision",
    "reason",
]

SNIPPET_RADIUS = 80


def is_true(value):
    return str(value).lower() == "true"


def keyword_pattern(keyword):
    # Mirrors comment_contains_ai: "ai" is whole-word, everything else substring.
    if keyword == "ai":
        return re.compile(r"\bai\b")
    return re.compile(re.escape(keyword))


KEYWORD_PATTERNS = [(k, keyword_pattern(k)) for k in genai_keywords]


def find_matches(text):
    """Return (matched keywords, snippet around the first hit) for one text."""
    lower = text.lower()
    matched = []
    first_pos = None
    for keyword, pattern in KEYWORD_PATTERNS:
        m = pattern.search(lower)
        if m:
            matched.append(keyword)
            if first_pos is None or m.start() < first_pos[0]:
                first_pos = (m.start(), m.end())
    snippet = ""
    if first_pos:
        start = max(first_pos[0] - SNIPPET_RADIUS, 0)
        end = min(first_pos[1] + SNIPPET_RADIUS, len(text))
        snippet = " ".join(text[start:end].split())
    return matched, snippet


def load_text(relative_path):
    if not relative_path:
        return ""
    path = os.path.join(DATA_DIR, relative_path)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def thread_texts(relative_path):
    """Non-bot comment/discussion texts, matching make_final_dataset's filtering."""
    return [
        item.get("comment") or item.get("message") or ""
        for item in load_json(relative_path)
        if not is_bot(item.get("name"))
    ]


def texts_for_row(row):
    """Texts for each source that was flagged True, in a fixed order."""
    texts = []
    if is_true(row["ai_keyword_desc"]):
        texts.append(("desc", [load_text(row["pr_desc"])]))
    if is_true(row["ai_keyword_comments"]):
        texts.append(("comments", thread_texts(row["pr_comments"])))
    if is_true(row["ai_keyword_discussion"]):
        texts.append(("discussion", thread_texts(row["pr_discussion"])))
    if is_true(row["ai_keyword_commits"]):
        texts.append(("commits", [load_text(row["pr_commits"])]))
    return texts


def file_link(relative_path):
    """Path relative to the sheet itself, so it works on every teammate's checkout."""
    if not relative_path:
        return ""
    target = os.path.join(DATA_DIR, relative_path)
    sheet_dir = os.path.dirname(VALIDATION_CSV_PATH)
    return "./" + os.path.relpath(target, sheet_dir).replace(os.sep, "/")


def build_validation_row(row):
    sources = []
    keywords = []
    snippet = ""
    for source, texts in texts_for_row(row):
        sources.append(source)
        for text in texts:
            matched, text_snippet = find_matches(text)
            for k in matched:
                if k not in keywords:
                    keywords.append(k)
            if text_snippet and not snippet:
                snippet = text_snippet

    return {
        "pr_number": row["pr_number"],
        "pr_creator": row["pr_creator"],
        "tags": row["tags"],
        "matched_sources": ";".join(sources),
        "matched_keywords": ";".join(keywords),
        "snippet": snippet,
        "pr_desc": file_link(row["pr_desc"]),
        "pr_comments": file_link(row["pr_comments"]),
        "pr_discussion": file_link(row["pr_discussion"]),
        "pr_commits": file_link(row["pr_commits"]),
        "decision": "",
        "reason": "",
    }


def is_keyword_only(row):
    return (
        not is_true(row["ai_assisted"])
        and not is_true(row["commit_assisted_by"])
        and any(is_true(row[k]) for k in KEYWORD_SOURCES)
    )


def main():
    with open(FINAL_CSV_PATH, "r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    candidates = [build_validation_row(r) for r in rows if is_keyword_only(r)]

    if os.path.exists(VALIDATION_CSV_PATH):
        raise SystemExit(
            f"{VALIDATION_CSV_PATH} already exists - refusing to overwrite "
            "hand-entered decisions. Move or delete it first."
        )

    with open(VALIDATION_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(candidates)

    print(f"Final dataset PRs: {len(rows)}")
    print(f"Keyword-only PRs to validate by hand: {len(candidates)}")
    print(f"Validation sheet: {VALIDATION_CSV_PATH}")


if __name__ == "__main__":
    main()
