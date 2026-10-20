# kiss

One skill. Three agents. Design, code and process stay as simple as the job allows.

Claude Code, OpenAI Codex CLI and Hermes Agent all read `skills/kiss/SKILL.md`. Same file.

## Why

Scope creep rarely arrives as a bad idea. It arrives as a layer. A flag. A service "for later". Nobody vetoes it. A year later the reason is gone.

So the agent has to answer first. Ladder: skip it, reuse it, platform, a dependency you already have, then the least new code, then run the thing. After that, 14 rules. A smell list. A "never cut" list, so simple doesn't turn into sloppy.

Long version: `skills/kiss/references/bible.md`. I checked the quotes on the source pages.

## Install

Pick the tool you actually use. Put your GitHub account where it says `OWNER`.

### Claude Code

Plugin:

```
/plugin marketplace add OWNER/kiss-skill
/plugin install kiss@kiss-skill
```

Personal skill, no plugin:

```bash
git clone https://github.com/OWNER/kiss-skill
cp -r kiss-skill/skills/kiss ~/.claude/skills/kiss
```

Plugin name: `/kiss:kiss`. Personal name: `/kiss`.

### OpenAI Codex CLI

```bash
git clone https://github.com/OWNER/kiss-skill
mkdir -p ~/.agents/skills
cp -r kiss-skill/skills/kiss ~/.agents/skills/kiss
```

Single repo? Copy into `.agents/skills/kiss` inside that repo. If `$kiss` is missing, restart Codex. Call it with `$kiss`. Or `/skills`.

### Hermes Agent

```bash
hermes skills install OWNER/kiss-skill/skills/kiss
```

It scans before install. You can also `hermes skills tap add OWNER/kiss-skill` and pull from there.

Hermes will read `~/.agents/skills` too, so the Codex copy can feed both. Point `skills.external_dirs` at that folder in `config.yaml`.

## Use

It loads itself when you design, pick an option, or review. You can also poke it:

```
Use the kiss skill to review this plan before I start.
```

```
$kiss  should this be a new service or a function in the existing one?
```

Expect a cut list, a reuse list, and one line about what got skipped.

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

Same pair in GitHub Actions, every push.

## Sources and credits

Names and pages: `skills/kiss/references/bible.md`. Kelly Johnson, Dijkstra, Hoare, Raymond, Fowler, Beck, Gall, Kernighan, Hickey, Brooks, Ousterhout, Metz, McKinley, Pike, Knuth. Others too.

Format notes: `docs/compatibility.md`.

## License

MIT. `LICENSE`.
