---
name: uppercase-not-collapsed
description: The standard counts one uppercase run as one word and another as two. We count word by word and let the glossary override.
metadata:
  type: decision
---

`ste_check.py` does not collapse a run of uppercase words into one word. The
glossary keys `placards`, `titles` and `proper_nouns` collapse them explicitly.

**Why:** rule 8.6 counts quoted text as one word, and uppercase can show quoted
text. But the standard is not consistent. It counts `SHORT-CIRCUIT TEST` as one
word in one worked example and `CROSS FEED` as two words in another, and neither
reading can be derived from the text. Counting word by word overstates a
sentence's length rather than understating it, which is the safe direction, and
it keeps the standard's own 20-word all-uppercase caution example correct.

**How to apply:** when a project has real placards or document titles, add them
to `.ste100/glossary.json` rather than changing the counting logic. Refer to
[[word-count-oracle]].
