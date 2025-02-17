# -*- coding: utf-8 -*-
# ENG 685, Lon Jones Cherryholmes, RegEx Python Exercise
import re
#------------------------------------------------------------------------------
text = """Why, in 1999 BOb sometimessometimes I've believed as as many many!
I eat 88 things for breakfast. Where are you are you a four-year-old?
Truly."""
#------------------------------------------------------------------------------
regex1 = "[A-Za-z]+"
print("1. the set of all alphabetic strings:")
print(regex1)
print(re.findall(regex1, text))
print()
#------------------------------------------------------------------------------
regex2 = "[A-Z]+b"
print("2. the set of all uppercase alphabetic strings ending in a b:")
print(regex2)
print(re.findall(regex2, text))
print()
#------------------------------------------------------------------------------
regex3 = "\\b((\\w+)\\s\\2)"
print("""3. the set of all strings with two consecutive repeated words (e.g.,
“Humbert Humbert” and “the the” but not “the bug” or “the big bug” or
"thethe"):""")
print(regex3)
for matching in re.findall(regex3, text):
    print(matching[0])
print()    
#------------------------------------------------------------------------------
regex4 = re.compile("^(b|b+ab+)*$")
print("""4. the set of all strings from the alphabet a,b such that each a is
"immediately preceded and immediately followed by a b:""")
print(regex4)
from itertools import product
for length in range(0, 6):
    for chars in product('ab', repeat=length):
        string = "".join(chars)
        matching = re.fullmatch(regex4, string)
        if matching:
            print(f'"{string}" -> "{matching.group(0)}"')
print()
#------------------------------------------------------------------------------
regex5 = "^(\\d+)(?:\\W*(\\w+))+$"
print("""5. all strings which start at the beginning of the line with an
integer (i.e.,1,2,3,...,10,...,10000,...) and which end at the end of the
line with a word:""")
texts5 = ["1", "word", "1word", "2 word", "11\twords"]
print(regex5)
for string in texts5:
    matching = re.fullmatch(regex5, string)
    if matching:
        print(string, matching.group(1), matching.group(2))
print()
#------------------------------------------------------------------------------
regex6 = "^([0-9]{3})-([0-9]{3})-([0-9]{4})$"
text6 = "469-555-1234"
print("6. as many 10-digit national phone numbers written as possible:")
print(text6)
print(regex6)
print(re.findall(regex6, text6))
print()
#------------------------------------------------------------------------------
regex7 = r"(?:^\s*|[?!]\s+|(?<!Mr)(?<!Mrs)(?<!\.[A-Z])\.\s+)([A-Z][A-Za-z]*)"
print("""7. [extra credit] write a pattern which places the first word of an
English sentence in a register. Deal with punctuation:""")
text7 = """This is a sentence. Another one too!  How about this?
Mr. Jones and his wife, Mrs. Jones, bought into the I.B.M. Company stock.
Whow! Did you know it went up 10 percent? Amazing...
Yep. I am, that I am. I am."""
print()
print(text7)
print()
print(regex7)
print('I found:', re.findall(regex7, text7))
print()
page = \
"""   Every person who, under color of any statute, ordinance, regulation,
custom, or usage, of any State or Territory or the District of Columbia,
subjects, or causes to be subjected, any citizen of the United States or
other person within the jurisdiction thereof to the deprivation of any
rights, privileges, or immunities secured by the Constitution and laws, shall
be liable to the party injured in an action at law, suit in equity, or other
proper proceeding for redress, except that in any action brought against
a judicial officer for an act or omission taken in such officer’s judicial
capacity, injunctive relief shall not be granted unless a declaratory decree
was violated or declaratory relief was unavailable. For the purposes of this
section, any Act of Congress applicable exclusively to the District of
Columbia shall be considered to be a statute of the District of Columbia.
"""
print(page)
print(regex7)
print('I found:', re.findall(regex7, page))
print()
#------------------------------------------------------------------------------
