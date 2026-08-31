---
name: ste100
description: "Apply ASD-STE100 Simplified Technical English (Issue 9) to English text — rewrite it, or audit it and report violations by rule number. Use for maintenance procedures, work instructions, safety warnings and cautions, notes, system descriptions, and for machine-facing strings such as tool descriptions, error messages, and inter-agent instructions, where a wrong reading has a cost. Triggers: STE, ASD-STE100, Simplified Technical English, controlled language, controlled natural language, technical writing rules, plain-language rewrite, disambiguate this, rewrite so it cannot be misread. Not for creative, marketing, or persuasive copy."
version: 1.0.0
---

# ASD-STE100 Simplified Technical English

ASD-STE100 is a controlled natural language. The aerospace and defence industry
wrote it because a technician on a tarmac reads a manual with no author to call,
and a misread instruction can kill people. It has two parts: 53 writing rules in
nine sections, and a controlled dictionary of 875 approved words and 1274 words
that are not approved.

This skill applies the writing rules. It does not include the dictionary.

## What this skill claims, and what it does not

**STE-informed, not STE-compliant.** Rules 1.1 thru 1.4, 1.6 and 9.2 are defined
by the approved dictionary in part 2. This project does not include the
dictionary, and cannot check those rules. Everything else in part 1 is
structural and this skill checks it.

Never tell a user their text is "STE compliant". Say which rules were applied,
and say that word choice was not verified against the approved dictionary. If
the work needs certified compliance, tell the user to get the standard free from
<https://www.asd-ste100.org/STE_downloads.html> and check word by word.

Refer to `references/dictionary-and-scope.md` before you make any claim about
compliance.

## Step 1 — Classify the text. Do this first.

STE is not one rule set. It applies different rules and different length limits
to different kinds of text, and almost every mistake a tool makes here comes
from skipping this step.

| Type | What it is | Word limit | Verb form |
|---|---|---|---|
| **Procedure** | Work steps that tell the reader to do something | **20** (5.1) | Imperative (5.3) |
| **Description** | Information about an item, a system, or how it operates | **25** (6.3) | No imperative |
| **Safety instruction** | Warning or caution | **20** (5.1) | Command or condition first (7.2) |
| **Note** | Information inside a procedure | **25** (5.5) | No imperative, no requirement |
| **Machine-facing string** | Tool description, error message, log line, inter-agent instruction | **25** | Follow the sense of the string |

A document usually mixes types. Classify each block, not the whole document.

Say the type out loud only in audit mode, or when the user asked. In rewrite
mode, keep it internal.

**Machine-facing strings** are not a category in the standard. STE was built for
a reader who cannot ask a follow-up question, and a program parsing a string is
in the same position. Apply the structural rules in full. Do not force the
imperative onto text that describes rather than instructs, and read the
"modality" rule in Boundaries before you shorten anything.

## Step 2 — Run the checker

```bash
python scripts/ste_check.py --type auto FILE
python scripts/ste_check.py --type procedure --glossary glossary.json FILE
cat text.md | python scripts/ste_check.py -
```

It reports every mechanical finding with its rule number, split into
`VIOLATION` (certain) and `review` (heuristic, needs your judgment). Use
`--json` to consume the result, `--quiet` for violations only.

Run it. Do not do this part by eye. The checker counts words under rules 8.4
thru 8.7, and those counts differ from a plain word count often enough that
eyeballing the 20-word and 25-word limits gives the wrong answer in both
directions. Refer to `references/word-count.md`.

## Step 3 — Apply the rules the checker cannot reach

The checker finds structure. These need reading:

- **6.1 Give information gradually.** One subject per sentence, each sentence
  building on the last.
- **6.2 Key words and key phrases.** Repeat the same term to connect sentences.
  Do not rotate synonyms for elegance.
- **6.4 and 6.5 Topic sentences.** Each paragraph opens with the sentence that
  names its topic, and has only one topic.
- **7.1 Level of risk.** A warning is for a risk of injury or death. A caution is
  for a risk of damage to objects. Both risks together means a warning. Judging
  the risk is the writer's job, not the tool's.
- **9.1 Different sentence construction.** When no word-for-word replacement
  works, rebuild the sentence. Do not force a bad substitution.
- **1.9 and 1.11 Technical nouns.** Short, well known, and the same noun for the
  same item every time.

## Step 4 — Produce the output

**Rewrite mode (default).** Output the rewritten text and nothing else. No
preamble, no mode announcement, no count of violations, no closing offer. One
permitted addition: if you kept a longer phrasing on purpose, add one line after
the text that starts `Kept as-is:` and names the phrase and the precision that a
shorter version would have lost.

**Audit mode.** Use when the user asks to see the reasoning: "which rules did it
break", "show the diff", "explain the changes", "check this". Output a table:

```markdown
| Rule | Type | Original | Rewritten |
|---|---|---|---|
| 3.2 | procedure | "The operator has adjusted the linkage." | "The operator adjusted the linkage." |
| 2.1 | description | "runway light connection resistance calibration" | "calibration of the resistance of the runway light connection" |
```

