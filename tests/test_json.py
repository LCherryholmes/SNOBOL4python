# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
# Parse JSON string
#-----------------------------------------------------------------------------------------------------------------------
import SNOBOL4python
from SNOBOL4python import pattern, _UCASE, _LCASE, _digits, MATCH
from SNOBOL4python import ε, σ, π, λ, Λ, ANY, ARBNO, BREAK, FENCE, LEN, POS, RPOS, SPAN
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce
#-----------------------------------------------------------------------------------------------------------------------
def ς(s):           yield (SPAN(" \t\r\n") | ε()) + σ(s)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def jRecognizer():  yield POS(0) + FENCE() + jParser() + ς('') + RPOS(0)
@pattern
def jParser():      yield jObject() + Reduce('JSON', 1)
@pattern
def jObject():      yield (   ς('{') + nPush()
                          +   π(jField() + nInc() + ARBNO(ς(',') + jField() + nInc()))
                          +   ς('}') + Reduce('{}') + nPop()
                          +   FENCE()
                          )
@pattern
def jArray():       yield (   ς('[') + nPush()
                          +   π(jElement() + nInc() + ARBNO(ς(',') + jElement() + nInc()))
                          +   ς(']') + Reduce('[]') + nPop()
                          +   FENCE()
                          )
@pattern
def jField():       yield jVar() + Shift('Name', "jxVar") + ς(':') + jElement() + Reduce(':', 2)
@pattern
def jElement():     yield ς('') \
                        + ( jRealVal() + Shift('Real', "jxVal")
                          | jIntVal()  + Shift('Integer', "jxVal")
                          | jBoolVal() + Shift('Bool', "jxVal")
#                         | jDateVal() + Shift('Datetime', "jxVal")
                          | jStrVal()  + Shift('String', "jxVal")
                          | jNullVal() + Shift('Null')
                          | jArray()
                          | jObject()
                          )
@pattern
def jVar():         yield σ('"') + (jIdent() + FENCE(' ' + jIdent() | ε()) | jInt()) ^ "jxVar" + σ('"')
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def jInt():         yield (FENCE(σ('+') | σ('-') | ε()) + SPAN('0123456789')) ^ "jxN"
@pattern
def jEscChar():     yield '\\' \
                        + (  ANY('ntbrf' + '"' + '\\' + '/' + "'")
                          |  ANY('01234567') + FENCE(ANY('01234567') | ε())
                          |  ANY('0123') + ANY('01234567') + ANY('01234567')
                          |  σ('u') + (LEN(4) & SPAN('0123456789ABCDEFabcdef'))
                          )
@pattern
def jNullVal():     yield σ('null') + ε() ^ "jxVal"
@pattern
def jTrueFalse():   yield (σ('true') | σ('false')) ^ "jxVal"
@pattern
def jIdent():       yield ANY(_UCASE + '_' + _LCASE) + FENCE(SPAN(_UCASE + '_' + _LCASE + '0123456789') | ε())
@pattern
def jString():      yield σ('"') + (ARBNO(BREAK('"'+'\\'+'\n') | jEscChar())) ^ "jxVal" + σ('"')
@pattern
def jStrVal():      yield jString() + Λ("jxVal = JSONDecode(jxVal)")
@pattern
def jBoolVal():     yield jTrueFalse() | σ('"') + jTrueFalse() + σ('"')
@pattern
def jRealVal():     yield ((σ('+') | σ('-') | ε()) + SPAN('0123456789') + σ('.') + SPAN('0123456789')) ^ "jxVal"
@pattern
def jIntVal():      yield (jInt() ^ "jxVal" | '"' + jInt() ^ "jxVal" + '"')
@pattern
def jDateVal():     yield jDatetime() + Λ("jxVal = jxDatetime")
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def jMonthName():   yield (   σ('Jan') | σ('Feb') | σ('Mar') | σ('Apr')
                          |   σ('May') | σ('Jun') | σ('Jul') | σ('Aug')
                          |   σ('Sep') | σ('Oct') | σ('Nov') | σ('Dec')
                          ) ^ "jxMonthName" + Λ("jxMonth = jMos[jxMonthName]")
@pattern
def jDayName():     yield σ('Sun') | σ('Mon') | σ('Tue') | σ('Wed') | σ('Thu') | σ('Fri') | σ('Sat')
@pattern
def jNum2():        yield SPAN('0123456789') @ "jxN" ^ "jxN" + λ("len(jxN) == 2") # + EQ("len(jxN)", "2")
@pattern
def jNum3():        yield SPAN('0123456789') @ "jxN" ^ "jxN" + λ("len(jxN) == 3")
@pattern
def jNum4():        yield SPAN('0123456789') @ "jxN" ^ "jxN" + λ("len(jxN) == 4")
@pattern
def jYYYY():        yield jNum4() ^ "jxYYYY"
@pattern
def jMM():          yield jNum2() ^ "jxMM"
@pattern
def jDD():          yield jNum2() ^ "jxDD"
@pattern
def jhh():          yield jNum2() ^ "jxhh"
@pattern
def jmm():          yield jNum2() ^ "jxmm"
@pattern
def jss():          yield jNum2() ^ "jxss"
@pattern
def jDate():        yield jYYYY() + σ('-') + jMM() + σ('-') + jDD()
@pattern
def Time():         yield jhh() + σ(':') + jmm() + σ(':') + jss()
@pattern
def jDatetime():    yield \
    ( σ('"')
    + Λ("jxHour = '00'")
    + Λ("jxMinute = '00'")
    + Λ("jxSecond = '00'")
    + ( jDayName() + σ(', ') + jDD() + σ(' ') + jMonthName() + σ(' ') + jYYYY() + σ(' ') + Time() + σ(' +') + jNum4()
      | jDayName() + σ(' ') + jMonthName() + σ(' ') + jDD() + σ(' ') + Time() + σ(' +') + jNum4() + σ(' ') + jYYYY()
      | jDate()
      | jDate() + σ('T') + Time()
      | jDate() + σ('T') + Time() + σ('.') + (jNum3() | ε()) + σ('Z')
      | jDate() + σ('T') + Time() + σ('+') + jNum4()
      | jDate() + σ('T') + Time() + σ('+') + jNum2() + σ(':') + jNum2()
      | jDate() + σ(' ') + Time() + σ(' +') + jNum4()
      )
    + σ('"')
    + Λ("jxDatetime = jxYYYY + '-' + jxMM + '-' + jxDD + ' ' + jxhh + ':' + jxmm + ':' + jxss")
    )
#-----------------------------------------------------------------------------------------------------------------------
JSON_sample = \
"""{  "list":
      [ {
        "id": 1,
        "first_name": "Jeanette",
        "last_name": "Penddreth",
        "email": "jpenddreth0@census.gov",
        "gender": "Female",
        "ip_address": "26.58.193.2"
        }
      , {
        "id": 2,
        "first_name": "Giavani",
        "last_name": "Frediani",
        "email": "gfrediani1@senate.gov",
        "gender": "Male",
        "ip_address": "229.179.4.212"
        }
      ]
}"""
MATCH(JSON_sample, jRecognizer())