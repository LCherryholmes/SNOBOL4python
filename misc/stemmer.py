# -*- coding: utf-8 -*-
"""
Combined Porter (1980) and Snowball (Porter2) Stemmers.
Refactored to use functional closures for namespace isolation and shorter names.

Logic is encapsulated within factory functions (`make_porter`, `make_snowball`),
removing the need for prefixes on helper functions.

Dependencies:
    SNOBOL4patterns.py
    SNOBOL4functions.py
"""

import logging
from SNOBOL4patterns import *
from SNOBOL4functions import *

# --- 1. Global State & Context ---

# Bind SNOBOL library to this module's global scope
GLOBALS(globals())
TRACE(logging.ERROR)

# Global Registers (Modified by SNOBOL patterns via side-effects)
stem = ""       # Current stem
target = ""     # Replacement string
r1_start = 0    # Region 1 index
r2_start = 0    # Region 2 index

# Shared Constants
vowels_set = set("aeiouy")
porter_vowels = set("aeiou")

# --- 2. Functional Helpers (Shared) ---

def contains_vowel(s, v_set):
    return any(c in v_set for c in s)

def ends_double_consonant(s, v_set):
    if len(s) < 2: return False
    return s[-1] == s[-2] and s[-1] not in v_set

def run_pipeline(word, pipeline):
    global stem, target
    for pattern in pipeline:
        target = None # Reset target
        SEARCH(word, pattern)
        if target is not None:
            word = stem + target
    return word

# --- 3. Porter Stemmer Factory ---

