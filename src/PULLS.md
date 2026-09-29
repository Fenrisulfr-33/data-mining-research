# Pull Request API

# GitHub API: Pull Request Reviews Reference

**Endpoint:** `GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews`

Returns an **array** of review objects. Each object is one review left on the pull request.

---

## Top-level keys

| Key | What it means |
|---|---|
| `id` | Numeric ID of this review |
| `node_id` | The same review's ID in GitHub's GraphQL API. You can usually ignore it. |
| `user` | The person who wrote the review (see [`user` keys](#user-keys)) |
| `body` | The review's comment text |
| `state` | The review's verdict: `APPROVED`, `CHANGES_REQUESTED`, `COMMENTED`, `DISMISSED`, or `PENDING` (not submitted yet) |
| `html_url` | Link to the review on github.com, for a browser |
| `pull_request_url` | API link to the PR this review belongs to |
| `_links` | The same two URLs again, in a nested format (`html` = web page, `pull_request` = API) |
| `submitted_at` | When the review was submitted (ISO 8601, UTC) |
| `commit_id` | SHA of the commit the reviewer was looking at when they reviewed |
| `author_association` | The reviewer's relationship to the repo: `OWNER`, `MEMBER`, `COLLABORATOR`, `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, `NONE`, etc. |

## `user` keys

| Key | What it means |
|---|---|
| `login` | Username |
| `id` | Numeric user ID |
| `node_id` | GraphQL user ID |
| `avatar_url` | Profile picture |
| `gravatar_id` | Old Gravatar field, almost always empty |
| `html_url` | Profile page on github.com |
| `url` | API link to the full user profile |
| `followers_url` | API link to the user's followers |
| `following_url` | API link to who the user follows |
| `gists_url` | API link to the user's gists |
| `starred_url` | API link to repos the user has starred |
| `subscriptions_url` | API link to repos the user is watching |
| `organizations_url` | API link to the user's organizations |
| `repos_url` | API link to the user's repositories |
| `events_url` | API link to the user's activity |
| `received_events_url` | API link to activity involving the user |
| `type` | `User`, `Bot`, or `Organization` |
| `site_admin` | Whether they're a GitHub staff admin |

> Parts of a URL in `{braces}` are optional templates. For example, `following{/other_user}` can become `/following/someone`.

---

## How reviews relate to PRs and issues

- **One review → one PR.** Each review belongs to exactly one pull request (`pull_request_url`).
- **One PR → many reviews.** A PR can have any number of reviews, which is why the endpoint returns an array.
- **One review → one commit.** `commit_id` is the version of the code the reviewer saw when they submitted.
- **PRs are issues.** In GitHub's model every pull request is also an issue, and the two share one numbering system, so PR #12 is also issue #12. A review is never attached to a regular issue (one that isn't a PR).
- **Linked issues live on the PR.** If a PR says "Closes #5", that link is on the PR, not on the review. To reach it, go review → PR → the PR's linked issues.

---

## Simplified mapping (Python)

Most of the useful data is in about 7 fields:

```python
readable = [
    {
        "reviewer": r["user"]["login"],
        "verdict": r["state"],
        "comment": r["body"],
        "submitted": r["submitted_at"],
        "commit": r["commit_id"],
        "role": r["author_association"],
        "link": r["html_url"],
    }
    for r in reviews
]
```

> `user` can be `null` if the reviewer's account was deleted. To guard against that, use `(r.get("user") or {}).get("login")`.

### Example output

```json
[
  {
    "reviewer": "octocat",
    "verdict": "APPROVED",
    "comment": "Here is the body for the review.",
    "submitted": "2019-11-17T17:43:43Z",
    "commit": "ecdd80bb57125d7ba9641ffaa4d7d2c19d3f3091",
    "role": "COLLABORATOR",
    "link": "https://github.com/octocat/Hello-World/pull/12#pullrequestreview-80"
  }
]
```
