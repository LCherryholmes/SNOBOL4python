# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
# Parse JSON string
#-----------------------------------------------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, pattern, ε, σ, π, λ, Λ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCESS, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from SNOBOL4python import JSONDecode
from datetime import datetime
import operator
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def ς(s):           yield from (SPAN(" \t\r\n") | ε()) + σ(s)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def jRecognizer():  yield from POS(0) + FENCE() + jJSON() + ς('') + Pop('JSON_tree') + RPOS(0)
@pattern
def jJSON():        yield from jObject() + Reduce('JSON', 1)
@pattern
def jObject():      yield from (   ς('{') + nPush()
                               +   π(jField() + nInc() + ARBNO(ς(',') + jField() + nInc()))
                               +   ς('}') + Reduce('Object') + nPop()
                               +   FENCE()
                               )
@pattern
def jArray():       yield from (   ς('[') + nPush()
                               +   π(jElement() + nInc() + ARBNO(ς(',') + jElement() + nInc()))
                               +   ς(']') + Reduce('Array') + nPop()
                               +   FENCE()
                               )
@pattern
def jField():       yield from jVar() + Shift('Name', "jxVar") + ς(':') + jElement() + Reduce('Attribute', 2)
@pattern
def jVar():         yield from ς('"') + ((jIdent() | jInt()) % "jxVar") + σ('"')
@pattern
def jElement():     yield from ς('') \
                             + ( jRealVal() + Shift('Real', "float(jxVal)")
                               | jIntVal()  + Shift('Integer', "int(jxVal)")
                               | jBoolVal() + Shift('Bool', "dict(true=True, false=False)[jxVal]")
                               | jDateVal() + Shift('Datetime', "datetime(*jxVal)")
                               | jStrVal()  + Shift('String', "jxVal")
                               | jNullVal() + Shift('None')
                               | jArray()
                               | jObject()
                               )
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def jInt():         yield from (FENCE(σ('+') | σ('-') | ε()) + SPAN('0123456789')) % "jxN"
@pattern
def jEscChar():     yield from σ('\\') \
                             + (  ANY('ntbrf' + '"' + '\\' + '/' + "'")
                               |  ANY('01234567') + FENCE(ANY('01234567') | ε())
                               |  ANY('0123') + ANY('01234567') + ANY('01234567')
                               |  σ('u') + (LEN(4) & SPAN('0123456789ABCDEFabcdef'))
                               )
@pattern
def jNullVal():     yield from σ('null') + ε() % "jxVal"
@pattern
def jTrueFalse():   yield from (σ('true') | σ('false')) % "jxVal"
@pattern
def jIdent():       yield from ANY(UCASE + '_' + LCASE) + FENCE(SPAN(UCASE + '_' + LCASE + '0123456789') | ε())
@pattern
def jString():      yield from σ('"') + ((ARBNO(BREAK('"'+'\\'+'\n') | jEscChar())) % "jxVal") + σ('"')
@pattern
def jStrVal():      yield from jString() + λ("jxVal = JSONDecode(jxVal)")
@pattern
def jBoolVal():     yield from jTrueFalse() | σ('"') + jTrueFalse() + σ('"')
@pattern
def jRealVal():     yield from ((σ('+') | σ('-') | ε()) + SPAN('0123456789') + σ('.') + SPAN('0123456789')) % "jxVal"
@pattern
def jIntVal():      yield from (jInt() % "jxVal") | σ('"') + (jInt() % "jxVal") + σ('"')
@pattern
def jDateVal():     yield from jDatetime() + λ("jxVal = jxDatetime")
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def jMonthName():   yield from \
                    (   σ('Jan') | σ('Feb') | σ('Mar') | σ('Apr')
                    |   σ('May') | σ('Jun') | σ('Jul') | σ('Aug')
                    |   σ('Sep') | σ('Oct') | σ('Nov') | σ('Dec')
                    ) % "jxMonthName" + λ("jxMonth = jMos[jxMonthName]")