Follow the table with one line on anything you deliberately did not change, and
one line naming the rules that were not checked.

If the text already obeys the rules, say so. Do not invent changes.

## The rules you will use most

Full list of all 53 rules and the 8 general recommendations:
`references/rules-reference.md`. These are the ones that fire constantly.

| Rule | Do | Not this |
|---|---|---|
| 3.2, 3.4 | Simple tenses only. "The job finished." | "The job has finished." "The job is finishing." "It must be finished." |
| 3.6 | Active voice. "A switching relay connects the circuits." | "The circuits are connected by a switching relay." |
| 3.7 | A verb for an action. "Inspect the filter." | "Do an inspection of the filter." when an approved verb exists |
| 9.3 | One verb. "Extinguish the fire." | "Put out the fire." Two words whose meaning the parts do not predict |
| 5.2 | One instruction per sentence, unless the actions happen at the same time | "Open the file and read line 3, then check the result." |
| 5.4 | Condition first, then a comma, then the command. "When the light comes on, set the switch to NORMAL." | "Set the switch to NORMAL when the light comes on." |
| 4.2 | Every word in full. "If shims are installed, remove them." | "If installed, remove the shims." Dropped subjects, verbs, articles, contractions |
| 4.5 | Keep the article. "Turn the shaft assembly." | "Turn shaft assembly." |
| 2.1 | Three words maximum in a multi-word noun. "Calibration of the resistance of the runway light connection." | "Runway light connection resistance calibration" |
| 8.1 | Two sentences. | Any semicolon at all. Every other standard punctuation mark is permitted, the em dash included. |
| 4.3 | A vertical list for three or more items or steps | The same content buried in one prose sentence |
| 6.6 | Six sentences maximum in a paragraph, one topic | A paragraph that changes subject halfway |
| 3.5 | "-ing" only as a technical noun or its modifier. "the opening in the panel" | "while the door is opening" |
| 1.14 | American English spelling | "colour", "fibre", "centre" |
| GR-1 | Keep "that". "Make sure that the valve is open." | "Make sure the valve is open." |
| GR-6 | English words. "for example" | "e.g.", "i.e.", "etc." |
| GR-7 | Gender-neutral terms | "he", "she", "his", "her" |

## Project glossary

Rules 1.8, 1.11 and 9.4 assume the writer has a company glossary or a
terminology database. If the project has one, pass it with `--glossary`. It also
tells the checker which multi-word groups count as one word under rule 8.6.

```json
{
  "terms":        {"actuator": ["servo control unit", "control unit"]},
  "titles":       ["Structural Repair Manual", "Testing and Fault Isolation"],
  "placards":     ["SHORT-CIRCUIT TEST", "DO NOT OPERATE"],
  "proper_nouns": ["United States of America"],
  "ing_nouns":    ["conditioning", "streaming"]
}
```

`terms` maps the approved technical noun to the synonyms that must not appear.
The other keys collapse to one word in the word count. Without them the checker
counts a document title word by word, which overstates the sentence length.

## Boundaries

**Will:**

- Rewrite text into short, single-meaning, active-voice sentences that obey the
  rules of the correct text type.
- Name every rule it applied, by number, and name the rules it could not check.
- Keep every fact, condition, limit, and scope qualifier from the original.
- Keep the strength of every hedge.
- Suggest a glossary entry for a technical noun that must stay.

**Will not:**

- Claim STE compliance, or reproduce the approved dictionary.
- **Turn a hedge into a fact.** "The request may have failed" is not "The request
  failed." "This could be caused by X" is not "X is the cause." A shorter
  sentence that upgrades a hedge is not a simplification, it is a different
  claim. This is the most common way a well-meant rewrite goes wrong, because
  hedges are exactly what a word limit tempts you to cut. **When rule 3.2 and a
  hedge conflict, keep the hedge and flag the departure.**
- Add a fact the source did not state. A rewrite that reads better because it
  supplies a cause, a frequency, or a mechanism has stopped being a rewrite.
- Drop a safety condition or an exception to get under a word limit. Keep the
  longer text and report the conflict.
- Simplify creative, marketing, or persuasive writing. STE is deliberately flat.
- Make weak content strong. STE controls the form of a text, not its substance.
  A hollow paragraph rewritten under these rules is a clean, short, hollow
  paragraph.
- Shorten past the point of clarity. Removing ambiguity is the goal. Cutting
  words is not.

## Files

| File | Read it when |
|---|---|
| `references/rules-reference.md` | You need a rule you do not know, or its number |
| `references/word-count.md` | You need to count words, or explain a count |
| `references/text-types.md` | You must decide which rules are applicable |
| `references/dictionary-and-scope.md` | Word choice, technical nouns and verbs, compliance claims |
| `examples/procedural.md` | Work steps |
| `examples/descriptive.md` | System and product descriptions |
| `examples/safety.md` | Warnings and cautions |
| `examples/agent-text.md` | Tool descriptions, error messages, agent instructions |
| `scripts/ste_check.py` | Always, in step 2 |
