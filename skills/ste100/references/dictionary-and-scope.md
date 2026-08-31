# The dictionary, technical terms, and the limit of this skill

Read this before you make any claim about compliance.

## What part 2 is

The dictionary holds **875 approved words** and **1274 words that are not
approved**. Each entry has four columns: the word with its part of speech, the
approved meaning or the approved alternatives, an STE example, and a non-STE
example.

A word in uppercase is approved. A word in lowercase is not, and its row gives
you the alternatives to use instead. Most approved words carry exactly one
meaning and one part of speech, and that meaning is usually narrower than in
ordinary English. Some entries carry a "help" marker that restricts them
further — one word is approved for safety instructions only.

The point of the whole design is that a reader never has to choose between two
readings of a word.

## What this project does not have

The dictionary is not in this repository and will not be. ASD-STE100 is free to
obtain and not free to redistribute. Refer to
[NOTICE.md](../../../NOTICE.md).

That has a precise consequence. **Six rules cannot be checked here:**

| Rule | What it needs |
|---|---|
| 1.1 | Whether a word is in the approved list |
| 1.2 | Which part of speech the entry gives it |
| 1.3 | Which meaning the entry gives it |
| 1.4 | Which verb and adjective forms the entry lists |
| 1.6 | Whether an unapproved word is acceptable as a technical noun in this context |
| 9.2 | Whether this use matches the approved meaning |

Everything else in part 1 is structural, and this skill checks or flags it.

## How to talk about it

Say: "This text obeys the structural rules of ASD-STE100. Word choice was not
checked against the approved dictionary."

Do not say: "This text is STE compliant."

The difference is not pedantry. A maintenance organization that ships a manual
believing it is STE compliant, when the vocabulary was never checked, has a real
problem. Get the standard from
<https://www.asd-ste100.org/STE_downloads.html> — the page is a request form
that mails you a link — and check word by word.

## What you can still do about word choice

The dictionary encodes a principle you can apply without owning it: **pick the
plainest, most common word available, and use it the same way every time.**

Practical moves that need no dictionary:

- **One word, one job, inside this document.** If "check" is the verb in step 1,
  do not write "verify" in step 4 and "confirm" in step 9. Consistency inside a
  document is checkable even when correctness against the approved list is not.
  This is rule 9.4, and the checker enforces it against a glossary.
- **One noun, one item.** Rule 1.11. Never "servo control unit", "actuator", and
  "control unit" for the same part.
- **Verb, not noun, for an action.** Rule 3.7. "Inspect the filter" over "do an
  inspection of the filter" — but note that STE itself prefers "Do a check of
  the battery" over "Check the battery", because "check" is approved as a noun
  and not as a verb. Which form wins is a dictionary fact. Prefer the verb when
  you have no way to know, and do not claim compliance either way.
- **Say what you cannot verify.** When a rewrite turns on a word choice you
  cannot check, name it.

## Technical nouns (rule 1.5)

A technical noun is a term for a concept in a subject field. The dictionary does
not list them, because every field has its own. A word that is not approved may
still be used when it fits one of **22 categories**:

official parts information; vehicles and machines and locations on them; tools
and support equipment; materials and consumables and unwanted material;
facilities and infrastructure and logistics; systems and components and
circuits; mathematical, scientific and engineering terms; navigation and
geographic terms; numbers, units and time; quoted text; professional roles,
organizations and geopolitical entities; parts of the body; personal effects,
food and drink; medical terms; official documents and standards; environmental
and operational conditions; colors; damage terms; computer science and
information and communication technology; civil and military operations; law and
regulations; animals, plants and other life forms.

Issue 9 added the last two categories, and expanded the computing category with
terms including artificial intelligence, machine learning, large language model,
embedding, token, prompt engineering, hallucination, tuning, and chatbot.

Three constraints on technical nouns:

- Use the one your company or industry already approves (1.8).
- If you must choose, keep it short and well known (1.9), and never regional,
  slang, or jargon (1.10).
- Never use it as a verb (1.7). Write "Apply oil to the surface", not "Oil the
  surface".

Colors are adjectives, but STE files them as technical nouns, and their
comparative and superlative forms are not permitted.

## Technical verbs (rule 1.12)

A technical verb is a verb for a process in a subject field. There are **four
categories**:

1. **Manufacturing processes** — remove material, add material, attach material,
   change mechanical properties, change surface finish, change shape.
2. **Computer processes and applications** — input and output, user interface and
   application processes, system operations.
3. **Instructions and information for applicable subject fields** —
   engineering and science, medical, civil and military operations, navigation,
   automotive and railway, energy and oil and gas.
4. **Law and regulations.**

Three constraints:

- If an approved verb says it accurately, use the approved verb instead (1.12).
- Use a technical verb only in the context where it is correct. The same word can
  be right in one field and wrong in another.
- Never use a technical verb as a noun (1.13). The past participle as an
  adjective is permitted: "the reamed hole".

The category lists in the standard are examples, not complete lists. The
standard says so, and it invites change forms that add examples from other
subject fields. This repository contains one such proposal, in
[`.change-proposals/`](../../../.change-proposals/).

## Company glossary

STE assumes you have one. Rules 1.8, 1.11 and 9.4 only work against a list of
the terms your project has settled on.

`scripts/ste_check.py --glossary glossary.json` reads it:

```json
{
  "terms":        {"actuator": ["servo control unit", "control unit"]},
  "titles":       ["Structural Repair Manual"],
  "placards":     ["SHORT-CIRCUIT TEST"],
  "proper_nouns": ["United States of America"],
  "ing_nouns":    ["conditioning", "streaming"]
}
```

`terms` maps the approved technical noun to the synonyms that must not appear;
the checker reports each synonym under rule 1.11. The other keys tell the word
counter which groups count as one word under rule 8.6, and which "-ing" words
are technical nouns under rule 3.5.

Building this file is the highest-value thing a project can do for its own
consistency, and it is the part of STE that works fully without the dictionary.
