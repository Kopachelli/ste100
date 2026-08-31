# Counting words the way STE counts them

Rules 5.1 and 6.3 set the sentence limits: 20 words for a procedure, 25 for a
description. Rules 8.4 thru 8.7 define what a word is. Without section 8 the
limits are unusable, because a plain word count and an STE word count disagree
often and in both directions.

Two examples, each with the count that the standard itself publishes:

```
Make sure that the temperature in the room is 10 °C.        STE: 10   plain: 11
Clean the surface with a soap-and-water solution.           STE:  7   plain:  7
Remove the safety pin (10).                                 STE:  5   plain:  5
The maintenance team does a test of this system each day at 10 a.m.
                                                            STE: 13   plain: 14
Refer to Testing and Fault Isolation, page block 1001.      STE:  6   plain:  9
```

The last one is the important case. A tool that counts nine words there will
report a violation in a sentence that has none, and a writer who trusts it will
damage a correct document.

## The algorithm

`scripts/ste_check.py` implements this. Run it rather than counting by hand.

**1. Remove what is not counted.**

- A number or letter that identifies a paragraph or a work step (rule 8.6).
  `1.`, `A.`, `(3)`, `-`, a bullet.
- The label of a safety instruction or a note. `WARNING:`, `CAUTION:`, `NOTE:`.
  The standard's own worked example — a 20-word caution — does not count its
  label.

**2. Collapse each group that counts as one word.**

| Group | Rule | Example | Counts as |
|---|---|---|---|
| Text in parentheses | 8.5 | `(the EMER legend is off)` | 1 |
| Quoted text | 8.6 | `"Service Overview"` | 1 |
| Number with its unit | 8.6 | `10 °C`, `20 kg`, `10 degrees Celsius`, `5 cc/minute`, `10 a.m.` | 1 |
| Abbreviation | 8.6 | `NASA`, `VPN`, `IFE` | 1 |
| Alphanumeric identifier | 8.6 | `36L7`, `No. 1`, `B/C` | 1 |
| Hyphenated group | 8.7 | `soap-and-water`, `In-Flight`, `main-gear-door` | 1 |
| Title, heading, placard, label | 8.6 | `Structural Repair Manual` | 1 |
| Proper noun of a person, organization, or geopolitical entity | 8.6 | `United States of America` | 1 |

**3. Count what is left.**

## What the tool cannot see, and what to do about it

The last two rows of that table are not detectable from the text. `Business
Class` and `Structural Repair Manual` look identical to a parser, but the
standard counts the first word by word and the second as one word, because the
second is a document title and the first is not.

So the checker does **not** guess. It counts those word by word unless you
declare them, which makes it report a count that is too high rather than too
low. Declare them in the glossary:

```json
{
  "titles":       ["Structural Repair Manual", "Testing and Fault Isolation"],
  "placards":     ["SHORT-CIRCUIT TEST", "DO NOT OPERATE"],
  "proper_nouns": ["United States of America", "George Washington"]
}
```

Then `python scripts/ste_check.py --glossary glossary.json FILE`.

## Uppercase text is not collapsed

Text in uppercase letters can show quoted text (rule 8.6), so it is tempting to
collapse an uppercase run to one word. The standard is not consistent here. It
counts `SHORT-CIRCUIT TEST` as one word in one example, and `CROSS FEED` as two
words in another. Neither reading can be derived from the text.

This tool therefore counts uppercase word by word and lets the glossary override
it. It also means an entirely uppercase safety instruction is counted normally,
which is what the standard's own 20-word caution example requires.

## The colon (rule 8.4)

In a vertical list, a colon ends the sentence. So:

```
To extinguish a possible fire, portable fire extinguishers are      (13 words)
in these areas:
    - The cockpit                                                    (2 words)
    - The cabin sub-compartment                                      (3 words)
    - The crew rest compartment.                                     (4 words)
```

The text before the colon is one sentence under the limit for its type. Each
item after it is a separate sentence under the same limit. A list is how you
legally carry more than 20 words of content in one procedural step.

## Parentheses count twice

Rule 8.5 gives the parenthetical two jobs. Inside the sentence it is one word.
It is also a sentence of its own, and that sentence has its own limit.

```
Make sure that the EMER pushbutton switch is released (the EMER legend is off).
   the sentence:      10 words
   the parenthetical:  5 words, counted separately
```

## Checking a count

Every count on this page comes from a test in
`scripts/test_ste_check.py`, which asserts it against the number that the
standard publishes for that sentence. Run:

```bash
python scripts/test_ste_check.py
```

If you change the counting logic and a published count stops matching, the logic
is wrong.
