# The 53 rules and the 8 general recommendations

ASD-STE100 Issue 9, January 2025. Part 1 has nine sections that contain 53
writing rules. Section 9 also gives eight general recommendations, which are not
rules.

Every entry below is a summary written for this project. None of it reproduces
the text of the standard, and every example sentence is written here. Cite the
rule number and get the standard when you need its exact wording. Refer to
[NOTICE.md](../../../NOTICE.md).

A marker shows what this project can do with each rule:

- **[check]** — `scripts/ste_check.py` tests it
- **[judge]** — a person or a model must decide
- **[dictionary]** — needs the approved dictionary of part 2, so this project
  cannot verify it

---

## Section 1 — Words (1.1 thru 1.14)

| Rule | Summary | |
|---|---|---|
| **1.1** | Use only three kinds of word: a word approved in the dictionary, a technical noun, or a technical verb. | [dictionary] |
| **1.2** | Use an approved word only as the part of speech that the dictionary gives it. "Test" as a noun does not license "test" as a verb. | [dictionary] |
| **1.3** | Use an approved word only with its approved meaning. The dictionary meaning is often narrower than ordinary English. | [dictionary] |
| **1.4** | Use only the verb forms and adjective forms that the dictionary lists. | [dictionary] |
| **1.5** | A word that is not in the dictionary is permitted when it fits one of 22 technical noun categories. Refer to `dictionary-and-scope.md`. | [judge] |
| **1.6** | A word listed as not approved can still be used when it is a technical noun or part of one, in that context only. | [dictionary] |
| **1.7** | Do not use a technical noun as a verb. Write "Apply oil to the surface", not "Oil the surface". | [judge] |
| **1.8** | Use the technical noun that your company, industry, or subject field already approves. | [judge] |
| **1.9** | When you must invent a technical noun, keep it short (three words at most) and easy to understand. | [judge] |
| **1.10** | Do not use regional words, slang, or jargon as technical nouns. "Do not brick the router" fails this rule. | [judge] |
| **1.11** | Use one technical noun for one item. Do not call the same part an actuator in one step and a control unit in the next. | [check] |
| **1.12** | A verb that is not in the dictionary is permitted when it fits one of four technical verb categories. Refer to `dictionary-and-scope.md`. | [judge] |
| **1.13** | Do not use a technical verb as a noun. The past participle as an adjective is permitted: "the reamed hole". | [judge] |
| **1.14** | Use American English spelling, unless a contract or a style guide says otherwise. Do not change the spelling inside quoted text. | [check] |

## Section 2 — Multi-word nouns (2.1 thru 2.2)

| Rule | Summary | |
|---|---|---|
| **2.1** | A multi-word noun has three words at most. Longer stacks hide how the words connect, and the head noun comes last in English but first in many other languages. Use prepositions to break them up. | [check] |
| **2.2** | When an official technical noun is longer than three words, write it in full the first time. Then either give a shorter form and use that, or join the words that act as one unit with hyphens. Do not hyphenate everything. | [judge] |

## Section 3 — Verbs (3.1 thru 3.7)

| Rule | Summary | |
|---|---|---|
| **3.1** | Use only the verb forms that the dictionary gives for each approved verb. | [dictionary] |
| **3.2** | Six forms are permitted: infinitive, imperative, simple present, simple past, simple future, and the past participle used as an adjective. Present perfect, past perfect, and progressive forms are not permitted. | [check] |
| **3.3** | The past participle as an adjective is permitted before a noun, or after "be", "become", or "stay". This shows a condition and is not the passive voice. | [judge] |
| **3.4** | Do not build compound verbs with auxiliaries. "can be adjusted", "is to be installed", and "must be adjusted" all need rewriting into the active voice. | [check] |
| **3.5** | An "-ing" form is permitted only as a technical noun, or as a modifier inside a technical noun: "grinding wheel", "the opening in the panel". Never as a verb form. | [check] |
| **3.6** | Use the active voice. In descriptive writing the passive voice is permitted only when the agent is genuinely unknown. Four methods to convert: promote the agent after "by"; replace a weak infinitive with the real verb; use the imperative in procedures; use "you" or "we" as the subject. | [check] |
| **3.7** | Describe an action with a verb, not with a noun made from a verb. "The ohmmeter shows 450 ohms", not "The ohmmeter gives an indication of 450 ohms". | [judge] |

