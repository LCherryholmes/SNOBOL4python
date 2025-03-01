# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, MATCH, GLOBALS
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ
from SNOBOL4python import ANY, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
#-------------------------------------------------------------------------------
import os
import sys
sys.path.append(os.getcwd())
#from transl8r_y import *
#from transl8r_yaml import *
#-------------------------------------------------------------------------------
@pattern
def μ():                yield from FENCE(SPAN(" \t\r\f") | ε())
@pattern
def ς(s):               yield from μ() + σ(s)
@pattern
def DOW():              yield from \
                        ( ς('Mon') | ς('Tue') | ς('Wed') | ς('Thu')
                        | ς('Fri') | ς('Sat') | ς('Sun')
                        )
@pattern
def Month():            yield from \
                        ( ς('Jan') | ς('Feb') | ς('Mar') | ς('Apr')
                        | ς('May') | ς('Jun') | ς('Jul') | ς('Aug')
                        | ς('Sep') | ς('Oct') | ς('Nov') | ς('Dec')
                        )
@pattern
def DOM():              yield from SPAN(_DIGITS)
@pattern
def Time():             yield from \
                        ( ANY(_DIGITS) + ANY(_DIGITS) + σ(':') 
                        + ANY(_DIGITS) + ANY(_DIGITS) + σ(':')
                        + ANY(_DIGITS) + ANY(_DIGITS) 
                        )
@pattern
def Year():             yield from \
                        ANY(_DIGITS) + ANY(_DIGITS) + ANY(_DIGITS) + ANY(_DIGITS)
@pattern
def From():             yield from \
                        ( ς('From - ') + DOW() 
                        + ς(' ') + Month()
                        + ς(' ') + DOM()
                        + ς(' ') + Time()
                        + ς(' ') + Year()
                        )
#-------------------------------------------------------------------------------
@pattern
def thing():                yield from μ() + SPAN(_DIGITS+_UCASE+_LCASE) % "tx"
@pattern
def ip_address():           yield from (          SPAN(_DIGITS) @ "tx" + λ(lambda: int(tx) >= 0 and int(tx) <= 255)
                                       + σ('.') + SPAN(_DIGITS) @ "tx" + λ(lambda: int(tx) >= 0 and int(tx) <= 255)
                                       + σ('.') + SPAN(_DIGITS) @ "tx" + λ(lambda: int(tx) >= 0 and int(tx) <= 255)
                                       + σ('.') + SPAN(_DIGITS) @ "tx" + λ(lambda: int(tx) >= 0 and int(tx) <= 255)
                                       )
@pattern
def email_address():        yield from \
                            ( ANY(_UCASE+_LCASE)
                            + SPAN(_DIGITS+_UCASE+_LCASE)
                            + σ('@') + 'yahoo.com'
                            )
#-------------------------------------------------------------------------------
@pattern
def X_account_key():            yield from ς('X-Account-Key: ') + BREAK('\n')
@pattern
def X_UIDL():                   yield from ς('X-UIDL: ') + LEN(27) + σ('\n')
@pattern
def X_Mozilla_Status():         yield from ς('X-Mozilla-Status: ') \
                                         + SPAN(_DIGITS) @ "tx" + λ(lambda: len(tx) == 4)
@pattern
def X_Mozilla_Status2():        yield from ς('X-Mozilla-Status2: ') \
                                         + SPAN(_DIGITS) @ "tx" + λ(lambda: len(tx) == 8)
@pattern
def X_Mozilla_Keys():           yield from ς('X-Mozilla-Keys:') + SPAN(' ') + σ('\n')
@pattern
def X_Apparently_To():          yield from \
                                ( ς('X-Apparently-To:')
                                + ς(' ') + email_address()
                                + ς(' ') + ς('via') + ς(' ') + ip_address() + ς(';')
                                + ς(' ') + ς('Mon,') + ς(' ') + ς('04') + ς(' ') + ς('Dec') + ς(' ') + ς('2006')
                                + ς(' ') + ς('05:51:56') + ς(' ') + ς('-0800')
                                )
