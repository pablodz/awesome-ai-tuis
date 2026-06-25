# Contributing to awesome-ai-tuis

Thanks for helping grow this list! Here's how to add a TUI.

## 🚀 Quick Start

1. **Fork** this repo
2. **Add** your TUI row to [`README.md`](README.md) (and optionally [`README.es.md`](README.es.md))
3. **Open a Pull Request**

## 📋 Row Template

```markdown
| # | [**ToolName**](https://github.com/owner/repo) | ⭐ Stars | Language | Short description. | 🏷 Feature1 · 🏷 Feature2 · 🏷 Feature3 |
```

Example:

```markdown
| 29 | [**MyTUI**](https://github.com/myname/mytui) | 150 | Rust | Blazing fast AI coding TUI with agentic loop. | ⚡ Fast · 🧠 Agentic loop · 🔌 Multi-provider · 🦀 Rust |
```

## ✅ Guidelines

### Position
- Insert the row in the correct position, **sorted by ⭐ stars descending**.
- Update the `#` column numbering for all subsequent rows.

### Description
- Keep it to **one line**, ideally under 100 characters.
- Start with a capital letter, end with a period.
- Focus on what makes it unique among AI coding TUIs.

### Features
- List **3 to 6 key features** using `·` (middle dot, `U+00B7`) as separator.
- Start each feature with an emoji for visual scannability.
- Common emoji ideas:
  - 🧠 agentic / autonomous / reasoning
  - 🦀 Rust · ⚡ Go · 🐍 Python · ☕ Java · 📜 TypeScript
  - 🔌 multi-provider · 🔒 local / private · 🏠 local-first
  - 🛠 MCP / tools · 📝 diffs · 🌳 git
  - ⚡ fast / performance · 🪶 lightweight
  - 🖥 TUI · 🎨 beautiful UI · 📊 dashboard
  - 🤖 multi-agent · 🐝 swarm · 🤝 collaboration
  - 📋 planning · 🧪 testing

### Stars
- Get the star count from the GitHub API:
  ```
  https://api.github.com/repos/owner/repo
  ```
- Use the `stargazers_count` field.
- Format large numbers as `178k`, `7.7k`, etc. (round to 1 decimal for thousands).
- Numbers under 1000: use exact count.

### Language
- Use the primary programming language as shown on GitHub.
- Use `—` if not applicable.

### What qualifies
A tool must:
1. Be an **AI-powered coding assistant** that helps write, edit, or understand code
2. Have a **TUI (Terminal User Interface)** — not just CLI arguments, but an interactive text-based UI
3. Be **publicly available** (open source or free tier)
4. Be actively maintained or have significant community adoption

### What does NOT qualify
- IDE plugins (VSCode, IntelliJ, etc.)
- Web-based tools (browser-only)
- Pure CLI tools without a TUI (one-shot commands)
- General-purpose AI chatbots without coding focus

## 🌐 Multi-language

If you speak Spanish (or another language), please also update [`README.es.md`](README.es.md) (or propose a new translation file like `README.fr.md`).

## 📬 Submitting

1. Ensure your changes follow the format exactly.
2. Test that links work by previewing the markdown.
3. Open a PR with a descriptive title like: `Add MyTUI - 150 ⭐`
4. In the PR body, include a link to the repo and mention why it belongs on the list.

Thank you! 🎉