## Section 4 — Sentences (4.1 thru 4.5)

| Rule | Summary | |
|---|---|---|
| **4.1** | Write short, clear, concrete sentences. One topic per descriptive sentence. Do not write abstractly: "When the temperature increases, the cure time decreases" beats "Different temperatures will change the cure time". | [judge] |
| **4.2** | Do not omit words or use contractions to shorten a sentence. Keep the subject, the verb, and the article. A shorter sentence that drops words is not clearer, it is ambiguous. | [check] |
| **4.3** | Use a vertical list for complex content. Colon before the list. Each item starts with an uppercase letter. Period after a full-sentence item and after the last item. No comma or semicolon at the end of an item. Do not mix procedural and descriptive items in one list. | [check] |
| **4.4** | Use connecting words and phrases ("and", "but", "then", "thus", "as a result", "at the same time") to link related sentences. | [judge] |
| **4.5** | Keep the article or the demonstrative adjective before a noun. Omit it only for general concepts, and never before an alphanumeric identifier: write "Tag circuit breaker 36L7", not "the circuit breaker 36L7". | [judge] |

## Section 5 — Procedural writing (5.1 thru 5.5)

| Rule | Summary | |
|---|---|---|
| **5.1** | 20 words maximum in a procedural sentence. Warnings and cautions obey this too. Notes do not; they get 25. | [check] |
| **5.2** | One instruction per sentence, unless two actions happen at the same time or a result follows an action immediately. | [check] |
| **5.3** | Write instructions in the imperative. Do not put "must" before an imperative unless the instruction is safety-critical or states an important condition. | [judge] |
| **5.4** | When the reader must know a condition first, write the condition first, then a comma, then the command. The position of the comma changes the meaning, so place it deliberately. | [judge] |
| **5.5** | A note gives information only. No imperative, no instruction, no requirement, no limit, no tolerance. 25 words per sentence. Test a procedure by reading it without the notes: if it still works, the notes are correct. | [check] |

## Section 6 — Descriptive writing (6.1 thru 6.6)

| Rule | Summary | |
|---|---|---|
| **6.1** | Give information gradually, one subject per sentence. | [judge] |
| **6.2** | Repeat key words and key phrases to connect sentences. Changing the term to avoid repetition breaks the chain the reader is following. | [judge] |
| **6.3** | 25 words maximum in a descriptive sentence. | [check] |
| **6.4** | Use paragraphs to group related information. Start each with a topic sentence. | [judge] |
| **6.5** | One topic per paragraph. Reading only the topic sentences should produce a usable outline of the text. | [judge] |
| **6.6** | Six sentences maximum per paragraph. | [check] |

## Section 7 — Safety instructions (7.1 thru 7.3)

| Rule | Summary | |
|---|---|---|
| **7.1** | Identify the level of risk with the right word. A **warning** is a risk of injury or death. A **caution** is a risk of damage to objects. Both together means a warning. Do the risk analysis first. | [judge] |
| **7.2** | Open a safety instruction with a clear command or a clear condition, not with an abstract statement. | [check] |
| **7.3** | Say what happens if the reader does not obey. A named consequence ("explosion", "injury", "corrosion") makes the reader careful; an abstract statement does not. | [check] |

## Section 8 — Punctuation and word count (8.1 thru 8.7)

