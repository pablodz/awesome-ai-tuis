#!/usr/bin/env python3
"""Fetch GitHub stars and regenerate README.md / README.es.md."""

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
README_ES = ROOT / "README.es.md"

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


def build_table(tuis: list, lang: str) -> str:
    """Build the markdown table for a given language."""
    rows = []
    for i, t in enumerate(tuis, 1):
        stars = fmt_stars(t["stars"])
        name = t["name"]
        repo = t["repo"]
        language = t["language"]
        desc = t["description"][lang]
        features = " · ".join(t["features"][lang])

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

📖 [Versión en español →](README.es.md)

---

## 📊 The List

> Ordered by GitHub stars (descending). Updated automatically every day.

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
    "en": "Short description.",
    "es": "Descripción corta."
  }},
  "features": {{
    "en": ["🏷 Feature 1", "🏷 Feature 2"],
    "es": ["🏷 Característica 1", "🏷 Característica 2"]
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

## 🌍 Multi-language

| Language | File |
|----------|------|
| English  | [`README.md`](README.md) |
| Español  | [`README.es.md`](README.es.md) |

---

## 🙌 Credits

Curated with ❤️ by the open-source community. Inspired by the [awesome](https://github.com/sindresorhus/awesome) list tradition.
"""

README_ES_TEMPLATE = """# 🤖 awesome-ai-tuis

> Interfaces de Terminal (TUI) para programación asistida por IA — curadas, ordenadas y listas para explorar.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: CC0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

Una lista seleccionada a mano de herramientas **TUI (Terminal User Interface)** que llevan la programación asistida por IA directamente a tu terminal. Sin navegador, sin plugin de IDE — solo tú, tu teclado y un agente de IA en una interfaz de texto.

📖 [English version →](README.md)

---

## 📊 La Lista

> Ordenada por estrellas de GitHub (descendente). Actualizada automáticamente cada día.

{stars_table}

---

## 📋 Plantilla — Añadir una nueva TUI

¿Quieres contribuir? Añade tu entrada en [`data/tuis.json`](data/tuis.json) y abre un PR:

```json
{{
  "repo": "owner/repo",
  "name": "NombreHerramienta",
  "language": "Rust",
  "description": {{
    "en": "Short description.",
    "es": "Descripción corta."
  }},
  "features": {{
    "en": ["🏷 Feature 1", "🏷 Feature 2"],
    "es": ["🏷 Característica 1", "🏷 Característica 2"]
  }}
}}
```

**La tabla se genera automáticamente** — no necesitas editar README.md directamente. Las estrellas se actualizan a diario vía GitHub Actions.

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para todos los detalles.

---

## 🤖 Automatización

Esta lista se auto-actualiza cada día mediante un [GitHub Action](.github/workflows/update-stars.yml):

1. Lee [`data/tuis.json`](data/tuis.json) (fuente de verdad)
2. Consulta las ⭐ actuales desde la API de GitHub
3. Reordena la tabla por estrellas descendente
4. Hace commit automáticamente

Para añadir una TUI, solo edita `data/tuis.json` — el script hace el resto.

---

## 🌍 Multi-idioma

| Idioma | Archivo |
|--------|---------|
| English  | [`README.md`](README.md) |
| Español  | [`README.es.md`](README.es.md) |

---

## 🙌 Créditos

Curado con ❤️ por la comunidad open-source. Inspirado en la tradición de las listas [awesome](https://github.com/sindresorhus/awesome).
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

    print("\n📝 Generating README.md...")
    table_en = build_table(tuis, "en")
    readme_en = README_EN_TEMPLATE.format(stars_table=table_en)
    with open(README_EN, "w") as f:
        f.write(readme_en)
    print(f"   ✅ {README_EN}")

    print("📝 Generating README.es.md...")
    table_es = build_table(tuis, "es")
    readme_es = README_ES_TEMPLATE.format(stars_table=table_es)
    with open(README_ES, "w") as f:
        f.write(readme_es)
    print(f"   ✅ {README_ES}")

    # Save updated star counts back to JSON (for reference)
    for t in tuis:
        t["_stars_fetched"] = t.pop("stars", 0)

    print("\n🎉 Done! Run `git diff` to see changes.")


if __name__ == "__main__":
    main()
