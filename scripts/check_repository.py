#!/usr/bin/env python3
"""Check public repository invariants with the Python standard library."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md",
    "SKILL.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "agents/openai.yaml",
    "references/MASTER_PROMPT.md",
    "references/PORTABLE_CONTEXT.md",
    "schemas/package.schema.json",
    "scripts/context_package.py",
    "scripts/validate.py",
    "scripts/test_repository_check.py",
    "scripts/test_context_package.py",
    "scripts/test_validate.py",
    "docs/architecture.md",
    "docs/artifact-contract.md",
    "docs/verification.md",
)
EXCLUDED = (
    "references/ORIGINAL_REFERENCE.txt",
    "references/PILOT_LESSONS_AND_TRANSFER_PROBE.md",
)
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
SENSITIVE_PATTERNS = {
    "absolute user path": re.compile(r"/" + r"Users/|[A-Za-z]:\\\\Users\\\\"),
    "downloads path": re.compile(r"(?:^|[/\\\\])Downloads(?:[/\\\\])"),
    "private key": re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    "GitHub token": re.compile(r"(?:ghp_|github_pat_)[A-Za-z0-9_]{12,}"),
    "OpenAI-style key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
}
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def text_files():
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def check_required(errors):
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    for relative in EXCLUDED:
        if (ROOT / relative).exists():
            errors.append(f"excluded research artifact is present: {relative}")


def check_skill(errors):
    path = ROOT / "SKILL.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md has no YAML frontmatter")
        return
    end = text.find("\n---\n", 4)
    if end < 0:
        errors.append("SKILL.md frontmatter is not closed")
        return
    frontmatter = text[4:end]
    if not re.search(r"^name:\s*economic-reasoning-engineering\s*$", frontmatter, re.MULTILINE):
        errors.append("SKILL.md has the wrong skill name")
    if not re.search(r"^description:\s*\S", frontmatter, re.MULTILINE):
        errors.append("SKILL.md has no description")


def check_local_links(errors):
    for path in text_files():
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK_PATTERN.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (path.parent / target).resolve().exists():
                relative = path.relative_to(ROOT)
                errors.append(f"broken local link in {relative}: {target}")


def check_sensitive_text(errors):
    for path in text_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in SENSITIVE_PATTERNS.items():
            if pattern.search(text):
                relative = path.relative_to(ROOT)
                errors.append(f"{name} found in {relative}")


def check_symlinks(errors):
    for path in ROOT.rglob("*"):
        if ".git" not in path.parts and path.is_symlink():
            errors.append(f"repository contains a symbolic link: {path.relative_to(ROOT)}")


def main():
    errors = []
    check_required(errors)
    check_skill(errors)
    check_local_links(errors)
    check_sensitive_text(errors)
    check_symlinks(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Repository contract passed: {len(REQUIRED)} required files checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
