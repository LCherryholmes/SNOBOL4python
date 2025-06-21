#-------------------------------------------------------------------------------
# 31 flavors of patterns to choose from ...
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import PATTERN, STRING, NULL
from pprint import pformat, pprint
#-------------------------------------------------------------------------------
def init():     return λ(f"scala = None; stack = []")   # + λ(f"pprint(stack)")
def push(v):    return λ(f"stack.append([{v}])")        # + λ(f"pprint(stack)")
def inject(v):  return ( λ(f"top = stack[-1].pop()")    # + λ(f"pprint(stack)")
                       + λ(f"stack.append([{v}, top])") # + λ(f"pprint(stack)")
                       )
def item(v):    return λ(f"stack[-1].append({v})")      # + λ(f"pprint(stack)")
def pop():      return ( λ(f"top = tuple(stack.pop())") # + λ(f"pprint(stack)")
                       + λ(f"stack[-1].append(top)")    # + λ(f"pprint(stack)")
                       )
def fini():     return λ(f"scala = tuple(stack.pop())") # + λ(f"pprint(stack)")
#-------------------------------------------------------------------------------
η           =   ARBNO(SPAN(' \t\r\n') | σ('//') + BREAK('\n'))
def ς(s):       return η + σ(s)
#-------------------------------------------------------------------------------
integer     =   η + (SPAN(DIGITS)) @ "OUTPUT" % "txtint"
string      =   η + (σ('"') + BREAK('"') + σ('"')) @ "OUTPUT" % "txtstr"
identifier  =   ( η
                + ( ANY(UCASE+LCASE)
                  + (SPAN(DIGITS+UCASE+'_'+LCASE) | ε())
                  ) @ "OUTPUT" % "id"
                )
#-------------------------------------------------------------------------------
parameters  =   ( identifier + item("id")
                + ARBNO(ς(',') + identifier + item("id"))
                )
function    =   ( push("'lambda'")
                + parameters
                + ς('=>')
                + ζ(lambda: expression)
                + pop()
                )
reference   =   ( identifier + push("'id'") + item("id") + pop()
                | identifier + push("id")
                + ς('(') + ζ(lambda: arguments) + ς(')') + pop()
                )
#-------------------------------------------------------------------------------
element     =   ( integer + push("'int'") + item("eval(txtint)") + pop()
                | string  + push("'str'") + item("eval(txtstr)") + pop()
                | reference
                | ς('(') + ζ(lambda: expression) + ς(')')
                )
factor      =   ( ς('+') + push("'+'") + ζ(lambda: factor) + pop()
                | ς('-') + push("'-'") + ζ(lambda: factor) + pop()
                | element
                + ARBNO(
                    ς('.')
                  + inject("'.'")
                  + reference
                  + pop()
                  )
                )
term        =   ( factor
                + ( ς('*') + inject("'*'") + ζ(lambda: term) + pop()
                  | ς('/') + inject("'/'") + ζ(lambda: term) + pop()
                  | ε()
                  )
                )
expression  =   ( term
                + ( ς('+') + inject("'+'") + ζ(lambda: expression) + pop()
                  | ς('-') + inject("'-'") + ζ(lambda: expression) + pop()
                  | ς('dot') + inject("'dot'") + ζ(lambda: expression) + pop()
                  | ε()
                  )
                )
#-------------------------------------------------------------------------------
argument    =   ( function
                | expression
                + (ς('until') + inject("'until'") + expression + pop() | ε())
                | ( ς('new') + push("'new'")
                  + identifier + item("id")
                  + ς('(') + ζ(lambda: arguments) + ς(')')
                  + pop()
                  )
                )
arguments   =   argument + ARBNO(ς(',') + argument) | ε()
#-------------------------------------------------------------------------------
assignment  =   ( (ς('var') | ς('val') | ε())
                + identifier
                + ( ς('=') + push("'='") + item("id")
                  | ς('+=') + push("'+='") + item("id")
                  | ς('-=') + push("'-='") + item("id")
                  )
                + expression
                + pop()
                )
#-------------------------------------------------------------------------------
loop        =   ( ς('for') + push("'for'")
                + ς('(') + identifier + item("id")
                + ς('<-') + expression + (ς('to') + expression | ε())
                + ς(')') + ς('{')
                + ζ(lambda: statements)
                + ς('}')
                + pop()
                )
#-------------------------------------------------------------------------------
statement   =   ( loop
                | assignment + ς(';')
                | push("'eval'") + expression + ς(';') + pop()
                )
