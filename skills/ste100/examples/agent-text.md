# Machine-facing strings — worked examples

Tool descriptions, error messages, log lines, inter-agent instructions, system
prompts. Not a category in ASD-STE100, so the mapping is set out in
`references/text-types.md`: descriptive limits by default, procedural limits
when the string instructs an executing agent.

STE was written for a reader who cannot ask a follow-up question. A program
parsing a string is in the same position.

Every example on this page was written for this project.

---

## 1. Tool description

Descriptive, 25-word limit.

**Before**

> This tool will attempt to synchronize state across the various backends that
> have been configured, and if a conflict is detected it may resolve it
> automatically depending on the strategy that has been set, or otherwise it will
> surface the conflict for manual review.

Findings: 44 words (6.3); present perfect twice, "have been configured" and "has
been set" (3.2); passive voice with a knowable agent, "is detected" (3.6);
several claims in one sentence (4.1); "otherwise it" leaves the branch condition
unstated.

**After**

> The tool synchronizes state across the configured backends. If the tool finds a
> conflict, it reads the configured strategy. If the strategy permits automatic
> resolution, the tool can resolve the conflict. If the tool does not resolve the
> conflict, it reports the conflict for manual review.

Two things worth stating rather than hiding:

- **"will attempt to" became "synchronizes", and "may resolve" stayed "can
  resolve".** The first is a hedge about the whole tool and the sentence carries
  it elsewhere; the second is a real limit on the outcome and had to survive.
- **The last branch turns on whether the conflict was resolved, not on what the
  strategy permits.** That is what "or otherwise" meant: the fallback covers a
  permitted resolution that still did not happen. Getting this wrong would have
  produced cleaner text and a different specification.

---

## 2. Error message

This is the example that the modality rule exists for.

**Before**

> An error may have occurred while processing your request due to a possible
> mismatch in the expected data format, which could be caused by an outdated
> client version.

Findings: 28 words (6.3); three separate claims in one sentence (4.1); "-ing"
form "processing" (3.5).

Not findings: "may have occurred" and "could be caused by". The system that
wrote this does not know what went wrong. Both hedges report that ignorance
accurately.

**After**

> Your request may have failed. The cause can be a data format that does not
> match what the server expects. An outdated client can cause this mismatch.
> Check your client version.

**A tempting rewrite that is wrong:**

> The request failed. The data format did not match what the server expects. An
> outdated client is the most common cause. Check your client version.

It is shorter, flatter, and easier to read. It also asserts a failure the system
only suspects, states a cause as fact, and invents a frequency claim that
appears nowhere in the input. A rewrite that supplies a cause, a frequency, or a
mechanism has stopped being a rewrite.

Note that "may have failed" keeps a compound verb form that rule 3.2 would
otherwise remove. **When rule 3.2 and modality conflict, modality wins.**
Dropping the auxiliary here deletes the uncertainty along with the tense. Flag
the departure; do not make it silently.

---

## 3. Inter-agent instruction

This one instructs an executing agent, so it is procedural: 20 words,
imperative.

**Before**

> Once the upstream job has completed and assuming no errors were raised, the
> downstream agent should proceed to consume the output artifact, though it is
> worth noting that partial artifacts are sometimes produced under timeout
> conditions.

Findings: 36 words (5.1); present perfect "has completed" (3.2); passive voice
"were raised" and "are produced" (3.6); "-ing" form "assuming" (3.5); three
facts in one sentence (5.2); the warning about partial artifacts has no
associated action.

**After**

> 1. Wait until the upstream job is complete and has no errors.
> 2. Make sure that the output artifact is complete.
> 3. Read the output artifact.
>
> NOTE: A timeout can cause a partial artifact.

One call to state openly: **step 2 is new.** The original warned about partial
artifacts and never said what to do about them. Adding the check makes the
warning actionable, and it is added content, so it is named here rather than
passed off as a rewrite. If the source's silence was deliberate, delete step 2
and keep the note.

The note obeys rule 5.5: it gives information, it carries no instruction, and
removing it leaves a procedure that still works.

---

## 4. Log line

**Before**

> Retrying connection to the primary datastore replica set coordinator node after
> transient failure; will back off exponentially.

Findings: semicolon (8.1); "-ing" forms "retrying" and "will back off" as a
phrasal verb (3.5, 9.3); a seven-word multi-word noun (2.1); no subject (4.2).

**After**

> The connection to the coordinator node of the primary replica set failed. The
> client will try again. The delay between each try will increase.

The seven-word stack "primary datastore replica set coordinator node" becomes
"the coordinator node of the primary replica set", which names what connects to
what. "Back off exponentially" becomes a statement of what the reader will
observe.

---

## 5. What not to apply this to

STE is deliberately flat. Applied to text where voice is the point, it produces
correct, lifeless prose.

Do not apply it to marketing copy, documentation that is trying to teach rather
than instruct, commit messages, or anything a person reads for pleasure or
persuasion.

Do apply it to the string a program parses.

---

## 6. The limit worth stating

**Before**

> Our caching layer is designed to slot seamlessly into your existing stack with
> minimal friction and no vendor lock-in; it leverages semantic similarity to
> dramatically reduce the cache misses that traditionally plague LLM workloads.

**After**

> A normal cache matches requests by exact text. A small change in the wording
> causes a cache miss. This cache compares the meaning of a new prompt against
> the prompts that it holds. It operates with your current stack and stores no
> data outside it.

The semicolon is gone (8.1), the sentences are inside the limit (6.3), the
marketing adjectives are gone, and the sentence now says what the thing does.

But notice what did not happen: nothing was made true. The rewrite improved the
form of the claim. Whether semantic matching actually reduces cache misses for
this workload is a fact about the software, and no rewrite establishes it. STE
controls form, not substance. A paragraph with nothing to say comes out short,
clean, and still empty.
