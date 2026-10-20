# KISS: our simplicity bible

We wrote this down because we kept having the same argument. Somebody wants to add a layer, a flag or a new service, somebody else asks "do we actually need that?", and twenty minutes later nobody remembers why it mattered. This file is the long answer. It applies to code, skills, servers and scripts, and to the way we organise work in general. If you remember one thing, make it this: complexity costs time and attention, and whoever wants to add some has to say why. Simple isn't a polite word for sloppy, though. If the simple version gives the wrong answer it's still wrong, and we'll take a slightly bigger thing that works over that every time.

Every rule says where it came from. I checked each quote against the original page in October 2026, so if a quote appears below, you'll find those words at the link in the sources list. The parts marked as house rules are ours. They aren't backed by a source, they're just how we like to work.

## When to use it

- You're about to design something new: a system, a skill, a plugin, a script, a service, a process.
- You have to pick between two approaches, two tools, or "write it" versus "use what's there".
- You're reviewing a change, a plan or someone's proposal.
- Something keeps growing. Another layer, another flag, another tool "just in case".

Don't use it as an excuse to drop validation, security or error handling. The section on where KISS stops covers that.

## Where the idea comes from

The phrase "keep it simple, stupid" is usually credited to Kelly Johnson, lead engineer at Lockheed's Skunk Works, the shop behind the U-2 and SR-71. The story Wikipedia tells is a good one. Johnson handed his design engineers a handful of tools and told them the jet had to be repairable by an average mechanic in the field, under combat conditions, with only those tools. So the "stupid" was never about the people. It's about the gap between how things break and what you'll have on hand when they do.

Software people got there on their own. Dijkstra wrote in 1975 that "simplicity is prerequisite for reliability" (EWD498). Tony Hoare put it as a choice between two kinds of design: one "so simple that there are obviously no deficiencies", the other "so complicated that there are no obvious deficiencies". The Unix tradition, as Eric Raymond wrote it down, says "design for simplicity; add complexity only where you must". The Agile Manifesto calls simplicity "the art of maximizing the amount of work not done" and says it's essential.

Older still is Occam's razor, usually given as "entities must not be multiplied beyond necessity". And Saint-Exupéry's line about design gets quoted in every engineering talk for a reason: perfection comes not when there's nothing left to add, but when there's nothing left to take away.

## The rules

### 1. Don't build it until someone needs it

This is YAGNI, "you aren't gonna need it". Martin Fowler's essay is the best explanation of why it pays off. A feature you build on a hunch can go wrong in a few ways. It might be the wrong feature, and then you paid the cost of building it for nothing. It might be the right one built wrong, and you pay the cost of repair. Even if you guessed perfectly, you still pay two costs. There's the cost of delay, because the work you actually needed waited. And there's the cost of carry: the extra code makes everything else harder to change and debug, every single day, until it finally gets used.

That last one is the cost people forget. A good guess is still expensive.

### 2. Add complexity only where you must

Raymond's Rule of Simplicity, and its sibling the Rule of Parsimony: "Write a big program only when it is clear by demonstration that nothing else will do." Note the "by demonstration" part. A feeling that the small version won't scale doesn't count. Show it.

In practice our default answer to a new layer, option or service is no. It changes to yes when someone can name the concrete need.

### 3. Start with something small that works, then grow it

John Gall's law, from *Systemantics*: "A complex system that works is invariably found to have evolved from a simple system that worked." The other half is harsher: "A complex system designed from scratch never works and cannot be patched up to make it work."

We take that literally. Version one of anything we build has to run end to end, even if all it does is a sliver of the real job, and we grow it from there without ever letting it stop working.

### 4. Simple is what makes it reliable

See Dijkstra and Hoare above. Nobody's claiming simple code is prettier. What matters is that you can see the bugs in it. Once a design no longer fits in one person's head the bugs don't leave, they just pile up where nobody looks.

### 5. Be clear, not clever

Raymond again: "Clarity is better than cleverness." Brian Kernighan explained why, decades ago, in *The Elements of Programming Style*: "Everyone knows that debugging is twice as hard as writing a program in the first place. So if you're as clever as you can be when you write it, how will you ever debug it?"

A one-liner you have to decode loses to three boring lines anyone can read, even though it's shorter.

### 6. Simple isn't the same as easy

This one comes from Rich Hickey's talk "Simple Made Easy". The InfoQ summary of it reads: "Complect" means to interleave, to entwine, to braid. Simple means things aren't braided together, one concern per piece. Easy only means familiar or close at hand. The trap is grabbing the easy thing, a framework you already know or a library that's one import away, and ending up with a system where everything is tangled with everything else.

So next time someone says "it's easier to just use X", ask whether X gives us a simpler system or just a shorter afternoon.

### 7. Know which complexity is yours to remove

Fred Brooks, in "No Silver Bullet", split complexity into essential and accidental. Essential complexity is in the problem itself. A tax calculation is complicated because tax law is. Accidental complexity is what we add on top with our tools, layers and habits. You can't remove the first kind, and trying to only hides it somewhere worse. The second kind is where most of our cutting should happen.

