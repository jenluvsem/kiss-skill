#!/usr/bin/env python3
"""Validate the KISS skill repo. Stdlib only.

Checks the SKILL.md frontmatter against the Agent Skills spec
(https://agentskills.io/specification), Hermes' 60-char description limit,
the repo layout, and the Claude Code plugin manifests.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "kiss"
SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HERMES_DESC_MAX = 60  # Hermes house limit; the spec allows 1024
SKILL_LINES_MAX = 250  # our target; the spec allows 500


def parse_frontmatter(text):
    """Return (fields, body, errors). Handles only the YAML subset we use:
    `key: value` lines plus one level of nested `key:` maps."""
    errors = []
    if not text.startswith("---\n"):
        return {}, "", ["SKILL.md must start with '---' on the first line"]
    head, sep, body = text[4:].partition("\n---\n")
    if not sep:
        return {}, "", ["frontmatter is not closed with '---'"]
    fields, current = {}, None
    for line in head.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^( *)([A-Za-z0-9_-]+):(?: +(.*))?$", line)
        if not m:
            errors.append(f"unsupported frontmatter line: {line!r}")
            continue
        indent, key, raw = len(m.group(1)), m.group(2), m.group(3)
        if indent == 0:
            if raw is None:
                fields[key], current = {}, key
            else:
                fields[key], current = _scalar(raw), None
        elif current is None or indent != 2 or raw is None:
            errors.append(f"unsupported nesting: {line!r}")
        else:
            fields[current][key] = _scalar(raw)
    return fields, body, errors


def _scalar(raw):
    """Quoted -> str. Unquoted -> str too, but bare numbers/booleans are tagged so
    the metadata check can reject them (the spec wants string values)."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    if re.fullmatch(r"-?\d+(\.\d+)?|true|false|null|yes|no", raw, re.I):
        return ("bare", raw)
    if raw.startswith(("[", "{", "|", ">", "&", "*", "!")) or ": " in raw or raw.endswith(":"):
        return ("bare", raw)
    return raw


def check_frontmatter(text, dirname="kiss"):
    fields, body, errors = parse_frontmatter(text)
    if errors and not fields:
        return errors
    unknown = set(fields) - SPEC_KEYS
    if unknown:
        errors.append(f"fields outside the Agent Skills spec: {sorted(unknown)}")
    name, desc = fields.get("name"), fields.get("description")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"name must be 1-64 chars, lowercase a-z 0-9 and single hyphens: {name!r}")
    elif name != dirname:
        errors.append(f"name {name!r} must match the directory name {dirname!r}")
    if not isinstance(desc, str) or not desc.strip():
        errors.append("description is required and must be a plain string "
                      "(quote it if it contains ': ')")
    else:
        if len(desc) > 1024:
            errors.append(f"description is {len(desc)} chars, spec max is 1024")
        if len(desc) > HERMES_DESC_MAX:
            errors.append(f"description is {len(desc)} chars, Hermes max is {HERMES_DESC_MAX}")
        if not desc.endswith("."):
            errors.append("description should end with a period (Hermes house style)")
    if "compatibility" in fields and not (isinstance(fields["compatibility"], str)
                                          and 1 <= len(fields["compatibility"]) <= 500):
        errors.append("compatibility must be a string of 1-500 chars")
    meta = fields.get("metadata", {})
    if not isinstance(meta, dict) or any(not isinstance(v, str) for v in meta.values()):
        errors.append("metadata must be a map of string keys to quoted string values")
    if not body.strip():
        errors.append("SKILL.md body is empty")
    if text.count("\n") + 1 > SKILL_LINES_MAX:
        errors.append(f"SKILL.md is longer than {SKILL_LINES_MAX} lines")
    return errors


def check_layout():
    errors = []
    skill_md = SKILL_DIR / "SKILL.md"
    if not skill_md.is_file():
        return [f"missing {skill_md.relative_to(ROOT)}"]
    text = skill_md.read_text(encoding="utf-8")
    errors += check_frontmatter(text, SKILL_DIR.name)
    for ref in re.findall(r"\]\(((?!https?:|#)[^)]+)\)", text):
        if not (SKILL_DIR / ref).exists():
            errors.append(f"SKILL.md links to a missing file: {ref}")
    bible = SKILL_DIR / "references" / "bible.md"
    if bible.is_file():
        sources = bible.read_text(encoding="utf-8").partition("\n## Sources")[2]
        if len(re.findall(r"https?://\S+", sources)) < 10:
            errors.append("references/bible.md has no Sources list")
    else:
        errors.append("missing skills/kiss/references/bible.md")
    for f in ("README.md", "LICENSE", "CHANGELOG.md", "docs/compatibility.md", ".gitignore",
              ".github/workflows/validate.yml"):
        if not (ROOT / f).is_file():
            errors.append(f"missing {f}")
    gi = ROOT / ".gitignore"
    if gi.is_file() and ".dev/" not in gi.read_text().splitlines():
        errors.append(".gitignore must list .dev/")
    for p in SKILL_DIR.rglob("*"):
        if p.is_file() and re.search(r"/(home|opt/data|Users)/", p.read_text(encoding="utf-8")):
            errors.append(f"machine-local path in {p.relative_to(ROOT)}")
    return errors


def check_claude_plugin():
    errors = []
    try:
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    except (OSError, ValueError) as e:
        return [f"claude manifest unreadable: {e}"]
    if not plugin.get("name"):
        errors.append("plugin.json needs a name")
    if not (market.get("name") and market.get("owner", {}).get("name") and market.get("plugins")):
        errors.append("marketplace.json needs name, owner.name and plugins")
    for entry in market.get("plugins", []):
        if not (entry.get("name") and entry.get("source")):
            errors.append(f"marketplace entry needs name and source: {entry}")
        elif entry["name"] != plugin.get("name"):
            errors.append("marketplace entry name must equal plugin.json name")
        elif entry["source"] != "." and not entry["source"].startswith("./"):
            errors.append("relative source must start with './'")
    return errors


def main():
    errors = check_layout() + check_claude_plugin()
    for e in errors:
        print(f"FAIL: {e}")
    if not errors:
        desc = re.search(r'^description: "?(.*?)"?$', (SKILL_DIR / "SKILL.md").read_text(), re.M)
        lines = (SKILL_DIR / "SKILL.md").read_text().count("\n") + 1
        print(f"OK: skills/kiss valid (description {len(desc.group(1))} chars, SKILL.md {lines} lines)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
