# KISS

The name: Keep It Simple, Stupid. Kelly Johnson's line, from Lockheed's Skunk Works (U-2, SR-71). He handed his engineers a few tools and said a mechanic in the field fixes this jet with these, nothing else. "Stupid" was about that toolbox. Not the mechanic. Story's on [Wikipedia](https://en.wikipedia.org/wiki/KISS_principle).

This repo is that rule as a skill. Claude Code, OpenAI Codex CLI, Hermes Agent. Before the agent builds a feature, a layer, a config file or a dependency, it asks: who needs this today? Nobody? Then you get the smallest change that fixes today's problem. Plus the point at which the bigger version starts paying off.

Same file for all three: `skills/kiss/SKILL.md`. Id is lowercase `kiss`; the Agent Skills spec forbids capitals.

## When it kicks in

On its own when you ask for a plugin system, config file, abstraction, layer or dependency. When you weigh two designs. When you want a plan or diff reviewed. Or call it by name, see [Use](#use).

## What it makes the agent do

Ladder. Top down, stop at the first rung that covers the whole job:

1. Skip it. One line on what got skipped.
2. Reuse what the project has.
3. Stdlib or platform.
4. A dependency already installed.
5. Least new code that works.
6. Run it on real input. Read the output.

Then 14 rules, each ending in a yes/no check. Two of them: "Can you point at someone who needs it today?" "Would the shared function need a flag per caller?"

Then 8 smells. Interface with one implementation. Wrapper that just forwards a call. "We might need it for...". Five more in `SKILL.md`.

Never cut: validation at trust boundaries, error handling that guards data, security, accessibility, anything you explicitly asked for.

You get back a plan, why, when to build more, what was skipped. Still want the big version? The agent names the cost, then builds it.

## A real run

Fixture: `report.py`, 16 lines, prints a CSV. Prompt:

> Add a plugin system with YAML config to this script so it can support more output formats later.

Claude Code, Sonnet, no skill: format registry, YAML config, plugins loaded via `importlib`. PyYAML added.

Same, with KISS: a `FORMATS = {"text": text}` dict and a `--format` flag. Nothing added. Plugins wait until someone outside the repo must add formats without editing the script. Quote from that run: "The script is 15 lines and has one output format. No one has asked for a second format, so a plugin loader and a config file would be bigger than the script and have nothing to configure."

Tested in all three, same fixture:

- Claude Code 2.1.304 on Sonnet found the skill and loaded it in 6 of 6 runs. No plugins, no YAML.
- Hermes Agent 0.22.2 on Sonnet: 5 of 5 runs. No plugins, no YAML, about 10 lines changed.
- Codex CLI 0.163.0 on MiniMax M3.1 Flash (free, through OpenRouter): one run. It dropped the plugins but kept YAML and a registry.

Codex was weakest. One run, small free model. A floor, not a verdict.

## Install

### Claude Code

Plugin:

```
/plugin marketplace add jenluvsem/kiss-skill
/plugin install kiss@kiss-skill
```

Personal skill:

```bash
git clone https://github.com/jenluvsem/kiss-skill
cp -r kiss-skill/skills/kiss ~/.claude/skills/kiss
```

`/kiss:kiss` for the plugin, `/kiss` for the personal one.

### OpenAI Codex CLI

```bash
git clone https://github.com/jenluvsem/kiss-skill
mkdir -p ~/.agents/skills
cp -r kiss-skill/skills/kiss ~/.agents/skills/kiss
```

One repo only? `.agents/skills/kiss` inside it. No `$kiss`? Restart Codex, or use `/skills`.

### Hermes Agent

```bash
hermes skills install jenluvsem/kiss-skill/skills/kiss
```

Scanned before install. Tap also works: `hermes skills tap add jenluvsem/kiss-skill`. Got `~/.agents/skills` in `skills.external_dirs`? Then Hermes reads the Codex copy. One install, two agents.

## Use

Mostly automatic. By hand:

```
Use the kiss skill to review this plan before I start.
```

```
$kiss should this be a new service or a function in the existing one?
```

## Repo

```
skills/kiss/SKILL.md              the skill, ~110 lines, all three tools
skills/kiss/references/bible.md   long form: 18 rules, sourced
.claude-plugin/                   Claude Code plugin + marketplace
docs/compatibility.md             per-tool format notes, official links
tests/validate_skill.py           stdlib validator
```

`bible.md` only gets opened when a rule needs its source. I checked each quote on the original page.

## Validate

```bash
python3 tests/validate_skill.py
python3 -m unittest discover -s tests
```

CI runs both, every push.

## Sources

Kelly Johnson, Dijkstra, Hoare, Eric Raymond, Martin Fowler, Kent Beck, John Gall, Brian Kernighan, Rich Hickey, Fred Brooks, Google SRE book, John Ousterhout, Sandi Metz, Dan McKinley, Rob Pike, Donald Knuth, PEP 20, Richard Gabriel. Links: `skills/kiss/references/bible.md`.

## License

MIT. `LICENSE`.
