# -*- coding: utf-8 -*-
import re
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pprint, pformat
#-----------------------------------------------------------------------------------------------------------------------
def trace(s): print(s, flush=True); return True
#-----------------------------------------------------------------------------------------------------------------------
Accept_Language           =   ( φ(r"(?P<tag>[Aa]ccept-?[Ll]anguage): ?")
                              + ( φ(r'en-US')
                                | φ(r"(?P<lit>.*)")
                                )
                              )
Authentication_Results    =   φ(r"(?P<tag>Authentication-Results): ?")  + φ(r"(?P<txt>.*)")
Cc                        =   φ(r"(?P<tag>Cc): ?")                      + φ(r"(?P<txt>.*(?:\n\t.*)*)")
Comment                   =   φ(r"(?P<tag>Comment): ?")                 + φ(r"(?P<txt>.*)")
Content_class             =   ( φ(r"(?P<tag>Content-[Cc]lass): ?") \
                              + ( φ(r'urn:content\-classes:message')
                                | φ(r"(?P<lit>.*)")
                                )
                              )
Content_Language          =   ( φ(r"(?P<tag>Content-Language): ?") \
                              + ( φ(r'en-US')
                                | φ(r"(?P<txt>.*)")
                                )
                              )
Content_Length            =   φ(r"(?P<tag>Content-Length): ?")            + φ(r"(?P<lit>[0-9]+)")
Content_Transfer_Encoding =   φ(r"(?P<tag>Content-Transfer-Encoding): ?") + φ(r"(?P<lit>.*)")
Content_Type              =   ( φ(r"(?P<tag>Content-Type): ?") \
                              + ( φ( r'multipart/alternative;\n'
                                     r'\tboundary="\-\-\-\-_=_NextPart_[0-9]{3}_[0-9A-F]{8}\.[0-9A-F]{8}"'
                                   )
                                | φ(r"(?P<lit>.*\n.*)")
                                )
                              )
Date                      =   φ(r"(?P<tag>Date): ?") + φ(r"(?P<txt>.*)")
DomainKey_Signature       =   φ(r"(?P<tag>DomainKey-Signature): ?") + φ(r"(?P<txt>.*(?:\n[ \t].*)?)")
From                      =   φ(r"(?P<tag>From): ?") + φ(r"(?P<lit>.*)")
Importance                =   ( φ(r"(?P<tag>Importance): ?") \
                              + ( φ(r'[Nn]ormal')
                                | φ(r"(?P<lit>.*)")
                                )
                              )
In_Reply_To               =   φ(r"(?P<tag>In-Reply-To): ?")       + φ(r"(?P<txt>.*)")
Message_ID                =   φ(r"(?P<tag>Message-ID): ?")        + φ(r"(?P<lit>.*)")
MIME_Version              =   ( φ(r"(?P<tag>MIME-Version): ?") \
                              + ( φ(r'1\.0')
                                | φ(r"(?P<lit>.*)")
                                )
                              )
Message_ID                =   φ(r"(?P<tag>Message-ID): ?")        + φ(r"(?P<txt>.*)")
Priority                  =   ( φ(r"(?P<tag>Priority): ?") \
                              + ( φ(r'[Nn]ormal')
                                | φ(r"(?P<lit>.*)")
                                )
                              )
Received                  =   φ(r"(?P<tag>Received): ?")          + φ(r"(.*(?:\n[ \t].*)*)")
References                =   φ(r"(?P<tag>References): ?")        + φ(r"(?P<txt>.*)")
Reply_To                  =   φ(r"(?P<tag>Reply-To): ?")          + φ(r"(?P<txt>.*)")
Return_Path               =   ( φ(r"(?P<tag>Return-Path): ?") \
                              + ( φ(r"<") + ζ(lambda: email_address) + φ(r">")
                                | φ(r"(?P<txt>.*)")
                                )
                              )
Subject                   =   φ(r"(?P<tag>Subject): ?") + φ(r"(.*)")
Thread_Index              =   ( φ(r"(?P<tag>[Tt]hread-[Ii]ndex): ?") \
                              + ( φ(r"[+=/0-9A-Za-z]{36}")
                                | φ(r"(?P<txt>.*)")
                                )
                              )
Thread_Topic              =   φ(r"(?P<tag>Thread-Topic): ?") + φ(r"(.*)")
To                        =   φ(r"(?P<tag>To): ?") + φ(r"(?P<txt>.*)")
X_Account_Key             =   ( φ(r"(?P<tag>X-Account-Key): ?") \
                              + ( φ(r"r'account1'")
                                | φ(r"(?P<txt>.*)")
                                )
                              )
