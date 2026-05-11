from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

DEFAULT_URLS = [
    "https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/",
    "https://www.darkenergysurvey.org/the-des-project/data-access/",
    "https://des.ncsa.illinois.edu/releases/y6a2/",
]

KEYWORDS = [
    "3x2",
    "3×2",
    "twopoint",
    "two-point",
    "data vector",
    "datavector",
    "covariance",
    "chain",
    ".fits",
    ".fits.gz",
    ".cosmosis",
    ".txt",
    ".csv",
    ".npz",
]

LINK_RE = re.compile(r'href=["\']([^"\']+)["\']', re.I)


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "dfm-mkc-cosmology-des-y6-release-monitor/1.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")


def discover(urls: list[str]) -> dict:
    pages = []
    links = []

    for url in urls:
        try:
            text = fetch(url)
            status = "ok"
        except Exception as exc:
            text = ""
            status = f"error:{type(exc).__name__}"

        page_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        pages.append(
            {
                "url": url,
                "status": status,
                "sha256": page_hash,
                "matched_keywords": sorted(
                    {kw for kw in KEYWORDS if kw.lower() in text.lower()}
                ),
            }
        )

        for raw_href in LINK_RE.findall(text):
            href = urljoin(url, raw_href)
            label = href.lower().replace("_", " ")
            matched = sorted({kw for kw in KEYWORDS if kw.lower() in label})
            artifact_matched = [
                kw for kw in matched
                if kw.lower() in {
                    "covariance",
                    "data vector",
                    "datavector",
                    ".fits",
                    ".fits.gz",
                    ".cosmosis",
                    ".npz",
                    ".npy",
                    ".csv",
                }
            ]
            if artifact_matched:
                links.append(
                    {
                        "source": url,
                        "url": href,
                        "matched_keywords": artifact_matched,
                    }
                )

    released = bool(links)

    return {
        "status": "CANDIDATE_RELEASE_LINKS_FOUND" if released else "PENDING_RELEASE",
        "pages": pages,
        "candidate_links": links,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="artifacts/des_y6_release_monitor/latest.json",
    )
    parser.add_argument("--url", action="append", default=[])
    args = parser.parse_args()

    urls = args.url or DEFAULT_URLS
    result = discover(urls)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print(result["status"])
    for link in result["candidate_links"]:
        print(link["url"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
