---
name: kiss
description: "KISS: use before adding a feature, plugin or layer. Also before a plugin system, config file, abstraction or dependency. Also when you choose between designs or review a plan or diff. Ask what is needed now, push back on speculative extras, propose the smallest change that works."
license: MIT
metadata:
  version: "1.0.1"
---

# KISS

Complexity costs time. It costs attention. Want to add some? Say why. That's the whole idea. This is the short working copy. The long one, with sources, is [references/bible.md](references/bible.md). Open it when a rule needs defending or a quote needs a page.

Simple isn't a word for sloppy. A simple version that gives the wrong answer is still wrong.

## When to use

- You're about to design something new: a system, a skill, a script, a service, a process.
- You have to choose between two approaches, or between "write it" and "use what's there".
- You're reviewing a change, a plan or someone's proposal.
- Something keeps growing. Another layer, another flag, another tool "just in case".

Not a license to drop validation, security or error handling. See "Never cut".

## Decision ladder

Walk down it and stop at the first rung that solves the whole problem. Half a solution doesn't count.

1. Need it at all? Often not. Skip it. Write one line so nobody thinks you forgot. Stop when you can name, out loud, why each leftover piece is there.
2. Got it already? Helpers we already have. Skills. Services. Use it the way neighbouring code does. Even if you'd have written it differently.
3. Stdlib? Platform? Then stop.
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
6. Remove the accidental kind (Brooks). Essential complexity lives in the problem and stays. Accidental complexity is ours: tools, layers, habits. Cut there. Check: is this hard bit in the problem, or did we put it there?
7. Small interfaces, real work behind them. A wrapper has to save the caller real thinking. One that only renames another function's arguments adds a layer and hides nothing. Check: does it do anything besides forward the call?
8. Copy twice, abstract on the third time (Metz), and only if all three really are the same thing. Duplication costs less than the wrong abstraction. Check: would the shared function need a flag per caller?
9. Choose boring technology (McKinley). A new, unproven tool burns one of your few innovation tokens, so spend them on what you're actually building. Check: what does the new tool actually buy?
10. Put the smarts in the data. A lookup table beats nested ifs. Check: could a table replace this branching?
11. Measure before you optimize. Speed work is complexity too, so wait for a profiler or a real complaint. Check: where's the measurement?
12. No surprises. Name matches behaviour. Log what happened. Check: could somebody debug it at 2am without reverse engineering it?
13. Delete things. Try to remove something before you hand over. Dead code and unused options go. Check: what did you try to delete? Why did it stay?
14. Trim the process as well. Handoffs. Docs nobody opens. Extra tools. Meetings. If dropping a step breaks nothing, drop it. Check: what breaks without it?

## How to apply it

Design: run the ladder first. Write down what you left out.

Implement: keep the structure that's already there. Fix the bug in the shared function. Not in every caller. Cutting a corner on purpose? Say so in a comment: `shortcut: <the limit>, <when to upgrade>`.

Review: scan for the smells below. For each hit, say what to cut or ask for the named need. Don't rewrite the whole diff.

Simplify existing code: before you list a module as a cut, read it and grep its callers. Names lie: a file called `voice_memory` can be the main conversation path. Cut a part only together with everything that depends on it, including deployed firmware, devices and other clients that speak its protocol. Until that counterpart changes, it stays, even if it looks like clutter. A cut that stops the alarm from switching off is a bug, not KISS. Check: can you name every caller and consumer you read?

Infrastructure: extra servers, containers, managed services page people at 3am. Look at what's already running. Platform config beats home-made glue.

Skills, prompts, agents: if a line doesn't change what the model does, it's dead weight. Cut it. One solid skill per topic. Not five thin ones. Don't spin a multi-agent pipeline for one call or a twenty-line script.

Docs: say it and stop. Tables to compare, prose to explain why.

## Smells

Not proof. Just a reason to look twice.

- Options, flags or config that nobody has asked to change.
- An interface or base class that has exactly one implementation.
- A wrapper that only calls one other function.
- "We might need it for..." in a design discussion.
- Picking a new tool because it's easier, while the old one still works.
- A shared helper full of `if` branches, one per caller.
- Docs explaining how the design works because the code can't show it.
- Cleanup "while I'm in there" that has nothing to do with the task. Flag it, don't do it.

## Never cut

"As simple as possible, but not simpler." Lose a real requirement and it isn't KISS. It's a bug. These stay, however tempting the cut:

- validation at trust boundaries (user input, external APIs, anything from the network)
- error handling that protects data from loss or corruption
- security and access control
- accessibility
- anything the person asking explicitly wanted

YAGNI needs code that's cheap to change later. Tests and refactoring make "build it later" safe. Keep them.

## Limits

- The ladder is a default. Asked for the bigger thing? Say what it costs and what the small version would be. They still want the big one? Build it.
- The ladder and the "How to apply it" bits are house habits. Not citations. The bible marks what has a source.
- This skill can't measure anything. Rule 11 needs real numbers from your own tools.

## Checklist

Before you hand it over:

- [ ] Every piece has a named need. Nothing is there just in case.
- [ ] Nothing we already had (our code, the standard library, the platform) got rewritten.
- [ ] No new dependency that a few lines could have replaced.
- [ ] Someone else could follow it without you explaining.
- [ ] Tried to delete something. Couldn't, without losing a real feature.
- [ ] Validation, security, error handling: left alone.
- [ ] Ran it. Saw the output.
- [ ] One line on what you skipped or didn't check.
