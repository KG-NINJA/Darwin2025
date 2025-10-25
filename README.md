# Darwin2025

## Self-Evolution Workflow

This repository includes an automated "self-evolution" loop defined in [`.github/workflows/evolve.yml`](.github/workflows/evolve.yml). The GitHub Actions workflow runs every day at 03:00 UTC (noon JST) or on manual dispatch. It checks out the repository, invokes the `openai/codex-action@v1` action with the `gpt-4o-mini` model, and asks it—via a Japanese prompt—to review the current `evol.md`, summarize the previous day's reflections, and append a new section titled `## 次の進化計画（{{ date }})`. The AI must keep the suggestions modest, sustainable, and in Japanese, preserving the historical log. After updating `evol.md`, the workflow commits and pushes the changes using the `github-actions[bot]` identity if any modifications were made.
