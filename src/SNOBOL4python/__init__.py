from .SNOBOL4 import pos, subject, PATTERN, pattern, assign
from .SNOBOL4 import _, ε, _UCASE, _LCASE, _digits
from .SNOBOL4 import ANY, ARBNO, BREAK, DIFFER, FAIL, FENCE, IDENT, INTEGER
from .SNOBOL4 import LEN, LIT, NOTANY, POS, REM, RPOS, RTAB, SPAN, SUCCESS, TAB
from .SNOBOL4 import AND, ALT, SEQ, MATCH
from .SNOBOL4 import EQ, LT, GT, NE, LE, GE
from .SNOBOL4 import eq, lt, gt, ne, le, ge
from .SNOBOL4 import LEQ, LLT, LGT, LNE, LLE, LGE

__all__ = [
    "pos", "subject", "PATTERN", "pattern", "assign",
    "_", "ε", "_UCASE", "_LCASE", "_digits",
    "ANY", "ARBNO", "BREAK", "FAIL", "FENCE", "LEN", "LIT", "NOTANY",
    "POS", "REM", "RPOS", "RTAB", "SPAN", "SUCCESS", "TAB",
    "AND", "ALT", "SEQ", "MATCH"
]