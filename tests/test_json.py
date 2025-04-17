# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
# Parse JSON string
#-----------------------------------------------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCESS, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from datetime import datetime
import operator
#-----------------------------------------------------------------------------------------------------------------------
def JSONDecode(s): return s
#-----------------------------------------------------------------------------------------------------------------------
def ς(s):       return (SPAN(" \t\r\n") | ε()) + σ(s)
#-----------------------------------------------------------------------------------------------------------------------
jInt        =   (FENCE(σ('+') | σ('-') | ε()) + SPAN('0123456789')) % "jxN"
jEscChar    =   σ('\\') \
              + (  ANY('ntbrf' + '"' + '\\' + '/' + "'")
                |  ANY('01234567') + FENCE(ANY('01234567') | ε())
                |  ANY('0123') + ANY('01234567') + ANY('01234567')
                |  σ('u') + (LEN(4) & SPAN('0123456789ABCDEFabcdef'))
                )
jNullVal    =   σ('null') + ε() % "jxVal"
jTrueFalse  =   (σ('true') | σ('false')) % "jxVal"
jIdent      =   ANY(UCASE + '_' + LCASE) + FENCE(SPAN(UCASE + '_' + LCASE + '0123456789') | ε())
jString     =   σ('"') + ((ARBNO(BREAK('"'+'\\'+'\n') | jEscChar)) % "jxVal") + σ('"')
jStrVal     =   jString + λ("jxVal = JSONDecode(jxVal)")
jBoolVal    =   jTrueFalse | σ('"') + jTrueFalse + σ('"')
jRealVal    =   ((σ('+') | σ('-') | ε()) + SPAN('0123456789') + σ('.') + SPAN('0123456789')) % "jxVal"
jIntVal     =   (jInt % "jxVal") | σ('"') + (jInt % "jxVal") + σ('"')
#-----------------------------------------------------------------------------------------------------------------------
jMonthName =   ( σ('Jan') | σ('Feb') | σ('Mar') | σ('Apr')
               | σ('May') | σ('Jun') | σ('Jul') | σ('Aug')
               | σ('Sep') | σ('Oct') | σ('Nov') | σ('Dec')
               ) % "jxMonthName" + λ("jxMonth = jMos[jxMonthName]")
jDayName =     σ('Sun') | σ('Mon') | σ('Tue') | σ('Wed') | σ('Thu') | σ('Fri') | σ('Sat')
jNum2 =        SPAN('0123456789') @ "jxN" % "jxN" + Λ("len(jxN) == 2")
jNum3 =        SPAN('0123456789') @ "jxN" % "jxN" + Λ("len(jxN) == 3")
jNum4 =        SPAN('0123456789') @ "jxN" % "jxN" + Λ("len(jxN) == 4")
jYYYY =        jNum4 % "jxYYYY"
jMM =          jNum2 % "jxMM"
jDD =          jNum2 % "jxDD"
jhh =          jNum2 % "jxhh"
jmm =          jNum2 % "jxmm"
jss =          jNum2 % "jxss"
jDate =        jYYYY + σ('-') + jMM + σ('-') + jDD
Time =         jhh + σ(':') + jmm + σ(':') + jss
jDatetime =     ( σ('"')
                + λ("jxhh = '00'")
                + λ("jxmm = '00'")
                + λ("jxss = '00'")
                + ( jDayName + σ(', ') + jDD + σ(' ') + jMonthName + σ(' ') + jYYYY + σ(' ') + Time + σ(' +') + jNum4
                  | jDayName + σ(' ') + jMonthName + σ(' ') + jDD + σ(' ') + Time + σ(' +') + jNum4 + σ(' ') + jYYYY
                  | jDate
                  | jDate + σ('T') + Time
                  | jDate + σ('T') + Time + σ('.') + (jNum3 | ε()) + σ('Z')
                  | jDate + σ('T') + Time + σ('+') + jNum4
                  | jDate + σ('T') + Time + σ('+') + jNum2 + σ(':') + jNum2
                  | jDate + σ(' ') + Time + σ(' +') + jNum4
                  )
                + σ('"')
                + λ("jxDatetime = (int(jxYYYY), int(jxMM), int(jxDD), int(jxhh), int(jxmm), int(jxss))")
                )
jDateVal =     jDatetime + λ("jxVal = jxDatetime")
#-----------------------------------------------------------------------------------------------------------------------
jElement =      ς('') \
              + ( jRealVal + Shift('Real', "float(jxVal)")
                | jIntVal  + Shift('Integer', "int(jxVal)")
                | jBoolVal + Shift('Bool', "dict(true=True, false=False)[jxVal]")
                | jDateVal + Shift('Datetime', "datetime(*jxVal)")
                | jStrVal  + Shift('String', "jxVal")
                | jNullVal + Shift('None')
                | ζ(lambda: jArray)
                | ζ(lambda: jObject)
                )
jVar =          ς('"') + (jIdent | jInt) % "jxVar" + σ('"')
jField =        jVar + Shift('Name', "jxVar") + ς(':') + jElement + Reduce('Attribute', 2)
jObject =       ( ς('{') + nPush()
                + π(jField + nInc() + ARBNO(ς(',') + jField + nInc()))
                + ς('}') + Reduce('Object') + nPop()
                + FENCE()
                )
jArray =        ( ς('[') + nPush()
                + π(jElement + nInc() + ARBNO(ς(',') + jElement + nInc()))
                + ς(']') + Reduce('Array') + nPop()
                + FENCE()
                )
jJSON =         jObject + Reduce('JSON', 1)
jRecognizer =   POS(0) + FENCE() + jJSON + ς('') + Pop('JSON_tree') + RPOS(0)
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
TRACE(40)
GLOBALS(globals())
print(JSON_sample)
print()
if JSON_sample in jRecognizer:
    pprint(JSON_tree)
    print()
    JSON = Traverse(JSON_tree)
    pprint(vars(JSON))
    pprint(vars(JSON.list[0]))
    pprint(vars(JSON.list[1]))
    print(JSON.list[0].first_name, JSON.list[0].last_name)
    print(JSON.list[1].first_name, JSON.list[1].last_name)
else: print("Boo!")
#-----------------------------------------------------------------------------------------------------------------------