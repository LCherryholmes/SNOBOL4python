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
def trace(s): print(s, flush=True); return True
#-------------------------------------------------------------------------------
@pattern
def Authentication_Results():       yield from Φ(r"(?P<tag>Authentication-Results:)(?P<tx>.*)")
@pattern
def Cc():                           yield from Φ(r"(?P<tag>Cc:(?P<tx>.*)(?:\n\t.*)*)")
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
def Content_Type():                 yield from Φ(r"(?P<tag>Content-Type:)(?P<tx>.*\n.*)")
@pattern
def DomainKey_Signature():          yield from Φ(r"(?P<tag>DomainKey-Signature:)(?P<tx>.*(?:\n[ \t].*)?)")
@pattern
def Received():                     yield from Φ(r"(?P<tag>Received:)(?P<tx>.*(?:\n[ \t].*)*)")
#-------------------------------------------------------------------------------
mem = dict()
def remember(tag, value):
    global mem
    if tag not in mem: mem[tag] = dict()
    if value not in mem[tag]:
        mem[tag][value] = 1
    else: mem[tag][value] += 1
    return True
#-------------------------------------------------------------------------------
hex_number= r"(0[xX])?[\dA-Fa-f]+"
real_number = r"(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?"
#-------------------------------------------------------------------------------
@pattern
def Inbox():
    global lineno
    yield from \
    ( POS(0)                                    + λ('''P = []''')
    + ARBNO(
#       θ("OUTPUT") +
        ( φ(reFromSection)                      + λ('''P.append("φ(reFromSection)")''')
        | φ(r"\n")                              + λ('''P.append('η()\\n')''')
        | φ(r"[ \t\r\f]+")                      + λ('''P.append('μ()')''')
        | ( Authentication_Results()            + λ("""P.append("Authentication_Results()")""")
          | Cc()                                + λ("""P.append("Cc()")""")
          | Comment()                           + λ("""P.append("Comment()")""")
          | Content_class()                     + λ("""P.append("Content_class()")""")
          | Content_Length()                    + λ("""P.append("Content_Length()")""")
          | Content_Transfer_Encoding()         + λ("""P.append("Content_Transfer_Encoding()")""")
          | Content_Type()                      + λ("""P.append("Content_Type()")""")
          | Date()                              + λ("""P.append("Date()")""")
          | DomainKey_Signature()               + λ("""P.append("DomainKey_Signature()")""")
          | From()                              + λ("""P.append("From()")""")
          | Importance()                        + λ("""P.append("Importance()")""")
          | In_Reply_To()                       + λ("""P.append("In_Reply_To()")""")
          | Message_ID()                        + λ("""P.append("Message_ID()")""")
          | MIME_Version()                      + λ("""P.append("MIME_Version()")""")
          | Priority()                          + λ("""P.append("Priority()")""")
          | Received()                          + λ("""P.append("Received()")""")
          | References()                        + λ("""P.append("References()")""")
          | Return_Path()                       + λ("""P.append("Return_Path()")""")
          | Subject()                           + λ("""P.append("Subject()")""")
          | Thread_Index()                      + λ("""P.append("Thread_Index()")""")
          | Thread_Topic()                      + λ("""P.append("Thread_Topic()")""")
          | To()                                + λ("""P.append("To()")""")
          | X_Account_Key()                     + λ("""P.append("X_Account_Key()")""")
          | X_Apparently_To()                   + λ("""P.append("X_Apparently_To()")""")
          | X_MAIL_FROM()                       + λ("""P.append("X_MAIL_FROM()")""")
          | X_Mailer()                          + λ("""P.append("X_Mailer()")""")
          | X_MimeOLE()                         + λ("""P.append("X_MimeOLE()")""")
          | X_Mozilla_Keys()                    + λ("""P.append("X_Mozilla_Keys()")""")
          | X_Mozilla_Status()                  + λ("""P.append("X_Mozilla_Status()")""")
          | X_Mozilla_Status2()                 + λ("""P.append("X_Mozilla_Status2()")""")
          | X_MS_Has_Attach()                   + λ("""P.append("X_MS_Has_Attach()")""")
          | X_MS_TNEF_Correlator()              + λ("""P.append("X_MS_TNEF_Correlator()")""")
          | X_MSMail_Priority()                 + λ("""P.append("X_MSMail_Priority()")""")
          | X_OriginalArrivalTime()             + λ("""P.append("X_OriginalArrivalTime()")""")
          | X_Originating_IP()                  + λ("""P.append("X_Originating_IP()")""")
          | X_Priority()                        + λ("""P.append("X_Priority()")""")
          | X_SF_Loop()                         + λ("""P.append("X_SF_Loop()")""")
          | X_SOURCE_IP()                       + λ("""P.append("X_SOURCE_IP()")""")
          | X_Spam()                            + λ("""P.append("X_Spam()")""")
          | X_UIDL()                            + λ("""P.append("X_UIDL()")""")
          | X_Virus_Scanned()                   + λ("""P.append("X_Virus_Scanned()")""")
          | X_Yahoo_Newman_Property()           + λ("""P.append("X_Yahoo_Newman_Property()")""")
          )                                     + λ("""remember(tag, tx)""") # REMEMBER every piece
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
    print("# Parsing emails.\n", flush=True)
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
        pprint(mem)
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    GLOBALS(globals())
    main()
#-------------------------------------------------------------------------------
