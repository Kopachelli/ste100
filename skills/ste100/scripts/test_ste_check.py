#!/usr/bin/env python3
"""Tests for ste_check.

The word-count tests use an unusually good oracle: ASD-STE100 Issue 9 publishes
the word count for many of its own example sentences in section 8. Each expected
number below is the number that the standard gives for that sentence. The
sentences are quoted here only as test input, in the smallest quantity that makes
the test meaningful.

Run:
    python test_ste_check.py
"""

from __future__ import annotations

import sys

from ste_check import check_text, split_sentences, ste_word_count

FAILURES = []


def check(label, got, want):
    if got != want:
        FAILURES.append("%s: got %r, want %r" % (label, got, want))


def rules_of(report):
    return {f.rule for f in report.findings}


def violations_of(report):
    return {f.rule for f in report.findings if f.severity == "violation"}


# --------------------------------------------------------------------------
# Word count, no glossary. Expected values come from section 8 of the standard.
# --------------------------------------------------------------------------

COUNT_CASES = [
    ("Make sure that the temperature in the room is 10 °C.", 10),
    ("Make sure that the temperature in the room is 10 degrees Celsius.", 10),
    ("The unit weighs 20 kg.", 4),
    ("The unit weighs 20 kilograms.", 4),
    ("The resistance must be 10 ohms.", 5),
    ("Remove the safety pin (10).", 5),
    ("Clean the surface with a soap-and-water solution.", 7),
    ("Use the trial-and-error method.", 4),
    ("Cutoff-switch power connection", 3),
    ("Main-gear-door retraction-winch handle", 3),
    ("Installation of a Business Class (B/C) Seat", 7),
    ("Hardware and Software Configuration Check of the In-Flight Entertainment "
     "(IFE) System", 11),
    ("Make sure that the EMER pushbutton switch is released "
     "(the EMER legend is off).", 10),
    ("The maintenance team does a test of this system each day at 10 a.m.", 13),
    ("During this safety check, obey NASA protocols.", 7),
    ("For remote access, use the VPN.", 6),
    ("Examine the No. 1 bearing installation.", 5),
    ("Tag circuit breaker 36L7.", 4),
    ('Touch the "Service Overview" arrow to select the function page.', 9),
    ("Install the three auxiliary screws (2) in the flange of the motor "
     "assembly (9).", 14),
    ("CAUTION: WHEN YOU REMOVE THE SHROUD (26), BE CAREFUL NOT TO CAUSE DAMAGE "
     "TO THE SURFACE OF THE FLANGE ASSEMBLY (22).", 20),
    ("Put preservation oil into the unit through the vent hole.", 10),
    ("Continue until the oil level is approximately 6 mm (0.24 in) below the "
     "surface of the flange cover.", 16),
    ("Put preservation oil into the unit through the vent hole until the oil "
     "level is approximately 6 mm (0.24 inches) below the surface of the "
     "flange cover.", 25),
    ("During the subsequent test, you get the cracking pressure when the fuel "
     "flow from the CROSS FEED port is more than 5 cc/minute.", 22),
    ("The data collection is not completed.", 6),
    ("Thus, the statistics module can give incorrect results.", 8),
    ("To extinguish a possible fire, portable fire extinguishers are installed "
     "in these areas:", 13),
    ("During the approach to the runway, deviation pointers in the course "
     "indicators show the pilot in which direction the aircraft must go.", 22),
    ("A smartphone is a cellular telephone that has an integrated computer and "
     "many other functions, such as an operating system, internet browsing as "
     "well as the ability to run software applications.", 31),
    ("A smartphone is a cellular telephone that has an integrated computer and "
     "many other functions.", 15),
    ("It includes an operating system and an internet browser, and it can also "
     "operate software applications.", 16),
    ("The cabin sub-compartment", 3),
    ("The crew rest compartment", 4),
]

for sentence, expected in COUNT_CASES:
    check("count %r" % sentence[:46], ste_word_count(sentence), expected)


# --------------------------------------------------------------------------
# Word count with a glossary. Rule 8.6 counts a title, a placard, or a proper
# noun as one word, and a tool cannot know which is which without being told.
# --------------------------------------------------------------------------

GLOSSARY_CASES = [
    (["Structural Repair Manual"],
     "Before you start a repair, refer to the Structural Repair Manual for the "
     "applicable safety procedures and precautions.", 16),
    (["Testing and Fault Isolation"],
     "Refer to Testing and Fault Isolation, page block 1001.", 6),
    (["Requirements after Job Completion"],
     "Refer to Requirements after Job Completion for the applicable procedures.", 7),
    (["SHORT-CIRCUIT TEST"], "Release the SHORT-CIRCUIT TEST switch.", 4),
    (["United States of America", "George Washington"],
     "The first president of the United States of America was George "
     "Washington.", 8),
]

for collapse, sentence, expected in GLOSSARY_CASES:
    check("glossary count %r" % sentence[:40],
          ste_word_count(sentence, collapse), expected)


# --------------------------------------------------------------------------
# Sentence splitting
# --------------------------------------------------------------------------

check("colon ends a sentence",
      len(split_sentences("The wheel assembly has these parts:")), 1)
check("two sentences",
      len(split_sentences("Remove the cover. Discard the packing.")), 2)
check("abbreviation does not split",
      len(split_sentences("Examine the No. 1 bearing installation.")), 1)
check("a.m. does not split",
      len(split_sentences("The test starts each day at 10 a.m.")), 1)


# --------------------------------------------------------------------------
# Rule checks
# --------------------------------------------------------------------------

def find(text, forced=None, glossary=None):
    return check_text(text, forced, glossary)


check("8.1 semicolon",
      "8.1" in violations_of(find("Examine the removed parts; replace the "
                                  "damaged ones.")), True)
