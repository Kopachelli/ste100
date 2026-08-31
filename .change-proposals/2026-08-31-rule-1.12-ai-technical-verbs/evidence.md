# Evidence for the rule 1.12 change proposal

Everything below was checked against ASD-STE100 Issue 9 (January 2025), the copy
obtained from the official downloads page. Page numbers are the document's own
page labels. No text of the standard is reproduced here beyond the short quoted
phrases that the claims depend on.

Method: the text layer of the PDF was extracted and searched. Part 1 (pages
1-0-1 thru 1-9-14) was read in full. Part 2 was searched term by term for each
word listed below.

---

## 1. Issue 9 added AI terms to the technical **nouns**

Rule 1.5, category 19, "Computer science, information and communication
technology" (page 1-1-8) lists, among others:

> AI, artificial intelligence, chatbot, deep learning, embedding, hallucination,
> large language model, machine learning, prompt engineering, token, tuning

The Highlights table for Issue 9 records, under Rule 1.5:

> New examples of technical nouns added in the applicable categories.

So the AI vocabulary entered the standard through rule 1.5, as nouns.

## 2. Issue 9 added no AI terms to the technical **verbs**

Rule 1.12 (pages 1-1-13 and 1-1-14) has four categories. Category 2, "Computer
processes and applications", has exactly three subcategories:

| | Subcategory | Verbs listed |
|---|---|---|
| 2 a) | Input and output processes | click, digitize, enter, press, print, swipe, tap, type |
| 2 b) | User interface and application processes | clear, close, copy, cut, delete, deselect, disable, drag, drag and drop, enable, encrypt, erase, filter, highlight, invalidate, maximize, minimize, navigate, open, paste, save, scroll, sort, store, tweet, validate, zoom in, zoom out |
| 2 c) | System operations | abort, boot, communicate, debug, download, format, install, load, manage, process, reboot, update, upgrade, upload |

None of the 50 verbs refers to an artificial intelligence or machine learning
process. The Highlights table records, under Rule 1.12, that category 3 was
restructured, a new category 4 was created, and new examples were added — but
the AI verbs are not among them.

**This is the asymmetry.** The nouns arrived in Issue 9. The verbs did not.

## 3. The proposed verbs are absent from part 2

Each term was searched across the full word list (pages 2-1-A1 thru the end).

| Term | Present in the dictionary? | Entry |
|---|---|---|
| train | **No** — zero occurrences | — |
| model | **No** — zero occurrences | — |
| embed | **No** — zero occurrences | — |
| infer | **No** — zero occurrences | — |
| annotate | **No** — zero occurrences | — |
| fine-tune | **No** — zero occurrences | — |
| prompt | Yes, as an adjective only | `prompt (adj)` is not approved. Alternative: IMMEDIATELY (adv) |
| label | Yes, as a verb | `label (v)` is not approved. Alternatives: IDENTIFY (v), LABEL (TN) |

`prompt` and `label` are the two cases where the standard has already ruled, and
both rulings are for a non-AI context: `prompt` as "immediate", `label` as
attaching a physical label. Neither addresses prompting a model or labeling
training data.

Rule 1.12 already covers this situation. Its subsection "Words that are not
approved but that can be technical verbs" gives `enter` and `respond` as words
that the dictionary does not approve but that are correct technical verbs inside
their category. `prompt` and `label` would work the same way.

## 4. The rule 1.3 hazard is concrete

Two approved verbs look available to an AI writer and are not.

**TUNE (v), TUNES, TUNED, TUNED** — approved meaning: "To adjust equipment to
the best performance". The STE example in the dictionary tunes a radio to a
frequency.

**DEPLOY (v), DEPLOYS, DEPLOYED, DEPLOYED** — approved meaning: "To move or
cause to move from a specified position of storage and into operation". The STE
examples deploy a slide raft and a thrust reverser.

A model is not equipment and a model is not in storage. So "tune the model" and
"deploy the model to production" both use an approved word outside its approved
meaning, which rule 1.3 forbids.

The hazard is not theoretical. Rule 1.5 approves the noun **tuning** in category
19. A writer who may write "the tuning of the model" will reach for "tune the
model", and the dictionary entry for TUNE looks like permission.

## 5. The nominalization route conflicts with rule 3.7

Without a verb, the writer must nominalize: "do the tuning of the model", "do
the training of the model".

Rule 3.7 tells the writer to use a verb for an action, not a noun made from a
verb, because the noun form hides who acts and adds a filler verb.

The standard does accept "Do a check of the laptop battery" when no approved
verb exists, so a nominalization is not itself an error. The point is narrower
and still stands: **every** AI action must be nominalized, in every sentence,
across a whole document, because no verb exists for any of them. That is a
systematic conflict with rule 3.7, not an occasional one.

## 6. The categories are explicitly open

Rule 1.12 ends with:

> The technical verbs in their related categories are only examples. Rule 1.12
> does not give a full list of all possible technical verbs.

Rule 1.5 carries the same statement for the nouns. So adding examples to a
category is the change that the rule's own structure anticipates, not an
exception to it.

Category 2 c) is the precedent inside the same category: `boot`, `debug` and
`reboot` are listed as technical verbs and the dictionary does not approve any
of them.

## 7. The direction matches the STEMG's own

The STEMG and its AI Task Team published *ASD-STE100 Simplified Technical
English and Artificial Intelligence* in June 2026. It states that AI is
reshaping technical writing, that the standard takes priority, and that AI
adoption must support rather than override STE requirements.

A writer who documents an AI system today cannot keep STE as the primary
reference for the actions in that system, because the standard gives no words
for them. This proposal closes that gap with the smallest possible change.

## 8. What this proposal deliberately does not ask for

- **No dictionary change.** Part 2 is untouched. The proposal adds examples to a
  rule in part 1.
- **No change to TUNE or DEPLOY.** Widening an approved meaning is a larger
  change with more consequences. The proposal cites them as evidence only.
- **No new category.** Category 2 already exists and already covers computer
  processes. A fourth subcategory inside it is the minimum change that solves
  the problem.

## Reproducing these checks

With your own copy of Issue 9:

```bash
pdftotext -f 45 -l 62 -layout ASD-STE100_ISSUE9.pdf - | grep -A10 "2. Computer processes"
pdftotext -f 45 -l 62 -layout ASD-STE100_ISSUE9.pdf - | grep -A8 "19. Computer science"
for w in train model embed infer annotate fine-tune; do
  echo "$w => $(pdftotext -f 149 -l 435 -layout ASD-STE100_ISSUE9.pdf - | grep -c -i -w "$w")"
done
```

Page ranges are for the 434-page PDF of Issue 9 dated 2025-01-15.
