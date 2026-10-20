# Compatibility

There is one skill, `skills/kiss/SKILL.md`, and three tools load it. This page says what each tool wants, what we picked, and why. I read the official pages on 2026-10-20, and the URLs are below.

## Decision

Stick to the six frontmatter fields from the Agent Skills spec. Keep the description at 60 characters or less.

```yaml
---
name: kiss
description: "KISS: choose the simplest design, cut scope and layers."
license: MIT
metadata:
  version: "1.0.0"
---
```

Why this shape:

- Claude Code takes every spec field. Its docs say a skill that follows the spec "loads in Claude Code without changes". Claude.ai uploads and the Skills API are stricter and fail on any field outside the six, so a top-level `version` or `platforms` would break that path.
- Codex needs `name` and `description`, and it builds on the same standard.
- Hermes needs the same two. Its authoring rules cap the description at 60 characters, since the skill index cuts it at 57 plus an ellipsis. The Hermes-only fields (`platforms`, `metadata.hermes`) are optional, so they're out.
- The spec wants `metadata` values to be strings. That's why the version is quoted.

The price: 60 characters is thin for matching. The trigger words (KISS, simplest, scope, layers) come first, and the body has a "When to use" list, but the model only reads that after the skill has loaded. If triggering turns out weak, lengthen the description. The spec allows 1024. The validator has a constant for the Hermes limit, so it's a one-line change there too.

Left out on purpose:

| Skipped | Reason |
| :- | :- |
| `agents/openai.yaml` | Optional Codex UI and invocation policy. The defaults are fine. |
| Codex plugin (`plugin.json` at the root, or `.codex-plugin/`) | Plugins are for distribution through the OpenAI directory. A skills folder is enough for one skill. |
| `metadata.hermes` (tags, related skills) | Optional. A non-string value there would also break the spec's string-only `metadata`. |
| `when_to_use`, `disable-model-invocation` and other Claude-only fields | The upload path rejects them. |
| One copy of the skill per tool | Every tool reads the same directory layout, so a second copy would only drift. |

## Per tool

### Agent Skills standard

- Directory with `SKILL.md`; optional `scripts/`, `references/`, `assets/`.
- Required: `name` (1-64 chars, lowercase letters, digits, single hyphens, must match the directory name) and `description` (1-1024 chars).
- Optional: `license`, `compatibility` (up to 500 chars), `metadata` (string to string map), `allowed-tools` (experimental).
- Keep `SKILL.md` under 500 lines and file references one level deep.
- Source: https://agentskills.io/specification

### Claude Code

- Personal: `~/.claude/skills/<name>/SKILL.md`. Project: `.claude/skills/<name>/SKILL.md`. Plugin: `<plugin>/skills/<name>/SKILL.md`, invoked as `/plugin-name:skill-name`.
- All frontmatter fields are optional; `description` is recommended and is cut at 1,536 characters together with `when_to_use`.
- The frontmatter is read only when `---` is the first line of the file.
- Source: https://code.claude.com/docs/en/skills
- Plugin manifest: `.claude-plugin/plugin.json`, only `name` is required, other plugin files sit at the plugin root. Source: https://code.claude.com/docs/en/plugins/manifest-reference
- Marketplace: `.claude-plugin/marketplace.json` needs `name`, `owner` and `plugins`; each entry needs `name` and `source`. A relative `source` starts with `./`. Users add it with `/plugin marketplace add <owner>/<repo>`. Source: https://code.claude.com/docs/en/plugin-marketplaces and https://code.claude.com/docs/en/plugins/marketplace-reference
- This repo is both marketplace and plugin: the entry uses `"source": "./"` and the default `skills/` folder is scanned.

### OpenAI Codex CLI

- A skill is a folder with `SKILL.md`; `name` and `description` are required. Optional `agents/openai.yaml`.
- Locations: `$CWD/.agents/skills`, parents up to the repository root, `$HOME/.agents/skills`, `/etc/codex/skills`, plus bundled system skills. Symlinked skill folders are followed.
- The list of skills at startup uses at most 2% of the context window, and descriptions are shortened first when it overflows. The docs advise putting the key use case and trigger words first.
- Invoke with `$skill-name` or `/skills`. Changes are picked up automatically; restart if not.
- `$skill-installer` can fetch a skill from a GitHub path. Its own SKILL.md says it installs into `$CODEX_HOME/skills` (default `~/.codex/skills`), which differs from the documented `~/.agents/skills`. We did not test which one a current Codex reads, so the README uses the documented path.
- Sources: https://developers.openai.com/codex/skills (redirects to https://learn.chatgpt.com/docs/build-skills) and https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md

### Hermes Agent

- Skills live in `~/.hermes/skills/`. Project skills are read from `.hermes/skills/` and `.agents/skills/`, but only after `hermes skills trust`. `~/.agents/skills` can be added through `skills.external_dirs`.
- Frontmatter: `name` and `description` required. Optional `version`, `platforms`, `metadata.hermes.*`. The in-repo authoring rule is a description of 60 characters or less, ending in a period; a description with a colon must be quoted.
- Install from GitHub: `hermes skills install <owner>/<repo>/<path-to-skill-dir>`, or `hermes skills tap add <owner>/<repo>` first. Checked with `hermes skills install --help` and `hermes skills tap --help`. Installs run a security scan.
- Sources: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills and https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills

## What was run

| Tool | Check | Result |
| :- | :- | :- |
| Claude Code 2.1.304 | `claude plugin validate .` | passed |
| Claude Code 2.1.304 | `claude plugin marketplace add`, `claude plugin install kiss@kiss-skill`, `claude plugin details kiss` | installed; inventory shows `Skills (1) kiss` |
| Hermes | skill copied into a throwaway `HERMES_HOME`, `hermes skills list`; Hermes' own `_validate_frontmatter` | listed as enabled; validator accepted it |
| Codex CLI | not run | no Codex install or login on the build machine; layout follows the official page |
| `hermes skills install OWNER/kiss-skill/skills/kiss` | not run | the repo is not on GitHub yet |
