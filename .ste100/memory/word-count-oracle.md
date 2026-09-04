---
name: word-count-oracle
description: The standard publishes word counts for its own examples. Those numbers are the test oracle for ste_check.py.
metadata:
  type: decision
---

`skills/ste100/scripts/test_ste_check.py` asserts 39 counts against numbers that
section 8 of the standard publishes for its own example sentences.

**Why:** section 8 defines what a word is, and an STE count differs from a plain
count in both directions. Parentheses, numbers with units, abbreviations,
alphanumeric identifiers, quoted text, titles, proper nouns and hyphenated groups
each count as one word, and a colon in a vertical list ends the sentence. Without
this, the 20-word and 25-word limits raise false violations against correct
documents.

**How to apply:** if you change the counting logic and a published count stops
matching, the logic is wrong, not the test. Run the suite before every commit.
Refer to [[uppercase-not-collapsed]] for the one case the standard leaves open.
