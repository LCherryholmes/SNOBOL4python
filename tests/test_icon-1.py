import timeit
#------------------------------------------------------------------------------
def report(s=""): pass # print(s)
#==============================================================================
# ICON Programming Language: (1st pass, attribute grammar generated)
#
#                       every write(5 > ((1 to 2) * (3 to 4)));
#==============================================================================
def x5(port):
    global              x5_V
    match port:
        case "start":   x5_V = 5; x5("succeed")
        case "resume":  x5("fail")
        case "fail":    greater("fail")
        case "succeed": mult("start")
#------------------------------------------------------------------------------
def x1(port):
    global              x1_V
    match port:
        case "start":   x1_V = 1; x1("succeed")
        case "resume":  x1("fail")
        case "fail":    to1("fail")
        case "succeed": x2("start")
#------------------------------------------------------------------------------
def x2(port):
    global              x2_V, to1_I, x1_V
    match port:
        case "start":   x2_V = 2; x2("succeed")
        case "resume":  x2("fail")
        case "fail":    x1("resume")
        case "succeed": to1_I = x1_V; to1("code")
#------------------------------------------------------------------------------
def to1(port):
    global              to1_V, to1_I, x2_V
    match port:
        case "start":   x1("start")
        case "resume":  to1_I = to1_I + 1; to1("code")
        case "code":    #
                        if to1_I <= x2_V:
                           to1_V = to1_I; to1("succeed")
                        else: x2("resume")
        case "fail":    mult("fail")
        case "succeed": to2("start")
#------------------------------------------------------------------------------
def x3(port):
    global              x3_V
    match port:
        case "start":   x3_V = 3; x3("succeed")
        case "resume":  x3("fail")
        case "fail":    to2("fail")
        case "succeed": x4("start")
#------------------------------------------------------------------------------
def x4(port):
    global              x4_V, to2_I, x3_V
    match port:
        case "start":   x4_V = 4; x4("succeed")
        case "resume":  x4("fail")
        case "fail":    x3("resume")
        case "succeed": to2_I = x3_V; to2("code")
#------------------------------------------------------------------------------
def to2(port):
    global              to2_V, to2_I, x4_V, mult_V, to1_V
    match port:
        case "start":   x3("start")
        case "resume":  to2_I = to2_I + 1; to2("code")
        case "code":    #
                        if to2_I <= x4_V:
                           to2_V = to2_I; to2("succeed")
                        else: x4("resume")
        case "fail":    to1("resume")
        case "succeed": mult_V = to1_V * to2_V; mult("succeed")
#------------------------------------------------------------------------------
def mult(port):
    global              mult_V, x5_V, greater_V
    match port:
        case "start":   to1("start")
        case "resume":  to2("resume")
        case "fail":    x5("resume")
        case "succeed": #
                        if x5_V <= mult_V: mult("resume")
                        else: greater_V = mult_V; greater("succeed")
#------------------------------------------------------------------------------
def greater(port):
    global              greater_V, write1_V
    match port:
        case "start":   x5("start")
        case "resume":  mult("resume")
        case "fail":    write1("fail")
        case "succeed": write1_V = greater_V; report(write1_V); write1("succeed")
#------------------------------------------------------------------------------
def write1(port):
    match port:
        case "start":   greater("start")
        case "resume":  greater("resume")
        case "fail":    report("Failure.") # Yeah! UNWIND already.
        case "succeed": report("Success!"); write1("resume")
#==============================================================================
# ICON Programming Language: (2nd pass, optimization)
#
#                           every write(5 > ((1 to 2) * (3 to 4)));
def write2(port):
    global                  to3_I, to4_I
    while True:
        match port:
            case "start":   to3_I = 1; to3("code"); break
            case "resume":  to4_I = to4_I + 1; to4("code"); break
            case "fail":    report("Failure."); break # Yeah! UNWIND already.
            case "succeed": #
                            report("Success!")
                            port = "resume" # loop
            case _:         raise Exception()
#------------------------------------------------------------------------------
def to3(port):
    global                  to3_I, to4_I
    while True:
        match port:
            case "resume":  to3_I = to3_I + 1; port = "code"
            case "code":    #
                            if to3_I > 2: write2("fail") 
                            else: to4_I = 3; to4("code")
                            break
            case _:         raise Exception()
#------------------------------------------------------------------------------
def to4(port):
    global                  to4_I, mult_V, to3_I, greater_V
    while True:
        match port:
            case "code":    #
                            if to4_I > 4: to3("resume"); break
                            else: mult_V = to3_I * to4_I
                            if 5 <= mult_V: write2("resume"); break
                            else: greater_V = mult_V
                            report(greater_V)
                            write2("succeed")
                            break
            case _:         raise Exception()
#==============================================================================
def main():
    if True:
        time1 = timeit.timeit(lambda: write1("start"), number = 1_000_000, globals = globals());
        print(time1)
        time2 = timeit.timeit(lambda: write2("start"), number = 1_000_000, globals = globals());
        print(time2)
    else:
        report()
        write1("start")
        report()
        write2("start")
#------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
#------------------------------------------------------------------------------
