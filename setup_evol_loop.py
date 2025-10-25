#!/usr/bin/env python3
"""
Darwin2025 Evolution Loop Setup Script
Author: KGNINJA
Description:
  Creates evol.md (self-improvement log)
  and a GitHub Actions workflow that makes Codex improve it weekly.
"""

import os
from datetime import datetime

# --- Directory setup ---
os.makedirs(".github/workflows", exist_ok=True)

# --- evol.md initial content ---
evol_content = f"""# 🧬 Darwin2025 Evolution Log

## 初期理念
AIと人間の共進化をテーマに、反省と改善を繰り返す自己進化システムを構築する。

## Week 0 Reflection ({datetime.now().strftime('%Y-%m-%d')})
- 概念を立ち上げた。
- 今後の目標: 「自己反省 → 改善提案 → 実行 → 再反省」の自動ループ化。

---

次回以降、この `evol.md` は Codex によって自動進化します。
"""

# --- evolve.yml workflow ---
workflow_content = """name: 🧬 Darwin2025 Evolver

on:
  schedule:
    - cron: "0 3 * * 1"   # JST正午（月曜）
  workflow_dispatch:

permissions:
  contents: write

jobs:
  evolve:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 🧠 Read and evolve evol.md
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          model: gpt-5-auto
          safety-strategy: unsafe
          prompt: |
            Read evol.md.
            Summarize recent reflections and lessons.
            Append a new section titled:
            "Next Evolution Plan ({{ date }})"
            that proposes concrete upgrades or learning directions
            for Darwin2025 to improve itself.
            Write naturally in Japanese.
            Preserve all previous logs.
          output-file: evol.md

      - name: 💾 Commit updated evol.md
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add evol.md
          git diff --staged --quiet || git commit -m "🧬 Evol.md auto-evolved by Codex"
          git push
"""

# --- Write files ---
with open("evol.md", "w", encoding="utf-8") as f:
    f.write(evol_content)

with open(".github/workflows/evolve.yml", "w", encoding="utf-8") as f:
    f.write(workflow_content)

print("✅ Darwin2025 evolution loop initialized.")
print("  - evol.md created")
print("  - .github/workflows/evolve.yml created")