X_Apparently_To           =   ( φ(r"(?P<tag>X-Apparently-To): ?") \
                              + ( φ( r"lcherryh@yahoo.com via"
                                     r" [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
                                     r"; (Sun|Mon|Tue|Wed|Thu|Fri|Sat)"
                                     r", [0-9]{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4}"
                                     r" [0-9]{2}:[0-9]{2}:[0-9]{2} -[0-9]{4}"
                                  )
                                | φ(r"(?P<txt>.*)")
                                )
                              )
X_ELNK_Trace              =   φ(r"(?P<tag>X-ELNK-Trace): ?")          + φ(r"(?P<txt>.*)")
X_MAIL_FROM               =   φ(r"(?P<tag>X-MAIL-FROM): ?")           + φ(r"(?P<txt>.*)")
X_Mailer                  =   φ(r"(?P<tag>X-Mailer): ?")              + φ(r"(?P<txt>.*)")
X_MimeOLE                 =   φ(r"(?P<tag>X-(?:Mime|MIME)OLE): ?")    + φ(r"(?P<txt>.*)")
X_Mozilla_Keys            =   φ(r"(?P<tag>X-Mozilla-Keys): ?")        + φ(r'[ ]{80}')
X_Mozilla_Status          =   φ(r"(?P<tag>X-Mozilla-Status): ?")      + φ(r'[0-9]{4}')
X_Mozilla_Status2         =   φ(r"(?P<tag>X-Mozilla-Status2): ?")     + φ(r'[0-9]{8}')
X_MS_Has_Attach           =   φ(r"(?P<tag>X-MS-Has-Attach): ?")       + φ(r"(?P<txt>.*)")
X_MS_TNEF_Correlator      =   φ(r"(?P<tag>X-MS-TNEF-Correlator) ?:")  + φ(r"(?P<txt>.*)")
X_MSMail_Priority         =   φ(r"(?P<tag>X-MSMail-Priority): ?")     + φ(r"(?P<txt>.*)")
X_OriginalArrivalTime     =   ( φ(r"(?P<tag>X-OriginalArrivalTime): ?")
                              + ( φ(r"[0-9]{2} "
                                    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) "
                                    r"[0-9]{4} "
                                    r"[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{4} "
                                    r"(UTC) FILETIME=\[[0-9A-F]{8}:[0-9A-F]{8}\]"
                                  )
                                | φ(r"(?P<txt>.*)")
                                )
                              )
X_Originating_IP          =   ( φ(r"(?P<tag>X-Originating-IP): ?")
                              + ( φ(r'\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\]')
                                | φ(r"(?P<txt>.*)")
                                )
                              )
X_Priority                =   φ(r"(?P<tag>X-Priority): ?")              + φ(r"(?P<txt>.*)")
X_SF_Loop                 =   φ(r"(?P<tag>X-SF-Loop): ?")               + φ(r"(?P<txt>.*)")
X_SOURCE_IP               =   φ(r"(?P<tag>X-SOURCE-IP): ?")             + φ(r"(?P<txt>.*)")
X_Spam                    =   φ(r"(?P<tag>X-Spam): ?")                  + φ(r"(?P<txt>.*)")
X_Spam_Flag               =   φ(r"(?P<tag>X-Spam-Flag): ?")             + φ(r"(?P<txt>.*)")
X_UIDL                    =   φ(r"(?P<tag>X-UIDL): ?")                  + φ(r"[+/0-9A-Za-z]{27}")
X_Virus_Scanned           =   φ(r"(?P<tag>X-Virus-Scanned): ?")         + φ(r"(?P<txt>.*)")
X_YMail_OSG               =   φ(r"(?P<tag>X-YMail-OSG): ?")             + φ(r"(?P<txt>.*)")
X_Yahoo_Newman_Property   =   φ(r"(?P<tag>X-Yahoo-Newman-Property): ?") + φ(r"(?P<txt>.*)")
#=======================================================================================================================
rex_decimal3      = r'[0-9]{3}'
rex_upper_hex8    = r'[0-9A-F]{8}'
rex_hex_number    = r'(0[xX])?[\dA-Fa-f]+'
rex_military_time = r'[0-9]{2}:[0-9]{2}:[0-9]{2}'
rex_real_number   = r'(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'
rex_day_of_week   = r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat)'
rex_short_month   = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
rex_time_zone     = r'(?<=\s)-[0-9]{4}(?=\s)'
rex_From          = ( r'From -'
                      r' (Sun|Mon|Tue|Wed|Thu|Fri|Sat)'
                      r' (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
                      r' [0-9]{1,2}'
                      r' [0-9]{2}:[0-9]{2}:[0-9]{2}'
                      r' [0-9]{4}'
                    )