| Rule | Summary | |
|---|---|---|
| **8.1** | Every standard English punctuation mark is permitted **except the semicolon**. The semicolon is banned because it lets writers build very long sentences and is hard to use correctly. The em dash is not banned. | [check] |
| **8.2** | Use hyphens to connect directly related words: adjective groups before a noun, two-word numbers, letter-plus-noun shapes ("L-shaped bracket"), verbs built on another part of speech ("heat-treat"), and vowel-vowel prefix joins ("de-icing"). A hyphen is not a dash. | [judge] |
| **8.3** | Parentheses are permitted for seven purposes: references to figures or text, item identifiers, work-step identifiers, abbreviations, singular-and-plural at once ("the test(s)"), explanation, and alternatives. | [judge] |
| **8.4** | In a vertical list, a colon ends the sentence for word-count purposes. Each item then counts as its own sentence, under its own limit. | [check] |
| **8.5** | Text in parentheses counts as **one word** of the sentence. It also forms its own sentence, counted separately. | [check] |
| **8.6** | Each of these counts as **one word**: a number, a number with its unit, an abbreviation, an alphanumeric identifier, quoted text, a title or heading or placard or label, and a proper noun of a person, organization, or geopolitical entity. Numbers that identify paragraphs or work steps are not counted at all. | [check] |
| **8.7** | A hyphenated group counts as **one word**. | [check] |

Section 8 is what makes the 20-word and 25-word limits real. Refer to
`word-count.md`.

## Section 9 — Writing practices (9.1 thru 9.4)

| Rule | Summary | |
|---|---|---|
| **9.1** | When a word-for-word replacement does not work, rebuild the sentence. It does not work when the grammar has to change, when the replacement is meaningless, when it changes the meaning, or when the word is absent from the dictionary. | [judge] |
| **9.2** | Use each approved word correctly, in its approved meaning and part of speech. Many approved words have a narrower meaning than in ordinary English. | [dictionary] |
| **9.3** | Do not put a verb and a preposition together to make a phrasal verb. The meaning of the pair is not predictable from the parts, and both non-native readers and machine translation mishandle them. A few, with restricted meanings, are approved. | [check] |
| **9.4** | Use a consistent style. When the same kind of work step recurs, write it the same way every time. Two sentences can both obey every rule and still hurt the reader if they say the same thing differently. | [check] |

## General recommendations (GR-1 thru GR-8)

These are not rules. They prevent errors that writers make repeatedly.

| | Recommendation | |
|---|---|---|
| **GR-1** | Keep the conjunction "that". It marks where the main clause ends, and many languages cannot drop the equivalent word. "Make sure that the valve is open." | [check] |
| **GR-2** | Be careful with "with". "Install the panel with the green fasteners" has three readings. Rewrite when the context does not settle it. | [judge] |
| **GR-3** | Use pronouns only when they can refer to one thing. If a pronoun could refer to two nouns, repeat the noun. | [judge] |
| **GR-4** | Be careful with "this". Make sure the reader knows what it refers to; repeat the context when it is not certain. | [judge] |
| **GR-5** | Watch for false friends. A word that looks like one in your own language may not mean the same thing in English. | [judge] |
| **GR-6** | Do not use Latin abbreviations. Write "for example", not "e.g.". | [check] |
| **GR-7** | Use inclusive, gender-neutral language. Gender-specific pronouns are not permitted. "Man" and "woman" are not permitted unless the context requires them, for example in a medical text. | [check] |
| **GR-8** | The possessive form is permitted, but use it only when you are sure it is correct. Many languages have no equivalent. | [judge] |

## Where each rule is checked

The checker tests these rules directly:

`1.11`, `1.14`, `2.1`, `3.2`, `3.4`, `3.5`, `3.6`, `4.2`, `4.3`, `5.1`, `5.2`,
`5.5`, `6.3`, `6.6`, `7.2`, `7.3`, `8.1`, `8.4`, `8.5`, `8.6`, `8.7`, `9.3`,
`9.4`, `GR-1`, `GR-6`, `GR-7`.

It cannot test these without the approved dictionary:

`1.1`, `1.2`, `1.3`, `1.4`, `1.6`, `9.2`.

The rest need a reader.
