# -*- coding: utf-8 -*-
import re
import SNOBOL4python
from SNOBOL4python import GLOBALS, pattern
from SNOBOL4python import ALPHABET, UCASE, LCASE, DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ, α, ω, φ, Φ
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCESS, TAB
from pprint import pformat, pprint
#-------------------------------------------------------------------------------
def trace(s): print(s, flush=True); return True
#-------------------------------------------------------------------------------
@pattern
def Authentication_Results():       yield from Φ(r"(?P<tag>Authentication-Results): ?") \
                                             + Φ(r"(?P<lit>.*)")
@pattern
def Comment():                      yield from Φ(r"(?P<tag>Comment): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def Content_class():                yield from Φ(r"(?P<tag>Content-[Cc]lass): ?") \
                                             + Φ(r"(?P<lit>.*)")
@pattern
def Content_Length():               yield from Φ(r"(?P<tag>Content-Length): ?") \
                                             + Φ(r"(?P<lit>[0-9]+)")
@pattern
def Content_Transfer_Encoding():    yield from Φ(r"(?P<tag>Content-Transfer-Encoding): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def Date():                         yield from Φ(r"(?P<tag>Date): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def From():                         yield from Φ(r"(?P<tag>From): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def Importance():                   yield from Φ(r"(?P<tag>Importance): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def In_Reply_To():                  yield from Φ(r"(?P<tag>In-Reply-To): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def Message_ID():                   yield from Φ(r"(?P<tag>Message-ID): ?") \
                                             + Φ(r"(?P<lit>.*)")
@pattern
def MIME_Version():                 yield from Φ(r"(?P<tag>MIME-Version): ?") \
                                             + Φ(r"(?P<lit>.*)")
@pattern
def Priority():                     yield from Φ(r"(?P<tag>Priority): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def References():                   yield from Φ(r"(?P<tag>References): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def Return_Path():                  yield from Φ(r"(?P<tag>Return-Path): ?") \
                                             + ( Φ(r"<") + email_address() + Φ(r">")
                                               | Φ(r"(?P<txt>.*)")
                                               )
@pattern
def Subject():                      yield from Φ(r"(?P<tag>Subject): ?") \
                                             + Φ(r"(.*)")
@pattern
def Thread_Index():                 yield from Φ(r"(?P<tag>[Tt]hread-[Ii]ndex): ?") \
                                             + ( Φ(r"[+=/0-9A-Za-z]{36}")
                                               | Φ(r"(?P<txt>.*)")
                                               )
@pattern
def Thread_Topic():                 yield from Φ(r"(?P<tag>Thread-Topic): ?") \
                                             + Φ(r"(.*)")
@pattern
def To():                           yield from Φ(r"(?P<tag>To): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_Account_Key():                yield from Φ(r"(?P<tag>X-Account-Key): ?") \
                                             + ( Φ(r"r'account1'")
                                               | Φ(r"(?P<txt>.*)")
                                               )
@pattern
def X_Apparently_To():              yield from  ( Φ(r"(?P<tag>X-Apparently-To): ?")
                                                + ( Φ( r"lcherryh@yahoo.com via"
                                                       r" [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
                                                       r"; (Sun|Mon|Tue|Wed|Thu|Fri|Sat)"
                                                       r", [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4}"
                                                       r" [0-9]{2}:[0-9]{2}:[0-9]{2} -[0-9]{4}"
                                                     )
                                                 | Φ(r"(?P<txt>.*)")
                                                   )
                                                )
@pattern
def X_MAIL_FROM():                  yield from Φ(r"(?P<tag>X-MAIL-FROM): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_Mailer():                     yield from Φ(r"(?P<tag>X-Mailer): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_MimeOLE():                    yield from Φ(r"(?P<tag>X-(?:Mime|MIME)OLE): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_Mozilla_Keys():               yield from Φ(r"(?P<tag>X-Mozilla-Keys): ?")    + Φ(r'[ ]{80}')
@pattern
def X_Mozilla_Status():             yield from Φ(r"(?P<tag>X-Mozilla-Status): ?")  + Φ(r'[0-9]{4}')
@pattern
def X_Mozilla_Status2():            yield from Φ(r"(?P<tag>X-Mozilla-Status2): ?") + Φ(r'[0-9]{8}')
@pattern
def X_MS_Has_Attach():              yield from Φ(r"(?P<tag>X-MS-Has-Attach): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_MS_TNEF_Correlator():         yield from Φ(r"(?P<tag>X-MS-TNEF-Correlator) ?:") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_MSMail_Priority():            yield from Φ(r"(?P<tag>X-MSMail-Priority): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_OriginalArrivalTime():        yield from ( Φ(r"(?P<tag>X-OriginalArrivalTime): ?")
                                               + ( Φ(r"[0-9]{2} "
                                                     r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) "
                                                     r"[0-9]{4} "
                                                     r"[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} "
                                                     r"(UTC) FILETIME=\[[0-9A-F]{8}:[0-9A-F]{8}\]"
                                                    )
                                                 | Φ(r"(?P<txt>.*)")
                                                 )
                                               )
@pattern
def X_Originating_IP():             yield from ( Φ(r"(?P<tag>X-Originating-IP): ?")
                                               + ( Φ(r'\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\]')
                                                 | Φ(r"(?P<txt>.*)")
                                                 )
                                               )
@pattern
def X_Priority():                   yield from Φ(r"(?P<tag>X-Priority): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_SF_Loop():                    yield from Φ(r"(?P<tag>X-SF-Loop): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_SOURCE_IP():                  yield from Φ(r"(?P<tag>X-SOURCE-IP): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_Spam():                       yield from Φ(r"(?P<tag>X-Spam): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_UIDL():                       yield from Φ(r"(?P<tag>X-UIDL): ?") + Φ(r"[+/0-9A-Za-z]{27}")
@pattern
def X_Virus_Scanned():              yield from Φ(r"(?P<tag>X-Virus-Scanned): ?") \
                                             + Φ(r"(?P<txt>.*)")
@pattern
def X_Yahoo_Newman_Property():      yield from Φ(r"(?P<tag>X-Yahoo-Newman-Property): ?") \
                                             + Φ(r"(?P<txt>.*)")
#-------------------------------------------------------------------------------
@pattern
def Cc():                           yield from Φ(r"(?P<tag>Cc): ?") \
                                             + Φ(r"(?P<txt>.*(?:\n\t.*)*)")
@pattern
def Content_Type():                 yield from Φ(r"(?P<tag>Content-Type): ?") \
                                             + ( Φ( r'multipart/alternative;\n'
                                                    r'\tboundary="\-\-\-\-_=_NextPart_[0-9]{3}_[0-9A-F]{8}\.[0-9A-F]{8}"'
                                                  )
                                               | Φ(r"(?P<lit>.*\n.*)")
                                               )
@pattern
def DomainKey_Signature():          yield from Φ(r"(?P<tag>DomainKey-Signature): ?") \
                                             + Φ(r"(?P<txt>.*(?:\n[ \t].*)?)")
@pattern
def Received():                     yield from Φ(r"(?P<tag>Received): ?") \
                                             + Φ(r"(.*(?:\n[ \t].*)*)")
#-------------------------------------------------------------------------------
rex_decimal3            = r'[0-9]{3}'
rex_upper_hex8          = r'[0-9A-F]{8}'
rex_hex_number          = r'(0[xX])?[\dA-Fa-f]+'
rex_military_time       = r'[0-9]{2}:[0-9]{2}:[0-9]{2}'
rex_real_number         = r'(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'
rex_day_of_week         = r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat)'
rex_short_month         = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
rex_time_zone           = r'(?<=\s)-[0-9]{4}(?=\s)'
rex_From                = ( r'From -'
                            r' (Sun|Mon|Tue|Wed|Thu|Fri|Sat)'
                            r' (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
                            r' [0-9]{1,2}'
                            r' [0-9]{2}:[0-9]{2}:[0-9]{2}'
                            r' [0-9]{4}'
                          )
#-------------------------------------------------------------------------------
rex_ip_address          = r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
exp_ip_address          = r'[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}'
#-------------------------------------------------------------------------------
rex_url_address         = r'(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\.){3}\d{1,3})(?::\d+)?(?:/\S*)?'
exp_url_address         = r'(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})(?::\d+)?(?:/\S*)?'
#-------------------------------------------------------------------------------
rex_email_address       = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
exp_email_address       = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}'
#-------------------------------------------------------------------------------
@pattern
def ip_address():       yield from Φ(rex_ip_address)
@pattern
def url_address():      yield from Φ(rex_url_address)
@pattern
def email_address():    yield from Φ(rex_email_address)
#-------------------------------------------------------------------------------
xlr8 = \
{
    'tag':                  (r'^[0-9-A-Za-z]+:'   , (lambda t: t[0:-1])),
    'time_zone':            (rex_time_zone        , (lambda t: r'-[0-9]{4}')),
    'ip_address':           (rex_ip_address       , (lambda t: exp_ip_address)),
    'day_of_week':          (rex_day_of_week      , (lambda t: rex_day_of_week)),
    'short_month':          (rex_short_month      , (lambda t: rex_short_month)),
    'rex_url_address':      (rex_url_address      , (lambda t: exp_url_address)),
    'rex_email_address':    (rex_email_address    , (lambda t: exp_email_address)),
    'military_time':        (rex_military_time    , (lambda t: rex_military_time)),
    'sps':                  (r'[ ]{2,}'           , (lambda t: r'[ ]{' + str(len(t)) + r'}')),
    'sp':                   (r'[ ]'               , (lambda t: r' ')),
    'tabs':                 (r'[\t]{2,}'          , (lambda t: r'\t{' + str(len(t)) + r'}')),
    'tab':                  (r'[\t]'              , (lambda t: r'\t')),
    'vt':                   (r'[\v]'              , (lambda t: r'\v')),
    'bel':                  (r'\a'                , (lambda t: r'\a')),
#   'bs':                   (r'\b'                , (lambda t: r'\b')),
    'lf':                   (r'\n'                , (lambda t: r'\n')),
    'cr':                   (r'\r'                , (lambda t: r'\r')),
    'ff':                   (r'\f'                , (lambda t: r'\f')),
    'bslash':               (r'\\'                , (lambda t: r'\\')),
    'dot':                  (r'\.'                , (lambda t: r'\.')),
    'star':                 (r'\*'                , (lambda t: r'\*')),
    'plus':                 (r'\+'                , (lambda t: r'\+')),
    'qmark':                (r'\?'                , (lambda t: r'\?')),
    'lbrakect':             (r'\['                , (lambda t: r'\[')),
    'rbracket':             (r'\]'                , (lambda t: r'\]')),
    'lparen':               (r'\('                , (lambda t: r'\(')),
    'rparen':               (r'\)'                , (lambda t: r'\)')),
    'lcurly':               (r'\{'                , (lambda t: r'\{')),
    'rcurly':               (r'\}'                , (lambda t: r'\}')),
    'caret':                (r'\^'                , (lambda t: r'\^')),
    'dolsign':              (r'\$'                , (lambda t: r'\$')),
    'vertbar':              (r'\|'                , (lambda t: r'\|')),
    'digits':               (r'[0-9]{2,}'         , (lambda t: r'[0-9]{' + str(len(t)) + r'}')),
    'digit':                (r'[0-9]'             , (lambda t: r'[0-9]')),
    'ucases':               (r'[A-Z]{2,}'         , (lambda t: r'[A-Z]{' + str(len(t)) + r'}')),
    'ucase':                (r'[A-Z]'             , (lambda t: r'[A-Z]')),
    'lcases':               (r'[a-z]{2,}'         , (lambda t: r'[a-z]{' + str(len(t)) + r'}')),
    'lcase':                (r'[a-z]'             , (lambda t: r'[a-z]')),
    'anychar':              (r'.'                 , (lambda t: t))
}
#-------------------------------------------------------------------------------
xlr8_rex = "|".join((f"(?P<{item[0]}>{item[1][0]})" for item in xlr8.items()))
xlr8_re  = re.compile(xlr8_rex)
#-------------------------------------------------------------------------------
def xlr8_pattern(string):
    regexs = []
    for matches in re.finditer(xlr8_re, string):
        lastgroup = matches.lastgroup
        expansion = xlr8[lastgroup][1]
        expansion = expansion(matches.groupdict()[lastgroup])
        if lastgroup in ('tag', 'anychar'):
            expansion = re.escape(expansion)
        regexs.append(expansion)
    return "".join(regexs)
#-------------------------------------------------------------------------------
@pattern
def Inbox(X):
    global lineno
    yield from \
    ( POS(0)                                    + λ(f'''{X} = []''')
    + ARBNO(
#       θ("OUTPUT") +
        ( Φ(rex_From) % "from_marker"           + λ(f'''{X}.append("Φ(rex_From)")''')
        | Φ(r"\n")                              + λ(f'''{X}.append("η()\\n")''')
        | Φ(r"[ \t\r\f]+")                      + λ(f'''{X}.append("μ()")''')
        | ε() % "tag" % "txt" % "lit"
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
          )                                     + λ(f"""remember(tag, txt, lit)""") # REMEMBER every piece
        | Φ(r'^(?P<tag>[^: \t\r\f\n]+):')       + λ(f'''{X}.append("σ('" + tag + "')")''')
        + Φ(r'(?P<lit>.*)')                     + λ(f"""remember(tag, txt, lit)""") # REMEMBER novel tag
        | Φ(r'[ ]+') % "tx"                     + λ(f'''{X}.append("σ('" + tx + "')")''')
        | Φ(r'[0-9]{2,}')                       + λ(f"""{X}.append("Φ(r'[0-9]+')")""")
        | Φ(r'[0-9]')                           + λ(f"""{X}.append("Φ(r'[0-9]')")""")
        | Φ(r'[A-Z]{2,}')                       + λ(f"""{X}.append("Φ(r'[A-Z]+')")""")
        | Φ(r'[A-Z]')                           + λ(f"""{X}.append("Φ(r'[A-Z]')")""")
        | Φ(r'[a-z]{2,}')                       + λ(f"""{X}.append("Φ(r'[a-z]+')")""")
        | Φ(r'[a-z]')                           + λ(f"""{X}.append("Φ(r'[a-z]')")""")
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
sections = []
def scan_sections():
    global sections
    print("# Scanning sections.", end="", flush=True)
    for match in re.finditer(fr"^{rex_From}$", inbox, re.MULTILINE):
        sections.append(match.span()[0])
    sections.append(total_size)
    print(f" {len(sections)} sections.", flush=True)
#-------------------------------------------------------------------------------
mem = dict()
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
                print('#', from_marker)
                email_pattern = " + ".join(H)
                if email_pattern not in mem:
                    mem[email_pattern] = 1
                else: mem[email_pattern] += 1
#-------------------------------------------------------------------------------
seen = None
def remember(tag, txt='', lit=''):
    global R, seen
    if seen is None: seen = dict()
    if tag not in seen: seen[tag] = dict()
    if txt != "":
        ptrn = xlr8_pattern(txt)
        if ptrn not in seen[tag]: seen[tag][ptrn] = dict()
        if txt not in seen[tag][ptrn]: seen[tag][ptrn][txt] = 1
        else: seen[tag][ptrn][txt] += 1
    if lit != "":
        ptrn = re.escape(lit) \
                 .replace('\\\n', '\\n') \
                 .replace('\\\t', '\\t')
        if ptrn not in seen[tag]: seen[tag][ptrn] = dict()
    return True
#-------------------------------------------------------------------------------
def reminisce():
    if False: pprint(seen, width=170, indent=2)
    for tag, patterns in sorted(seen.items()):
        if len(patterns) > 0:
            print(f"#{'-' * 119}")
            print(f"@pattern")
            print(f"def {tag.replace('-', '_')}(): yield from (")
            bar = ' '
            for ptrn, texts in patterns.items():
                print(f"{bar}   Φ(r'" + ptrn.replace("'", "\\'") + "')") #
                for text, count in texts.items():
                    print(f"""     #{count}:""" + text.replace('\n', '\\n'))
                bar = '|'
            print(f")")
    if False: pprint(mem, width=170, indent=2)
    print(f"#{'-' * 119}")
    print(f"@pattern")
    print(f"def Inbox(): yield from (")
    bar = ' '
    for code, count in mem.items():
        code = code.replace('\n + ', ' + ')
        print(f"{bar}   {code}", end="")
        bar = '|'
    print(f")")
#-------------------------------------------------------------------------------
inbox = None
total_size = None
ITERATIONS = 32
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
        reminisce()
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    GLOBALS(globals())
    main()
#-------------------------------------------------------------------------------