The Google SRE book uses the same split in its chapter on simplicity. Its example: a web server has the essential complexity of serving pages quickly, but write it in Java and you may add accidental complexity fighting the garbage collector. The book tells SRE teams to push back when accidental complexity is introduced into the systems they're responsible for. We agree.

### 8. Small interfaces, real work behind them

John Ousterhout's *A Philosophy of Software Design* argues for "deep" modules: a simple interface that hides a lot of functionality. The bad kind is a shallow module whose interface is about as complicated as what it does, so it hides nothing and only adds a layer.

For us this means: don't add a wrapper unless it saves the caller real thinking. A function that renames another function's arguments is a shallow module.

Ousterhout's distinction between tactical and strategic programming fits here too. Gergely Orosz's review sums it up as knowing whether you're putting out a fire or building for the long term. Both are fine. Pretending a fire fix is architecture is not.

### 9. Prefer duplication over the wrong abstraction

Sandi Metz: "duplication is far cheaper than the wrong abstraction". Her blog post about it describes how it goes wrong. Someone pulls two similar bits of code into one shared function. The next requirement doesn't quite fit, so a parameter gets added, then a conditional, then another, until the abstraction is harder to understand than the copies ever were.

Our rule: copy it twice, abstract on the third time, and only if the three cases really are the same thing.

### 10. Choose boring technology

Dan McKinley's "Choose Boring Technology" gives each company about three "innovation tokens". Every unproven database, language or service you adopt spends one. Spend them where they make a real difference to what you're building, not on the plumbing.

The SRE book says something similar in a section called "The Virtue of Boring": boring is a positive attribute in software. We want programs that stick to the script and do the same thing every time.

### 11. Put the smarts in the data

Raymond's Rule of Representation: "Fold knowledge into data so program logic can be stupid and robust." Rob Pike's Rule 5 is the same idea from another angle: "Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident."

In our experience a little lookup table beats a pile of nested ifs almost every time, mostly because the next person can actually read it.

### 12. Measure before you optimize

Pike's Rule 3: "Fancy algorithms are slow when n is small, and n is usually small." His Rule 2 is short: measure, and don't tune for speed until you have. Raymond: "Prototype before polishing. Get it working before you optimize it." And Knuth's line, which everyone half-remembers, really is on record as "premature optimization is the root of all evil".

Optimization is complexity too, and we only pay for it once a profiler or an actual user complaint tells us to.

### 13. No surprises, nothing hidden

Raymond's Rule of Least Surprise: "In interface design, always do the least surprising thing." And his Rule of Transparency: "Design for visibility to make inspection and debugging easier."

A tool that does what its name says and logs what it did is simpler to live with than a smarter tool that you have to reverse engineer at 2am.

### 14. Delete things

Saint-Exupéry, again. The SRE book has a section titled "The 'Negative Lines of Code' Metric", and it recommends routinely removing dead code and building bloat detection into testing. A PR that deletes a couple hundred lines and breaks nothing is about the nicest thing you can send us.

### 15. Do less work in the process too

The Agile principle was never only about code. It applies just as well to handoffs, to documents nobody opens, to the number of tools a task passes through, and to meetings. If a step can disappear without anything breaking, it probably should.

### 16. Beck's four rules for code

When Kent Beck developed Extreme Programming he gave four rules of simple design. Fowler writes them as: passes the tests, reveals intention, no duplication, fewest elements, and notes that they're in priority order. Working beats readable, readable beats small, and "fewest elements" only decides between options that already pass the first three. Fowler adds that the last rule means anything that doesn't serve the first three should go. Rule 9 above is our footnote to "no duplication".

### 17. The Python version

PEP 20, the Zen of Python, has a few lines we like: "Simple is better than complex. Complex is better than complicated." And our favourite as a review tool: "If the implementation is hard to explain, it's a bad idea."

If you can't explain your design in a few sentences to someone outside the project, treat that as a bug report.

### 18. Simple implementation beats perfect interface (sometimes)

Richard Gabriel's essay "The Rise of Worse is Better" has a line that still starts arguments: "It is more important for the implementation to be simple than the interface." That's a provocation, not a law, and plenty of good engineers disagree with it. We keep it here as a counterweight to rule 8. A pretty API sitting on top of code that nobody dares to touch is a bad deal, and the clumsy but honest version often ends up cheaper.

## The decision ladder

