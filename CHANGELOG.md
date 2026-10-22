# Changelog

I dumped notable changes here so I wouldn't have to dig through git log later. The headings copy [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Numbers follow [Semantic Versioning](https://semver.org/), because that's what people already expect.

## [1.0.1] - 2026-10-22

### Added
- Rule for simplifying existing code: read the module and grep its callers before cutting it, and keep it while firmware, devices or other clients still depend on it.

### Changed
- README rewritten. Says what KISS stands for, what the agent actually does, and shows a real test run.
- Plugin descriptions say what the skill does instead of a slogan.

## [1.0.0] - 2026-10-20

### Added
- `skills/kiss/SKILL.md`. One skill. Claude Code, OpenAI Codex CLI, Hermes Agent.
- `skills/kiss/references/bible.md`. Long version. Every quote has a page.
- `.claude-plugin/` holds the Claude Code plugin and marketplace files.
- `tests/validate_skill.py` is a stdlib validator. Tests sit in the same folder.
- GitHub Actions just runs those two commands on push. Nothing fancy.