def make_porter():
    """
    Creates and returns a functional Porter (1980) stemmer.
    Encapsulates logic helpers locally to avoid namespace pollution.
    """

    # -- Local Helpers --
    def is_consonant(s, i):
        c = s[i]
        if c in porter_vowels: return False
        if c == 'y':
            return True if i == 0 else not is_consonant(s, i - 1)
        return True

    def measure(s):
        if not s: return 0
        m = 0; i = 0; length = len(s)
        while i < length and is_consonant(s, i): i += 1
        while i < length:
            while i < length and not is_consonant(s, i): i += 1
            if i >= length: break
            while i < length and is_consonant(s, i): i += 1
            m += 1
        return m

    def cvc_ending(s):
        if len(s) < 3: return False
        last = len(s) - 1
        if is_consonant(s, last) and \
           not is_consonant(s, last - 1) and \
           is_consonant(s, last - 2):
               return s[-1] not in "wxy"
        return False

    def step1b_cleanup():
        global stem, target
        if stem.endswith("at") or stem.endswith("bl") or stem.endswith("iz"):
            target = "e"
        elif ends_double_consonant(stem, porter_vowels) and stem[-1] not in "lsz":
            stem = stem[:-1]
            target = ""
        elif measure(stem) == 1 and cvc_ending(stem):
            target = "e"
        else:
            target = ""

    # Export cleanup closure to globals so λ("string") commands can find it
    globals()['porter_step1b_cleanup'] = step1b_cleanup

    # -- Pattern Definitions --

    # Step 1a
    p1a = POS(0) + (
          RTAB(4) @ "stem" + σ('sses') + λ("target = 'ss'")
        | RTAB(3) @ "stem" + σ('ies')  + λ("target = 'i'")
        | RTAB(2) @ "stem" + σ('ss')   + λ("target = 'ss'")
        | RTAB(1) @ "stem" + σ('s')    + λ("target = ''")
    ) + RPOS(0)

    # Step 1b
    p1b = POS(0) + (
          RTAB(3) @ "stem" + σ('eed') + Λ(lambda: measure(stem) > 0) + λ("target = 'ee'")
        | RTAB(2) @ "stem" + σ('ed')  + Λ(lambda: contains_vowel(stem, porter_vowels)) + λ("porter_step1b_cleanup()")
        | RTAB(3) @ "stem" + σ('ing') + Λ(lambda: contains_vowel(stem, porter_vowels)) + λ("porter_step1b_cleanup()")
    ) + RPOS(0)

    # Step 1c
    p1c = POS(0) + (
        RTAB(1) @ "stem" + σ('y') + Λ(lambda: contains_vowel(stem, porter_vowels)) + λ("target = 'i'")
    ) + RPOS(0)

    # Step 2
    p2 = POS(0) + (
          RTAB(7) @ "stem" + σ('ational') + Λ(lambda: measure(stem) > 0) + λ("target = 'ate'")
        | RTAB(6) @ "stem" + σ('tional')  + Λ(lambda: measure(stem) > 0) + λ("target = 'tion'")
        | RTAB(4) @ "stem" + σ('enci')    + Λ(lambda: measure(stem) > 0) + λ("target = 'ence'")
        | RTAB(4) @ "stem" + σ('anci')    + Λ(lambda: measure(stem) > 0) + λ("target = 'ance'")
        | RTAB(4) @ "stem" + σ('izer')    + Λ(lambda: measure(stem) > 0) + λ("target = 'ize'")
        | RTAB(3) @ "stem" + σ('bli')     + Λ(lambda: measure(stem) > 0) + λ("target = 'ble'")
        | RTAB(4) @ "stem" + σ('alli')    + Λ(lambda: measure(stem) > 0) + λ("target = 'al'")
        | RTAB(5) @ "stem" + σ('entli')   + Λ(lambda: measure(stem) > 0) + λ("target = 'ent'")
        | RTAB(3) @ "stem" + σ('eli')     + Λ(lambda: measure(stem) > 0) + λ("target = 'e'")
        | RTAB(5) @ "stem" + σ('ousli')   + Λ(lambda: measure(stem) > 0) + λ("target = 'ous'")
        | RTAB(7) @ "stem" + σ('ization') + Λ(lambda: measure(stem) > 0) + λ("target = 'ize'")
        | RTAB(5) @ "stem" + σ('ation')   + Λ(lambda: measure(stem) > 0) + λ("target = 'ate'")
        | RTAB(4) @ "stem" + σ('ator')    + Λ(lambda: measure(stem) > 0) + λ("target = 'ate'")
        | RTAB(5) @ "stem" + σ('alism')   + Λ(lambda: measure(stem) > 0) + λ("target = 'al'")
        | RTAB(7) @ "stem" + σ('iveness') + Λ(lambda: measure(stem) > 0) + λ("target = 'ive'")
        | RTAB(7) @ "stem" + σ('fulness') + Λ(lambda: measure(stem) > 0) + λ("target = 'ful'")
        | RTAB(7) @ "stem" + σ('ousness') + Λ(lambda: measure(stem) > 0) + λ("target = 'ous'")
        | RTAB(5) @ "stem" + σ('aliti')   + Λ(lambda: measure(stem) > 0) + λ("target = 'al'")
        | RTAB(5) @ "stem" + σ('iviti')   + Λ(lambda: measure(stem) > 0) + λ("target = 'ive'")
        | RTAB(6) @ "stem" + σ('biliti')  + Λ(lambda: measure(stem) > 0) + λ("target = 'ble'")
    ) + RPOS(0)

    # Step 3
    p3 = POS(0) + (
          RTAB(5) @ "stem" + σ('icate') + Λ(lambda: measure(stem) > 0) + λ("target = 'ic'")
        | RTAB(5) @ "stem" + σ('ative') + Λ(lambda: measure(stem) > 0) + λ("target = ''")
        | RTAB(5) @ "stem" + σ('alize') + Λ(lambda: measure(stem) > 0) + λ("target = 'al'")
        | RTAB(5) @ "stem" + σ('iciti') + Λ(lambda: measure(stem) > 0) + λ("target = 'ic'")
        | RTAB(4) @ "stem" + σ('ical')  + Λ(lambda: measure(stem) > 0) + λ("target = 'ic'")
        | RTAB(3) @ "stem" + σ('ful')   + Λ(lambda: measure(stem) > 0) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('ness')  + Λ(lambda: measure(stem) > 0) + λ("target = ''")
    ) + RPOS(0)

    # Step 4
    p4 = POS(0) + (
          RTAB(2) @ "stem" + σ('al')    + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('ance')  + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('ence')  + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(2) @ "stem" + σ('er')    + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(2) @ "stem" + σ('ic')    + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('able')  + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('ible')  + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ant')   + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(5) @ "stem" + σ('ement') + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('ment')  + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ent')   + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ou')    + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ism')   + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ate')   + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('iti')   + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ous')   + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ive')   + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ize')   + Λ(lambda: measure(stem) > 1) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ion')   + Λ(lambda: measure(stem) > 1) + Λ(lambda: stem[-1] in 'st') + λ("target = ''")
    ) + RPOS(0)

    # Step 5
    p5a = POS(0) + (
        RTAB(1) @ "stem" + σ('e') + (
            Λ(lambda: measure(stem) > 1) |
            (Λ(lambda: measure(stem) == 1) + Λ(lambda: not cvc_ending(stem)))
        ) + λ("target = ''")
    ) + RPOS(0)

    p5b = POS(0) + (
        RTAB(2) @ "stem" + σ('ll') + Λ(lambda: measure(stem) > 1) + λ("target = 'l'")
    ) + RPOS(0)

    pipeline = [p1a, p1b, p1c, p2, p3, p4, p5a, p5b]

    def stemmer(token):
        if len(token) <= 2: return token
        return run_pipeline(token.lower(), pipeline)

    return stemmer