check("4.2 contraction",
      "4.2" in violations_of(find("If your hands are wet, don't touch the "
                                  "adapter.")), True)
check("3.2 present perfect",
      "3.2" in violations_of(find("The operator has adjusted the linkage.")), True)
check("3.2 progressive",
      "3.2" in violations_of(find("The door is closing at this time.")), True)
check("3.4 modal passive",
      "3.4" in violations_of(find("The volume control can be adjusted.")), True)
check("3.4 infinitive passive",
      "3.4" in violations_of(find("The seat is to be installed first.")), True)
check("3.6 passive with agent",
      "3.6" in violations_of(find("The circuits are connected by a switching "
                                  "relay.")), True)
check("9.3 phrasal verb",
      "9.3" in violations_of(find("After you put out the fire, close the "
                                  "valve.")), True)
check("9.3 approved pair is allowed",
      "9.3" in violations_of(find("Put on the protective clothing.")), False)
check("GR-6 Latin abbreviation",
      "GR-6" in violations_of(find("Discard the standard parts (e.g., washers "
                                   "and bolts).")), True)
check("GR-7 gendered pronoun",
      "GR-7" in violations_of(find("The operator must clean his tools.")), True)
check("GR-1 dropped that",
      "GR-1" in rules_of(find("Make sure the valve is open.")), True)
check("GR-1 not fired when that is present",
      "GR-1" in rules_of(find("Make sure that the valve is open.")), False)
check("1.14 British spelling",
      "1.14" in rules_of(find("Change the colour of the display.")), True)
check("3.5 -ing form",
      "3.5" in rules_of(find("Before you start, examine the leaking valve.")), True)
check("3.5 allows an approved -ing noun",
      "3.5" in rules_of(find("Examine the opening in the panel.")), False)

# Length limits by text type.
long_procedure = ("Put preservation oil into the unit through the vent hole "
                  "until the oil level is approximately 6 mm (0.24 inches) "
                  "below the surface of the flange cover.")
check("5.1 procedure over 20 words",
      "5.1" in violations_of(find(long_procedure, "procedure")), True)
check("6.3 same sentence is inside the descriptive limit",
      "6.3" in violations_of(find(long_procedure, "description")), False)

check("5.5 note over 25 words",
      "5.5" in violations_of(find("NOTE: " + long_procedure + " The unit then "
                                  "holds the oil at the correct level for the "
                                  "full duration of the storage period.")), True)
check("5.5 imperative in a note",
      "5.5" in violations_of(find("NOTE: Remove the four bolts.")), True)

check("7.3 safety instruction with no risk statement",
      "7.3" in rules_of(find("WARNING: DO NOT SWALLOW THE SOLVENT.")), True)
check("7.3 satisfied when the risk is given",
      "7.3" in rules_of(find("WARNING: DO NOT SWALLOW THE SOLVENT. SOLVENTS "
                             "ARE POISONOUS AND CAN CAUSE INJURY OR DEATH.")),
      False)

check("4.3 comma at the end of a list item",
      "4.3" in violations_of(find("- The service cabinet,\n- The toilet "
                                  "shrouds.")), True)

check("6.6 paragraph over six sentences",
      "6.6" in violations_of(find(
          "The unit is small. The unit is red. The unit is heavy. The unit is "
          "new. The unit is clean. The unit is dry. The unit is safe.")), True)

check("2.1 multi-word noun over three words",
      "2.1" in rules_of(find("Runway light connection resistance calibration "
                             "gives the value.")), True)
check("2.1 does not fire on a verb inside the run",
      "2.1" in rules_of(find("The tool synchronizes state across the configured "
                             "backends.")), False)
check("2.1 does not fire on a normal clause",
      "2.1" in rules_of(find("If the strategy permits automatic resolution, the "
                             "tool can resolve the conflict.")), False)
check("2.1 allows a plural head noun at the end",
      "2.1" in rules_of(find("Install the forward turbine overheat thermocouple "
                             "terminal tags.")), True)

# A modal in front of the perfect form is reported for review, not as a
# violation. The modal carries the writer's confidence, and this skill keeps it.
modal = find("Your request may have failed.")
check("3.2 modal perfect is not a violation", violations_of(modal), set())
check("3.2 modal perfect is reported for review", "3.2" in rules_of(modal), True)
check("3.2 plain perfect is still a violation",
      "3.2" in violations_of(find("Your request has failed.")), True)

check("1.11 glossary synonym",
      "1.11" in violations_of(find(
          "Disconnect the control unit from the test rig.",
          None, {"terms": {"actuator": ["control unit", "servo control unit"]}})),
      True)

# Text type detection.
report = find("Remove the four bolts.\n\nThe unit has three parts.\n\n"
              "WARNING: DO NOT TOUCH THE BLADE. IT CAN CAUSE INJURY.\n\n"
              "NOTE: The gyroscope becomes stable after 15 seconds.")
check("type detection", report.types,
      {"procedure": 1, "description": 1, "safety": 1, "note": 1})

# A clean STE sentence produces no violations.
clean = find("Remove the four screws (10) that attach the flange (15) to the "
             "cover (20).")
check("clean procedural sentence", violations_of(clean), set())


# --------------------------------------------------------------------------

if FAILURES:
    print("FAILED %d of %d checks\n" % (len(FAILURES),
                                        len(COUNT_CASES) + len(GLOSSARY_CASES) + 30))
    for line in FAILURES:
        print("  " + line)
    sys.exit(1)

print("All checks passed.")
print("  %d word-count cases against counts published in the standard"
      % (len(COUNT_CASES) + len(GLOSSARY_CASES)))
print("  rule detection, text-type detection, and sentence splitting")
