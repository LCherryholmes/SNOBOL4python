# -*- coding: utf-8 -*-
import re
import SNOBOL4python
from SNOBOL4python import GLOBALS, pattern
from SNOBOL4python import ALPHABET, UCASE, LCASE, DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ, α, ω, φ, Φ
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCESS, TAB
from pprint import pprint
#-------------------------------------------------------------------------------
ITERATIONS = 4
def trace(s): print(s, flush=True); return True
#-------------------------------------------------------------------------------
@pattern
def Authentication_Results():       yield from Φ(r"(?P<tag>Authentication-Results:)(?P<tx>.*)")
@pattern
def Comment():                      yield from Φ(r"(?P<tag>Comment:)(?P<tx>.*)")
@pattern
def Content_class():                yield from Φ(r"(?P<tag>Content-[Cc]lass:)(?P<tx>.*)")
@pattern
def Content_Length():               yield from Φ(r"(?P<tag>Content-Length:)(?P<tx>.*)")
@pattern
def Content_Transfer_Encoding():    yield from Φ(r"(?P<tag>Content-Transfer-Encoding:)(?P<tx>.*)")
@pattern
def Date():                         yield from Φ(r"(?P<tag>Date:)(?P<tx>.*)")
@pattern
def From():                         yield from Φ(r"(?P<tag>From:)(?P<tx>.*)")
@pattern
def Importance():                   yield from Φ(r"(?P<tag>Importance:)(?P<tx>.*)")
@pattern
def In_Reply_To():                  yield from Φ(r"(?P<tag>In-Reply-To:)(?P<tx>.*)")
@pattern
def Message_ID():                   yield from Φ(r"(?P<tag>Message-ID:)(?P<tx>.*)")
@pattern
def MIME_Version():                 yield from Φ(r"(?P<tag>MIME-Version:)(?P<tx>.*)")
@pattern
def Priority():                     yield from Φ(r"(?P<tag>Priority:)(?P<tx>.*)")
@pattern
def References():                   yield from Φ(r"(?P<tag>References:)(?P<tx>.*)")
@pattern
def Return_Path():                  yield from Φ(r"(?P<tag>Return-Path:)(?P<tx>.*)")
@pattern
def Subject():                      yield from Φ(r"(?P<tag>Subject:)(?P<tx>.*)")
@pattern
def Thread_Index():                 yield from Φ(r"(?P<tag>[Tt]hread-[Ii]ndex:)(?P<tx>.*)")
@pattern
def Thread_Topic():                 yield from Φ(r"(?P<tag>Thread-Topic:)(?P<tx>.*)")
@pattern
def To():                           yield from Φ(r"(?P<tag>To:)(?P<tx>.*)")
@pattern
def X_Account_Key():                yield from Φ(r"(?P<tag>X-Account-Key:)(?P<tx>.*)")
@pattern
def X_Apparently_To():              yield from Φ(r"(?P<tag>X-Apparently-To:)(?P<tx>.*)")
@pattern
def X_MAIL_FROM():                  yield from Φ(r"(?P<tag>X-MAIL-FROM:)(?P<tx>.*)")
@pattern
def X_Mailer():                     yield from Φ(r"(?P<tag>X-Mailer:)(?P<tx>.*)")
@pattern
def X_MimeOLE():                    yield from Φ(r"(?P<tag>X-(?:Mime|MIME)OLE:)(?P<tx>.*)")
@pattern
def X_Mozilla_Keys():               yield from Φ(r"(?P<tag>X-Mozilla-Keys:)(?P<tx>.*)")
@pattern
def X_Mozilla_Status():             yield from Φ(r"(?P<tag>X-Mozilla-Status:)(?P<tx>.*)")
@pattern
def X_Mozilla_Status2():            yield from Φ(r"(?P<tag>X-Mozilla-Status2:)(?P<tx>.*)")
@pattern
def X_MS_Has_Attach():              yield from Φ(r"(?P<tag>X-MS-Has-Attach:)(?P<tx>.*)")
@pattern
def X_MS_TNEF_Correlator():         yield from Φ(r"(?P<tag>X-MS-TNEF-Correlator:)(?P<tx>.*)")
@pattern
def X_MSMail_Priority():            yield from Φ(r"(?P<tag>X-MSMail-Priority:)(?P<tx>.*)")
@pattern
def X_OriginalArrivalTime():        yield from Φ(r"(?P<tag>X-OriginalArrivalTime:)(?P<tx>.*)")
@pattern
def X_Originating_IP():             yield from Φ(r"(?P<tag>X-Originating-IP:)(?P<tx>.*)")
@pattern
def X_Priority():                   yield from Φ(r"(?P<tag>X-Priority:)(?P<tx>.*)")
@pattern
def X_SF_Loop():                    yield from Φ(r"(?P<tag>X-SF-Loop:)(?P<tx>.*)")
@pattern
def X_SOURCE_IP():                  yield from Φ(r"(?P<tag>X-SOURCE-IP:)(?P<tx>.*)")
@pattern
def X_Spam():                       yield from Φ(r"(?P<tag>X-Spam:)(?P<tx>.*)")
@pattern
def X_UIDL():                       yield from Φ(r"(?P<tag>X-UIDL:)(?P<tx>.*)")
@pattern
def X_Virus_Scanned():              yield from Φ(r"(?P<tag>X-Virus-Scanned:)(?P<tx>.*)")
@pattern
def X_Yahoo_Newman_Property():      yield from Φ(r"(?P<tag>X-Yahoo-Newman-Property:)(?P<tx>.*)")
#-------------------------------------------------------------------------------
@pattern
def Cc():                           yield from Φ(r"(?P<tag>Cc:)(?P<tx>.*(?:\n\t.*)*)")
@pattern
def Content_Type():                 yield from Φ(r"(?P<tag>Content-Type:)(?P<tx>.*\n.*)")
@pattern
def DomainKey_Signature():          yield from Φ(r"(?P<tag>DomainKey-Signature:)(?P<tx>.*(?:\n[ \t].*)?)")
@pattern
def Received():                     yield from Φ(r"(?P<tag>Received:)(?P<tx>.*(?:\n[ \t].*)*)")
#-------------------------------------------------------------------------------
hex_number= r"(0[xX])?[\dA-Fa-f]+"
real_number = r"(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?"
#-------------------------------------------------------------------------------
@pattern
def Value(X):
    yield from \
    ( POS(0)                                    + λ(f'''{X} = []''')
    + ARBNO(
#       θ("OUTPUT") +
        ( φ(r"\n")                              + λ(f'''{X}.append('η()\\n')''')
        | φ(r"[ \t\r\f]+")                      + λ(f'''{X}.append('μ()')''')
        | φ(r"^[^: \t\r\f\n]+:") % "tx"         + λ(f'''{X}.append("σ('" + tx + "')")''')
        | φ(r"[ ]+") % "tx"                     + λ(f'''{X}.append("σ('" + tx + "')")''')
        | φ(r"[0-9]{2,}")                       + λ(f"""{X}.append('φ(r"[0-9]+")')""")
        | φ(r"[0-9]")                           + λ(f"""{X}.append('φ(r"[0-9]")')""")
        | φ(r"[A-Z]{2,}")                       + λ(f"""{X}.append('φ(r"[A-Z]+")')""")
        | φ(r"[A-Z]")                           + λ(f"""{X}.append('φ(r"[A-Z]")')""")
        | φ(r"[a-z]{2,}")                       + λ(f"""{X}.append('φ(r"[a-z]+")')""")
        | φ(r"[a-z]")                           + λ(f"""{X}.append('φ(r"[a-z]")')""")
        | LEN(1) % "tx"                         + λ(f'''{X}.append("σ('" + ("\\\\" if tx == "\\\\" else "") + tx + "')")''')
        ) # @ "OUTPUT"
      )
    + RPOS(0)
    )
