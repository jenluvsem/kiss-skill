# kiss

One skill, three agents. It keeps design, code and process as simple as the job allows.

It works in Claude Code, OpenAI Codex CLI and Hermes Agent. All three read the same file: `skills/kiss/SKILL.md`.

## Why

Most scope creep starts with a reasonable question. Do we need another layer? Another flag? Another service? Nobody answers it, the layer ships, and a year later nobody knows why it exists.

The skill makes the agent answer first. It walks a short decision ladder (skip it, reuse it, use the platform, use a dependency you already have, write the least code, run it). Then it checks the result against 14 rules, a list of smells and a "never cut" list, so that simple never turns into sloppy.

The long version is `skills/kiss/references/bible.md`. Every quote in it was checked against the source page.

## Install

Pick the tool you use. Replace `OWNER` with the GitHub account that hosts this repo.

### Claude Code

As a plugin:

```
/plugin marketplace add OWNER/kiss-skill
/plugin install kiss@kiss-skill
```

Or as a personal skill, with no plugin:

```bash
git clone https://github.com/OWNER/kiss-skill
cp -r kiss-skill/skills/kiss ~/.claude/skills/kiss
```

The plugin form names the skill `/kiss:kiss`. The personal form names it `/kiss`.

### OpenAI Codex CLI

```bash
git clone https://github.com/OWNER/kiss-skill
mkdir -p ~/.agents/skills
cp -r kiss-skill/skills/kiss ~/.agents/skills/kiss
```

For one repository only, copy it to `.agents/skills/kiss` inside that repo. Restart Codex if the skill does not show up. Invoke it with `$kiss`, or run `/skills`.

### Hermes Agent

```bash
hermes skills install OWNER/kiss-skill/skills/kiss
```

Hermes scans the skill before it installs. Or add the repo as a source first with `hermes skills tap add OWNER/kiss-skill`.

Hermes can also read `~/.agents/skills`, so the Codex copy above can serve both. Add that folder to `skills.external_dirs` in `config.yaml`.

## Use

The agent loads the skill on its own when you design, choose between options, or review. You can also call it by name:

```
Use the kiss skill to review this plan before I start.
```

```
$kiss  should this be a new service or a function in the existing one?
```

A typical answer names what to cut, what to reuse, and one line about what was skipped.

## Layout

```
skills/kiss/SKILL.md              the skill (all three tools)
skills/kiss/references/bible.md   full text with sources
.claude-plugin/                   Claude Code plugin and marketplace manifests
docs/compatibility.md             format decisions, with official URLs
tests/validate_skill.py           stdlib-only validator
```

## Validate

```bash
python3 tests/validate_skill.py
python3 -m unittest discover -s tests
```

The same two commands run in GitHub Actions on every push.

## Sources and credits

The ideas belong to the people quoted in `skills/kiss/references/bible.md`: Kelly Johnson, Dijkstra, Hoare, Raymond, Fowler, Beck, Gall, Kernighan, Hickey, Brooks, Ousterhout, Metz, McKinley, Pike, Knuth and others. The bible lists the page for each.

Format references are in `docs/compatibility.md`.

## License

MIT. See `LICENSE`.
