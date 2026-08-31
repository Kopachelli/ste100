#!/usr/bin/env python3
"""ste_check - structural checks for ASD-STE100 Simplified Technical English.

Checks the rules of ASD-STE100 Issue 9 that are self-contained, and counts words
the way section 8 of the standard counts them. Each finding gives the rule
number that it comes from.

This tool does not check rules 1.1 thru 1.4, 1.6, and 9.2. The approved
dictionary in part 2 of the standard defines those rules, and this project does
not include the dictionary. Refer to references/dictionary-and-scope.md.

Usage:
    ste_check.py FILE [FILE ...]
    ste_check.py --type procedure FILE
    cat text.md | ste_check.py -
    ste_check.py --json --glossary glossary.json FILE

No third-party packages. Python 3.9 or later.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from typing import Iterable, Optional

# --------------------------------------------------------------------------
# Word counting (rules 8.4 thru 8.7)
# --------------------------------------------------------------------------

# Units that count as one word together with the number before them (rule 8.6).
UNIT_WORDS = {
    "mm", "cm", "m", "km", "um", "nm", "in", "in.", "ft", "yd", "mi", "sq.in.",
    "kg", "g", "mg", "lb", "lbs", "oz",
    "l", "ml", "cc", "gal", "qt",
    "psi", "psig", "kpa", "mpa", "pa", "bar", "atm", "torr",
    "kn", "lbf", "nm",
    "a", "ma", "v", "mv", "kv", "w", "kw", "mw", "hp", "va", "ah",
    "hz", "khz", "mhz", "ghz", "rpm", "db",
    "s", "sec", "ms", "us", "min", "h", "hr", "hrs",
    "k", "c", "f",
    "%", "ohm", "ohms", "volt", "volts", "ampere", "amperes", "amp", "amps",
    "watt", "watts", "hertz", "degree", "degrees", "percent",
    "meter", "meters", "millimeter", "millimeters",
    "centimeter", "centimeters", "inch", "inches", "foot", "feet",
    "kilogram", "kilograms", "gram", "grams", "pound", "pounds",
    "liter", "liters", "second", "seconds", "minute", "minutes",
    "hour", "hours", "day", "days", "month", "months", "year", "years",
    "knot", "knots", "mile", "miles", "newton", "newtons", "joule", "joules",
    "a.m.", "p.m.", "am", "pm",
}

# Words that stay part of the unit, for example "10 degrees Celsius".
UNIT_TAIL = {"celsius", "fahrenheit", "kelvin", "centigrade"}

# Abbreviations whose period does not end a sentence.
NON_TERMINAL_ABBREV = {
    "no.", "nos.", "fig.", "figs.", "para.", "paras.", "ref.", "refs.",
    "approx.", "max.", "min.", "vol.", "ch.", "sec.", "p.", "pp.", "in.",
    "a.m.", "p.m.", "e.g.", "i.e.", "etc.", "cf.", "viz.", "vs.", "st.",
    "mr.", "mrs.", "ms.", "dr.", "inc.", "ltd.", "co.", "corp.", "sq.in.",
}

LIST_MARKER = re.compile(r"^\s*(?:[-*•–]|\(?[0-9]{1,3}[.)]|\(?[a-zA-Z][.)])\s+")
SAFETY_LABEL = re.compile(
    r"^\s*(WARNING|CAUTION|DANGER|NOTICE|ATTENTION)\s*[:.]\s*", re.IGNORECASE
)
NOTE_LABEL = re.compile(r"^\s*(NOTE|NOTES)\s*[:.]\s*", re.IGNORECASE)

STRIP_CHARS = ",.;:!?()[]{}\"'—–“”‘’"


def _strip_labels(text: str) -> str:
    """Remove a leading step marker or a WARNING, CAUTION, or NOTE label.

    Rule 8.6 tells you not to count the numbers that identify paragraphs or work
    steps. The word counts that the standard gives for its own safety examples
    also do not include the label.
    """
    out = LIST_MARKER.sub("", text, count=1)
    out = SAFETY_LABEL.sub("", out, count=1)
    out = NOTE_LABEL.sub("", out, count=1)
    return out


def _mask_groups(text: str, collapse: Iterable[str] = ()) -> str:
    """Replace each group that counts as one word with one token.

    Rule 8.5: text in parentheses counts as one word.
    Rule 8.6: quoted text counts as one word.
    Glossary entries (titles, placards, proper nouns) also count as one word.
    """
    for phrase in sorted(collapse, key=len, reverse=True):
        if phrase:
            text = re.sub(re.escape(phrase), " COLLAPSED ", text)
    text = re.sub(r"\([^()]*\)", " PAREN ", text)
    text = re.sub(r"[\"“][^\"”]{0,300}[\"”]", " QUOTED ", text)
    return text


def _merge_number_units(tokens: list) -> list:
    """Join a number with the unit after it, and join "No." with its number.

    Rule 8.6: a number together with its unit of measurement counts as one word,
    and an alphanumeric identifier counts as one word.
    """
    merged = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        low = tok.lower().strip(STRIP_CHARS)
        is_number = bool(re.fullmatch(r"[+-]?\d+(?:[.,]\d+)*(?:/\d+)?", low))
        if is_number and i + 1 < len(tokens):
            nxt_full = tokens[i + 1].lower()
            nxt = nxt_full.strip(STRIP_CHARS)
            is_unit = (
                nxt in UNIT_WORDS
                or nxt_full in UNIT_WORDS
                or bool(re.fullmatch(r"[°℃℉][cfk]?", nxt))
                or bool(re.fullmatch(r"[µμ]?[a-z]{1,6}/[a-z]{1,10}", nxt))
            )
            if is_unit:
                step = 2
                if (i + 2 < len(tokens)
                        and tokens[i + 2].lower().strip(STRIP_CHARS) in UNIT_TAIL):
                    step = 3
                merged.append("".join(tokens[i:i + step]))
                i += step
                continue
        if low in {"no", "nos"} and tok.lower().strip() in {"no.", "nos."} \
                and i + 1 < len(tokens):
            merged.append(tokens[i] + tokens[i + 1])
            i += 2
            continue
        merged.append(tok)
        i += 1
    return merged


def ste_word_count(sentence: str, collapse: Iterable[str] = ()) -> int:
    """Count the words in one sentence under the rules of section 8."""
    text = _strip_labels(sentence)
    text = _mask_groups(text, collapse)
    raw = [t for t in re.split(r"\s+", text) if t]
    tokens = [t for t in raw if t.strip(STRIP_CHARS)]
    tokens = _merge_number_units(tokens)
    return len(tokens)


# --------------------------------------------------------------------------
# Sentence and block splitting
# --------------------------------------------------------------------------

def split_sentences(block: str) -> list:
    """Split a block into sentences.

    Rule 8.4: in a vertical list, a colon has the same effect on word count as a
    period. Thus a colon ends the sentence.
    """
    text = block.strip()
    if not text:
        return []
    parts = []
    buf = ""
    for i, ch in enumerate(text):
        buf += ch
        if ch in ".!?":
            words = buf.split()
            tail = words[-1].lower() if words else ""
            single_letter = bool(re.fullmatch(r"[a-z]\.", tail))
            if tail not in NON_TERMINAL_ABBREV and not single_letter:
                nxt = text[i + 1:i + 2]
                if nxt in ("", " ", "\t", "\n", '"', ")"):
                    parts.append(buf.strip())
                    buf = ""
        elif ch == ":":
            parts.append(buf.strip())
            buf = ""
    if buf.strip():
        parts.append(buf.strip())
    return [p for p in parts if p.strip(" .:—-")]


@dataclass
class Block:
    text: str
    line: int
    is_list_item: bool
    kind: str  # procedure | description | safety | note | machine


# Common base-form verbs, written for this project.
# This is not ASD's list of approved verbs and does not reproduce it.
IMPERATIVE_VERBS = {
    "add", "adjust", "align", "apply", "attach", "bleed", "calibrate", "cancel",
    "change", "check", "clean", "clear", "close", "connect", "continue", "copy",
    "cut", "delete", "disconnect", "discard", "do", "drain", "eject", "enter",
    "examine", "extend", "fill", "find", "flush", "hold", "identify", "increase",
    "inflate", "install", "isolate", "keep", "lift", "listen", "lock", "look",
    "loosen", "lower", "lubricate", "make", "measure", "monitor", "move", "obey",
    "open", "operate", "paint", "polish", "prepare", "press", "pull", "push",
    "put", "read", "record", "refer", "release", "remove", "repair", "replace",
    "retract", "run", "seal", "select", "send", "set", "show", "start",
    "stop", "supply", "tag", "tighten", "torque", "touch", "transmit", "try",
    "tune", "turn", "unlock", "use", "wait", "wear", "write", "verify", "wipe",
}

FUNCTION_WORDS = {
    "a", "an", "the", "and", "but", "or", "if", "then", "thus", "of", "to", "in",
    "on", "at", "by", "for", "with", "from", "into", "onto", "over", "under",
    "above", "below", "before", "after", "during", "while", "when", "that",
    "this", "these", "those", "it", "its", "you", "your", "we", "our", "they",
    "them", "their", "is", "are", "was", "were", "be", "been", "being", "can",
    "cannot", "must", "will", "not", "no", "as", "than", "there", "each", "all",
    "more", "less", "most", "other", "same", "also", "only", "again", "because",
    "make", "sure", "do", "does", "did", "has", "have", "had", "use", "used",
    "which", "who", "what", "how", "where", "why", "so", "such", "any", "some",
    "across", "through", "between", "along", "around", "behind", "beside",
    "beyond", "near", "until", "without", "within", "against", "toward",
    "towards", "per", "via", "upon", "about", "off", "out", "up", "down",
    "back", "both", "either", "neither", "every", "another", "few", "many",
    "several", "next", "last", "first", "one", "two", "three", "four", "five",
}

# Endings that are part of the word, not a plural or a third-person "-s".
_S_ENDINGS_OK = ("ss", "us", "is", "as", "ys", "os")

IRREGULAR_PARTICIPLES = {
    "been", "become", "begun", "blown", "broken", "brought", "built", "caught",
    "chosen", "done", "drawn", "driven", "eaten", "fallen", "felt", "found",
    "frozen", "given", "gone", "grown", "held", "hung", "kept", "known", "left",
    "lost", "made", "meant", "met", "paid", "seen", "sent", "shown", "shut",
    "sold", "spoken", "spent", "split", "struck", "sunk", "swung", "taken",
    "taught", "thrown", "told", "torn", "understood", "worn", "written",
}

# "-ing" words that STE permits, plus common technical nouns and technical-noun
# modifiers. Extend this with the "ing_nouns" key of a glossary file.
ING_ALLOWED = {
    "lighting", "opening", "openings", "routing", "servicing", "mating",
    "missing", "remaining", "something", "during", "nothing", "anything",
    "everything", "air-conditioning", "conditioning", "degreasing", "grinding",
    "polishing", "sanding", "switching", "welding", "cleaning", "testing",
    "handling", "packaging", "shipping", "troubleshooting", "bearing",
    "bearings", "ring", "rings", "spring", "springs", "string", "strings",
    "thing", "things", "wing", "wings", "engineering", "warning", "warnings",
    "ceiling", "housing", "housings", "casing", "coating", "coatings", "tubing",
    "wiring", "bushing", "fitting", "fittings", "setting", "settings",
    "reading", "readings", "drawing", "drawings", "heading", "headings",
    "meaning", "building", "training", "briefing", "logging", "sealing",
    "plating", "machining", "landing", "boarding", "docking", "mooring",
    "rigging", "labeling", "monitoring", "sampling", "swing", "king",
    "embedding", "tuning", "learning", "sizing", "timing", "wording",
}

# Verb plus particle. The meaning is not predictable from the parts (rule 9.3).
# PUT ON, COME ON, and GO OFF are approved in the dictionary and are not here.
PHRASAL_VERBS = {
    ("take", "off"), ("take", "out"), ("take", "up"), ("take", "over"),
    ("put", "out"), ("put", "off"), ("put", "up"), ("put", "away"),
    ("give", "off"), ("give", "up"), ("give", "in"), ("give", "out"),
    ("set", "up"), ("set", "off"), ("set", "out"), ("set", "aside"),
    ("shut", "down"), ("shut", "off"), ("shut", "up"),
    ("turn", "on"), ("turn", "off"), ("turn", "over"), ("turn", "out"),
    ("turn", "up"), ("turn", "down"),
    ("carry", "out"), ("bring", "about"), ("bring", "up"),
    ("look", "up"), ("look", "into"), ("look", "after"), ("look", "over"),
    ("check", "out"), ("check", "in"), ("back", "up"), ("break", "down"),
    ("break", "up"), ("break", "out"), ("blow", "out"), ("blow", "off"),
    ("burn", "out"), ("call", "off"), ("cut", "off"), ("cut", "out"),
    ("fill", "in"), ("fill", "out"), ("find", "out"), ("get", "out"),
    ("get", "in"), ("get", "off"), ("get", "on"), ("get", "through"),
    ("go", "through"), ("go", "down"), ("go", "up"), ("go", "over"),
    ("hold", "on"), ("hold", "up"), ("keep", "on"), ("let", "down"),
    ("make", "up"), ("pick", "up"), ("pull", "out"), ("pull", "off"),
    ("push", "in"), ("run", "out"), ("send", "out"), ("spin", "up"),
    ("spin", "down"), ("start", "up"), ("tear", "down"), ("throw", "away"),
    ("throw", "out"), ("try", "out"), ("wear", "out"), ("work", "out"),
    ("write", "down"), ("drop", "off"), ("hand", "over"), ("hook", "up"),
    ("kick", "off"), ("lay", "out"), ("line", "up"), ("point", "out"),
    ("reach", "out"), ("roll", "out"), ("roll", "back"), ("sort", "out"),
    ("stand", "by"), ("sum", "up"), ("switch", "on"), ("switch", "off"),
    ("top", "up"), ("wind", "up"), ("wipe", "out"), ("dive", "into"),
    ("plug", "in"), ("log", "in"), ("log", "out"), ("sign", "in"),
    ("sign", "up"), ("back", "off"), ("boot", "up"), ("fire", "up"),
    ("ramp", "up"), ("scale", "up"), ("scale", "down"), ("ship", "out"),
    ("figure", "out"), ("hang", "on"), ("map", "out"), ("flesh", "out"),
}

_PARTICIPLES = "|".join(sorted(IRREGULAR_PARTICIPLES))

# Extra base verbs used only to stop a multi-word noun run (rule 2.1). They are
# not part of the imperative set that classifies a block as a procedure.
_EXTRA_VERBS = {
    "give", "have", "include", "contain", "comprise", "become", "occur",
    "remain", "come", "go", "prevent", "allow", "cause", "help", "need",
    "want", "know", "think", "mean", "tell", "get", "take", "work", "provide",
    "support", "report", "return", "require", "follow", "let", "put", "hold",
    "send", "show", "attach", "align", "engage", "supply", "count", "agree",
    "accept", "collect", "compare", "divide", "protect", "receive", "reject",
}


def _verb_forms(bases):
    forms = set()
    for base in bases:
        forms.update({base, base + "s", base + "ed", base + "d", base + "es"})
        if base.endswith("y"):
            forms.add(base[:-1] + "ies")
        if base.endswith("e"):
            forms.add(base[:-1] + "ing")
        else:
            forms.add(base + "ing")
    return forms


# Tokens that end a run of stacked nouns and adjectives.
NOUN_RUN_STOPPERS = (
    FUNCTION_WORDS
    | _verb_forms(IMPERATIVE_VERBS)
    | _verb_forms(_EXTRA_VERBS)
    | IRREGULAR_PARTICIPLES
    | {"gives", "gave", "goes", "went", "took", "made", "said", "must", "may",
       "might", "shall", "should", "would", "could", "cannot", "always",
       "never", "usually", "then", "thus", "also", "here", "now"}
)

CONTRACTIONS = re.compile(
    r"\b(?:do|does|did|is|are|was|were|has|have|had|would|should|could|will|"
    r"can|must|might|need|ought|wo|ai)n[’']t\b"
    r"|\b(?:it|that|there|here|what|who|let)[’']s\b"
    r"|\b(?:we|you|they)[’']re\b"
    r"|\b(?:i|we|you|they|it)[’'](?:ll|ve|d|m)\b",
    re.IGNORECASE,
)

BRITISH_SPELLING = {
    "colour": "color", "colours": "colors", "behaviour": "behavior",
    "favour": "favor", "labour": "labor", "honour": "honor",
    "neighbour": "neighbor", "vapour": "vapor", "odour": "odor",
    "centre": "center", "centres": "centers", "metre": "meter",
    "metres": "meters", "litre": "liter", "litres": "liters",
    "fibre": "fiber", "fibres": "fibers", "theatre": "theater",
    "organise": "organize", "organisation": "organization",
    "realise": "realize", "recognise": "recognize", "analyse": "analyze",
    "catalogue": "catalog", "dialogue": "dialog", "programme": "program",
    "licence": "license", "practise": "practice", "aluminium": "aluminum",
    "tyre": "tire", "tyres": "tires", "grey": "gray", "jewellery": "jewelry",
    "storey": "story", "kerb": "curb", "plough": "plow", "sulphur": "sulfur",
    "aeroplane": "airplane", "manoeuvre": "maneuver", "draught": "draft",
    "mould": "mold", "travelling": "traveling", "modelling": "modeling",
    "cancelled": "canceled", "labelled": "labeled", "signalling": "signaling",
    "defence": "defense", "offence": "offense", "sceptical": "skeptical",
}

LATIN_ABBREV = re.compile(
    r"(?<![A-Za-z])(e\.g\.|i\.e\.|etc\.|viz\.|cf\.|et al\.|N\.B\.)", re.IGNORECASE
)
GENDERED = re.compile(r"\b(he|she|him|her|hers|his|himself|herself)\b", re.IGNORECASE)
GENDERED_NOUN = re.compile(
    r"\b(man|men|woman|women|manned|manpower|manhour|manhours)\b", re.IGNORECASE
)
DROPPED_THAT = re.compile(
    r"\b(make sure|makes sure|made sure|show|shows|showed|recommend|recommends)\s+"
    r"(?!that\b|how\b)(the|a|an|this|these|those|it|you|we|they|there)\b",
    re.IGNORECASE,
)
PRESENT_PERFECT = re.compile(
    r"\b(have|has|had)\s+(?:not\s+|never\s+|already\s+|\w+ly\s+)?"
    r"(been|" + _PARTICIPLES + r"|\w+ed)\b",
    re.IGNORECASE,
)
# A modal in front of the perfect form carries the writer's confidence, not only
# a tense. Refer to the Boundaries section of SKILL.md.
MODAL_PERFECT = re.compile(
    r"\b(may|might|could|can|must|should|would|will)\s+(?:not\s+)?have\s+"
    r"(?:been\s+)?(?:\w+ly\s+)?(\w+ed|" + _PARTICIPLES + r")\b",
    re.IGNORECASE,
)
PROGRESSIVE = re.compile(
    r"\b(am|is|are|was|were|be|been|being)\s+(?:not\s+)?(\w+ing)\b", re.IGNORECASE
)
MODAL_PASSIVE = re.compile(
    r"\b(can|could|must|will|shall|should|may|might)\s+(?:not\s+)?be\s+"
    r"(?:\w+ly\s+)?(\w+ed|" + _PARTICIPLES + r")\b",
    re.IGNORECASE,
)
INFINITIVE_PASSIVE = re.compile(
    r"\b(is|are|was|were)\s+to\s+be\s+(\w+ed|" + _PARTICIPLES + r")\b", re.IGNORECASE
)
PASSIVE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+(?:not\s+)?(?:\w+ly\s+)?"
    r"(\w+ed|" + _PARTICIPLES + r")\b(\s+by\b)?",
    re.IGNORECASE,
)

CAPS = {
    "procedure": 20,     # rule 5.1
    "safety": 20,        # rule 5.1 is applicable to safety instructions
    "description": 25,   # rule 6.3
    "note": 25,          # rule 5.5
    "machine": 25,       # a machine-facing string obeys the descriptive limit
}

NOT_CHECKED = ["1.1", "1.2", "1.3", "1.4", "1.6", "9.2"]


@dataclass
class Finding:
    rule: str
    severity: str  # violation | review
    line: int
    message: str
    excerpt: str = ""


@dataclass
class Report:
    findings: list = field(default_factory=list)
    blocks: int = 0
    sentences: int = 0
    types: dict = field(default_factory=dict)

    def add(self, rule, severity, line, message, excerpt=""):
        self.findings.append(
            Finding(rule, severity, line, message, excerpt.strip()[:110])
        )


# --------------------------------------------------------------------------
# Block classification
# --------------------------------------------------------------------------

def classify(text: str, forced: Optional[str]) -> str:
    if forced and forced != "auto":
        return forced
    if SAFETY_LABEL.match(text):
        return "safety"
    if NOTE_LABEL.match(text):
        return "note"
    body = _strip_labels(text).strip()
    words = re.split(r"[\s,]+", body, maxsplit=1)
    head = words[0].lower().strip(STRIP_CHARS) if words and words[0] else ""
    if head in IMPERATIVE_VERBS:
        return "procedure"
    if head in {"if", "when", "before", "after", "while"} and LIST_MARKER.match(text):
        return "procedure"
    return "description"


def parse_blocks(text: str, forced: Optional[str]) -> list:
    blocks = []
    buf = []
    buf_line = 1
    line_no = 0

    def flush():
        if buf:
            joined = " ".join(buf)
            blocks.append(Block(joined, buf_line, False, classify(joined, forced)))
            buf.clear()

    for raw in text.splitlines():
        line_no += 1
        stripped = raw.strip()
        if not stripped:
            flush()
            continue
        if stripped.startswith("#") or re.fullmatch(r"[-=|+_\s]{3,}", stripped):
            flush()
            continue
        if stripped.startswith("```") or stripped.startswith("|"):
            flush()
            continue
        if (LIST_MARKER.match(raw) or SAFETY_LABEL.match(stripped)
                or NOTE_LABEL.match(stripped)):
            flush()
            is_item = bool(LIST_MARKER.match(raw))
            blocks.append(Block(stripped, line_no, is_item, classify(stripped, forced)))
            continue
        if not buf:
            buf_line = line_no
        buf.append(stripped)
    flush()
    return blocks


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_text(text: str, forced: Optional[str] = None,
               glossary: Optional[dict] = None) -> Report:
    glossary = glossary or {}
    collapse = (list(glossary.get("titles", []))
                + list(glossary.get("placards", []))
                + list(glossary.get("proper_nouns", [])))
    ing_ok = ING_ALLOWED | {w.lower() for w in glossary.get("ing_nouns", [])}
    terms = glossary.get("terms", {})

    report = Report()
    blocks = parse_blocks(text, forced)
    report.blocks = len(blocks)
    list_run = []

    for block in blocks:
        kind = block.kind
        line = block.line
        body = block.text
        report.types[kind] = report.types.get(kind, 0) + 1

        # Rule 8.1 - the semicolon is not permitted.
        for m in re.finditer(r";", body):
            report.add("8.1", "violation", line,
                       "Semicolon is not permitted. Write two sentences.", body)

        # Rule 4.2 - do not use contractions.
        for m in CONTRACTIONS.finditer(body):
            report.add("4.2", "violation", line,
                       'Contraction "%s". Write the words in full.' % m.group(0), body)

        # Rule 1.14 - American English spelling.
        for tok in re.findall(r"[A-Za-z][A-Za-z\-']+", body):
            repl = BRITISH_SPELLING.get(tok.lower())
            if repl:
                report.add("1.14", "review", line,
                           'British spelling "%s". American English uses "%s". '
                           "Quoted text and proper nouns keep their spelling."
                           % (tok, repl), body)

        # GR-6 - Latin abbreviations.
        for m in LATIN_ABBREV.finditer(body):
            report.add("GR-6", "violation", line,
                       'Latin abbreviation "%s". Use English words.' % m.group(0), body)

        # GR-7 - inclusive language.
        for m in GENDERED.finditer(body):
            report.add("GR-7", "violation", line,
                       'Gender-specific pronoun "%s" is not permitted.' % m.group(0),
                       body)
        for m in GENDERED_NOUN.finditer(body):
            report.add("GR-7", "review", line,
                       '"%s" is permitted only when the context makes it necessary, '
                       "for example a medical text." % m.group(0), body)

        # GR-1 - the conjunction "that".
        for m in DROPPED_THAT.finditer(body):
            report.add("GR-1", "review", line,
                       'Add "that" after "%s" to show where the subordinate clause '
                       "starts." % m.group(1), body)

        # Rule 9.3 - do not make phrasal verbs.
        tokens = [t.lower().strip(STRIP_CHARS) for t in body.split()]
        for i in range(len(tokens) - 1):
            pair = (tokens[i], tokens[i + 1])
            if pair in PHRASAL_VERBS:
                report.add("9.3", "violation", line,
                           'Phrasal verb "%s %s". Use one verb that has the meaning '
                           "you want." % pair, body)

        # Rule 3.5 - the "-ing" form.
        for tok in re.findall(r"\b[A-Za-z][A-Za-z\-]{3,}ing\b", body):
            if tok.lower() not in ing_ok:
                report.add("3.5", "review", line,
                           '"%s" is an "-ing" form. STE permits it only as a technical '
                           "noun or as a modifier in a technical noun." % tok, body)

        # Rules 3.2 and 3.4 - verb forms and tenses.
        hedged = []
        for m in MODAL_PERFECT.finditer(body):
            hedged.append(m.span())
            report.add("3.2", "review", line,
                       'Compound tense "%s" after a modal verb. Rule 3.2 excludes '
                       "this form, but the modal carries the writer's confidence. "
                       "Keep the hedge and flag the departure, or rewrite the "
                       "sentence so that a simple tense states the same degree of "
                       "certainty." % m.group(0).strip(), body)
        for m in PRESENT_PERFECT.finditer(body):
            if any(start <= m.start() < end for start, end in hedged):
                continue
            report.add("3.2", "violation", line,
                       'Compound tense "%s". Use the simple past tense.'
                       % m.group(0).strip(), body)
        for m in PROGRESSIVE.finditer(body):
            if m.group(2).lower() not in ing_ok:
                report.add("3.2", "violation", line,
                           'Progressive form "%s". Use a simple tense.'
                           % m.group(0).strip(), body)
        for m in MODAL_PASSIVE.finditer(body):
            report.add("3.4", "violation", line,
                       'Complex verb construction "%s". Write the sentence in the '
                       "active voice." % m.group(0).strip(), body)
        for m in INFINITIVE_PASSIVE.finditer(body):
            report.add("3.4", "violation", line,
                       'Complex verb construction "%s". Write the sentence in the '
                       "active voice." % m.group(0).strip(), body)

        # Rule 3.6 - the active voice.
        for m in PASSIVE.finditer(body):
            span = m.group(0)
            if MODAL_PASSIVE.search(span) or PROGRESSIVE.search(span):
                continue
            has_agent = bool(m.group(3))
            severity = "violation" if (kind in ("procedure", "safety") or has_agent) \
                else "review"
            if has_agent:
                note = ' The agent comes after "by", so the agent is known.'
            else:
                note = (" In descriptive text, the passive voice is permitted only "
                        "when the agent is unknown. A past participle after "
                        '"be" can also be an adjective (rule 3.3).')
            report.add("3.6", severity, line,
                       'Passive voice: "%s".%s' % (span.strip(), note), body)

        # Rule 5.5 - notes give information only.
        if kind == "note":
            head = _strip_labels(body).split()
            if head and head[0].lower().strip(STRIP_CHARS) in IMPERATIVE_VERBS:
                report.add("5.5", "violation", line,
                           "A note must not use the imperative form. Make it a work "
                           "step.", body)
            if re.search(r"\b(must|do not|shall)\b", body, re.IGNORECASE):
                report.add("5.5", "review", line,
                           "A note must not give instructions, requirements, or limits. "
                           "Move this to a work step or a safety instruction.", body)

        # Rules 7.2 and 7.3 - safety instructions.
        if kind == "safety":
            core = SAFETY_LABEL.sub("", body).strip()
            words = core.split()
            first = words[0].lower().strip(STRIP_CHARS) if words else ""
            starts_ok = first in IMPERATIVE_VERBS or first in {
                "always", "never", "if", "when", "while", "before", "after"}
            if not starts_ok:
                report.add("7.2", "review", line,
                           "Start a safety instruction with a clear command or "
                           "condition.", body)
            if not re.search(
                r"\b(can cause|will cause|causes|risk|injury|death|damage|corrosion|"
                r"explosion|can occur|will occur|is dangerous|are dangerous|poisonous)\b",
                core, re.IGNORECASE
            ):
                report.add("7.3", "review", line,
                           "Give an explanation that shows the risk or the possible "
                           "result.", body)

        # Rule 4.3 - vertical lists.
        if block.is_list_item:
            list_run.append(block)
            item = body.rstrip()
            if item.endswith(",") or item.endswith(";"):
                report.add("4.3", "violation", line,
                           "Do not put a comma or a semicolon at the end of an item in "
                           "a vertical list.", body)
            core = LIST_MARKER.sub("", item, count=1)
            if core and core[0].isalpha() and core[0].islower():
                report.add("4.3", "review", line,
                           "Start each item in a vertical list with an uppercase "
                           "letter.", body)
        else:
            _flush_list(list_run, report)
            list_run = []

        # Rule 2.1 - multi-word nouns of no more than three words.
        masked = _strip_labels(_mask_groups(body, collapse))
        for run in _noun_runs(masked):
            report.add("2.1", "review", line,
                       'Possible multi-word noun of %d words: "%s". The limit is '
                       "three words." % (len(run), " ".join(run)), body)

        # Rules 1.11 and 9.4 - one technical noun for one item.
        low = body.lower()
        for approved, synonyms in terms.items():
            for syn in synonyms:
                if re.search(r"\b" + re.escape(syn.lower()) + r"\b", low):
                    report.add("1.11", "violation", line,
                               '"%s" refers to the same item as "%s". Use one technical '
                               "noun for one item." % (syn, approved), body)

        # Sentence length and paragraph length.
        sentences = split_sentences(body)
        report.sentences += len(sentences)
        cap = CAPS.get(kind, 25)
        rule = {"procedure": "5.1", "safety": "5.1", "note": "5.5"}.get(kind, "6.3")
        for sent in sentences:
            count = ste_word_count(sent, collapse)
            if count > cap:
                report.add(rule, "violation", line,
                           "%d words in a %s sentence. The limit is %d. The word count "
                           "obeys rules 8.4 thru 8.7." % (count, kind, cap), sent)
        if kind == "description" and not block.is_list_item and len(sentences) > 6:
            report.add("6.6", "violation", line,
                       "%d sentences in one paragraph. The limit is six."
                       % len(sentences), body)

        # Rule 5.2 - one instruction in each sentence.
        if kind == "procedure":
            for sent in sentences:
                core = _strip_labels(sent)
                verbs = [w for w in re.findall(r"\b[a-z]+\b", core.lower())
                         if w in IMPERATIVE_VERBS]
                if re.search(r"\bthen\b", core, re.IGNORECASE) and len(verbs) > 1:
                    report.add("5.2", "review", line,
                               "Two actions that do not occur at the same time. Write "
                               "one instruction in each sentence.", sent)

    _flush_list(list_run, report)
    return report


def _noun_runs(masked: str, limit: int = 3) -> list:
    """Find runs of stacked nouns and adjectives longer than the limit (rule 2.1).

    This is a heuristic. It has no part-of-speech tagger, so it finds runs of
    words that are not function words and not recognized verb forms. Findings
    from this check are always reported for review, never as violations.

    A run also stops at a word that ends in "-s" unless that word is last. In a
    stack of nouns, only the head noun at the end is usually plural, so an
    "-s" word in the middle is more often a third-person verb.
    """
    runs = []
    current = []

    def flush(run):
        for index, word in enumerate(run[:-1]):
            low = word.lower()
            if low.endswith("s") and not low.endswith(_S_ENDINGS_OK):
                run = run[:index]
                break
        if len(run) > limit:
            runs.append(list(run))

    for raw in masked.split():
        word = raw.strip(STRIP_CHARS)
        ends_group = raw != word and raw.rstrip(STRIP_CHARS) != raw
        if (word and re.fullmatch(r"[A-Za-z][A-Za-z\-]*", word)
                and word.lower() not in NOUN_RUN_STOPPERS
                and word not in ("PAREN", "QUOTED", "COLLAPSED")):
            current.append(word)
            if ends_group:
                flush(current)
                current = []
            continue
        flush(current)
        current = []
    flush(current)
    return runs


def _flush_list(run: list, report: Report) -> None:
    if not run:
        return
    last = run[-1].text.rstrip()
    if not last.endswith("."):
        report.add("4.3", "review", run[-1].line,
                   "Put a period at the end of the last item in a vertical list.", last)


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def render(report: Report, name: str, quiet: bool) -> str:
    order = {"violation": 0, "review": 1}
    findings = sorted(report.findings, key=lambda f: (order[f.severity], f.line, f.rule))
    if quiet:
        findings = [f for f in findings if f.severity == "violation"]
    violations = sum(1 for f in report.findings if f.severity == "violation")
    reviews = sum(1 for f in report.findings if f.severity == "review")
    types = ", ".join("%s=%d" % (k, v) for k, v in sorted(report.types.items()))
    lines = [
        "# %s" % name,
        "  %d blocks (%s), %d sentences" % (report.blocks, types or "none",
                                            report.sentences),
        "  %d violations, %d to review" % (violations, reviews),
    ]
    if not findings:
        lines.append("  No findings.")
    else:
        lines.append("")
        for f in findings:
            tag = "VIOLATION" if f.severity == "violation" else "review   "
            lines.append("  %s  line %-4d rule %-5s %s" % (tag, f.line, f.rule, f.message))
            if f.excerpt:
                lines.append("      | %s" % f.excerpt)
    lines.append("")
    lines.append("  Not checked: rules %s. They need the approved dictionary of part 2."
                 % ", ".join(NOT_CHECKED))
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Structural checks for ASD-STE100 Simplified Technical English."
    )
    parser.add_argument("files", nargs="*", default=["-"],
                        help="Files to check. Use - for standard input.")
    parser.add_argument("--type", default="auto",
                        choices=["auto", "procedure", "description", "safety", "note",
                                 "machine"],
                        help="Force the text type instead of detecting it per block.")
    parser.add_argument("--glossary", help="JSON file with the project terminology.")
    parser.add_argument("--json", action="store_true", help="Write JSON.")
    parser.add_argument("--quiet", action="store_true", help="Show violations only.")
    args = parser.parse_args(argv)

    glossary = {}
    if args.glossary:
        with open(args.glossary, encoding="utf-8") as handle:
            glossary = json.load(handle)

    results = {}
    exit_code = 0
    for path in (args.files or ["-"]):
        if path == "-":
            text, name = sys.stdin.read(), "<stdin>"
        else:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            name = path
        report = check_text(text, args.type, glossary)
        results[name] = report
        if any(f.severity == "violation" for f in report.findings):
            exit_code = 1

    if args.json:
        payload = {
            name: {
                "blocks": rep.blocks,
                "sentences": rep.sentences,
                "types": rep.types,
                "findings": [asdict(f) for f in rep.findings],
                "not_checked": NOT_CHECKED,
            }
            for name, rep in results.items()
        }
        print(json.dumps(payload, indent=2))
    else:
        for name, rep in results.items():
            print(render(rep, name, args.quiet))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
