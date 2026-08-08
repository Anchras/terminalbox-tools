#!/usr/bin/env python3
"""Validate the public Codex plugin and marketplace without external dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-remote-ssh"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_https(value: str, field: str) -> None:
    parsed = urlparse(value)
    require(parsed.scheme == "https" and bool(parsed.netloc), f"{field} must be an HTTPS URL")


def main() -> None:
    manifest = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
    generic_manifest = load_json(PLUGIN / "plugin.json")
    claude_manifest = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
    marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")

    require(manifest["name"] == PLUGIN.name, "plugin folder and manifest name must match")
    require(
        re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", manifest["version"]) is not None,
        "plugin version must be strict semver",
    )
    require(
        {manifest["version"], generic_manifest["version"], claude_manifest["version"]}
        == {manifest["version"]},
        "all plugin manifests must use the same version",
    )

    interface = manifest["interface"]
    require(0 < len(interface["displayName"]) <= 30, "displayName must fit directory limits")
    require(
        0 < len(interface["shortDescription"]) <= 30,
        "shortDescription must fit directory limits",
    )
    require(0 < len(interface["longDescription"]) <= 4000, "longDescription is out of bounds")
    require(0 < len(interface["developerName"]) <= 80, "developerName is out of bounds")
    require(interface["category"] == "Developer Tools", "plugin category must remain explicit")

    prompts = interface["defaultPrompt"]
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "provide one to three prompts")
    require(len(set(prompts)) == len(prompts), "starter prompts must be unique")
    require(all(0 < len(prompt) <= 128 and "\n" not in prompt for prompt in prompts), "starter prompts are out of bounds")

    for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        require_https(interface[field], field)
    require_https(manifest["homepage"], "homepage")
    require_https(manifest["repository"], "repository")

    require(marketplace["name"] == "terminalbox-tools", "unexpected marketplace name")
    entries = [entry for entry in marketplace["plugins"] if entry.get("name") == manifest["name"]]
    require(len(entries) == 1, "marketplace must expose codex-remote-ssh exactly once")
    entry = entries[0]
    require(entry["source"] == {"source": "local", "path": "./plugins/codex-remote-ssh"}, "unexpected marketplace source")
    require(
        entry["policy"] == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "unexpected marketplace policy",
    )
    require(entry["category"] == "Developer Tools", "marketplace category must match")

    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require(
        "codex plugin marketplace add Anchras/terminalbox-tools" in root_readme
        and "codex plugin add codex-remote-ssh@terminalbox-tools" in root_readme,
        "README must retain the native Codex install path",
    )

    submission = (ROOT / "submission" / "codex-remote-ssh.md").read_text(encoding="utf-8")
    require("## Positive test cases" in submission and "## Negative test cases" in submission, "submission test sections are missing")
    positive = submission.split("## Positive test cases", 1)[1].split("## Negative test cases", 1)[0]
    negative = submission.split("## Negative test cases", 1)[1].split("## Manual portal prerequisites", 1)[0]
    require(len(re.findall(r"^### [1-5]\. ", positive, re.MULTILINE)) == 5, "submission must contain five positive test cases")
    require(len(re.findall(r"^### [1-3]\. ", negative, re.MULTILINE)) == 3, "submission must contain three negative test cases")

    print("Terminalbox Codex plugin repository validation passed")


if __name__ == "__main__":
    main()
