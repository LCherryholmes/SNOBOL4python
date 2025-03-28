import random
#import cython
#------------------------------------------------------------------------------
# Generate random expression
def rand_item():
    r = random.randint(1, 100)
    if   r <=  20: return "x"
    elif r <=  40: return "y"
    elif r <=  60: return "z"
    elif r <=  80: return str(random.randint(1, 100))
    elif r <= 100: return "(" + rand_term() + ")"

def rand_element():
    r = random.randint(1, 100)
    if   r <=  80: return rand_item()
    elif r <=  90: return '+' + rand_element()
    elif r <= 100: return '-' + rand_element()

def rand_factor():
    r = random.randint(1, 100)
    if   r <=  70: return rand_element()
    elif r <=  85: return rand_element() + '*' + rand_factor()
    elif r <= 100: return rand_element() + '/' + rand_factor()
    
def rand_term():
    r = random.randint(1, 100)
    if   r <=  70: return rand_factor()
    elif r <=  85: return rand_factor() + '+' + rand_term()
    elif r <= 100: return rand_factor() + '-' + rand_term()

def rand_expression():
    return rand_term()
#------------------------------------------------------------------------------
# Generate expressions haphazardly
def gen_item():
    g_term = gen_term()
    while True:
        yield "x"
        yield "y"
        yield "z"
        yield str(random.randint(1, 100))
        yield "(" + next(g_term) + ")"

def gen_element():
    g_item = gen_item()
    g_element = gen_element()
    while True:
        yield next(g_item)
        yield '+' + next(g_element)
        yield '-' + next(g_element)

def gen_factor():
    g_factor = gen_factor()
    g_element = gen_element()
    while True:
        yield next(g_element)
        yield next(g_element) + '*' + next(g_factor)
        yield next(g_element) + '/' + next(g_factor)
    
def gen_term():
    g_term = gen_term()
    g_factor = gen_factor()
    while True:
        yield next(g_factor)
        yield next(g_factor) + '+' + next(g_term)
        yield next(g_factor) + '-' + next(g_term)
#------------------------------------------------------------------------------
e_term = gen_term()
for i in range(0):
    print(i, next(e_term))
print()
#------------------------------------------------------------------------------
# Parse expression

#pos: cython.int = 0
#subject: cython.char = ""

pos = 0
subject = ""

def POS(n):
    global pos
    if pos == n:
        yield ""

def RPOS(n):
    global pos, subject
    if pos == len(subject) - n:
        yield ""

def _(lit):
    global pos, subject
    if pos + len(lit) <= len(subject):
        if lit == subject[pos : pos + len(lit)]:
            pos += len(lit)
            yield lit
            pos -= len(lit)

def SPAN(characters):
    global pos, subject
    pos0 = pos
    while True:
        if pos >= len(subject): break
        if subject[pos] in characters:
            pos += 1
        else: break
    if pos > pos0:
        yield subject[pos0 : pos]
        pos = pos0
#------------------------------------------------------------------------------
def parse_item():
    for _1 in SPAN("0123456789"): yield int(_1)
    for _1 in _("x"): yield _1
    for _1 in _("y"): yield _1
    for _1 in _("z"): yield _1
    for _1 in _("("):
        for _2 in parse_term():
            for _3 in _(")"):
                yield _2

def parse_element():
    for _1 in parse_item(): yield _1
    for _1 in _("+"):
        for _2 in parse_element():
            yield (_1, _2)
    for _1 in _("-"):
        for _2 in parse_element():
            yield (_1, _2)

def parse_factor():
    for _1 in parse_element(): yield _1
    for _1 in parse_element():
        for _2 in _("*"):
            for _3 in parse_factor():
                yield (_2, _1, _3)
    for _1 in parse_element():
        for _2 in _("/"):
            for _3 in parse_factor():
                yield (_2, _1, _3)

def parse_term():
    for _1 in parse_factor(): yield _1
    for _1 in parse_factor():
        for _2 in _("+"):
            for _3 in parse_term():
                yield (_2, _1, _3)
    for _1 in parse_factor():
        for _2 in _("-"):
            for _3 in parse_term():
                yield (_2, _1, _3)

def parse_expression():
    for _1 in POS(0):
        for _2 in parse_term():
            for _3 in RPOS(0):
                yield _2
#------------------------------------------------------------------------------
# Evaluate expression
def evaluate(tree):
    if type(tree) == int:
        return tree    
    elif type(tree) == str:
        match tree:
            case 'x': return 10
            case 'y': return 20
            case 'z': return 30
            case _: print("Yikes!!!")
    elif type(tree) == tuple:
        try:
            match tree[0]:
                case '+':
                    match len(tree):
                        case 2: return +evaluate(tree[1])
                        case 3: return evaluate(tree[1]) + evaluate(tree[2])
                case '-':
                    match len(tree):
                        case 2: return -evaluate(tree[1])
                        case 3: return evaluate(tree[1]) - evaluate(tree[2])
                case '*': return evaluate(tree[1]) * evaluate(tree[2])
                case '/': return evaluate(tree[1]) // evaluate(tree[2])
                case _: print("Yikes!!!")
        except ZeroDivisionError:
            print("Error: Division by zero.")
            return 0
    else: print('ERROR!!!', type(tree))
#------------------------------------------------------------------------------
def main():
    global pos, subject
    for _ in range(0, 100):
        pos = 0
        subject = rand_expression();
        print(subject)
        try:
            tree = next(parse_expression());
            print(tree)
            result = evaluate(tree);
            print(result)
        except StopIteration:
            print("Parse error!")
        print()
    print("Finished!")
#------------------------------------------------------------------------------
import sys
import trace
if True: main()
else:
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace = 1, count = 1)
    tracer.run('main()')
    tracer.results().write_results(show_missing = True, coverdir = ".")
#------------------------------------------------------------------------------
