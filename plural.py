yield from (
σ('%{') + η() +
cStyleComment() + η() +
η() +
cStyleComment() + η() +
σ('#') + σ('if') + identifier() + identifier() + σ('&') + σ('&') + σ('!') + identifier() + identifier() + η() +
σ('#') + identifier() + identifier() + η() +
σ('#') + identifier() + η() +
η() +
σ('#') + identifier() + identifier() + η() +
σ('#') + identifier() + σ('<') + identifier() + σ('.') + identifier() + σ('>') + η() +
σ('#') + identifier() + η() +
η() +
σ('#') + identifier() + σ('<') + identifier() + σ('.') + identifier() + σ('>') + η() +
σ('#') + identifier() + σ('<') + identifier() + σ('.') + identifier() + σ('>') + η() +
σ('#') + identifier() + σ('<') + identifier() + σ('.') + identifier() + σ('>') + η() +
σ('#') + identifier() + stringLiteral() + η() +
η() +
cStyleComment() + η() +
σ('#') + identifier() + identifier() + η() +
σ('#') + identifier() + identifier() + identifier() + η() +
σ('#') + identifier() + η() +
η() +
σ('%}') + η() +
σ('%') + identifier() + σ('-') + identifier() + σ('{') + σ('struct') + identifier() + σ('*') + identifier() + σ('}') + η() +
σ('%') + identifier() + σ('-') + identifier() + σ('{') + σ('struct') + identifier() + σ('*') + identifier() + σ('}') + η() +
σ('%') + identifier() + identifier() + σ('.') + identifier() + identifier() + η() +
σ('%') + identifier() + integerLiteral() + η() +
η() +
σ('%') + σ('union') + σ('{') + η() +
identifier() + identifier() + identifier() + identifier() + σ(';') + η() +
identifier() + identifier() + identifier() + σ(';') + η() +
σ('struct') + identifier() + σ('*') + identifier() + σ(';') + η() +
σ('}') + η() +
η() +
σ('%{') + η() +
cStyleComment() + η() +
identifier() + identifier() + identifier() + σ('(') + identifier() + σ('*') + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + identifier() + σ(')') + σ(';') + η() +
identifier() + identifier() + identifier() + σ('(') + σ('struct') + identifier() + σ('*') + identifier() + σ(',') + identifier() + identifier() + σ('*') + identifier() + σ(')') + σ(';') + η() +
η() +
cStyleComment() + η() +
η() +
identifier() + σ('struct') + identifier() + σ('*') + η() +
identifier() + σ('(') + identifier() + identifier() + σ(',') + identifier() + identifier() + identifier() + σ(',') + η() +
σ('struct') + identifier() + σ('*') + identifier() + σ('*') + identifier() + σ(')') + η() +
σ('{') + η() +
identifier() + identifier() + σ(';') + η() +
σ('struct') + identifier() + σ('*') + identifier() + σ(';') + η() +
η() +
cStyleComment() + η() +
σ('for') + σ('(') + identifier() + σ('=') + identifier() + σ('-') + integerLiteral() + σ(';') + identifier() + σ('>') + σ('=') + integerLiteral() + σ(';') + identifier() + σ('-') + σ('-') + σ(')') + η() +
σ('if') + σ('(') + identifier() + σ('[') + identifier() + σ(']') + σ('=') + σ('=') + identifier() + σ(')') + η() +
σ('goto') + identifier() + σ(';') + η() +
η() +
cStyleComment() + η() +
identifier() + σ('=') + σ('(') + σ('struct') + identifier() + σ('*') + σ(')') + identifier() + σ('(') + identifier() + σ('(') + σ('*') + identifier() + σ(')') + σ(')') + σ(';') + η() +
σ('if') + σ('(') + identifier() + σ('!') + σ('=') + identifier() + σ(')') + η() +
σ('{') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
σ('for') + σ('(') + identifier() + σ('=') + identifier() + σ('-') + integerLiteral() + σ(';') + identifier() + σ('>') + σ('=') + integerLiteral() + σ(';') + identifier() + σ('-') + σ('-') + σ(')') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('.') + identifier() + σ('[') + identifier() + σ(']') + σ('=') + identifier() + σ('[') + identifier() + σ(']') + σ(';') + η() +
identifier() + identifier() + σ(';') + η() +
σ('}') + η() +
η() +
identifier() + σ(':') + η() +
σ('for') + σ('(') + identifier() + σ('=') + identifier() + σ('-') + integerLiteral() + σ(';') + identifier() + σ('>') + σ('=') + integerLiteral() + σ(';') + identifier() + σ('-') + σ('-') + σ(')') + η() +
identifier() + σ('(') + identifier() + σ('[') + identifier() + σ(']') + σ(')') + σ(';') + η() +
η() +
identifier() + identifier() + σ(';') + η() +
σ('}') + η() +
η() +
identifier() + identifier() + σ('struct') + identifier() + σ('*') + η() +
identifier() + σ('(') + identifier() + identifier() + identifier() + σ(')') + η() +
σ('{') + η() +
identifier() + identifier() + σ('(') + integerLiteral() + σ(',') + identifier() + σ(',') + identifier() + σ(')') + σ(';') + η() +
σ('}') + η() +
η() +
identifier() + identifier() + σ('struct') + identifier() + σ('*') + η() +
identifier() + σ('(') + identifier() + identifier() + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + σ('right') + σ(')') + η() +
σ('{') + η() +
σ('struct') + identifier() + σ('*') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(';') + η() +
η() +
identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('right') + σ(';') + η() +
identifier() + identifier() + σ('(') + integerLiteral() + σ(',') + identifier() + σ(',') + identifier() + σ(')') + σ(';') + η() +
σ('}') + η() +
η() +
identifier() + σ('struct') + identifier() + σ('*') + η() +
identifier() + σ('(') + identifier() + identifier() + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + σ('left') + σ(',') + η() +
σ('struct') + identifier() + σ('*') + σ('right') + σ(')') + η() +
σ('{') + η() +
σ('struct') + identifier() + σ('*') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(';') + η() +
η() +
identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('left') + σ(';') + η() +
identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('right') + σ(';') + η() +
identifier() + identifier() + σ('(') + integerLiteral() + σ(',') + identifier() + σ(',') + identifier() + σ(')') + σ(';') + η() +
σ('}') + η() +
η() +
identifier() + identifier() + σ('struct') + identifier() + σ('*') + η() +
identifier() + σ('(') + identifier() + identifier() + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + identifier() + σ(',') + η() +
σ('struct') + identifier() + σ('*') + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + identifier() + σ(')') + η() +
σ('{') + η() +
σ('struct') + identifier() + σ('*') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(';') + η() +
η() +
identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + identifier() + σ(';') + η() +
identifier() + identifier() + σ('(') + integerLiteral() + σ(',') + identifier() + σ(',') + identifier() + σ(')') + σ(';') + η() +
σ('}') + η() +
η() +
σ('%}') + η() +
η() +
cStyleComment() + η() +
σ('%') + σ('right') + characterLiteral() + cStyleComment() + η() +
σ('%') + σ('left') + characterLiteral() + cStyleComment() + η() +
σ('%') + σ('left') + characterLiteral() + cStyleComment() + η() +
σ('%') + σ('left') + identifier() + cStyleComment() + η() +
σ('%') + σ('left') + identifier() + cStyleComment() + η() +
σ('%') + σ('left') + identifier() + cStyleComment() + η() +
σ('%') + σ('left') + identifier() + σ('/') + σ('*') + σ('*') + σ('/') + σ('%') + σ('*') + σ('/') + η() +
σ('%') + σ('right') + characterLiteral() + cStyleComment() + η() +
η() +
σ('%') + σ('token') + σ('<') + identifier() + σ('>') + identifier() + identifier() + identifier() + identifier() + η() +
σ('%') + σ('token') + σ('<') + identifier() + σ('>') + identifier() + η() +
σ('%') + σ('type') + σ('<') + identifier() + σ('>') + identifier() + η() +
η() +
σ('%%') + η() +
η() +
σ('start') + σ(':') + identifier() + η() +
σ('{') + η() +
σ('if') + σ('(') + ζ('$#') + σ('=') + σ('=') + identifier() + σ(')') + η() +
identifier() + σ(';') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + ζ('$#') + σ(';') + η() +
σ('}') + η() +
σ(';') + η() +
η() +
identifier() + σ(':') + identifier() + characterLiteral() + identifier() + characterLiteral() + identifier() + η() +
σ('{') + η() +
σ('$$') + σ('=') + identifier() + σ('(') + identifier() + σ(',') + ζ('$#') + σ(',') + ζ('$#') + σ(',') + ζ('$#') + σ(')') + σ(';') + η() +
σ('}') + η() +
σ('|') + identifier() + characterLiteral() + identifier() + η() +
σ('{') + η() +
σ('$$') + σ('=') + identifier() + σ('(') + identifier() + σ(',') + ζ('$#') + σ(',') + ζ('$#') + σ(')') + σ(';') + η() +
σ('}') + η() +
σ('|') + identifier() + characterLiteral() + identifier() + η() +
σ('{') + η() +
σ('$$') + σ('=') + identifier() + σ('(') + identifier() + σ(',') + ζ('$#') + σ(',') + ζ('$#') + σ(')') + σ(';') + η() +
σ('}') + η() +
σ('|') + identifier() + identifier() + identifier() + η() +
σ('{') + η() +
σ('$$') + σ('=') + identifier() + σ('(') + ζ('$#') + σ(',') + ζ('$#') + σ(',') + ζ('$#') + σ(')') + σ(';') + η() +
σ('}') + η() +
σ('|') + identifier() + identifier() + identifier() + η() +
σ('{') + η() +
σ('$$') + σ('=') + identifier() + σ('(') + ζ('$#') + σ(',') + ζ('$#') + σ(',') + ζ('$#') + σ(')') + σ(';') + η() +
σ('}') + η() +
σ('|') + identifier() + identifier() + identifier() + η() +
σ('{') + η() +
σ('$$') + σ('=') + identifier() + σ('(') + ζ('$#') + σ(',') + ζ('$#') + σ(',') + ζ('$#') + σ(')') + σ(';') + η() +
σ('}') + η() +
σ('|') + identifier() + identifier() + identifier() + η() +
σ('{') + η() +
σ('$$') + σ('=') + identifier() + σ('(') + ζ('$#') + σ(',') + ζ('$#') + σ(',') + ζ('$#') + σ(')') + σ(';') + η() +
σ('}') + η() +
σ('|') + characterLiteral() + identifier() + η() +
σ('{') + η() +
σ('$$') + σ('=') + identifier() + σ('(') + identifier() + σ(',') + ζ('$#') + σ(')') + σ(';') + η() +
σ('}') + η() +
σ('|') + characterLiteral() + η() +
σ('{') + η() +
σ('$$') + σ('=') + identifier() + σ('(') + identifier() + σ(')') + σ(';') + η() +
σ('}') + η() +
σ('|') + identifier() + η() +
σ('{') + η() +
σ('if') + σ('(') + σ('(') + σ('$$') + σ('=') + identifier() + σ('(') + identifier() + σ(')') + σ(')') + σ('!') + σ('=') + identifier() + σ(')') + η() +
σ('$$') + σ('-') + σ('>') + identifier() + σ('.') + identifier() + σ('=') + ζ('$#') + σ(';') + η() +
σ('}') + η() +
σ('|') + characterLiteral() + identifier() + characterLiteral() + η() +
σ('{') + η() +
σ('$$') + σ('=') + ζ('$#') + σ(';') + η() +
σ('}') + η() +
σ(';') + η() +
η() +
σ('%%') + η() +
η() +
identifier() + η() +
identifier() + η() +
identifier() + σ('(') + σ('struct') + identifier() + σ('*') + identifier() + σ(')') + η() +
σ('{') + η() +
σ('if') + σ('(') + identifier() + σ('=') + σ('=') + identifier() + σ(')') + η() +
identifier() + σ(';') + η() +
η() +
cStyleComment() + η() +
σ('switch') + σ('(') + identifier() + σ('-') + σ('>') + identifier() + σ(')') + η() +
σ('{') + η() +
σ('case') + integerLiteral() + σ(':') + η() +
identifier() + σ('(') + identifier() + σ('-') + σ('>') + identifier() + σ('.') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(')') + σ(';') + η() +
cStyleComment() + η() +
σ('case') + integerLiteral() + σ(':') + η() +
identifier() + σ('(') + identifier() + σ('-') + σ('>') + identifier() + σ('.') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(')') + σ(';') + η() +
cStyleComment() + η() +
σ('case') + integerLiteral() + σ(':') + η() +
identifier() + σ('(') + identifier() + σ('-') + σ('>') + identifier() + σ('.') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(')') + σ(';') + η() +
cStyleComment() + η() +
σ('default') + σ(':') + η() +
σ('break') + σ(';') + η() +
σ('}') + η() +
η() +
identifier() + σ('(') + identifier() + σ(')') + σ(';') + η() +
σ('}') + η() +
η() +
η() +
identifier() + identifier() + η() +
identifier() + σ('(') + identifier() + σ('*') + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + identifier() + σ(')') + η() +
σ('{') + η() +
identifier() + identifier() + σ('*') + identifier() + σ('=') + identifier() + σ('-') + σ('>') + identifier() + σ(';') + η() +
identifier() + identifier() + σ(';') + η() +
η() +
σ('while') + σ('(') + integerLiteral() + σ(')') + η() +
σ('{') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('=') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + identifier() + σ(';') + η() +
σ('}') + η() +
η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('!') + σ('=') + characterLiteral() + σ('&') + σ('&') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('!') + σ('=') + characterLiteral() + σ(')') + η() +
σ('break') + σ(';') + η() +
η() +
σ('+') + σ('+') + identifier() + σ(';') + η() +
σ('}') + η() +
η() +
identifier() + σ('=') + σ('*') + identifier() + σ('+') + σ('+') + σ(';') + η() +
σ('switch') + σ('(') + identifier() + σ(')') + η() +
σ('{') + η() +
σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + η() +
σ('{') + η() +
identifier() + identifier() + identifier() + identifier() + σ('=') + identifier() + σ('-') + characterLiteral() + σ(';') + η() +
σ('while') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('>') + σ('=') + characterLiteral() + σ('&') + σ('&') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('<') + σ('=') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
identifier() + σ('*') + σ('=') + integerLiteral() + σ(';') + η() +
identifier() + σ('+') + σ('=') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('-') + characterLiteral() + σ(';') + η() +
σ('+') + σ('+') + identifier() + σ(';') + η() +
σ('}') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('}') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('=') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
σ('+') + σ('+') + identifier() + σ(';') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('}') + η() +
σ('else') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('=') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
σ('+') + σ('+') + identifier() + σ(';') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('}') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('=') + identifier() + σ(')') + η() +
σ('+') + σ('+') + identifier() + σ(';') + η() +
σ('else') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('=') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
σ('+') + σ('+') + identifier() + σ(';') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
σ('}') + η() +
σ('else') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('=') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
σ('+') + σ('+') + identifier() + σ(';') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
σ('}') + η() +
σ('else') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
cStyleComment() + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
cStyleComment() + η() +
σ('-') + σ('-') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('default') + σ(':') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('#') + σ('if') + identifier() + σ('!') + σ('=') + integerLiteral() + η() +
σ('-') + σ('-') + identifier() + σ(';') + η() +
σ('#') + identifier() + η() +
σ('break') + σ(';') + η() +
σ('}') + η() +
η() +
identifier() + σ('-') + σ('>') + identifier() + σ('=') + identifier() + σ(';') + η() +
η() +
identifier() + identifier() + σ(';') + η() +
σ('}') + η() +
η() +
η() +
identifier() + identifier() + η() +
identifier() + σ('(') + σ('struct') + identifier() + σ('*') + identifier() + σ(',') + identifier() + identifier() + σ('*') + identifier() + σ(')') + η() +
σ('{') + η() +
cStyleComment() + η() +
σ('}') + η() +