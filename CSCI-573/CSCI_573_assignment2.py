#-------------------------------------------------------------------------------
import datetime
from pprint import pprint
#-------------------------------------------------------------------------------
if False:
    from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
    from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
    from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
    from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
    from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
    from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
    GLOBALS(globals())
else:
    from spipat import *
    def ε(): return Pattern('')
    def σ(string): return Pattern(string)
    def ζ(function): return Pattern(function)
#-------------------------------------------------------------------------------
month_map = { 'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
              'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
#-------------------------------------------------------------------------------
def apache_time(s):
    return datetime.datetime(
        int(s[7:11]),
        month_map[s[3:6]],
        int(s[0:2]),
        int(s[12:14]),
        int(s[15:17]),
        int(s[18:20]))
#-------------------------------------------------------------------------------
globals()['DIGITS'] = "0123456789"
globals()['UCASE']  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
globals()['LCASE']  = "abcdefghijklmnopqrstuvwxyz"
#-------------------------------------------------------------------------------
CLF     =   ( POS(0) + BREAK(' ') % "host"
            + σ(' ') + BREAK(' ') % "client_id"
            + σ(' ') + BREAK(' ') % "user_id"
            + σ(' ') + σ('[') + BREAK(']') % "date_time" + σ(']')
            + σ(' "')
            + (σ('GET') | σ('HEAD') | σ('POST')) % "method"
            + σ(' ')
            + ARB() % "endpoint"
            + (σ(' HTTP/1.0') | σ(' HTTP/V1.0') | ε()) % "protocol"
            + σ('" ') + SPAN(DIGITS) % "response_code"
            + σ(' ') + (SPAN(DIGITS) | σ('-')) % "content_size"
            + RPOS(0)
            )
#-------------------------------------------------------------------------------
import re
re_CLF  =   ( r"^(?P<host>[^ ]*)"
              r" (?P<client_id>[^ ]*)"
              r" (?P<user_id>[^ ]*)"
              r" \[(?P<date_time>[^]]*)\]"
              r" \"(?P<method>GET|HEAD|POST)"
              r" (?P<endpoint>.*?)"
              r"(?: (?P<protocol>HTTP/(V|)1.0)|)"
              r"\" (?P<response_code>[0-9]+)"
              r" (?P<content_size>[0-9]+|-)"
              r"$"
            )
#re_CLF =   r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S*)" (\d{3}) (\S+)'
re_CLF  =   re.compile(re_CLF)
#-------------------------------------------------------------------------------
def process_line():
    if False:
        print('%s %s %s %s %s %d %s %s %s' % \
            ( host, client_id, user_id,
              apache_time(date_time), method, len(endpoint), protocol,
              response_code, content_size)
            )
#-------------------------------------------------------------------------------
with open("NASAlog.txt", "r", encoding="latin1") as clf_file:
    iteration = 0
    while line := clf_file.readline():
        line = line[:-1]
        if iteration % 10000 == 0:
            print(iteration)
    #   ------------------------------------------------------------------------
        if False:
            if line in CLF:
                process_line()
            else: print(f'"{line}"')
    #   ------------------------------------------------------------------------
        if True:
            if m := CLF.search(line, globals()):
                process_line()
            else: print(f'"{line}"')
    #   ------------------------------------------------------------------------
        if False:
            if m := re.search(re_CLF, line):
                for x in m.groupdict():
                    globals()[x] = m.groupdict()[x]
                process_line()
            else: print(f'"{line}"')
    #   ------------------------------------------------------------------------
        iteration += 1
print(iteration)
#-------------------------------------------------------------------------------