#-----------------------------------------------------------------------------------------------------------------------
rex_ip_address    = r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
exp_ip_address    = r'[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}'
#-----------------------------------------------------------------------------------------------------------------------
rex_url_address   = r'(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\.){3}\d{1,3})(?::\d+)?(?:/\S*)?'
exp_url_address   = r'(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})(?::\d+)?(?:/\S*)?'
#-----------------------------------------------------------------------------------------------------------------------
rex_domain_name   = r'(?:(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\.){3}\d{1,3})'
exp_domain_name   = r'(?:(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}|localhost|(?:\d{1,3}\\.){3}\d{1,3})'
#-----------------------------------------------------------------------------------------------------------------------
rex_email_address = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
exp_email_address = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}'
#=======================================================================================================================
ip_address        = φ(rex_ip_address)
domain_name       = φ(rex_domain_name)
url_address       = φ(rex_url_address)
email_address     = φ(rex_email_address)
#-----------------------------------------------------------------------------------------------------------------------
xlr8 = \
{
    'tag1':                 (r'^[0-9-A-Za-z]+: '  , (lambda t: t[0:-2])),
    'tag2':                 (r'^[0-9-A-Za-z]+:'   , (lambda t: t[0:-1])),
    'time_zone':            (rex_time_zone        , (lambda t: r'-[0-9]{4}')),
    'ip_address':           (rex_ip_address       , (lambda t: exp_ip_address)),
    'day_of_week':          (rex_day_of_week      , (lambda t: rex_day_of_week)),
    'short_month':          (rex_short_month      , (lambda t: rex_short_month)),
    'rex_domain_name':      (rex_domain_name      , (lambda t: exp_domain_name)),
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
#-----------------------------------------------------------------------------------------------------------------------
xlr8_rex = "|".join((f"(?P<{item[0]}>{item[1][0]})" for item in xlr8.items()))
xlr8_re  = re.compile(xlr8_rex)
#-----------------------------------------------------------------------------------------------------------------------
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
#=======================================================================================================================
def Inbox(X):
    global lineno
    return \
    ( POS(0)                                    + λ(f'''{X} = []''')
    + ARBNO(
#       Θ("OUTPUT") +
        ( φ(rex_From) % "from_marker"           + λ(f'''{X}.append("φ(rex_From)")''')
        | φ(r"\n")                              + λ(f'''{X}.append("η\\n")''')
        | φ(r"[ \t\r\f]+")                      + λ(f'''{X}.append("μ")''')
        | ε() % "tag" % "txt" % "lit"
        + ( Authentication_Results              + λ(f"""{X}.append("Authentication_Results")""")
          | Cc                                  + λ(f"""{X}.append("Cc")""")
          | Comment                             + λ(f"""{X}.append("Comment")""")
          | Content_class                       + λ(f"""{X}.append("Content_class")""")
          | Content_Length                      + λ(f"""{X}.append("Content_Length")""")
          | Content_Transfer_Encoding           + λ(f"""{X}.append("Content_Transfer_Encoding")""")
          | Content_Type                        + λ(f"""{X}.append("Content_Type")""")
          | Date                                + λ(f"""{X}.append("Date")""")
          | DomainKey_Signature                 + λ(f"""{X}.append("DomainKey_Signature")""")
          | From                                + λ(f"""{X}.append("From")""")
          | Importance                          + λ(f"""{X}.append("Importance")""")
          | In_Reply_To                         + λ(f"""{X}.append("In_Reply_To")""")
          | Message_ID                          + λ(f"""{X}.append("Message_ID")""")
          | MIME_Version                        + λ(f"""{X}.append("MIME_Version")""")
          | Priority                            + λ(f"""{X}.append("Priority")""")
          | Received                            + λ(f"""{X}.append("Received")""")
          | References                          + λ(f"""{X}.append("References")""")
          | Return_Path                         + λ(f"""{X}.append("Return_Path")""")
          | Subject                             + λ(f"""{X}.append("Subject")""")
          | Thread_Index                        + λ(f"""{X}.append("Thread_Index")""")
          | Thread_Topic                        + λ(f"""{X}.append("Thread_Topic")""")
          | To                                  + λ(f"""{X}.append("To")""")
          | X_Account_Key                       + λ(f"""{X}.append("X_Account_Key")""")
          | X_Apparently_To                     + λ(f"""{X}.append("X_Apparently_To")""")
          | X_MAIL_FROM                         + λ(f"""{X}.append("X_MAIL_FROM")""")
          | X_Mailer                            + λ(f"""{X}.append("X_Mailer")""")
          | X_MimeOLE                           + λ(f"""{X}.append("X_MimeOLE")""")
          | X_Mozilla_Keys                      + λ(f"""{X}.append("X_Mozilla_Keys")""")
          | X_Mozilla_Status                    + λ(f"""{X}.append("X_Mozilla_Status")""")
          | X_Mozilla_Status2                   + λ(f"""{X}.append("X_Mozilla_Status2")""")
          | X_MS_Has_Attach                     + λ(f"""{X}.append("X_MS_Has_Attach")""")
          | X_MS_TNEF_Correlator                + λ(f"""{X}.append("X_MS_TNEF_Correlator")""")
          | X_MSMail_Priority                   + λ(f"""{X}.append("X_MSMail_Priority")""")
          | X_OriginalArrivalTime               + λ(f"""{X}.append("X_OriginalArrivalTime")""")
          | X_Originating_IP                    + λ(f"""{X}.append("X_Originating_IP")""")
          | X_Priority                          + λ(f"""{X}.append("X_Priority")""")
          | X_SF_Loop                           + λ(f"""{X}.append("X_SF_Loop")""")
          | X_SOURCE_IP                         + λ(f"""{X}.append("X_SOURCE_IP")""")
          | X_Spam                              + λ(f"""{X}.append("X_Spam")""")
          | X_UIDL                              + λ(f"""{X}.append("X_UIDL")""")
          | X_Virus_Scanned                     + λ(f"""{X}.append("X_Virus_Scanned")""")
          | X_Yahoo_Newman_Property             + λ(f"""{X}.append("X_Yahoo_Newman_Property")""")
          )                                     + λ(f"""remember(tag, txt, lit)""") # REMEMBER every piece
        | φ(r'^(?P<tag>[^: \t\r\f\n]+):')       + λ(f'''{X}.append("σ('" + tag + "')")''')
        + φ(r'(?P<lit>.*)')                     + λ(f"""remember(tag, txt, lit)""") # REMEMBER novel tag
        | φ(r'[ ]+') % "tx"                     + λ(f'''{X}.append("σ('" + tx + "')")''')
        | φ(r'[0-9]{2,}')                       + λ(f"""{X}.append("φ(r'[0-9]+')")""")
        | φ(r'[0-9]')                           + λ(f"""{X}.append("φ(r'[0-9]')")""")
        | φ(r'[A-Z]{2,}')                       + λ(f"""{X}.append("φ(r'[A-Z]+')")""")
        | φ(r'[A-Z]')                           + λ(f"""{X}.append("φ(r'[A-Z]')")""")
        | φ(r'[a-z]{2,}')                       + λ(f"""{X}.append("φ(r'[a-z]+')")""")
        | φ(r'[a-z]')                           + λ(f"""{X}.append("φ(r'[a-z]')")""")
        | LEN(1) % "tx"                         + λ(f'''{X}.append("σ('" + ("\\\\" if tx == "\\\\" else "") + tx + "')")''')
        ) # @ "OUTPUT"
      )
    + RPOS(0)
    )
#=======================================================================================================================
def lineno(offset):
    while offset < total_size and offset not in linenos:
        offset += 1
    return linenos[offset]
#-----------------------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------------------
sections = []
def scan_sections():
    global sections
    print("# Scanning sections.", end="", flush=True)
    for match in re.finditer(fr"^{rex_From}$", inbox, re.MULTILINE):
        sections.append(match.span()[0])
    sections.append(total_size)
    print(f" {len(sections)} sections.", flush=True)
#-----------------------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------------------
def reminisce():
    if False: pprint(seen, width=170, indent=2)
    for tag, patterns in sorted(seen.items()):
        if len(patterns) > 0:
            print(f"#{'-' * 119}")
            print(f"@pattern")
            print(f"def {tag.replace('-', '_')}(): yield from (")
            bar = ' '
            for ptrn, texts in patterns.items():
                print(f"{bar}   φ(r'" + ptrn.replace("'", "\\'") + "')") #
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
#-----------------------------------------------------------------------------------------------------------------------
inbox = None
total_size = None
ITERATIONS = 32
def main():
    global inbox, total_size
    inbox_nm = "/mnt/c/Users/lcher/AppData/Local/Packages/" \
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
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    GLOBALS(globals())
    main()
#-----------------------------------------------------------------------------------------------------------------------
