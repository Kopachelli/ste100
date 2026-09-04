---
name: never-claim-ste-compliance
description: Rules 1.1 thru 1.4, 1.6 and 9.2 need the approved dictionary. Say STE-informed, never STE-compliant.
metadata:
  type: decision
---

The correct phrasing is: "This text obeys the structural rules of ASD-STE100.
Word choice was not checked against the approved dictionary."

**Why:** those six rules are defined entirely by the 875 approved words of part
2, which this project does not have and cannot redistribute. A maintenance
organization that ships a manual believing it is compliant, when the vocabulary
was never checked, has a real problem. This is a safety-adjacent claim, not a
marketing one.

**How to apply:** `ste_check.py` prints the unchecked rule numbers on every run.
Repeat them in any report. The word to use is **STE-informed**. Refer to
[[no-asd-material-in-repo]].
