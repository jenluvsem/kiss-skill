---
name: kiss
description: "KISS: choose the simplest design, cut scope and layers."
license: MIT
metadata:
  version: "1.0.0"
---

# KISS

Complexity costs time and attention, and whoever wants to add some has to say why. That's the whole idea. What follows is the working version; the long one, with sources, sits in [references/bible.md](references/bible.md) and you only need it when a rule needs defending or a quote needs citing.

Simple isn't a word for sloppy. If the simple version gives the wrong answer, it's still wrong.

## When to use

- You're about to design something new: a system, a skill, a script, a service, a process.
- You have to choose between two approaches, or between "write it" and "use what's there".
- You're reviewing a change, a plan or someone's proposal.
- Something keeps growing. Another layer, another flag, another tool "just in case".

Not a license to drop validation, security or error handling. See "Never cut".

## Decision ladder

Walk down it and stop at the first rung that solves the whole problem. Half a solution doesn't count.

1. Need it at all? Often not. Skip it, and write one line about what you skipped so nobody assumes you forgot. Done when every piece you keep has a need you could name out loud.
2. Got it already? Our helpers, our skills, our services. Use it the way the code next to it does, even if you'd have done it differently.
3. Can the standard library or the platform do it? Then stop here.
4. Does a dependency we already have do it? Use that. A new package for five lines, no.
5. Now, and only now, write code. As little as you can get away with. Done when nothing can come out without somebody missing it.
6. Run it on real input and read the real output. Code that never ran isn't finished, however good it looks. Non-trivial logic gets a test or a self-check, and one is plenty.

## Rules

Every rule ends in a check you can answer with yes or no.

1. Name the need (YAGNI). Before you add a feature, option, layer, dependency or file, write down who needs it. Check: can you point at someone who needs it today?
2. Default to no. A new layer, flag or service stays out until somebody names the concrete need. "It won't scale" is a feeling, so show it. Check: is there a demonstration, or only a worry?
3. Start small, keep it working (Gall's law). Version one runs end to end even if it covers a sliver of the job, and it never stops running while you grow it. Check: does the current version run right now?
4. Clear beats clever. A line you have to decode loses to three boring lines. Check: could a colleague read it cold?
5. Simple isn't easy (Hickey). Easy means familiar. Simple means one concern per piece, nothing braided together. Check: does the tool you picked untangle the system, or just save you an afternoon?
6. Remove the accidental kind (Brooks). Essential complexity lives in the problem and stays. Accidental complexity comes from our own tools, layers and habits, and that's where the cutting happens. Check: for each hard part, is it in the problem or in our choices?
7. Small interfaces, real work behind them. A wrapper has to save the caller real thinking. One that only renames another function's arguments adds a layer and hides nothing. Check: does it do anything besides forward the call?
8. Copy twice, abstract on the third time (Metz), and only if all three really are the same thing. Duplication costs less than the wrong abstraction. Check: would the shared function need a flag per caller?
9. Choose boring technology (McKinley). A new, unproven tool burns one of your few innovation tokens, so spend them on what you're actually building. Check: what exactly does the new tool buy us?
10. Put the smarts in the data. A little lookup table beats a stack of nested ifs. Check: could a table replace this branching?
11. Measure before you optimize. Speed work is complexity too, so wait for a profiler or a real complaint. Check: where's the measurement?
12. No surprises. A tool does what its name says and logs what it did. Check: could somebody debug it at 2am without reverse engineering it?
13. Delete things. Try to remove something before you hand over. Dead code and unused options go. Check: what did you try to delete, and why did it have to stay?
14. Trim the process as well. Handoffs, documents nobody opens, extra tools, meetings. If a step can vanish and nothing breaks, drop it. Check: what breaks without it?

## How to apply it

Design: run the ladder before you sketch anything, and write down what you left out.

Implement: keep the structure the codebase already has. Fix a bug once, in the shared function, not in each caller. Cutting a corner on purpose? Say so in a comment: `shortcut: <the limit>, <when to upgrade>`.

Review: scan for the smells below. For each hit, say what to cut or ask for the named need. Don't rewrite the whole change.

Infrastructure: every extra server, container or managed service can page somebody at 3am, so look at what's already running first. Platform config beats home-made glue.

Skills, prompts, agents: a line that doesn't change what the model does is dead weight in every call, so cut it. One solid skill per topic, not five thin ones. A single call or a twenty-line script doesn't need a multi-agent pipeline.

Docs: say it and stop. Tables to compare, prose to explain why.

## Smells

Not proof, just a reason to look twice.

- Options, flags or config that nobody has asked to change.
- An interface or base class with exactly one implementation.
- A wrapper whose only job is to call one other function.
- "We might need it for..." in a design discussion.
- A new tool picked because it's easier, while the old one works.
- A shared helper full of `if` branches, one per caller.
- Docs explaining how the design works because the code can't show it.
- A cleanup "while I'm in there" that has nothing to do with the task. Flag it, don't do it.

## Never cut

"As simple as possible, but not simpler." A simplification that loses a real requirement is a bug, not KISS. These stay, however tempting the cut:

- validation at trust boundaries (user input, external APIs, anything from the network)
- error handling that protects data from loss or corruption
- security and access control
- accessibility
- anything the person asking explicitly wanted

YAGNI also depends on code that's easy to change later. Tests and refactoring are what make "build it later" safe, so keep them.

## Limits

- The ladder is a default. If the person asks for the bigger thing, build it and say what it costs.
- The ladder and the "How to apply it" advice are house habits, not citations. The bible marks what has a source.
- This skill can't measure anything. Rule 11 needs real numbers from your own tools.

## Checklist

Before you hand it over:

- [ ] Every piece has a named need. Nothing is there just in case.
- [ ] Nothing we already had (our code, the standard library, the platform) got rewritten.
- [ ] No new dependency that a few lines could have replaced.
- [ ] Someone else could follow it without you explaining.
- [ ] You tried to delete something and couldn't without losing a real feature.
- [ ] Validation, security and error handling are untouched.
- [ ] You ran it for real and saw the output.
- [ ] One line says what you skipped or didn't check.