statements  =   ARBNO(statement)
program     =   ( POS(0)
                + init()
                + push("'scala'")
                + statements
                + fini()
                + η + RPOS(0)
                )
#===============================================================================
def interp(t):
    match t[0]:
        case 'id':      #
                        if t[1] in globals():
                            return globals()[t[1]]
                        else: return None
        case 'int':     return t[1]
        case 'str':     return t[1]
        case '=':       globals()[t[1]] = interp(t[2])
        case '+=':      globals()[t[1]] += interp(t[2])
        case '-=':      globals()[t[1]] -= interp(t[2])
        case '*':       return interp(t[1]) * interp(t[2])
        case '/':       return interp(t[1]) / interp(t[2])
        case '+':       # positive and addition
                        if len(t) == 2: return +interp(t[1])
                        elif len(t) == 3: return interp(t[1]) + interp(t[2])
        case '-':       # negative and subtraction
                        if len(t) == 2: return -interp(t[1])
                        elif len(t) == 3: return interp(t[1]) - interp(t[2])
        case 'eval':    return interp(t[1])
        case 'print':   return print(interp(t[1]))
        case 'for':     #
                        for index in range(interp(t[2]), interp(t[3])):
                            globals()[t[1]] = index
                            for s in t[4:]: interp(s)
        case 'scala':   # interpret each statement
                        for s in t[1:]: interp(s)
        case _:         raise Exception(f"interp: {t}")
#===============================================================================
GLOBALS(globals())
TRACE(40)
program_source = """\
x = 0;
for (i <- 0 to 10) {
    x += 1;
    print(x);
}
"""
if program_source in program:
    pprint(scala)
    pprint(interp(scala))
else: print("Boo!")
#-------------------------------------------------------------------------------
"""\
val file = spark.textFile("hdfs://...");
val errs = file.filter(line => line.contains("ERROR"));
val ones = errs.map(item => 1);
val count = ones.reduce(total, count => total + count);

val file = spark.textFile("hdfs://...");
val errs = file.filter(line => line.contains("ERROR"));
val cachedErrs = errs.cache();
val ones = cachedErrs.map(item => 1);
val count = ones.reduce(total, count => total + count);

// Read points from a text file and cache them
val points = spark.textFile("...").map(parsePoint).cache();
// Initialize w to random D-dimensional vector
var w = Vector.random(D);
// Run multiple iterations to update w
for (i <- 1 to ITERATIONS) {
    val grad = spark.accumulator(new Vector(D));
    for (p <- points) { // Runs in parallel
        val s = (1/(1+exp(-p.y*(w dot p.x)))-1)*p.y;
        grad += s * p.x;
    }
    w -= grad.value;
}

val Rb = spark.broadcast(R);
for (i <- 1 to ITERATIONS) {
    U = spark.parallelize(0 until u).map(j => updateUser(j, Rb, M)).collect();
    M = spark.parallelize(0 until m).map(j => updateUser(j, Rb, U)).collect();
}

lines = spark.textFile("hdfs://...");
errors = lines.filter(line => line.startsWith("ERROR"));
errors.persist();
errors.count();
//------------------------------------------------------------------------------
// Count errors mentioning MySQL:
errors.filter(line => line.contains("MySQL")).count()
// Return the time fields of errors mentioning
// HDFS as an array (assuming time is field
// number 3 in a tab-separated format):
errors.filter(line => line.contains("HDFS")).map(line => line.split('\t')[3]).collect()
//------------------------------------------------------------------------------
val points = spark.textFile("...").map(parsePoint).persist();
var w = 0; // random initial vector
for (i <- 1 to ITERATIONS) {
    val gradient = points.map( p =>
        p.x * (1/(1+exp(-p.y*(w dot p.x)))-1)*p.y
    ).reduce((a,b) => a+b);
    w -= gradient;
}
//------------------------------------------------------------------------------
// Load graph as an RDD of (URL, outlinks) pairs
val links = spark.textFile(...).map(...).persist()
var ranks = // RDD of (URL, rank) pairs
for (i <- 1 to ITERATIONS) {
    // Build an RDD of (targetURL, float) pairs
    // with the contributions sent by each page
    val contribs = links.join(ranks).flatMap {
        (url, (links, rank)) =>
        links.map(dest => (dest, rank/links.size))
    }
    // Sum contributions by URL and get new ranks
    ranks = contribs.reduceByKey((x,y) => x+y).mapValues(sum => a/N + (1-a)*sum)
}
links = spark.textFile("...").map("...").partitionBy(myPartFunc).persist()
//------------------------------------------------------------------------------
"""