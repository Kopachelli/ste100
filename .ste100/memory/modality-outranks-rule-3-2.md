---
name: modality-outranks-rule-3-2
description: A modal perfect such as "may have failed" keeps its compound tense. A hedge carries the writer's confidence, and confidence is content.
metadata:
  type: decision
---

Rule 3.2 excludes compound tenses. When a modal verb comes before the perfect
form, `ste_check.py` reports it as **review**, not as a violation, and a rewrite
keeps the hedge and flags the departure.

**Why:** "The request may have failed" and "The request failed" are different
claims. Dropping the auxiliary deletes the uncertainty along with the tense. A
word limit tempts a writer to cut exactly the words that carry the author's
confidence, which is the most common way a well-meant STE rewrite goes wrong.

**How to apply:** never promote a hedge to a fact to save words, and never add a
cause, a frequency, or a mechanism that the source did not state. Flag the
departure from rule 3.2 rather than making it silently.
