# -*- coding: utf-8 -*-
import re
import SNOBOL4python
from SNOBOL4python import pattern, MATCH, GLOBALS
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ, φ
from SNOBOL4python import ANY, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
from pprint import pprint
#-------------------------------------------------------------------------------
reFrom =                        ( r"From -"
                                  r" (Sun|Mon|Tue|Wed|Thu|Fri|Sat)"
                                  r" (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                                  r" [0-9]{1,2}"
                                  r" [0-9]{2}:[0-9]{2}:[0-9]{2}"
                                  r" [0-9]{4}"
                                )
@pattern
def From():                     yield from φ(reFrom)
#-------------------------------------------------------------------------------
@pattern
def μ():                        yield from φ(r"[ \t\r\f]") | ε()
@pattern
def ς(s):                       yield from μ() + φ(s)
@pattern
def DOW():                      yield from φ(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)")
@pattern
def Month():                    yield from φ(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)")
@pattern
def DOM():                      yield from φ(r"[0-9]+")
@pattern
def Time():                     yield from φ(r"([0-9]{2}:[0-9]{2}:[0-9]{2})")
@pattern
def Year():                     yield from φ(r"([0-9]{4})")
@pattern
def Date_Time():                yield from ( DOW() 
                                           + ς(' ') + Month()
                                           + ς(' ') + DOM()
                                           + ς(' ') + Time()
                                           + ς(' ') + Year()
                                           )
