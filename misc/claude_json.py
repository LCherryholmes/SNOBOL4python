#------------------------------------------------------------------------------
# JSON parser using SNOBOL4 pattern matching
# Produces native Python objects: dict, list, str, int, float, bool, None
#------------------------------------------------------------------------------
from SNOBOL4python import (GLOBALS, ε, σ, π, Λ, ζ, Φ,
                           ANY, ARBNO, FENCE, POS, RPOS, SPAN,
                           DIGITS, PATTERN, STRING)
from pprint import pprint

GLOBALS(globals())

#------------------------------------------------------------------------------
# Value stack
#------------------------------------------------------------------------------
_stk = []

def _push(v):             _stk.append(v);               return True
def _array_open():        _stk.append([]);              return True
def _array_append():      _stk[-2].append(_stk.pop());  return True
def _object_open():       _stk.append({});              return True
def _object_insert():
    v = _stk.pop()
    k = _stk.pop()
    _stk[-1][k] = v
    return True

#------------------------------------------------------------------------------
# Whitespace
#------------------------------------------------------------------------------
WS = π(SPAN(' \t\n\r'))

#------------------------------------------------------------------------------
# Literals
#------------------------------------------------------------------------------
json_null  = σ('null')  + Λ(lambda: _push(None))
json_true  = σ('true')  + Λ(lambda: _push(True))
json_false = σ('false') + Λ(lambda: _push(False))

#------------------------------------------------------------------------------
# Number — @ captures token as module-level _num_raw; Λ converts and pushes
#------------------------------------------------------------------------------
json_number = (
    (   π(σ('-'))
      + (σ('0') | (ANY('123456789') + π(SPAN(DIGITS))))
      + π(σ('.') + SPAN(DIGITS))
      + π(ANY('eE') + π(ANY('+-')) + SPAN(DIGITS))
    ) @ '_num_raw'
    + Λ(lambda: _push(
          float(_num_raw) if any(c in _num_raw for c in '.eE')
          else int(_num_raw)
      ))
)

#------------------------------------------------------------------------------
# String — Φ immediately assigns (?P<_str_raw>…) as module-level _str_raw
#------------------------------------------------------------------------------
_UNESCAPE = {'\\\"': '"', '\\\\': '\\', '\\/':  '/',
             '\\b':  '\b', '\\f': '\f', '\\n': '\n',
             '\\r':  '\r', '\\t': '\t'}

def _push_str():
    s = _str_raw
    for esc, ch in _UNESCAPE.items():
        s = s.replace(esc, ch)
    return _push(s)

json_string = (
    Φ(r'"(?P<_str_raw>(?:[^"\\]|\\(?:["\\/bfnrt]|u[0-9A-Fa-f]{4}))*)"')
    + Λ(_push_str)
)

#------------------------------------------------------------------------------
# Forward reference for recursion
#------------------------------------------------------------------------------
json_value_ref = ζ(lambda: json_value)

#------------------------------------------------------------------------------
# Array
#------------------------------------------------------------------------------
json_array = (
      σ('[') + Λ(_array_open) + WS
    + π(  json_value_ref + Λ(_array_append)
        + ARBNO(WS + σ(',') + WS + json_value_ref + Λ(_array_append))
      )
    + WS + σ(']')
)

#------------------------------------------------------------------------------
# Object
#------------------------------------------------------------------------------
json_pair = (
    WS + json_string + WS + σ(':') + WS + json_value_ref + Λ(_object_insert)
)

json_object = (
      σ('{') + Λ(_object_open) + WS
    + π(json_pair + ARBNO(WS + σ(',') + json_pair))
    + WS + σ('}')
)

#------------------------------------------------------------------------------
# Value / Document
#------------------------------------------------------------------------------
json_value = (
      json_null
    | json_true
    | json_false
    | json_number
    | json_string
    | json_array
    | json_object
)

json_document = POS(0) + WS + json_value + WS + RPOS(0)

#------------------------------------------------------------------------------
def parse_json(text: str):
    _stk.clear()
    if text in json_document:
        return _stk[-1]
    raise ValueError(f"JSON parse failed: {text!r}")

#------------------------------------------------------------------------------
# Tests
#------------------------------------------------------------------------------
if __name__ == '__main__':
    tests = [
        ('null',                       None),
        ('true',                       True),
        ('false',                      False),
        ('0',                          0),
        ('42',                         42),
        ('-7',                         -7),
        ('3.14',                       3.14),
        ('-2.5e3',                     -2500.0),
        ('"hello"',                    'hello'),
        ('"say \\"hi\\""',             'say "hi"'),
        ('"line\\nbreak"',             'line\nbreak'),
        ('""',                         ''),
        ('[]',                         []),
        ('[1]',                        [1]),
        ('[1,2,3]',                    [1, 2, 3]),
        ('[ 1 , 2 , 3 ]',             [1, 2, 3]),
        ('[[1,2],[3,4]]',              [[1, 2], [3, 4]]),
        ('[true,false,null]',          [True, False, None]),
        ('[1,"a",true,null,[]]',       [1, 'a', True, None, []]),
        ('{}',                         {}),
        ('{"a":1}',                    {'a': 1}),
        ('{"a":1,"b":2}',              {'a': 1, 'b': 2}),
        ('{"a":1,"b":2,"c":3}',        {'a': 1, 'b': 2, 'c': 3}),
        ('{"x":[1,{"y":true},null]}',  {'x': [1, {'y': True}, None]}),
        ('  { "k" : [ 1 , 2 ] }  ',   {'k': [1, 2]}),
    ]

    passed = failed = 0
    for src, expected in tests:
        try:
            result = parse_json(src)
            ok = result == expected
        except Exception as e:
            result = e;  ok = False
        mark = '✓' if ok else '✗'
        if ok:
            passed += 1
            print(f"{mark}  {src!r:48s}  →  {result!r}")
        else:
            failed += 1
            print(f"{mark}  {src!r:48s}")
            print(f"     expected: {expected!r}")
            print(f"     got:      {result!r}")

    print(f"\n{passed}/{passed+failed} passed")

    print()
    big = parse_json('''{
        "name": "Alice",
        "age": 30,
        "scores": [9.5, 8.0, 10.0],
        "address": { "city": "Wonderland", "zip": "00001" },
        "active": true,
        "nickname": null
    }''')
    pprint(big)