# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, MATCH, GLOBALS
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ
from SNOBOL4python import ANY, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
#-------------------------------------------------------------------------------
@pattern
def blanks():           yield from  σ('\\\n') | SPAN(" \t\r\f")
@pattern
def white():            yield from  σ('\\\n') | SPAN(" \t\r\f\n")
@pattern
def hashStyleComment(): yield from  σ('#') + BREAK("\n") + σ('\n')
@pattern
def space():            yield from  (   blanks()
                                    |   hashStyleComment()
                                    ) + FENCE(space() | ε())
@pattern
def whitespace():       yield from  (   white()
                                    |   hashStyleComment()
                                    ) + FENCE(whitespace() | ε())
#-------------------------------------------------------------------------------
@pattern
def μ():                yield from  FENCE(space() | ε())
@pattern
def η():                yield from  FENCE(whitespace() | ε())
@pattern
def ς(s):               yield from  μ() + σ(s)
#-------------------------------------------------------------------------------
@pattern
def operator():         yield from  (σ(':') | σ('-'))
#-------------------------------------------------------------------------------
@pattern
def escapedCharacter(): yield from  \
                        ( σ('\\')
                        + (  ANY('"\\abfnrtv\n' + "'")
                          |  ANY('01234567') + FENCE(ANY('01234567') | ε())
                          |  ANY('0123') + ANY('01234567') + ANY('01234567')
                          |  ANY('Xx') + SPAN('0123456789ABCDEFabcdef')
                          )
                        )
@pattern
def stringLiteral():    yield from  \
                        ( σ("'") + BREAK("'") + σ("'")
                        | σ('"') + BREAK('"') + σ('"')
                        )
#-------------------------------------------------------------------------------
keywords = {
    'requirements', 'patches', 'commands', 'host',
    'detect_binary_files_with_prefix', 'source', 'https', 'requires',
    'description', 'test', 'run_exports', 'build', 'script_env', 'downstreams',
    'run_constrained', 'about', 'no_link', 'activate_in_script', 'number',
    'url', 'name', 'string', 'noarch', 'missing_dso_whitelist',
    'skip_compile_pyc', 'run', 'package', 'md5', 'version', 'weak', 'files'
    }
@pattern
def ident():            yield from  \
                        ( ANY(_LCASE) 
                        + FENCE(SPAN(_DIGITS + '_' + _LCASE) | ε())
                        ) % "tx"
@pattern
def keyword():          yield from  ident() @ "tx" + λ("tx in keywords")
@pattern
def identifier():       yield from  ident() @ "tx" + λ("tx not in keywords")
#-------------------------------------------------------------------------------
@pattern
def yamlPatch():        yield from  ( ς('-') + ς('patches')
                                    + σ('/') + SPAN(_DIGITS)
                                    + σ('-') + BREAK('\n')
                                    + η()
                                    )
@pattern
def yamlPatches():      yield from  yamlPatch() + FENCE(yamlPatches() | ε())
#-------------------------------------------------------------------------------
@pattern
def yamlStatement():    yield from  \
    ( ς('package')                          + σ(':') + BREAK('\n')
    | ς('name')                             + σ(':') + μ() + identifier()
    | ς('version')                          + σ(':') + μ() + SPAN(_DIGITS) + ς('.') + SPAN(_DIGITS) + ς('.') + SPAN(_DIGITS)
    | ς('source')                           + σ(':') + BREAK('\n')
    | ς('patches')                          + σ(':') + BREAK('\n') + η() + (yamlPatches() | ε())
    | ς('url')                              + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('build')                            + σ(':') + BREAK('\n')
    | ς('activate_in_script')               + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('detect_binary_files_with_prefix')  + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('missing_dso_whitelist')            + σ(':') + BREAK('\n')
    | ς('no_link')                          + σ(':') + BREAK('\n')
    | ς('number')                           + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('run_exports')                      + σ(':') + BREAK('\n')
    | ς('noarch')                           + σ(':') + BREAK('\n')
    | ς('weak')                             + σ(':') + BREAK('\n')
    | ς('script_env')                       + σ(':') + BREAK('\n')
    | ς('skip_compile_pyc')                 + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('string')                           + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('requirements')                     + σ(':') + BREAK('\n')
    | ς('host')                             + σ(':') + BREAK('\n')
    | ς('run')                              + σ(':') + BREAK('\n')
    | ς('run_constrained')                  + σ(':') + BREAK('\n')
    | ς('test')                             + σ(':') + BREAK('\n')
    | ς('commands')                         + σ(':') + BREAK('\n')
    | ς('downstreams')                      + σ(':') + BREAK('\n')
    | ς('files')                            + σ(':') + BREAK('\n')
    | ς('requires')                         + σ(':') + BREAK('\n')
    | ς('about')                            + σ(':') + BREAK('\n')
    | ς('description')                      + σ(':') + μ() + stringLiteral()
    | ς('dev_url')                          + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('doc_source_url')                   + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('doc_url')                          + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('home')                             + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('license')                          + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('license_file')                     + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('summary')                          + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('extra')                            + σ(':') + BREAK('\n')
    | ς('copy_test_source_files')           + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('feedstock-name')                   + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('final')                            + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('flow_run_id')                      + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('recipe-maintainers')               + σ(':') + BREAK('\n')
    | ς('remote_url')                       + σ(':') + NOTANY('\n') + BREAK('\n')
    | ς('sha')                              + σ(':') + NOTANY('\n') + BREAK('\n')
    )
#-------------------------------------------------------------------------------
@pattern
def yamlTokens():
    yield from  \
    ( POS(0)                    + Λ("""P = "yield from (\\n\"""")
    + ARBNO(
        θ("OUTPUT") +
        ( σ('\\\n')             + Λ("""P += "σ('\\\n') + \"""")
        | σ('\n')               + Λ("""P += "η() +\\n\"""") 
        | SPAN(" \t\r\f")     # + Λ("""P += "μ() + \"""")
#       | SPAN(" \t\r\f\n")   # + Λ("""P += "η() +\\n\"""") # currently unreachable
        | hashStyleComment()    + Λ("""P += "hashStyleComment() +\\n\"""")
        | yamlStatement()       + Λ("""P += "yamlStatement() + \"""")
        | stringLiteral()       + Λ("""P += "stringLiteral() + \"""")
        | keyword()             + Λ("""P += "ς('" + tx + "') + \"""")
        | identifier() + σ(':') + Λ("""P += "ς('" + tx + "') + σ(':') + \"""")
        | identifier()          + Λ("""P += "identifier() + \"""")
        | operator() % "tx"     + Λ("""P += "ς('" + tx + "') + \"""")
        | SPAN(_DIGITS)         + Λ("""P += "SPAN(_DIGITS) + \"""")
        | SPAN(_UCASE)          + Λ("""P += "SPAN(_UCASE) + \"""")
        | SPAN(_LCASE)          + Λ("""P += "SPAN(_LCASE) + \"""")
        | NOTANY(_DIGITS+_UCASE+_LCASE) % "tx" + Λ("""P += "ς('" + ("\\\\" if tx == "\\\\" else "") + tx + "') + \"""")
        ) @ "OUTPUT"
      )
    + RPOS(0)                   + Λ("""P += ")\\n\"""")
    )
#-------------------------------------------------------------------------------
