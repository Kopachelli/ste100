# ste100

A Claude Code skill that applies **ASD-STE100 Simplified Technical English** (Issue 9,
January 2025) to English text, plus one change proposal submitted to the standard's
maintenance group.

ASD-STE100 is the controlled language that the aerospace and defence industry wrote so
that a maintenance technician cannot misread an instruction. It has two parts: 53 writing
rules in nine sections, and a controlled dictionary of 875 approved words. This repository
implements what can be implemented from the rules alone, and says clearly what cannot.

## What lives here

| Path | What it is |
|---|---|
| [`skills/ste100/`](skills/ste100/) | **The skill.** The rules, the checker, the examples. |
| [`.claude/commands/ste100.md`](.claude/commands/ste100.md) | **`/ste100`** — check or rewrite a target, now. |
| [`.claude/agents/ste100.md`](.claude/agents/ste100.md) | **The agent.** Autonomous documentation work, with memory. |
| [`.ste100/`](.ste100/) | Project memory and the terminology glossary. Committed. |
| [`.change-proposals/`](.change-proposals/) | A filled ASD change form proposing one addition to Issue 9. |

Three ways in, in order of how much you want to think:

| | Use it when |
|---|---|
| `/ste100 <target>` | You know what you want checked or rewritten. |
| `ste100` agent | The job is open-ended — "make our docs STE" — and needs scoping, memory, and questions asked first. |
| `ste100` skill | You are doing the work yourself and want the rules and the checker. |

## The skill in one paragraph

Give it text. It works out what kind of text it is — a procedure, a description, a safety
instruction, a note, or a machine-facing string — because STE applies different rules and
different length limits to each. It then runs a checker that finds every mechanical
violation, cites the rule number, and rewrites the text. It never claims compliance it
cannot verify.

## What makes it different

**It counts words the way STE counts words.** Section 8 of the standard says a
parenthetical counts as one word, a number with its unit counts as one word, and so do
abbreviations, alphanumeric identifiers, quoted text, titles, proper nouns of
organizations, and hyphenated groups. A colon in a vertical list ends the sentence. Under
those rules `Make sure that the temperature in the room is 10 °C.` is ten words, not
twelve, and `Clean the surface with a soap-and-water solution.` is seven, not nine. A tool
that counts tokens instead of STE words gets the 20-word and 25-word limits wrong in both
directions. This one implements the counting rules, and the test suite checks them against
word counts that the standard publishes for its own examples.

**It routes on text type.** A procedure caps at 20 words and must use the imperative. A
description caps at 25 and must not. A note carries information only and caps at 25. A
safety instruction opens with the command or the condition and then states the risk. These
are four different jobs, not one setting.

**It states its own boundary by rule number.** Rules 1.1 thru 1.4, 1.6 and 9.2 are defined
by the approved dictionary. Without the dictionary they cannot be checked, so the skill
does not pretend to check them. Everything structural it does check, and every finding it
reports carries the rule it came from.

## Install

```bash
git clone https://github.com/Kopachelli/ste100
cd ste100
cp -r skills/ste100            ~/.claude/skills/ste100
cp .claude/commands/ste100.md  ~/.claude/commands/ste100.md
cp .claude/agents/ste100.md    ~/.claude/agents/ste100.md
```

The skill alone is enough to start. Add the command and the agent to get `/ste100`
and the `ste100` subagent in every project, not only this one.

Then ask Claude to "rewrite this in STE", "check this against ASD-STE100", or "audit this
procedure for STE violations" — or run `/ste100 docs/install.md`.

### The agent's memory

The agent keeps two stores, split by who the knowledge belongs to.

| Store | Where | Committed | Holds |
|---|---|---|---|
| Project | `.ste100/memory/` | Yes | Terminology rulings, scope decisions, audit history |
| User | `~/.claude/agent-memory/ste100/` | No | Preferences, corrections, working style |

Project memory is committed on purpose. STE prescribes a company terminology
database, and a terminology decision belongs to the project and its team, not to
whoever happened to make it. When the next person asks why the part is called the
actuator and not the control unit, the answer is in the repository.

You can also run the checker on its own, without Claude:

```bash
python skills/ste100/scripts/ste_check.py --type procedure yourfile.md
```

## What it will not do

It will not certify a document as STE-compliant. It will not reproduce ASD's dictionary.
It will not turn a hedge into a fact to save words — `may have failed` is not `failed`. It
will not simplify creative or persuasive writing, because STE is deliberately flat. And it
will not make an empty paragraph worth reading; STE fixes the form of a text, not its
substance.

## Get the standard

ASD-STE100 is free. This repository does not include it and cannot redistribute it. See
[NOTICE.md](NOTICE.md) for why, then request your own copy at
<https://www.asd-ste100.org/STE_downloads.html>.

## License

MIT. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
