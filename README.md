# Repo Trust Radar

A tiny CLI starter that scores a GitHub repository URL for suspicious trend/spam signals and prints a shareable Markdown report.

## Install

```bash
python -m pip install -e .
```

## Use

```bash
repo-trust-radar https://github.com/owner/repo
repo-trust-radar https://github.com/owner/repo --json
```

This minimal version uses URL/name heuristics only; extend `src/repo_trust_radar/main.py` with GitHub API and README checks.

## Development

```bash
python -m pip install -e .[dev]
pytest
```
