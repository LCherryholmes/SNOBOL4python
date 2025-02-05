# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
# Parse JSON string
#-----------------------------------------------------------------------------------------------------------------------
import SNOBOL4python
import inspect
from SNOBOL4python import pattern, MATCH, _UCASE, _LCASE, _digits
from SNOBOL4python import ε, σ, π, λ, Λ
from SNOBOL4python import ANY, ARBNO, BREAK, FENCE, LEN, POS, RPOS, SPAN
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce
from SNOBOL4python import JSONDecode, _shift, _reduce
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def ς(s):           yield from (SPAN(" \t\r\n") | ε()) + σ(s)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def jRecognizer():  yield from POS(0) + FENCE() + jJSON() + ς('') + RPOS(0)
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
def jField():       yield from jVar() + Shift('Name', "jxVar") + ς(':') + jElement() + Reduce('Member', 2)
@pattern
def jVar():         yield from ς('"') + ((jIdent() | jInt()) % "jxVar") + σ('"')
@pattern
def jElement():     yield from ς('') \
                             + ( jRealVal() + Shift('Real', "float(jxVal)")
                               | jIntVal()  + Shift('Integer', "int(jxVal)")
                               | jBoolVal() + Shift('Bool', "jxVal.capitalize()")
#                              | jDateVal() + Shift('Datetime', "jxVal")
                               | jStrVal()  + Shift('String', "jxVal")
                               | jNullVal() + Shift('Null')
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
def jNullVal():     yield from σ('null') + (ε() % "jxVal")
@pattern
def jTrueFalse():   yield from (σ('true') | σ('false')) % "jxVal"
@pattern
def jIdent():       yield from ANY(_UCASE + '_' + _LCASE) + FENCE(SPAN(_UCASE + '_' + _LCASE + '0123456789') | ε())
@pattern
def jString():      yield from σ('"') + ((ARBNO(BREAK('"'+'\\'+'\n') | jEscChar())) % "jxVal") + σ('"')
@pattern
def jStrVal():      yield from jString() + Λ("jxVal = JSONDecode(jxVal)")
@pattern
def jBoolVal():     yield from jTrueFalse() | σ('"') + jTrueFalse() + σ('"')
@pattern
def jRealVal():     yield from ((σ('+') | σ('-') | ε()) + SPAN('0123456789') + σ('.') + SPAN('0123456789')) % "jxVal"
@pattern
def jIntVal():      yield from (jInt() % "jxVal") | σ('"') + (jInt() % "jxVal") + σ('"')
@pattern
def jDateVal():     yield from jDatetime() + Λ("jxVal = jxDatetime")
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def jMonthName():   yield from \
                    (   σ('Jan') | σ('Feb') | σ('Mar') | σ('Apr')
                    |   σ('May') | σ('Jun') | σ('Jul') | σ('Aug')
                    |   σ('Sep') | σ('Oct') | σ('Nov') | σ('Dec')
                    ) % "jxMonthName" + Λ("jxMonth = jMos[jxMonthName]")
@pattern
def jDayName():     yield from σ('Sun') | σ('Mon') | σ('Tue') | σ('Wed') | σ('Thu') | σ('Fri') | σ('Sat')
@pattern
def jNum2():        yield from (SPAN('0123456789') / "jxN" % "jxN") + λ("len(jxN) == 2") # + EQ("len(jxN)", "2")
@pattern
def jNum3():        yield from (SPAN('0123456789') / "jxN" % "jxN") + λ("len(jxN) == 3")
@pattern
def jNum4():        yield from (SPAN('0123456789') / "jxN" % "jxN") + λ("len(jxN) == 4")
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
        "average": +0.75,
        "single": true,
        "ip_address": "26.58.193.2"
        }
      , {
        "id": 2,
        "first_name": "Giavani",
        "last_name": "Frediani",
        "email": "gfrediani1@senate.gov",
        "gender": "Male",
        "average": -1.25,
        "single": false,
        "ip_address": "229.179.4.212"
        }
      ]
}"""
#-----------------------------------------------------------------------------------------------------------------------
['JSON',
 ['Object',
  ['Member',
   ['Name', 'list'],
   ['Array',
    ['Object',
     ['Member', ['Name', 'id'], ['Integer', 1]],
     ['Member', ['Name', 'first_name'], ['String', 'Jeanette']],
     ['Member', ['Name', 'last_name'], ['String', 'Penddreth']],
     ['Member', ['Name', 'email'], ['String', 'jpenddreth0@census.gov']],
     ['Member', ['Name', 'gender'], ['String', 'Female']],
     ['Member', ['Name', 'average'], ['Real', 0.75]],
     ['Member', ['Name', 'single'], ['Bool', 'True']],
     ['Member', ['Name', 'ip_address'], ['String', '26.58.193.2']]],
    ['Object',
     ['Member', ['Name', 'id'], ['Integer', 2]],
     ['Member', ['Name', 'first_name'], ['String', 'Giavani']],
     ['Member', ['Name', 'last_name'], ['String', 'Frediani']],
     ['Member', ['Name', 'email'], ['String', 'gfrediani1@senate.gov']],
     ['Member', ['Name', 'gender'], ['String', 'Male']],
     ['Member', ['Name', 'average'], ['Real', -1.25]],
     ['Member', ['Name', 'single'], ['Bool', 'False']],
     ['Member', ['Name', 'ip_address'], ['String', '229.179.4.212']]]]]]]
#-----------------------------------------------------------------------------------------------------------------------
import types
def OBJECT(tree):
    print()
#   pprint(tree)
    name = "Dynamic"
    fields = {}
    for i in range(1, len(tree)):
        fields[tree[i][1][1]] = tree[i][2][1]
#   print(name, fields)
    namespace = dict()
    namespace['__dict__'] = fields
    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
    namespace['__init__'] = __init__
    Dynamic = types.new_class(name, (object,), {}, lambda ns: ns.update(fields))
    dynamic = Dynamic()
#   print(dir('Dynamic'), Dynamic)
#   print(dir('dynamic'), dynamic)
    print(inspect.getsource(dynamic))
#   print(dynamic)
#-----------------------------------------------------------------------------------------------------------------------
from pprint import pprint
level = -1
def Traverse(tree):
    global level
    level += 1
    match tree[0]:
        case 'JSON':      Traverse(tree[1])
        case 'Object':    # Object
                          if level >= 4: OBJECT(tree)
                          else:
                              for i in range(1, len(tree)):
                                  Traverse(tree[i])
        case 'Array':     # Array
                          for i in range(1, len(tree)):
                              Traverse(tree[i])
        case 'Member':    # Member
                          Traverse(tree[1])
                          Traverse(tree[2])
        case 'Name':      None
        case 'Real':      None
        case 'Integer':   None
        case 'String':    None
        case 'Bool':      None
        case 'Datetime':  None
        case 'Null':      None
        case _: raise Exception(f"Error type: {tree[0]}")
    level -= 1
    return ""
#-----------------------------------------------------------------------------------------------------------------------
MATCH(JSON_sample, jRecognizer(), globals())
JSON_tree = vstack.pop()
print()
Traverse(JSON_tree)
#-----------------------------------------------------------------------------------------------------------------------