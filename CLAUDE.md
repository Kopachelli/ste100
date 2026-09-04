# CLAUDE.md

This repository builds tooling for **ASD-STE100 Simplified Technical English**.

**Read the project brief before doing work here.** It carries the two rules that
are not negotiable, the checker commands, and the layout:

@ste100.md

## The short version

If you read nothing else:

1. **`.input/` never enters git.** It holds ASD-STE100 Issue 9, which is free to
   obtain and not free to redistribute. Cite rule numbers, paraphrase, write your
   own examples. `git ls-files | grep -cE '^\.input/|\.docx$|\.pdf$'` must print
   `0` before any commit.
2. **Never claim "STE compliant".** Rules 1.1 thru 1.4, 1.6 and 9.2 need the
   approved dictionary, which this project does not have. The word is
   **STE-informed**.
3. **Run the checker, do not count words by eye.**
   `python skills/ste100/scripts/ste_check.py --type auto FILE`. STE counts words
   under section 8, and that count differs from a plain count in both directions.
4. **Classify the text first.** Procedure 20 words, description 25, safety
   instruction 20, note 25. Different verb rules for each. Per block, not per
   document.
5. **`python skills/ste100/scripts/test_ste_check.py` passes before every
   commit.** Its word counts are asserted against numbers the standard publishes
   for its own examples.

## Working on STE text

Three ways in, in order of how much you want to think:

| | Use it when |
|---|---|
| `/ste100 <target>` | You know what you want checked or rewritten. Fast. |
| `ste100` agent | The job is open-ended — "make our docs STE" — and needs scoping, memory, and questions asked first. |
| `ste100` skill | You are doing the work yourself and want the rules and the checker. |

## Work style here

- Branch `dev`. `main` takes merges.
- Terminology decisions go to `.ste100/memory/` and are committed. They belong to
  the project, not to whoever made them.
- A proposal to the STEMG is written in STE and checked with our own tool.
- Nothing is emailed to `stemg@asd-ste100.org` without the author saying so.