#-------------------------------------------------------------------------------
@pattern
def Inbox(X):
    global lineno
    yield from \
    ( POS(0)                                    + λ(f'''{X} = []''')
    + ARBNO(
#       θ("OUTPUT") +
        ( φ(reFromSection)                      + λ(f'''{X}.append("φ(reFromSection)")''')
        | φ(r"\n")                              + λ(f'''{X}.append('η()\\n')''')
        | φ(r"[ \t\r\f]+")                      + λ(f'''{X}.append('μ()')''')
        | ε() % "tag"
        + ε() % "tx"
        + ( Authentication_Results()            + λ(f"""{X}.append("Authentication_Results()")""")
          | Cc()                                + λ(f"""{X}.append("Cc()")""")
          | Comment()                           + λ(f"""{X}.append("Comment()")""")
          | Content_class()                     + λ(f"""{X}.append("Content_class()")""")
          | Content_Length()                    + λ(f"""{X}.append("Content_Length()")""")
          | Content_Transfer_Encoding()         + λ(f"""{X}.append("Content_Transfer_Encoding()")""")
          | Content_Type()                      + λ(f"""{X}.append("Content_Type()")""")
          | Date()                              + λ(f"""{X}.append("Date()")""")
          | DomainKey_Signature()               + λ(f"""{X}.append("DomainKey_Signature()")""")
          | From()                              + λ(f"""{X}.append("From()")""")
          | Importance()                        + λ(f"""{X}.append("Importance()")""")
          | In_Reply_To()                       + λ(f"""{X}.append("In_Reply_To()")""")
          | Message_ID()                        + λ(f"""{X}.append("Message_ID()")""")
          | MIME_Version()                      + λ(f"""{X}.append("MIME_Version()")""")
          | Priority()                          + λ(f"""{X}.append("Priority()")""")
          | Received()                          + λ(f"""{X}.append("Received()")""")
          | References()                        + λ(f"""{X}.append("References()")""")
          | Return_Path()                       + λ(f"""{X}.append("Return_Path()")""")
          | Subject()                           + λ(f"""{X}.append("Subject()")""")
          | Thread_Index()                      + λ(f"""{X}.append("Thread_Index()")""")
          | Thread_Topic()                      + λ(f"""{X}.append("Thread_Topic()")""")
          | To()                                + λ(f"""{X}.append("To()")""")
          | X_Account_Key()                     + λ(f"""{X}.append("X_Account_Key()")""")
          | X_Apparently_To()                   + λ(f"""{X}.append("X_Apparently_To()")""")
          | X_MAIL_FROM()                       + λ(f"""{X}.append("X_MAIL_FROM()")""")
          | X_Mailer()                          + λ(f"""{X}.append("X_Mailer()")""")
          | X_MimeOLE()                         + λ(f"""{X}.append("X_MimeOLE()")""")
          | X_Mozilla_Keys()                    + λ(f"""{X}.append("X_Mozilla_Keys()")""")
          | X_Mozilla_Status()                  + λ(f"""{X}.append("X_Mozilla_Status()")""")
          | X_Mozilla_Status2()                 + λ(f"""{X}.append("X_Mozilla_Status2()")""")
          | X_MS_Has_Attach()                   + λ(f"""{X}.append("X_MS_Has_Attach()")""")
          | X_MS_TNEF_Correlator()              + λ(f"""{X}.append("X_MS_TNEF_Correlator()")""")
          | X_MSMail_Priority()                 + λ(f"""{X}.append("X_MSMail_Priority()")""")
          | X_OriginalArrivalTime()             + λ(f"""{X}.append("X_OriginalArrivalTime()")""")
          | X_Originating_IP()                  + λ(f"""{X}.append("X_Originating_IP()")""")
          | X_Priority()                        + λ(f"""{X}.append("X_Priority()")""")
          | X_SF_Loop()                         + λ(f"""{X}.append("X_SF_Loop()")""")
          | X_SOURCE_IP()                       + λ(f"""{X}.append("X_SOURCE_IP()")""")
          | X_Spam()                            + λ(f"""{X}.append("X_Spam()")""")
          | X_UIDL()                            + λ(f"""{X}.append("X_UIDL()")""")
          | X_Virus_Scanned()                   + λ(f"""{X}.append("X_Virus_Scanned()")""")
          | X_Yahoo_Newman_Property()           + λ(f"""{X}.append("X_Yahoo_Newman_Property()")""")
          )                                     + λ(f"""remember(tag, tx)""") # REMEMBER every piece
        | φ(r"^[^: \t\r\f\n]+:") % "tx"         + λ(f'''{X}.append("σ('" + tx + "')")''')
        | φ(r"[ ]+") % "tx"                     + λ(f'''{X}.append("σ('" + tx + "')")''')
        | φ(r"[0-9]{2,}")                       + λ(f"""{X}.append('φ(r"[0-9]+")')""")
        | φ(r"[0-9]")                           + λ(f"""{X}.append('φ(r"[0-9]")')""")
        | φ(r"[A-Z]{2,}")                       + λ(f"""{X}.append('φ(r"[A-Z]+")')""")
        | φ(r"[A-Z]")                           + λ(f"""{X}.append('φ(r"[A-Z]")')""")
        | φ(r"[a-z]{2,}")                       + λ(f"""{X}.append('φ(r"[a-z]+")')""")
        | φ(r"[a-z]")                           + λ(f"""{X}.append('φ(r"[a-z]")')""")
        | LEN(1) % "tx"                         + λ(f'''{X}.append("σ('" + ("\\\\" if tx == "\\\\" else "") + tx + "')")''')
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
reFromSection = (
    r"From -"
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
    for match in re.finditer(r"^" + reFromSection + r"$", inbox, re.MULTILINE):
        sections.append(match.span()[0])
    sections.append(total_size)
    print(f" {len(sections)} sections.", flush=True)
#-------------------------------------------------------------------------------
def parse_emails():
    global H
    print("# Parsing emails.\n", flush=True)
    iteration = 0
    start_offset = None
    finish_offset = 0
    for section in sections:
        if iteration > ITERATIONS: break
        iteration += 1
        start_offset = finish_offset
        finish_offset = section
        email = inbox[start_offset:finish_offset]
        if match := re.match(r"(?:.*\n)+(?:Content-Length: [0-9]+\n)", email):
            email_header = match.group()
            if email_header in Inbox('H'):
                print(" + ".join(H))
#-------------------------------------------------------------------------------
seen = None
def remember(tag, value):
    global R, seen
    if seen is None: seen = dict()
    if tag not in seen: seen[tag] = dict()
    if value in Value('R'):
        ptrn = " + ".join(R)
        if ptrn not in seen[tag]: seen[tag][ptrn] = dict()
        if value not in seen[tag][ptrn]:
            seen[tag][ptrn][value] = 1
        else: seen[tag][ptrn][value] += 1
    else: print("Yikes!")
    return True
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
        pprint(seen, width=170, indent=2)
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    GLOBALS(globals())
    main()
#-------------------------------------------------------------------------------
