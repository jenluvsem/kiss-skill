# Compatibility

I sat down with the three official skill pages on 2026-10-20 and wrote this so I wouldn't have to do it again. One file, `skills/kiss/SKILL.md`. Claude Code, Codex CLI and Hermes all load it. The links are in the paragraphs.

## Decision

Six frontmatter fields, nothing else. That's the Agent Skills spec. Description stays under 60 characters because Hermes cuts it.

```yaml
---
name: kiss
description: "KISS: choose the simplest design, cut scope and layers."
license: MIT
metadata:
  version: "1.0.0"
---
```

Claude Code is the easy one. It takes every spec field. Their docs even say a spec-following skill "loads in Claude Code without changes". The pain is Claude.ai uploads and the Skills API: anything outside those six fields fails. So no top-level `version`. No `platforms`.

Codex wants `name` and `description`. Same standard.

Hermes wants those two as well. Their authoring notes cap the description at 60 characters. The skill index shows 57 plus an ellipsis, which is why. `platforms` and `metadata.hermes` exist but they're optional and Hermes-only, so I left them off. Spec also wants `metadata` values as strings, which is why `"1.0.0"` is quoted.

Sixty characters is a lousy trigger. I stuffed KISS, simplest, scope, layers at the front and hoped. The "When to use" list is in the body, which the model only reads after the skill already loaded. If matching turns out weak, bump the description. Spec allows 1024. The validator has the Hermes cap as a constant.

Things I didn't add:

| Skipped | Why |
| :- | :- |
| `agents/openai.yaml` | Codex UI extras. Defaults are fine. |
| Codex plugin (`plugin.json` at the root, or `.codex-plugin/`) | That's the OpenAI directory path. We have one skill. A folder is enough. |
| `metadata.hermes` (tags, related skills) | Optional. Also, a non-string value would break the spec. |
| `when_to_use`, `disable-model-invocation`, other Claude-only keys | Upload path rejects them. |
| A second copy of the skill per tool | Same layout everywhere. Two copies would drift. |

## Per tool

### Agent Skills standard

https://agentskills.io/specification

Directory. `SKILL.md` inside it. You can add `scripts/`, `references/`, `assets/` if you want. We only needed `references/`.

`name`: 1-64 chars, lowercase, digits, single hyphens, same as the folder. `description`: up to 1024 chars.

Optional bits I didn't really use: `license` (we set MIT anyway), `compatibility` (500 char max), `metadata` as strings, `allowed-tools` which they still call experimental.

They also say keep `SKILL.md` under 500 lines and don't nest file refs more than one level. Ours is around 110 lines, so whatever.

### Claude Code

https://code.claude.com/docs/en/skills

Drop it in `~/.claude/skills/<name>/SKILL.md` for yourself. Project copy: `.claude/skills/<name>/SKILL.md`. Plugin copy: `<plugin>/skills/<name>/SKILL.md`, and then you type `/plugin-name:skill-name`.

Weirdly, none of the frontmatter fields are required in Claude Code. They still want a `description`. Stick `when_to_use` next to it and the pair gets chopped at 1,536 characters.

Don't forget: `---` has to be line 1. I have seen files where it wasn't, and the frontmatter just vanished.

Plugin manifest: `.claude-plugin/plugin.json`. `name` is the only required key. Other plugin files live at the plugin root. See https://code.claude.com/docs/en/plugins/manifest-reference.

Marketplace: `.claude-plugin/marketplace.json`. Needs `name`, `owner`, `plugins`. Each plugin row needs `name` and `source`. Relative `source` starts with `./`. People add it with `/plugin marketplace add <owner>/<repo>`. I used https://code.claude.com/docs/en/plugin-marketplaces and https://code.claude.com/docs/en/plugins/marketplace-reference.

This repo is both. `"source": "./"`. The default `skills/` folder is what gets scanned.

### OpenAI Codex CLI

https://developers.openai.com/codex/skills (it bounced me to https://learn.chatgpt.com/docs/build-skills)

Folder plus `SKILL.md`. `name` and `description` required. There's an `agents/openai.yaml` we didn't bother with.

Search order, as documented: `$CWD/.agents/skills`, then parents up to the repo root, then `$HOME/.agents/skills`, then `/etc/codex/skills`, then bundled system skills. Symlinks are followed.

They cap the startup skill list at 2% of the context window. Overflow? Descriptions get shortened first. That's another reason the trigger words sit at the front of ours.

Type `$skill-name` or `/skills`. Usually picks up edits. Restart if it doesn't.

`$skill-installer` can clone from GitHub. Its own SKILL.md (https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md) says the install dir is `$CODEX_HOME/skills`, default `~/.codex/skills`. The docs say `~/.agents/skills`. I didn't have a logged-in Codex on this machine, so the README follows the docs.

### Hermes Agent

https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills

Home dir: `~/.hermes/skills/`. Project skills from `.hermes/skills/` and `.agents/skills/`, but only after `hermes skills trust`. You can point `skills.external_dirs` at `~/.agents/skills` and share the Codex copy.

Required: `name`, `description`. Optional: `version`, `platforms`, `metadata.hermes.*`. The in-repo authoring notes want ≤60 characters, period at the end. Colon in the text? Quote the whole string.

Install from GitHub: `hermes skills install <owner>/<repo>/<path-to-skill-dir>`. Or tap first: `hermes skills tap add <owner>/<repo>`. I actually ran `--help` on both. Installs go through a security scan.

## What was run

| Tool | Check | Result |
| :- | :- | :- |
| Claude Code 2.1.304 | `claude plugin validate .` | passed |
| Claude Code 2.1.304 | `claude plugin marketplace add`, `claude plugin install kiss@kiss-skill`, `claude plugin details kiss` | installed; inventory shows `Skills (1) kiss` |
| Hermes | skill copied into a throwaway `HERMES_HOME`, `hermes skills list`; Hermes' own `_validate_frontmatter` | listed as enabled; validator accepted it |
| Codex CLI | not run | no Codex install or login on the build machine; layout follows the official page |
| `hermes skills install OWNER/kiss-skill/skills/kiss` | not run | the repo is not on GitHub yet |
