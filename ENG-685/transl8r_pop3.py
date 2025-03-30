# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, MATCH, GLOBALS
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ, φ
from SNOBOL4python import ANY, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
from pprint import pprint
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
@pattern
def From():                     yield from φ(r"From - ")
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
def From():                     yield from φ(r"From:.*\n")
@pattern
def To():                       yield from φ(r"To:.*\n")
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
@pattern
#-------------------------------------------------------------------------------
def NextPart_BEGIN():           yield from φ(r"------_=_NextPart_[0-9]{3}_[0-9A-F]{8}\.[0-9A-F]{8}") # \n
@pattern
def NextPart_END():             yield from φ(r"------_=_NextPart_[0-9]{3}_[0-9A-F]{8}\.[0-9A-F]{8}") # \n
@pattern
def Line():                     yield from φ(r".*\n")
@pattern
def UptoPart():                 yield from φ(r"(.*\n)+(?=------_=_NextPart_[0-9]{3}_[0-9A-F]{8}\.[0-9A-F]{8})")
@pattern
def NextPart():                 yield from φ( r"------_=_NextPart_"
                                              r"([0-9]{3}_[0-9A-F]{8}\.[0-9A-F]{8})\n"
                                              r"(?:.*\n)*"
                                              r"------_=_NextPart_"
                                              r"\1\n"
                                            )
#-------------------------------------------------------------------------------
lineno = 1
def inc_lineno():   global lineno; lineno += 1; return True
def trace(s):       print(s); return True
#-------------------------------------------------------------------------------
@pattern
def Inbox():
    global lineno
    yield from  \
    ( POS(0)
    + ARBNO(
        θ("p0") + # θ("OUTPUT") +
        ( base64()            + θ("p1") + λ(lambda: trace(f"@{p0}-{p1} BASE64"))
#       | UptoPart() @ "upto" + θ("p1") + λ(lambda: trace(f"@{p0}-{p1} {upto[0:21]}"))
        | NextPart() @ "part" + θ("p1") + λ(lambda: trace(f"@{p0}-{p1} {part[18:39]}"))
        | Line() # @ "line" + θ("p1")   # + λ(lambda: trace(f"#{lineno} @{p0}-{p1} {line[0:21]}"))
#       | σ('\n')                       + λ(lambda: inc_lineno()) # + λ(lambda: trace("η() +\\n"))
#       | NextPart_BEGIN() @ "part"     + λ(lambda: trace(f"#{lineno} {part} @ {p0}"))
#       | NextPart_END() @ "part"       + λ(lambda: trace(f"#{lineno} {part} @ {p0}"))
#       | φ(r"[ ]+") @ "tx"           # + λ(lambda: trace("ς('" + tx + "')"))
#       | φ(r"[ \t\r\f]+")            # + λ(lambda: trace("μ()"))
#       | Date_Time()                 # + λ(lambda: trace("Date_Time()"))
#       | From()                      # + λ(lambda: trace("From()"))
#       | X_account_key()             # + λ(lambda: trace("X_account_key()"))
#       | X_UIDL()                    # + λ(lambda: trace("X_UIDL()"))
#       | X_Mozilla_Status()          # + λ(lambda: trace("X_Mozilla_Status()"))
#       | X_Mozilla_Status2()         # + λ(lambda: trace("X_Mozilla_Status2()"))
#       | X_Mozilla_Keys()            # + λ(lambda: trace("X_Mozilla_Keys()"))
#       | X_Originating_IP()          # + λ(lambda: trace("X_Originating_IP()"))
#       | Return_Path()               # + λ(lambda: trace("Return_Path()"))
#       | Authentication_Results()    # + λ(lambda: trace("Authentication_Results()"))
#       | Received()                  # + λ(lambda: trace("Received()"))
#       | X_MimeOLE()                 # + λ(lambda: trace("X_MimeOLE()"))
#       | Content_class()             # + λ(lambda: trace("Content_class()"))
#       | MIME_Version()              # + λ(lambda: trace("MIME_Version()"))
#       | Content_Type()              # + λ(lambda: trace("Content_Type()"))
#       | Subject()                   # + λ(lambda: trace("Subject()"))
#       | Date()                      # + λ(lambda: trace("Date()"))
#       | Message_ID()                # + λ(lambda: trace("Message_ID()"))
#       | X_MS_Has_Attach()           # + λ(lambda: trace("X_MS_Has_Attach()"))
#       | X_MS_TNEF_Correlator()      # + λ(lambda: trace("X_MS_TNEF_Correlator()"))
#       | Thread_Topic()              # + λ(lambda: trace("Thread_Topic()"))
#       | Thread_Index()              # + λ(lambda: trace("Thread_Index()"))
#       | From()                      # + λ(lambda: trace("From()"))
#       | To()                        # + λ(lambda: trace("To()"))
#       | X_OriginalArrivalTime()     # + λ(lambda: trace("X_OriginalArrivalTime()"))
#       | Content_Length()            # + λ(lambda: trace("Content_Length()"))
#       | Content_Type()              # + λ(lambda: trace("Content_Type()"))
#       | Content_Transfer_Encoding() # + λ(lambda: trace("Content_Transfer_Encoding()"))
        | φ(r"[^ \t\r\f\n]+") @ "tx"  # + λ(lambda: trace("ς('" + tx + "')"))
        | φ(r"[0-9]")                 # + λ(lambda: trace("SPAN(_DIGITS)"))
        | φ(r"[A-Z]")                 # + λ(lambda: trace("SPAN(_UCASE)"))
        | φ(r"[a-z]")                 # + λ(lambda: trace("SPAN(_LCASE)"))
        | φ(r"[^0-9A-Za-z]+") @ "tx"  # + λ(lambda: trace("ς('" + ("\\\\" if tx == "\\\\" else "") + tx + "')"))
        ) # @ "OUTPUT"
      )
    + RPOS(0)
    )
#-------------------------------------------------------------------------------
def main():
    inbox_nm = "C:/Users/lcher/AppData/Local/Packages/MozillaThunderbird.MZLA_h5892qc0xkpca" \
               "/LocalCache/Roaming/Thunderbird/Profiles/nsn6odxd.default-esr" \
               "/Mail/pop.mail.yahoo.com/Inbox"
    with open(inbox_nm, "r", encoding="latin-1") as inbox_file:
        print("Reading.")
        inbox = inbox_file.read()
        print("Matching.")
        if inbox in Inbox():
            print(" + ".join(P))
        else: print("Yikes!!!")
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    GLOBALS(globals())
    main()
#-------------------------------------------------------------------------------
