#-------------------------------------------------------------------------------
from .SNOBOL4patterns   import GLOBALS, TRACE
from .SNOBOL4patterns   import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from .SNOBOL4patterns   import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from .SNOBOL4patterns   import RTAB, SPAN, SUCCESS, TAB
from .SNOBOL4functions  import ALPHABET, DIGITS, UCASE, LCASE
from .SNOBOL4functions  import DEFINE, REPLACE, SUBSTITUTE
from .SNOBOL4patterns   import nPush, nInc, nPop, Shift, Reduce, Pop
#-------------------------------------------------------------------------------
from .SNOBOL4patterns   import PATTERN, STRING, NULL
from .SNOBOL4patterns   import F, SEARCH, MATCH, FULLMATCH
#-------------------------------------------------------------------------------
from .SNOBOL4functions  import CHAR, DIFFER, IDENT, INTEGER
from .SNOBOL4functions  import END, RETURN, FRETURN, NRETURN
#-------------------------------------------------------------------------------
# Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ   Τ Υ Φ Χ Ψ Ω
# α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ ς τ υ φ χ ψ ω
#-------------------------------------------------------------------------------
from .SNOBOL4patterns   import epsilon, sigma, pi, LLAMBDA, llambda, zeta
def ε():                return epsilon()
def σ(s):               return sigma(s)
def π(P):               return pi(P)
def Λ(command):         return LLAMBDA(command)
def λ(expression):      return llambda(expression)
def ζ(N):               return zeta(N)
from .SNOBOL4patterns   import THETA, theta, PHI, phi, alpha, omega
def Θ(N):               return THETA(N)
def θ(N):               return theta(N)
def Φ(rex):             return PHI(rex)
def φ(rex):             return phi(rex)
def α():                return alpha()
def ω():                return omega()
def Ϩ(s):               return STRING(s)
#-------------------------------------------------------------------------------
from .SNOBOL4patterns   import SIGMA, PI, rho, DELTA, delta
def Σ(*AP):             return SIGMA(*AP)
def Π(*AP):             return PI(*AP)
def ρ(*AP):             return rho(*AP)
def Δ(P, N):            return DELTA(P, N)
def δ(P, N):            return delta(P, N)
#-------------------------------------------------------------------------------
__all__ = [
            "GLOBALS", "TRACE",
            "ε", "σ", "π", "λ", "Λ", "ζ", "θ", "Θ", "φ", "Φ", "α", "ω",
            "ABORT", "ANY", "ARB", "ARBNO", "BAL", "BREAK", "BREAKX", "FAIL",
            "FENCE", "LEN", "MARB", "MARBNO", "NOTANY", "POS", "REM", "RPOS",
            "RTAB", "SPAN", "SUCCESS", "TAB",
            "ALPHABET", "DIGITS", "UCASE", "LCASE",
            "DEFINE", "REPLACE", "SUBSTITUTE"
            "nPush", "nInc", "nPop", "Shift", "Reduce", "Pop",

            "PATTERN", "Ϩ", "STRING", "NULL",
            "F", "SEARCH", "MATCH", "FULLMATCH",
            "Σ", "Π", "ρ", "Δ", "δ",

            "CHAR", "DIFFER", "IDENT", "INTEGER",
            "END", "RETURN", "FRETURN", "NRETURN",
]
#-------------------------------------------------------------------------------