House rule, built from rules 1, 2 and 10. Go down the list and stop at the first rung that solves the whole thing (half doesn't count).

1. Need it at all? Often not. Skip it, and write one line about what you skipped so nobody thinks you forgot. This rung is done when every piece you keep has a need you could name out loud.
2. Got it already? Our helpers, our skills, our services. Use it like the code next to it does, even if you'd have done it differently.
3. Stdlib or the platform can do it? Then you're done.
4. Some dependency we already have can do it? Use that. A new package for five lines, no.
5. Now, and only now, write code. As little as you can get away with. Done when nothing can come out without someone missing it.
6. Run it. Real input, real output. Code that never ran isn't finished, no matter how good it reads. Non-trivial logic gets a test or a self-check; one is plenty.

## How it looks in different kinds of work

Our own reading of the sources, applied to the stuff we run. No citations here, just habits.

Code: the ladder covers most of it. Keep the structure the codebase already has. Fix a bug once, in the shared function, not in every caller. Cut a corner on purpose? Leave `shortcut: <the limit>, <when to upgrade>` in a comment.

Infrastructure: every extra server, container or managed service can page someone at 3am. So first look at what's already running. Platform config over home-made glue. Dull and documented over shiny.

Skills, prompts, agents: if a line in a skill doesn't change what the model does, cut it, it's dead weight in every call. One solid skill per topic, not five thin ones. And no multi-agent pipeline for something a single call or a twenty-line script handles.

Docs: say it, stop. Nobody wants three paragraphs of background before the one line they came for. Tables to compare, prose to explain why.

Process: the sneakiest one. "We always do it" isn't a reason. Find out what breaks without the step. Usually nothing does.

## Where KISS stops

"Everything should be made as simple as possible, but not simpler." It's usually credited to Einstein, but Quote Investigator found no direct evidence he wrote it. The idea holds whoever said it. A simplification that loses a real requirement is a bug, not KISS.

YAGNI only works if the code is easy to change later. Fowler is explicit: "Yagni is only a viable strategy if the code is easy to change, so expending effort on refactoring isn't a violation of yagni." Tests and refactoring are what make "build it later" safe. Skip them and "simple now" turns into "expensive later".

Some things we never cut, however tempting:

- validation at trust boundaries (user input, external APIs, anything from the network)
- error handling that protects data from being lost or corrupted
- security and access control
- accessibility
- anything the person asking explicitly wanted

## Smells

Things that usually mean KISS has slipped. They aren't proof, but each one is worth a second look.

- Options, flags or config that nobody has asked to change yet.
- An interface or base class with exactly one implementation.
- A wrapper whose only job is to call one other function.
- "We might need it for..." in a design discussion.
- A new tool picked because it's easier, when the old one already works.
- A shared helper full of `if` branches for each caller.
- Docs that explain how the design works, because nobody can tell from the code.
- A cleanup "while I'm in there" that has nothing to do with the task. Flag it, don't do it.

## Before you hand it over

- [ ] Every piece has a named need. Nothing is there just in case.
- [ ] Nothing we already had (in our code, the standard library, the platform) was rewritten.
- [ ] No new dependency that a few lines could have replaced.
- [ ] Someone else could understand it without you explaining it.
- [ ] You tried to delete something, and couldn't without losing a real feature.
- [ ] Validation, security and error handling are untouched.
- [ ] It was run for real, and you saw the output.

## Sources

All checked against the full pages on 2026-10-20.

- Kelly Johnson and Skunk Works: https://en.wikipedia.org/wiki/KISS_principle
- Dijkstra, EWD498: https://www.cs.virginia.edu/~evans/cs655/readings/ewd498.html
- Hoare: https://en.wikiquote.org/wiki/C._A._R._Hoare
- Raymond, *The Art of Unix Programming*, ch. 1: http://www.catb.org/esr/writings/taoup/html/ch01s06.html
- Agile Manifesto principles: https://agilemanifesto.org/principles.html
- Occam's razor: https://en.wikipedia.org/wiki/Occam%27s_razor
- Saint-Exupéry: https://quotesondesign.com/antoine-de-saint-exupery/
- Fowler, Yagni: https://martinfowler.com/bliki/Yagni.html
- Fowler on Beck's design rules: https://martinfowler.com/bliki/BeckDesignRules.html
- Gall's law: https://en.wikipedia.org/wiki/John_Gall_(author)
- Kernighan: https://en.wikiquote.org/wiki/Brian_Kernighan
- Hickey, "Simple Made Easy": https://www.infoq.com/presentations/Simple-Made-Easy/
- Brooks, "No Silver Bullet": https://en.wikipedia.org/wiki/No_Silver_Bullet
- Google SRE book, "Simplicity": https://sre.google/sre-book/simplicity/
- Ousterhout, review by Gergely Orosz: https://blog.pragmaticengineer.com/a-philosophy-of-software-design-review/
- Metz, "The Wrong Abstraction": https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
- McKinley, "Choose Boring Technology": https://mcfunley.com/choose-boring-technology
- Pike's rules of programming: http://doc.cat-v.org/bell_labs/pikestyle
- Knuth: https://en.wikiquote.org/wiki/Donald_Knuth
- PEP 20: https://peps.python.org/pep-0020/
- Gabriel, "The Rise of Worse is Better": https://www.dreamsongs.com/RiseOfWorseIsBetter.html
- Einstein attribution: https://quoteinvestigator.com/2011/05/13/einstein-simple/