@pattern
def X_Originating_IP():         yield from ς('X-Originating-IP: ') + σ('[') + ip_address() + σ(']')
@pattern
def Return_Path():              yield from ς('Return-Path: ') + BREAK(" \t\r\f\n")
@pattern
def Authentication_Results():   yield from \
                                ( ς('Authentication-Results:')
                                + ς(' ')  + BREAK(" \t\r\f\n")
                                + ς('  ') + BREAK(";") + σ(';')
                                + ς(' ')  + BREAK(" \t\r\f\n")
                                + ς(' ')  + BREAK(" \t\r\f\n")
                                )
@pattern
def Received_from():            yield from \
                                ( ς('Received:')
                                + ς(' ')  + ς('from')
                                + ς(' ')  + ip_address()
                                + ς('  ') + ς('(EHLO')
                                + ς(' ')  + BREAK(" \t\r\f\n")
                                + ς(' ')  + σ('(') + ip_address() + σ(')')
                                )

@pattern
def Received():                     yield from ς('Received:') + BREAK('\n')
@pattern
def X_MimeOLE():                    yield from ς('X-MimeOLE:') + BREAK('\n')
@pattern
def Content_class():                yield from ς('Content-class:') + BREAK('\n')
@pattern
def MIME_Version():                 yield from ς('MIME-Version:') + BREAK('\n')
@pattern
def Content_Type():                 yield from ς('Content-Type:') + BREAK('\n')
@pattern
def Subject():                      yield from ς('Subject:') + BREAK('\n')
@pattern
def Date():                         yield from ς('Date:') + BREAK('\n')
@pattern
def Message_ID():                   yield from ς('Message-ID:') + BREAK('\n')
@pattern
def X_MS_Has_Attach():              yield from ς('X-MS-Has-Attach:') + BREAK('\n')
@pattern
def X_MS_TNEF_Correlator():         yield from ς('X-MS-TNEF-Correlator:') + BREAK('\n')
@pattern
def Thread_Topic():                 yield from ς('Thread-Topic:') + BREAK('\n')
@pattern
def Thread_Index():                 yield from ς('Thread-Index:') + BREAK('\n')
@pattern
def From():                         yield from ς('From:') + BREAK('\n')
@pattern
def To():                           yield from ς('To:') + BREAK('\n')
@pattern
def X_OriginalArrivalTime():        yield from ς('X-OriginalArrivalTime:') + BREAK('\n')
@pattern
def Content_Length():               yield from ς('Content-Length:') + BREAK('\n')
@pattern
def Content_Type():                 yield from ς('Content-Type:') + BREAK('\n')
@pattern
def Content_Transfer_Encoding():    yield from ς('Content-Transfer-Encoding:') + BREAK('\n')
@pattern
def Content_Transfer_Encoding():    yield from ς('Content-Transfer-Encoding:') + BREAK('\n')
#-------------------------------------------------------------------------------
@pattern
def Inbox():
    yield from  \
    ( POS(0) + Λ("""P = "yield from (\\n\"""")
    + ARBNO(
        θ("OUTPUT") +
        ( σ('\\\n')                     + Λ("""P += "σ('\\\n') + \"""")
        | σ('\n')                       + Λ("""P += "η() +\\n\"""") 
        | SPAN(" ") % "tx"              + Λ("""P += "ς('" + tx + "') + \"""")
        | SPAN("\t\r\f")                + Λ("""P += "μ() + \"""")
        | From()                        + Λ("""P += "From() + \"""")
        | X_account_key()               + Λ("""P += "X_account_key() + \"""")
        | X_UIDL()                      + Λ("""P += "X_UIDL() + \"""")
        | X_Mozilla_Status()            + Λ("""P += "X_Mozilla_Status() + \"""")
        | X_Mozilla_Status2()           + Λ("""P += "X_Mozilla_Status2() + \"""")
        | X_Mozilla_Keys()              + Λ("""P += "X_Mozilla_Keys() + \"""")
        | X_Originating_IP()            + Λ("""P += "X_Originating_IP() + \"""")
        | Return_Path()                 + Λ("""P += "Return_Path() + \"""")
        | Authentication_Results()      + Λ("""P += "Authentication_Results() + \"""")
        | Received()                    + Λ("""P += "Received() + \"""")                 
        | X_MimeOLE()                   + Λ("""P += "X_MimeOLE() + \"""")                
        | Content_class()               + Λ("""P += "Content_class() + \"""")            
        | MIME_Version()                + Λ("""P += "MIME_Version() + \"""")             
        | Content_Type()                + Λ("""P += "Content_Type() + \"""")             
        | Subject()                     + Λ("""P += "Subject() + \"""")                  
        | Date()                        + Λ("""P += "Date() + \"""")                     
        | Message_ID()                  + Λ("""P += "Message_ID() + \"""")               
        | X_MS_Has_Attach()             + Λ("""P += "X_MS_Has_Attach() + \"""")          
        | X_MS_TNEF_Correlator()        + Λ("""P += "X_MS_TNEF_Correlator() + \"""")     
        | Thread_Topic()                + Λ("""P += "Thread_Topic() + \"""")             
        | Thread_Index()                + Λ("""P += "Thread_Index() + \"""")             
        | From()                        + Λ("""P += "From() + \"""")                     
        | To()                          + Λ("""P += "To() + \"""")                       
        | X_OriginalArrivalTime()       + Λ("""P += "X_OriginalArrivalTime() + \"""")    
        | Content_Length()              + Λ("""P += "Content_Length() + \"""")           
        | Content_Type()                + Λ("""P += "Content_Type() + \"""")             
        | Content_Transfer_Encoding()   + Λ("""P += "Content_Transfer_Encoding() + \"""")
        | Content_Transfer_Encoding()   + Λ("""P += "Content_Transfer_Encoding() + \"""")
        | ( NOTANY(" \t\r\f\n")
          + BREAK(" \t\r\f\n")
          ) % "tx"                      + Λ("""P += "ς('" + tx + "') + \"""")
        | SPAN(_DIGITS)                 + Λ("""P += "SPAN(_DIGITS) + \"""")
        | SPAN(_UCASE)                  + Λ("""P += "SPAN(_UCASE) + \"""")
        | SPAN(_LCASE)                  + Λ("""P += "SPAN(_LCASE) + \"""")
        | NOTANY(_DIGITS+_UCASE+_LCASE) % "tx"
                                        + Λ("""P += "ς('" + ("\\\\" if tx == "\\\\" else "") + tx + "') + \"""")
        ) # @ "OUTPUT"
      )
    + RPOS(0) + Λ("""P += "'')\\n\"""")
    )
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    yamlInput_nm = r"""C:/Users/lcher/.conda/pkgs/python-3.12.3-h2628c8c_0_cpython/info/recipe/meta.yaml"""
    inbox_nm = "C:/Users/lcher/AppData/Local/Packages/MozillaThunderbird.MZLA_h5892qc0xkpca" \
               "/LocalCache/Roaming/Thunderbird/Profiles/nsn6odxd.default-esr" \
               "/Mail/pop.mail.yahoo.com/Inbox"
    pyOutput_nm = "./inbox-pop3.py"
    GLOBALS(globals())
    inbox = ""
    lineno = 0
    with open(inbox_nm, "r") as Input:
        while line := Input.readline():
            if lineno < 100:
                inbox += line
                lineno += 1
            else: break
    if MATCH(inbox, Inbox()):
        with open(pyOutput_nm, "w", encoding="utf-8") as pyOutput:
            pyOutput.write(P)
    else: print("Yikes!!!")
#-------------------------------------------------------------------------------
