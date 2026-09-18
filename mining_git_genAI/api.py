# api.py
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from CONSTANTS import BASE_URL, HEADERS


def get_session():
    """Open a requests Session for the GitHub API.

    Reuses one TCP connection across thousands of requests and retries
    transient failures (5xx, connection resets) with backoff.
    """
    session = requests.Session()
    session.headers.update(HEADERS)

    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def fetch_request(session, endpoint, params=None):
    """GET a GitHub API endpoint on an open session, honoring rate limits.

    `endpoint` is either a path relative to BASE_URL or a full URL (as
    returned in a Link header for pagination).
    """
    url = endpoint if endpoint.startswith("http") else BASE_URL + endpoint

    try:
        response = session.get(url, params=params)
    except requests.exceptions.RequestException as err:
        print(err)
        return None

    # Primary rate limit exhausted: sleep until GitHub's reset time.
    if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
        reset_at = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
        wait = max(reset_at - time.time(), 0) + 1
        print(f"Primary rate limit hit, sleeping {wait:.0f}s")
        time.sleep(wait)
        response = session.get(url, params=params)

    # Secondary (abuse detection) rate limit: GitHub tells us how long to wait.
    elif response.status_code == 403 and "Retry-After" in response.headers:
        wait = int(response.headers["Retry-After"]) + 1
        print(f"Secondary rate limit hit, sleeping {wait}s")
        time.sleep(wait)
        response = session.get(url, params=params)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return None

    return response


def fetch_all_pages(session, endpoint, params=None):
    """Yield each page's JSON list, following the Link header until exhausted."""
    url = endpoint
    request_params = params

    while url:
        response = fetch_request(session, url, params=request_params)
        if response is None:
            return

        yield response.json()

        url = response.links.get("next", {}).get("url")
        # Pagination params are already baked into the `next` URL.
        request_params = None
