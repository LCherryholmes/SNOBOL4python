# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, _UCASE, _LCASE, _digits, MATCH
from SNOBOL4python import ε, σ, λ, Λ, ANY, ARBNO, BREAK, EQ, FENCE, LEN, POS, RPOS, SPAN
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce
#------------------------------------------------------------------------------
# Parse JSON string
#------------------------------------------------------------------------------
def jRecognizer():  yield POS(0) + FENCE() + jParser() + ς('') + RPOS(0)
def jParser():      yield jObject() + Reduce('JSON', 1)
def jObject():      yield (   ς('{') + nPush()
                          +   π(jField() + nInc() + ARBNO(ς(',') + jField() + nInc()))
                          +   ς('}') + Reduce('{}') + nPop()
                          +   FENCE()
                          )
def jArray():       yield (   ς('[') + nPush()
                          +   π(jElement() + nInc() + ARBNO(ς(',') + jElement() + nInc()))
                          +   ς(']') + Reduce('[]') + nPop()
                          +   FENCE()
                          )
def jField():       yield jVar() + Shift('Name', "jxVar") + ς(':') + jElement() + Reduce(':', 2)
def jElement():     yield ς('') \
                        + ( jRealVal() + Shift('Real', "jxVal")
                          | jIntVal()  + Shift('Integer', "jxVal")
                          | jBoolVal() + Shift('Bool', "jxVal")
                          | jDateVal() + Shift('Datetime', "jxVal")
                          | jStrVal()  + Shift('String', "jxVal")
                          | jNullVal() + Shift('Null')
                          | jArray()
                          | jObject()
                          )
def jVar():         yield σ('"') + (jIdent() + FENCE(' ' + jIdent() | ε()) | jInt()) ^ "jxVar" + σ('"')
#------------------------------------------------------------------------------
def ς(s):           yield (SPAN(" \t\r\n") | ε()) + σ(s)
def π(p):           yield from p; yield ""
def jInt():         yield (FENCE(σ('+') | σ('-') | ε()) + SPAN('0123456789')) ^ "jxN"
def jEscChar():     yield '\\' \
                        + (  ANY('ntbrf' + '"' + '\\' + '/' + "'")
                          |  ANY('01234567') + FENCE(ANY('01234567') | ε())
                          |  ANY('0123') + ANY('01234567') + ANY('01234567')
                          |  σ('u') + (LEN(4) & SPAN('0123456789ABCDEFabcdef'))
                          )
def jNullVal():     yield σ('null') + ε() ^ "jxVal"
def jTrueFalse():   yield (σ('true') | σ('false')) ^ "jxVal"
def jIdent():       yield ANY(_UCASE + '_' + _LCASE) + FENCE(SPAN(_UCASE + '_' + _LCASE + '0123456789') | ε())
def jString():      yield σ('"') + (ARBNO(BREAK('"'+'\\'+'\n') | jEscChar())) ^ "jxVal" + σ('"')
def jStrVal():      yield jString() + Λ("jxVal = JSONDecode(jxVal)")
def jBoolVal():     yield jTrueFalse() | σ('"') + jTrueFalse() + σ('"')
def jRealVal():     yield ((σ('+') | σ('-') | ε()) + SPAN('0123456789') + σ('.') + SPAN('0123456789')) ^ "jxVal"
def jIntVal():      yield (jInt() ^ "jxVal" | '"' + jInt() ^ "jxVal" + '"')
#------------------------------------------------------------------------------
def jMonthName():   yield (   σ('Jan') | σ('Feb') | σ('Mar') | σ('Apr')
                          |   σ('May') | σ('Jun') | σ('Jul') | σ('Aug')
                          |   σ('Sep') | σ('Oct') | σ('Nov') | σ('Dec')
                          ) ^ "jxMonthName" + Λ("jxMonth = jMos[jxMonthName]")
def jDayName():     yield σ('Sun') | σ('Mon') | σ('Tue') | σ('Wed') | σ('Thu') | σ('Fri') | σ('Sat')
def jNum2():        yield SPAN('0123456789') @ "jxN" ^ "jxN" + λ("len(jxN) == 2")
def jNum3():        yield SPAN('0123456789') @ "jxN" ^ "jxN" + λ("len(jxN) == 3")
def jNum4():        yield SPAN('0123456789') @ "jxN" ^ "jxN" + λ("len(jxN) == 4")
def jYYYY():        yield jNum4 ^ "jxYYYY"
def jMM():          yield jNum2 ^ "jxMM"
def jDD():          yield jNum2 ^ "jxDD"
def jhh():          yield jNum2 ^ "jxhh"
def jmm():          yield jNum2 ^ "jxmm"
def jss():          yield jNum2 ^ "jxss"
def jDatetime():    yield \
    ( σ('"') + Λ("jxHour = '00'")
             + Λ("jxMinute = '00'")
             + Λ("jxSecond = '00'")
  + (   jDayName() + σ(', ') + jDD() + σ(' ') + jMonthName() + σ(' ') + jYYYY() + σ(' ') + jhh() + σ(':') + jmm() + σ(':') + jss() + σ(' +') + jNum4()
    |   jDayName() + σ(' ') + jMonthName() + σ(' ') + jDD() + σ(' ') + jhh() + σ(':') + jmm() + σ(':') + jss() + σ(' +') + jNum4() + σ(' ') + jYYYY()
    |   jYYYY()    + σ('-') + jMM() + σ('-') + jDD()
    |   jYYYY()    + σ('-') + jMM() + σ('-') + jDD() + σ('T') + jhh() + σ(':') + jmm() + σ(':') + jss()
    |   jYYYY()    + σ('-') + jMM() + σ('-') + jDD() + σ('T') + jhh() + σ(':') + jmm() + σ(':') + jss() + σ('.') + (jNum3() | ε()) + σ('Z')
    |   jYYYY()    + σ('-') + jMM() + σ('-') + jDD() + σ('T') + jhh() + σ(':') + jmm() + σ(':') + jss() + σ('+') + jNum4()
    |   jYYYY()    + σ('-') + jMM() + σ('-') + jDD() + σ('T') + jhh() + σ(':') + jmm() + σ(':') + jss() + σ('+') + jNum2() + σ(':') + jNum2()
    |   jYYYY()    + σ('-') + jMM() + σ('-') + jDD() + σ(' ') + jhh() + σ(':') + jmm() + σ(':') + jss() + σ(' +') + jNum4()
    )
  + σ('"')
  + Λ("jxDatetime = jxYYYY + '-' + jxMM + '-' + jxDD + ' ' + jxhh + ':' + jxmm + ':' + jxss")
  )
def jDateVal():     yield jDatetime() + Λ("jxVal = jxDatetime")
#------------------------------------------------------------------------------
