# Change proposals to ASD-STE100

STE is a living standard. The STEMG takes feedback through a change form, which
ships with the specification and is also available on the STEMG website. The
group records every form, discusses them in its meetings, and folds the agreed
changes into the next issue.

This directory holds proposals written for this project.

| Date | Target | Proposal | Status |
|---|---|---|---|
| 2026-08-31 | Rule 1.12, category 2 | [Technical verbs for AI and machine learning](2026-08-31-rule-1.12-ai-technical-verbs/proposal.md) | Drafted, not sent |

Each directory holds:

- `CHANGE-FORM-filled.docx` — the official ASD form, filled. **Not committed.**
  The form is part of Issue 9, and publishing a filled copy would publish part
  of the standard. Regenerate it locally from your own copy of the blank form:
  `python fill_form.py <dir>/CHANGE-FORM-filled.docx <dir>/form-fields.txt`,
  after copying the blank form to that path. This is the file to send.
- `proposal.md` — the same content, readable in the repository.
- `evidence.md` — the audit that backs every claim, with the checks written out
  so anyone with a copy of Issue 9 can reproduce them.
- `form-fields.txt` — the exact field text, used to fill the form and to run the
  checker over it.
- `glossary.json` — the terminology file for that check.

## The proposals are written in STE

A proposal to the maintenance group of a controlled language, written in
uncontrolled English, argues against itself. Each proposal is checked with this
repository's own tool:

```bash
sed -e '/^FIELD [0-9]$/d' 2026-08-31-rule-1.12-ai-technical-verbs/form-fields.txt \
  | python ../skills/ste100/scripts/ste_check.py --type description \
      --glossary 2026-08-31-rule-1.12-ai-technical-verbs/glossary.json -
```

Current result: zero violations. Two items are reported for review, and both are
the quoted layout of the rule that the proposal asks to change, not prose.

## Nothing here has been sent

Sending a proposal to `stemg@asd-ste100.org` is the author's decision.
