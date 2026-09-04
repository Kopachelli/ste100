---
name: no-asd-material-in-repo
description: .input/ and every filled change form stay out of git. ASD-STE100 is free to obtain and not free to redistribute.
metadata:
  type: scope
---

`.input/` is gitignored in full, and `.docx` and `.pdf` under
`.change-proposals/` are gitignored too. No dictionary content, no verbatim rule
text, no copied examples. Cite the rule number and paraphrase.

**Why:** ASD-STE100 Issue 9 permits reproduction only with the written authority
of an officer of ASD, or by eight listed categories of organization. This project
is in none of them. The repository is public, so a mistake here is published.

**How to apply:** before any commit, run
`git ls-files | grep -cE '^\.input/|\.docx$|\.pdf$'` and confirm it prints
`0`. The filled change form is regenerated locally by
`.change-proposals/fill_form.py`. Refer to [[never-claim-ste-compliance]] for the
other constraint that follows from not holding the standard.
