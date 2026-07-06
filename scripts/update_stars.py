#!/usr/bin/env python3
"""Fetch GitHub stars and regenerate README.md."""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "tuis.json"
README_EN = ROOT / "README.md"

# Only list tools with more than this many stars in the README.
# The data file keeps every entry; anything above the threshold shows up
# automatically once it grows past it.
MIN_STARS = 100

# GitHub token from env (optional, avoids rate limiting)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "awesome-ai-tuis-bot/1.0",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def fmt_stars(n: int) -> str:
    """Format star count for display."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


def fetch_star_count(repo: str) -> int:
    """Fetch stargazers_count for a GitHub repo."""
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get("stargazers_count", 0)
    except urllib.error.HTTPError as e:
        print(f"  ⚠ HTTP {e.code} for {repo}", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"  ⚠ Error fetching {repo}: {e}", file=sys.stderr)
        return 0


def load_data() -> list:
    """Load TUI data from JSON."""
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return data["tuis"]


TABLE_HEADER = "| # | Name | ⭐ Stars | Language | Description | Key Features |"

TABLE_SEPARATOR = "|---|------|---------|----------|-------------|--------------|"


def build_table(tuis: list) -> str:
    """Build the markdown table."""
    rows = [TABLE_HEADER, TABLE_SEPARATOR]
    for i, t in enumerate(tuis, 1):
        stars = fmt_stars(t["stars"])
        name = t["name"]
        repo = t["repo"]
        language = t["language"]
        desc = t["description"]["en"]
        features = " · ".join(t["features"]["en"])

        row = (
            f"| {i} | [**{name}**](https://github.com/{repo}) "
            f"| {stars} | {language} "
            f"| {desc} "
            f"| {features} |"
        )
        rows.append(row)
    return "\n".join(rows)


README_EN_TEMPLATE = """# 🤖 awesome-ai-tuis

> Terminal User Interfaces for AI-powered coding — curated, ranked, and ready to explore.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: CC0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

A hand-picked list of **TUI (Terminal User Interface)** tools that bring AI-assisted coding straight into your terminal. No browser, no IDE plugin — just you, your keyboard, and an AI agent in a text-based interface.

---

## 📊 The List

> Ordered by GitHub stars (descending). Only tools with 100+ stars are listed. Updated automatically every day.

{stars_table}

---

## 📋 Template — Add a new TUI

Want to contribute? Add your entry to [`data/tuis.json`](data/tuis.json) and open a PR:

```json
{{
  "repo": "owner/repo",
  "name": "ToolName",
  "language": "Rust",
  "description": {{
    "en": "Short description."
  }},
  "features": {{
    "en": ["🏷 Feature 1", "🏷 Feature 2"]
  }}
}}
```

**The table is auto-generated** — no need to edit README.md directly. Stars are fetched daily via GitHub Actions.

See [CONTRIBUTING.md](CONTRIBUTING.md) for full details.

---

## 🤖 Automation

This list self-updates every day via a [GitHub Action](.github/workflows/update-stars.yml):

1. Reads [`data/tuis.json`](data/tuis.json) (source of truth)
2. Fetches live ⭐ counts from the GitHub API
3. Reorders the table by stars descending
4. Commits changes automatically

To add a TUI, just edit `data/tuis.json` — the script handles the rest.

---

## 🙌 Credits

Curated with ❤️ by the open-source community. Inspired by the [awesome](https://github.com/sindresorhus/awesome) list tradition.
"""


def main():
    print("📡 Loading TUI data...")
    tuis = load_data()
    print(f"   {len(tuis)} TUIs in data file\n")

    print("⭐ Fetching star counts from GitHub API...")
    for i, t in enumerate(tuis, 1):
        repo = t["repo"]
        stars = fetch_star_count(repo)
        t["stars"] = stars
        print(f"   [{i:2d}/{len(tuis)}] {repo:45s} → {fmt_stars(stars):>8s}")
        time.sleep(0.3)  # Be gentle to the API

    # Sort by stars descending
    tuis.sort(key=lambda t: t["stars"], reverse=True)

    # Only list tools with more than MIN_STARS stars in the README
    listed = [t for t in tuis if t["stars"] > MIN_STARS]
    hidden = len(tuis) - len(listed)
    print(f"\n📝 Generating README.md ({len(listed)} listed, "
          f"{hidden} below {MIN_STARS}★ threshold)...")
    table_en = build_table(listed)
    readme_en = README_EN_TEMPLATE.format(stars_table=table_en)
    with open(README_EN, "w") as f:
        f.write(readme_en)
    print(f"   ✅ {README_EN}")

    # Save updated star counts back to JSON (for reference)
    for t in tuis:
        t["_stars_fetched"] = t.pop("stars", 0)

    print("\n🎉 Done! Run `git diff` to see changes.")


if __name__ == "__main__":
    main()
