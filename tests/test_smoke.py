from repo_trust_radar.main import main, parse_repo, score_repo


def test_parse_repo_url() -> None:
    assert parse_repo("https://github.com/octocat/Hello-World") == "octocat/Hello-World"


def test_score_flags_risky_keyword() -> None:
    report = score_repo("arenaasd/Roblox_BedWars_Auto-Farm___Aimbot")
    assert report.score < 80
    assert report.reasons


def test_main_json_output() -> None:
    output = main(["octocat/Hello-World", "--json"])
    assert '"repo": "octocat/Hello-World"' in output
