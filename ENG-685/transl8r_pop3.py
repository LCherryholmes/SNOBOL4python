# -*- coding: utf-8 -*-
import re
import SNOBOL4python
from SNOBOL4python import pattern, MATCH, GLOBALS
from SNOBOL4python import ALPHABET, UCASE, LCASE, DIGITS
from SNOBOL4python import ε, σ, π, Λ, λ, θ, φ
from SNOBOL4python import ANY, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
from pprint import pprint
#-------------------------------------------------------------------------------
def trace(s): print(s, flush=True); return True
#-------------------------------------------------------------------------------
@pattern
def Inbox():
    global lineno
    yield from \
    ( POS(0)                                    + λ('''P = [];''')
    + ARBNO(
#       θ("OUTPUT") +
        ( φ(r"\n")                              + λ('''P.append('η()\\n')''')
        | φ(r"[ \t\r\f]+")                      + λ('''P.append('μ()')''')
        | (φ(r"[A-Za-z]+") + σ(' - ')) % "tx"   + λ('''P.append("σ('" + tx + "')")''')
        | φ(r"^[^: \t\r\f\n]+:") % "tx"         + λ('''P.append("σ('" + tx + "')")''')
        | φ(r"[ ]+") % "tx"                     + λ('''P.append("σ('" + tx + "')")''')
        | φ(r"[0-9]{2,}")                       + λ("""P.append('φ(r"[0-9]+")')""")
        | φ(r"[0-9]")                           + λ("""P.append('φ(r"[0-9]")')""")
        | φ(r"[A-Z]{2,}")                       + λ("""P.append('φ(r"[A-Z]+")')""")
        | φ(r"[A-Z]")                           + λ("""P.append('φ(r"[A-Z]")')""")
        | φ(r"[a-z]{2,}")                       + λ("""P.append('φ(r"[a-z]+")')""")
        | φ(r"[a-z]")                           + λ("""P.append('φ(r"[a-z]")')""")
        | LEN(1) % "tx"                         + λ('''P.append("σ('" + ("\\\\" if tx == "\\\\" else "") + tx + "')")''')
        ) # @ "OUTPUT"
      )
    + RPOS(0)
    )
#-------------------------------------------------------------------------------
def lineno(offset):
    while offset < total_size and offset not in linenos:
        offset += 1
    return linenos[offset]
#-------------------------------------------------------------------------------
linenos = dict()
def scan_lines():
    global linenos
    print("# Scanning lines.", end="", flush=True)
    lineno = 1
    for match in re.finditer(r"\n", inbox):
        offset = match.span()[0] + 1
        linenos[offset] = lineno
        lineno += 1
    print(f" {len(linenos)} lines.", flush=True)
#-------------------------------------------------------------------------------
reFrom =    ( r"From -"
              r" (Sun|Mon|Tue|Wed|Thu|Fri|Sat)"
              r" (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
              r" [0-9]{1,2}"
              r" [0-9]{2}:[0-9]{2}:[0-9]{2}"
              r" [0-9]{4}"
            )
#-------------------------------------------------------------------------------
sections = []
def scan_sections():
    global sections
    print("# Scanning sections.", end="", flush=True)
    for match in re.finditer(r"^" + reFrom + r"$", inbox, re.MULTILINE):
        sections.append(match.span()[0])
    sections.append(total_size)
    print(f" {len(sections)} sections.", flush=True)
#-------------------------------------------------------------------------------
def parse_emails():
    print("# Parsing emails.", flush=True)
    iteration = 0
    start_offset = None
    finish_offset = 0
    for section in sections:
        if iteration > 8: break
        iteration += 1
        start_offset = finish_offset
        finish_offset = section
        email = inbox[start_offset:finish_offset]
        if match := re.match(r"(?:.*\n)+(?:Content-Length: [0-9]+\n)", email):
            email_header = match.group()
            if email_header in Inbox():
                print(" + ".join(P))
#-------------------------------------------------------------------------------
inbox = None
total_size = None
def main():
    global inbox, total_size
    inbox_nm = "C:/Users/lcher/AppData/Local/Packages/" \
        "MozillaThunderbird.MZLA_h5892qc0xkpca/LocalCache/Roaming/" \
        "Thunderbird/Profiles/nsn6odxd.default-esr/" \
        "Mail/pop.mail.yahoo.com/Inbox"
    with open(inbox_nm, "r", encoding="latin-1") as inbox_file:
        print("# Reading inbox.", end="", flush=True)
        inbox = inbox_file.read()
        total_size = len(inbox)
        print(f" {total_size} bytes.", flush=True)
        scan_lines()
        scan_sections()
        parse_emails()
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    GLOBALS(globals())
    main()
#-------------------------------------------------------------------------------
