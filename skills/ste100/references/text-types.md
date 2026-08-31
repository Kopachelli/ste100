# Text types: which rules are applicable

STE has one dictionary and two kinds of writing: procedural and descriptive.
Safety instructions and notes are special cases with their own rules. Get the
type wrong and you apply the wrong limit and the wrong verb form, which is worse
than applying nothing.

Classify each **block**. A real document mixes types on the same page.

| | Procedure | Description | Safety instruction | Note |
|---|---|---|---|---|
| Purpose | Tell the reader to do something | Tell the reader how something is or works | Tell the reader about a risk | Help the reader during a procedure |
| Word limit | **20** (5.1) | **25** (6.3) | **20** (5.1) | **25** (5.5) |
| Imperative | Required (5.3) | Not permitted | Required or condition first (7.2) | Not permitted (5.5) |
| Passive voice | Not permitted (3.6) | Only when the agent is unknown (3.6) | Not permitted | Only when the agent is unknown |
| Own rules | 5.1 thru 5.5 | 6.1 thru 6.6 | 7.1 thru 7.3 | 5.5 |
| Also obeys | 1 thru 4, 8, 9 | 1 thru 4, 8, 9 | 1 thru 5, 8, 9 | Descriptive rules |

## Procedure

Work steps. The verb is in the imperative and comes first.

```
1. Remove the four screws (10) that attach the flange (15) to the cover (20).
2. Remove the cover (20) from the housing (12).
3. Remove and discard the preformed packing (13).
```

One instruction per sentence (5.2). Two actions may share a sentence only when
they happen at the same time — "Cut and remove the wire" — or when a result
follows the action immediately.

Put the condition first and separate it with a comma (5.4):

```
When the light comes on, set the switch to NORMAL.
```

Do not write "must" before an imperative unless the instruction is
safety-critical or carries an important condition (5.3).

## Description

Information, not instruction. No imperative.

Give information gradually (6.1). One subject per sentence. Each sentence
carries a key word forward from the last (6.2), which is what makes a
description readable rather than a list of facts:

```
The Instrument Landing System shows data that helps the pilot during the
approach to the runway. This system shows the pilot the deviations from the
localizer course and the glideslope path. The localizer course aligns with the
centerline of the runway.
```

"System", "pilot", "runway", "localizer course" each appear again on purpose.
Replacing one with a synonym for variety would cut the chain.

Every paragraph opens with its topic sentence (6.4), has one topic (6.5), and
has six sentences at most (6.6).

## Safety instruction

Three decisions, in order.

**1. Which word? (7.1)** A **warning** is a risk of injury or death. A
**caution** is a risk of damage to objects. If both risks are present, it is a
warning. This is a risk analysis and it is the writer's job — no tool can do it.
The classic error is calling something a caution when the real outcome is an
explosion.

**2. Command or condition first (7.2).** Not an abstract statement.

```
not this:  EXTREME CLEANLINESS OF OXYGEN TUBES IS IMPERATIVE.
this:      MAKE SURE THAT THE OXYGEN TUBES ARE FULLY CLEAN.
```

**3. Then the consequence (7.3).** Name it.

```
MAKE SURE THAT THE OXYGEN TUBES ARE FULLY CLEAN. OXYGEN AND GREASE MAKE AN
EXPLOSIVE MIXTURE. AN EXPLOSION CAN CAUSE INJURY OR DEATH.
```

"Explosion", "injury", "death" are doing the work. A reader who knows the
outcome behaves differently from one who reads "is imperative".

The uppercase in these examples is a convention of the aerospace specifications,
not an STE rule. STE does not regulate formatting. The 20-word limit still
applies, and the label is not counted.

In a vertical list, repeat the negative command on every item, so that each item
reads correctly on its own:

```
not this:  DO NOT:
             - PUT YOUR FEET ON THE APU LINE.
             - USE THE APU LINE AS A HANDLE.
this:        - DO NOT PUT YOUR FEET ON THE APU LINE.
             - DO NOT USE THE APU LINE AS A HANDLE.
```

## Note

A note gives information. That is all it does (5.5).

A note must not contain an instruction, a requirement, a limit, or a tolerance.
If the reader must do something, it is a work step. If not doing it causes
damage or injury, it is a safety instruction.

```
not a note:  NOTE: Make sure that the ventilation system operates correctly.
                   -> this is work step 6 of the procedure

not a note:  NOTE: When you connect the lines, do not bend them too much.
                   -> this is a CAUTION

a note:      NOTE: The gyroscope becomes stable after approximately 15 seconds.
```

**The test.** Read the procedure with the notes removed. If the reader can still
do the job correctly, the notes are correct. If something is missing, that
something was never a note — move it into a work step and test again.

## Machine-facing strings

Not a category in the standard. STE was built for a reader who cannot ask a
follow-up question, and a program parsing a string is in that position: no
back-channel, no way to resolve "does this mean the caller does X, or the callee
does X?"

Treat these as descriptive text (25 words) unless the string is an instruction
to an executing agent, which makes it procedural (20 words, imperative).

Apply the structural rules in full. Two cautions:

- **Do not force the imperative onto a description.** A tool description
  describes; it does not command.
- **Keep the hedge.** Status text and error messages carry the writer's
  confidence, and confidence is content. "The request may have failed" and "The
  request failed" are different claims. Rule 3.2 removes compound tenses, and
  "may have failed" is a compound tense — but cutting it deletes the
  uncertainty. Keep it and flag the departure. Refer to the Boundaries section
  of `SKILL.md`.