# --- 4. Snowball Stemmer Factory ---

def make_snowball():
    """
    Creates and returns a functional Snowball (Porter2) stemmer.
    Encapsulates logic helpers locally to avoid namespace pollution.
    """

    # -- Local Helpers --
    def in_r1(): return len(stem) >= r1_start
    def in_r2(): return len(stem) >= r2_start
    def has_vowel(): return contains_vowel(stem, vowels_set)

    def is_short_syllable(s):
        if len(s) < 2: return False
        if len(s) == 2:
            return (s[0] in vowels_set) and (s[1] not in vowels_set)
        return (s[-3] not in vowels_set) and (s[-2] in vowels_set) and \
               (s[-1] not in vowels_set) and (s[-1] not in "wxy")

    def is_short_word(s):
        return is_short_syllable(s) and (r1_start >= len(s))

    def step1b_cleanup():
        global stem, target
        if stem.endswith("at") or stem.endswith("bl") or stem.endswith("iz"):
            target = "e"
        elif ends_double_consonant(stem, vowels_set):
            stem = stem[:-1]
            target = ""
        elif is_short_word(stem):
            target = "e"
        else:
            target = ""

    # Export cleanup closure to globals so λ("string") commands can find it
    globals()['snowball_step1b_cleanup'] = step1b_cleanup

    # -- Pattern Definitions --

    p_regions = (
        POS(0) +
        ((BREAK("aeiouy") + SPAN("aeiouy") + NOTANY("aeiouy")) @ "r1_prefix") +
        λ("r1_start = len(r1_prefix)") +
        ((ARBNO(LEN(1))) @ "r2_gap") + FENCE() +
        (BREAK("aeiouy") + SPAN("aeiouy") + NOTANY("aeiouy")) +
        λ("r2_start = r1_start + len(r2_gap) + len(MATCH)") +
        REM
    )

    p1a = POS(0) + (
          RTAB(4) @ "stem" + σ('sses') + λ("target = 'ss'")
        | RTAB(3) @ "stem" + σ('ies')  + Λ(lambda: len(stem) > 1) + λ("target = 'i'")
        | RTAB(3) @ "stem" + σ('ied')  + Λ(lambda: len(stem) > 1) + λ("target = 'i'")
        | RTAB(3) @ "stem" + σ('ies')  + λ("target = 'ie'")
        | RTAB(3) @ "stem" + σ('ied')  + λ("target = 'ie'")
        | RTAB(2) @ "stem" + σ('us')   + λ("target = 'us'")
        | RTAB(2) @ "stem" + σ('ss')   + λ("target = 'ss'")
        | RTAB(1) @ "stem" + σ('s')    + Λ(lambda: any(c in vowels_set for c in stem[:-1])) + λ("target = ''")
    ) + RPOS(0)

    p1b = POS(0) + (
          RTAB(5) @ "stem" + σ('eedly') + Λ(lambda: in_r1()) + λ("target = 'ee'")
        | RTAB(5) @ "stem" + σ('ingly') + Λ(has_vowel) + λ("snowball_step1b_cleanup()")
        | RTAB(4) @ "stem" + σ('edly')  + Λ(has_vowel) + λ("snowball_step1b_cleanup()")
        | RTAB(3) @ "stem" + σ('eed')   + Λ(lambda: in_r1()) + λ("target = 'ee'")
        | RTAB(3) @ "stem" + σ('ing')   + Λ(has_vowel) + λ("snowball_step1b_cleanup()")
        | RTAB(2) @ "stem" + σ('ed')    + Λ(has_vowel) + λ("snowball_step1b_cleanup()")
    ) + RPOS(0)

    p1c = POS(0) + (
        RTAB(1) @ "stem" + σ('y') + Λ(lambda: len(stem)>1) + Λ(lambda: stem[-1] not in vowels_set) + λ("target = 'i'")
    ) + RPOS(0)

    p2 = POS(0) + (
          RTAB(7) @ "stem" + σ('tional')  + Λ(lambda: in_r1()) + λ("target = 'tion'")
        | RTAB(7) @ "stem" + σ('ization') + Λ(lambda: in_r1()) + λ("target = 'ize'")
        | RTAB(7) @ "stem" + σ('fulness') + Λ(lambda: in_r1()) + λ("target = 'ful'")
        | RTAB(7) @ "stem" + σ('ousness') + Λ(lambda: in_r1()) + λ("target = 'ous'")
        | RTAB(7) @ "stem" + σ('iveness') + Λ(lambda: in_r1()) + λ("target = 'ive'")
        | RTAB(6) @ "stem" + σ('lessli')  + Λ(lambda: in_r1()) + λ("target = 'less'")
        | RTAB(6) @ "stem" + σ('biliti')  + Λ(lambda: in_r1()) + λ("target = 'ble'")
        | RTAB(5) @ "stem" + σ('entli')   + Λ(lambda: in_r1()) + λ("target = 'ent'")
        | RTAB(5) @ "stem" + σ('ousli')   + Λ(lambda: in_r1()) + λ("target = 'ous'")
        | RTAB(5) @ "stem" + σ('iviti')   + Λ(lambda: in_r1()) + λ("target = 'ive'")
        | RTAB(5) @ "stem" + σ('fulli')   + Λ(lambda: in_r1()) + λ("target = 'ful'")
        | RTAB(5) @ "stem" + σ('alism')   + Λ(lambda: in_r1()) + λ("target = 'al'")
        | RTAB(4) @ "stem" + σ('enci')    + Λ(lambda: in_r1()) + λ("target = 'ence'")
        | RTAB(4) @ "stem" + σ('anci')    + Λ(lambda: in_r1()) + λ("target = 'ance'")
        | RTAB(4) @ "stem" + σ('abli')    + Λ(lambda: in_r1()) + λ("target = 'able'")
        | RTAB(4) @ "stem" + σ('izer')    + Λ(lambda: in_r1()) + λ("target = 'ize'")
        | RTAB(4) @ "stem" + σ('ator')    + Λ(lambda: in_r1()) + λ("target = 'ate'")
        | RTAB(4) @ "stem" + σ('alli')    + Λ(lambda: in_r1()) + λ("target = 'al'")
        | RTAB(4) @ "stem" + σ('logi')    + Λ(lambda: in_r1()) + λ("target = 'log'")
        | RTAB(3) @ "stem" + σ('bli')     + Λ(lambda: in_r1()) + λ("target = 'ble'")
        | RTAB(2) @ "stem" + σ('li')      + Λ(lambda: in_r1()) + Λ(lambda: stem[-1] in 'cdeghkmnrt') + λ("target = ''")
    ) + RPOS(0)

    p3 = POS(0) + (
          RTAB(7) @ "stem" + σ('ational') + Λ(lambda: in_r1()) + λ("target = 'ate'")
        | RTAB(6) @ "stem" + σ('tional')  + Λ(lambda: in_r1()) + λ("target = 'tion'")
        | RTAB(5) @ "stem" + σ('alize')   + Λ(lambda: in_r1()) + λ("target = 'al'")
        | RTAB(5) @ "stem" + σ('icate')   + Λ(lambda: in_r1()) + λ("target = 'ic'")
        | RTAB(5) @ "stem" + σ('iciti')   + Λ(lambda: in_r1()) + λ("target = 'ic'")
        | RTAB(5) @ "stem" + σ('ative')   + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('ical')    + Λ(lambda: in_r1()) + λ("target = 'ic'")
        | RTAB(4) @ "stem" + σ('ness')    + Λ(lambda: in_r1()) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ful')     + Λ(lambda: in_r1()) + λ("target = ''")
    ) + RPOS(0)

    p4 = POS(0) + (
          RTAB(5) @ "stem" + σ('ement') + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('ance')  + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('ence')  + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('able')  + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('ible')  + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(4) @ "stem" + σ('ment')  + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ent')   + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ism')   + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ate')   + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('iti')   + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ous')   + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ive')   + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ize')   + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ion')   + Λ(lambda: in_r2()) + Λ(lambda: stem[-1] in 'st') + λ("target = ''")
        | RTAB(2) @ "stem" + σ('al')    + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(2) @ "stem" + σ('er')    + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(2) @ "stem" + σ('ic')    + Λ(lambda: in_r2()) + λ("target = ''")
        | RTAB(3) @ "stem" + σ('ant')   + Λ(lambda: in_r2()) + λ("target = ''")
    ) + RPOS(0)

    p5 = POS(0) + (
          RTAB(1) @ "stem" + σ('e') + (
              Λ(lambda: in_r2()) | (Λ(lambda: in_r1()) + Λ(lambda: not is_short_syllable(stem)))
          ) + λ("target = ''")
        | RTAB(2) @ "stem" + σ('ll') + Λ(lambda: in_r2()) + λ("target = 'l'")
    ) + RPOS(0)

    pipeline = [p1a, p1b, p1c, p2, p3, p4, p5]

    def stemmer(token):
        if len(token) <= 2: return token
        global r1_start, r2_start
        r1_start = 1000; r2_start = 1000
        SEARCH(token.lower(), p_regions)
        return run_pipeline(token.lower(), pipeline)

    return stemmer

# --- 5. Demonstration ---

if __name__ == "__main__":
    porter_stem = make_porter()
    snowball_stem = make_snowball()

    test_terms = [
        "caresses", "ponies", "ties", "cats", "feed", "agreed", "plastered",
        "bled", "motoring", "sing", "happy", "sky", "apology",
        "relational", "conditional", "rational", "valency", "hesitancy",
        "triplicate", "formative", "formalize", "revival", "allowance",
        "inference", "airliner", "probate", "rate", "cease", "controll", "roll",
        "generously"
    ]
    
    print(f"{'Input':<15} | {'Porter (1980)':<15} | {'Snowball (Porter2)':<15}")
    print("-" * 52)
    
    for t in test_terms:
        p_res = porter_stem(t)
        s_res = snowball_stem(t)
        print(f"{t:<15} | {p_res:<15} | {s_res:<15}")