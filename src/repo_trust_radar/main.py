from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from urllib.parse import urlparse

RISKY_KEYWORDS = {
    "airdrop",
    "aimbot",
    "auto-farm",
    "booster",
    "cheat",
    "crypto",
    "esp",
    "free-money",
    "generator",
    "hack",
    "token",
}


@dataclass(frozen=True)
class TrustReport:
    repo: str
    score: int
    verdict: str
    reasons: list[str]

    def to_markdown(self) -> str:
        reasons = "\n".join(f"- {reason}" for reason in self.reasons) or "- No obvious URL/name red flags."
        return f"""# Repo Trust Radar Report\n\n**Repository:** `{self.repo}`  \n**Trust score:** **{self.score}/100**  \n**Verdict:** **{self.verdict}**\n\n## Signals\n{reasons}\n"""


def parse_repo(value: str) -> str:
    parsed = urlparse(value)
    path = parsed.path if parsed.netloc else value
    parts = [part for part in path.strip("/").split("/") if part]
    if len(parts) < 2:
        raise ValueError("expected a GitHub URL or owner/repo")
    return "/".join(parts[:2])


def score_repo(value: str) -> TrustReport:
    repo = parse_repo(value)
    haystack = repo.lower().replace("_", "-")
    reasons: list[str] = []
    penalty = 0

    hits = sorted(word for word in RISKY_KEYWORDS if word in haystack)
    if hits:
        penalty += min(60, 15 * len(hits))
        reasons.append(f"Suspicious keyword(s) in repo name: {', '.join(hits)}")

    if re.search(r"[-_]{2,}|\d{4,}", repo):
        penalty += 15
        reasons.append("Name contains repeated separators or long number runs.")

    if len(repo.split("/", 1)[1]) > 45:
        penalty += 10
        reasons.append("Repository name is unusually long/keyword-stuffed.")

    score = max(0, 100 - penalty)
    verdict = "organic" if score >= 80 else "low-signal" if score >= 50 else "risky"
    return TrustReport(repo=repo, score=score, verdict=verdict, reasons=reasons)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score a GitHub repository for lightweight trust signals.")
    parser.add_argument("repo", help="GitHub URL or owner/repo")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    return parser


def main(argv: list[str] | None = None) -> str:
    args = build_parser().parse_args(argv)
    report = score_repo(args.repo)
    return json.dumps(asdict(report), indent=2) if args.json else report.to_markdown()


def cli() -> None:
    print(main())


if __name__ == "__main__":
    cli()
