# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
#-------------------------------------------------------------------------------
blanks =            σ('\\\n') | SPAN(" \t\r\f")
white =             σ('\\\n') | SPAN(" \t\r\f\n")
hashStyleComment =  σ('#') + BREAK("\n") + σ('\n')
space =             (   blanks
                    |   hashStyleComment
                    ) + FENCE(ζ(lambda: space) | ε())
whitespace =        (   white
                    |   hashStyleComment
                    ) + FENCE(ζ(lambda: whitespace) | ε())
#-------------------------------------------------------------------------------
μ =                 FENCE(space | ε())
η =                 FENCE(whitespace | ε())
def ς(s):           return μ + σ(s)
#-------------------------------------------------------------------------------
operator =          (σ(':') | σ('-'))
#-------------------------------------------------------------------------------
escapedCharacter =  ( σ('\\')
                    + (  ANY('"\\abfnrtv\n' + "'")
                      |  ANY('01234567') + FENCE(ANY('01234567') | ε())
                      |  ANY('0123') + ANY('01234567') + ANY('01234567')
                      |  ANY('Xx') + SPAN('0123456789ABCDEFabcdef')
                      )
                    )
stringLiteral =     ( σ("'") + BREAK("'") + σ("'")
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
#-------------------------------------------------------------------------------
ident =             ( ANY(LCASE)
                    + FENCE(SPAN(DIGITS + '_' + LCASE) | ε())
                    ) % "tx"
keyword =           ident @ "tx" + Λ("tx in keywords")
identifier =        ident @ "tx" + Λ("tx not in keywords")
#-------------------------------------------------------------------------------
yamlPatch =         ( ς('-') + ς('patches')
                    + σ('/') + SPAN(DIGITS)
                    + σ('-') + BREAK('\n')
                    + η()
                    )
yamlPatches =       yamlPatch + FENCE(ζ(lambda: yamlPatches) | ε())
#-------------------------------------------------------------------------------
yamlStatement = \
    ( ς('package')                          + σ(':') + BREAK('\n')
    | ς('name')                             + σ(':') + μ() + identifier
    | ς('version')                          + σ(':') + μ() + SPAN(DIGITS) + ς('.') + SPAN(DIGITS) + ς('.') + SPAN(DIGITS)
    | ς('source')                           + σ(':') + BREAK('\n')
    | ς('patches')                          + σ(':') + BREAK('\n') + η() + (yamlPatches | ε())
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
    | ς('description')                      + σ(':') + μ() + stringLiteral
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
yamlTokens = \
    ( POS(0)                    + λ("""P = "yield from (\\n\"""")
    + ARBNO(
        Θ("OUTPUT") +
        ( σ('\\\n')             + λ("""P += "σ('\\\n') + \"""")
        | σ('\n')               + λ("""P += "η() +\\n\"""")
        | SPAN(" \t\r\f")     # + λ("""P += "μ() + \"""")
#       | SPAN(" \t\r\f\n")   # + λ("""P += "η() +\\n\"""") # currently unreachable
        | hashStyleComment      + λ("""P += "hashStyleComment +\\n\"""")
        | yamlStatement         + λ("""P += "yamlStatement + \"""")
        | stringLiteral         + λ("""P += "stringLiteral + \"""")
        | keyword               + λ("""P += "ς('" + tx + "') + \"""")
        | identifier + σ(':')   + λ("""P += "ς('" + tx + "') + σ(':') + \"""")
        | identifier            + λ("""P += "identifier + \"""")
        | operator % "tx"       + λ("""P += "ς('" + tx + "') + \"""")
        | SPAN(DIGITS)          + λ("""P += "SPAN(DIGITS) + \"""")
        | SPAN(UCASE)           + λ("""P += "SPAN(UCASE) + \"""")
        | SPAN(LCASE)           + λ("""P += "SPAN(LCASE) + \"""")
        | NOTANY(DIGITS+UCASE+LCASE) % "tx" + λ("""P += "ς('" + ("\\\\" if tx == "\\\\" else "") + tx + "') + \"""")
        ) @ "OUTPUT"
      )
    + RPOS(0)                   + λ("""P += ")\\n\"""")
    )
#-------------------------------------------------------------------------------