#-------------------------------------------------------------------------------
@pattern
def ip_address():               yield from φ(r"([0-9]{1,3})\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
@pattern
def email_address():            yield from φ(r"[A-Za-z][0-9A-Za-z]+@yahoo.com")
#-------------------------------------------------------------------------------
@pattern
def X_account_key():            yield from φ(r"X-Account-Key: .*\n")
@pattern
def X_UIDL():                   yield from φ(r"X-UIDL: .{27}\n")
@pattern
def X_Mozilla_Status():         yield from φ(r"X-Mozilla-Status: [0-9]{4}")
@pattern
def X_Mozilla_Status2():        yield from φ(r"X-Mozilla-Status2: [0-9]{8}")
@pattern
def X_Mozilla_Keys():           yield from φ(r"X-Mozilla-Keys:[ ]+\n")
@pattern
def X_Apparently_To():          yield from φ(r"X-Apparently-To:.*\n")
@pattern
def X_Originating_IP():         yield from φ(r"X-Originating-IP: \[([^]])\]")
@pattern
def Return_Path():              yield from φ(r"Return-Path: [^ \t\r\f\n]")
@pattern
def Authentication_Results():   yield from φ(r"Authentication-Results: [ \t\r\f\n]  [^;]; [ \t\r\f\n] [ \t\r\f\n]")
@pattern
def Received_from():            yield from φ(r"Received: from")
@pattern
def Received():                 yield from φ(r"Received:.*\n")
@pattern
def X_MimeOLE():                yield from φ(r"X-MimeOLE:.*\n")
@pattern
def Content_class():            yield from φ(r"Content-class:.*\n")
@pattern
def MIME_Version():             yield from φ(r"MIME-Version:'.*\n")
@pattern
def Content_Type():             yield from φ(r"Content-Type:'.*\n")
@pattern
def Subject():                  yield from φ(r"Subject:.*\n")
@pattern
def Date():                     yield from φ(r"Date:.*\n")
@pattern
def Message_ID():               yield from φ(r"Message-ID:.*\n")
@pattern
def X_MS_Has_Attach():          yield from φ(r"X-MS-Has-Attach:.*\n")
@pattern
def X_MS_TNEF_Correlator():     yield from φ(r"X-MS-TNEF-Correlator:.*\n")
@pattern
def Thread_Topic():             yield from φ(r"Thread-Topic:.*\n")
@pattern
def Thread_Index():             yield from φ(r"Thread-Index:.*\n")
@pattern
def From_address():             yield from φ(r"From:.*\n")
@pattern
def To_address():               yield from φ(r"To:.*\n")
@pattern
def X_OriginalArrivalTime():    yield from φ(r"X-OriginalArrivalTime:.*\n")
@pattern
def Content_Length():           yield from φ(r"Content-Length:.*\n")
@pattern
def Content_Type():             yield from φ(r"Content-Type:.*\n")
#-------------------------------------------------------------------------------
@pattern
def Content_Transfer_Encoding():    yield from φ(r"Content-Transfer-Encoding:.*\n")
@pattern
def Content_Transfer_Encoding():    yield from φ(r"Content-Transfer-Encoding:.*\n")
#-------------------------------------------------------------------------------
@pattern
def base64():                   yield from φ(r"(([0-9/+A-Za-z]{76})\n)+")
@pattern
def part_id():                  yield from φ(r"[0-9]{3}[0-9A-F]{8}[0-9A-F]{8}")
#-------------------------------------------------------------------------------
@pattern
def Line():                     yield from φ(r".*\n")
@pattern
def UptoPart():                 yield from φ( r"(?!------_=_NextPart_)"
                                              r"(?:.*\n)+?"
                                              r"(?=------_=_NextPart_)"
                                            ) % "upto"
@pattern
def NextPart():                 yield from φ( r"------_=_NextPart_"
                                              r"([0-9]{3}_[0-9A-F]{8}\.[0-9A-F]{8})\n"
                                              r"(?:.*\n)*"
                                              r"------_=_NextPart_"
                                              r"\1--\n"
                                            )
#-------------------------------------------------------------------------------
def trace(s): print(s); return True
#-------------------------------------------------------------------------------
@pattern
def Inbox():
    global lineno
    yield from \
    ( POS(0)                                + Λ("""P = [];""")
    + ARBNO(
        θ("p0") + # θ("OUTPUT") +
        ( σ('\n')                           + Λ("""P.append("η() +\\n")""")
        | φ(r"[ ]+") @ "tx"                 + Λ("""P.append("ς('" + tx + "')")""")
        | φ(r"[ \t\r\f]+")                  + Λ("""P.append("μ()")""")
        | Date_Time()                       + Λ("""P.append("Date_Time()")""")
        | From()                            + Λ("""P.append("From()")""")
        | X_account_key()                   + Λ("""P.append("X_account_key()")""")
        | X_UIDL()                          + Λ("""P.append("X_UIDL()")""")
        | X_Mozilla_Status()                + Λ("""P.append("X_Mozilla_Status()")""")
        | X_Mozilla_Status2()               + Λ("""P.append("X_Mozilla_Status2()")""")
        | X_Mozilla_Keys()                  + Λ("""P.append("X_Mozilla_Keys()")""")
        | X_Originating_IP()                + Λ("""P.append("X_Originating_IP()")""")
        | Return_Path()                     + Λ("""P.append("Return_Path()")""")
        | Authentication_Results()          + Λ("""P.append("Authentication_Results()")""")
        | Received()                        + Λ("""P.append("Received()")""")
        | X_MimeOLE()                       + Λ("""P.append("X_MimeOLE()")""")
        | Content_class()                   + Λ("""P.append("Content_class()")""")
        | MIME_Version()                    + Λ("""P.append("MIME_Version()")""")
        | Content_Type()                    + Λ("""P.append("Content_Type()")""")
        | Subject()                         + Λ("""P.append("Subject()")""")
        | Date()                            + Λ("""P.append("Date()")""")
        | Message_ID()                      + Λ("""P.append("Message_ID()")""")
        | X_MS_Has_Attach()                 + Λ("""P.append("X_MS_Has_Attach()")""")
        | X_MS_TNEF_Correlator()            + Λ("""P.append("X_MS_TNEF_Correlator()")""")
        | Thread_Topic()                    + Λ("""P.append("Thread_Topic()")""")
        | Thread_Index()                    + Λ("""P.append("Thread_Index()")""")
        | From_address()                    + Λ("""P.append("From_address()")""")
        | To_address()                      + Λ("""P.append("To_address()")""")
        | X_OriginalArrivalTime()           + Λ("""P.append("X_OriginalArrivalTime()")""")
        | Content_Length()                  + Λ("""P.append("Content_Length()")""")
        | Content_Type()                    + Λ("""P.append("Content_Type()")""")
        | Content_Transfer_Encoding()       + Λ("""P.append("Content_Transfer_Encoding()")""")
        | φ(r"[0-9]+")                      + Λ("""P.append("SPAN(_DIGITS)")""")
        | φ(r"[A-Z]+")                      + Λ("""P.append("SPAN(_UCASE)")""")
        | φ(r"[a-z]+")                      + Λ("""P.append("SPAN(_LCASE)")""")
        | φ(r"[^ \t\r\f\n]+") @ "tx"        + Λ("""P.append("ς('" + ("\\\\" if tx == "\\\\" else "") + tx + "')")""")
        | φ(r"[^0-9A-Za-z]+") @ "tx"        + Λ("""P.append("ς('" + ("\\\\" if tx == "\\\\" else "") + tx + "')")""")
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
    print("Scanning lines.", end="", flush=True)
    lineno = 1
    for match in re.finditer(r"\n", inbox):
        offset = match.span()[0] + 1
        linenos[offset] = lineno
        lineno += 1
    print(f" {len(linenos)} lines.")
#-------------------------------------------------------------------------------
sections = []
def scan_sections():
    global sections
    print("Scanning sections.", end="", flush=True)
    for match in re.finditer(r"^" + reFrom + r"$", inbox, re.MULTILINE):
        sections.append(match.span()[0])
    sections.append(total_size)
    print(f" {len(sections)} sections.")
#-------------------------------------------------------------------------------
def parse_emails():
    print("Parsing emails.", end="")
    start_offset = None
    finish_offset = 0
    for section in sections:
        start_offset = finish_offset
        finish_offset = section
        email = inbox[start_offset:finish_offset]
        if match := re.match(r"(?:.*\n){12}", email):
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
        print("Reading inbox.", end="", flush=True)
        inbox = inbox_file.read()
        total_size = len(inbox)
        print(f" {total_size} bytes.")
        scan_lines()
        scan_sections()
        parse_emails()
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    GLOBALS(globals())
    main()
#-------------------------------------------------------------------------------