@pattern
def jDayName():     yield from σ('Sun') | σ('Mon') | σ('Tue') | σ('Wed') | σ('Thu') | σ('Fri') | σ('Sat')
@pattern
def jNum2():        yield from SPAN('0123456789') @ "jxN" % "jxN" + Λ("len(jxN) == 2")
@pattern
def jNum3():        yield from SPAN('0123456789') @ "jxN" % "jxN" + Λ("len(jxN) == 3")
@pattern
def jNum4():        yield from SPAN('0123456789') @ "jxN" % "jxN" + Λ("len(jxN) == 4")
@pattern
def jYYYY():        yield from jNum4() % "jxYYYY"
@pattern
def jMM():          yield from jNum2() % "jxMM"
@pattern
def jDD():          yield from jNum2() % "jxDD"
@pattern
def jhh():          yield from jNum2() % "jxhh"
@pattern
def jmm():          yield from jNum2() % "jxmm"
@pattern
def jss():          yield from jNum2() % "jxss"
@pattern
def jDate():        yield from jYYYY() + σ('-') + jMM() + σ('-') + jDD()
@pattern
def Time():         yield from jhh() + σ(':') + jmm() + σ(':') + jss()
@pattern
def jDatetime():    yield from \
    ( σ('"')
    + λ("jxhh = '00'")
    + λ("jxmm = '00'")
    + λ("jxss = '00'")
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
    + λ("jxDatetime = (int(jxYYYY), int(jxMM), int(jxDD), int(jxhh), int(jxmm), int(jxss))")
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
        "average": +0.75,
        "single": true,
        "ip_address": "26.58.193.2",
        "start_date": "2025-02-06"
        }
      , {
        "id": 2,
        "first_name": "Giavani",
        "last_name": "Frediani",
        "email": "gfrediani1@senate.gov",
        "gender": "Male",
        "average": -1.25,
        "single": false,
        "ip_address": "229.179.4.212",
        "start_date": "2024-12-31"
        }
      ]
}"""
#-----------------------------------------------------------------------------------------------------------------------
import types
def OBJECT(tree):
    attributes = {}
    for i in range(1, len(tree)):
        attribute = Traverse(tree[i])
        attributes[attribute[0]] = attribute[1]
    namespace = dict()
    namespace['__dict__'] = attributes
    def __init__(self, **kwargs):
        for field, value in self.__dict__.items():
            setattr(self, field, value)
    namespace['__init__'] = __init__
#   Dynamic = types.new_class("Dynamic", (object,), {}, lambda ns: ns.update(attributes))
    Dynamic = type("Dynamic", (object,), namespace)
    return Dynamic()
#-----------------------------------------------------------------------------------------------------------------------
from pprint import pprint
def Traverse(tree):
    match tree[0]:
        case 'JSON':      result = Traverse(tree[1])
        case 'Object':    result = OBJECT(tree)
        case 'Array':     # Array
                          result = []
                          for i in range(1, len(tree)):
                              result.append(Traverse(tree[i]))
        case 'Attribute': result = Traverse(tree[1]), Traverse(tree[2])
        case 'Name':      result = tree[1]
        case 'Real':      result = tree[1]
        case 'Integer':   result = tree[1]
        case 'String':    result = tree[1]
        case 'Bool':      result = tree[1]
        case 'Datetime':  result = tree[1]
        case 'Null':      result = tree[1]
        case _:           raise Exception(f"Traverse ERROR: type {tree[0]} unknown.")
    return result
#-----------------------------------------------------------------------------------------------------------------------
print(JSON_sample)
print()
GLOBALS(globals())
JSON_sample in jRecognizer()
pprint(JSON_tree)
print()
JSON = Traverse(JSON_tree)
pprint(vars(JSON))
pprint(vars(JSON.list[0]))
pprint(vars(JSON.list[1]))
print(JSON.list[0].first_name, JSON.list[0].last_name)
print(JSON.list[1].first_name, JSON.list[1].last_name)
#-----------------------------------------------------------------------------------------------------------------------
