yield from (
σ('#') + σ('if') + identifier() + identifier() + σ('&&') + σ('!') + identifier() + identifier() + σ('#') + identifier() + identifier() + σ('#') + identifier() + σ('#') + identifier() + identifier() + σ('#') + identifier() + σ('<') + identifier() + σ('.') + identifier() + σ('>') + σ('#') + identifier() + σ('#') + identifier() + σ('<') + identifier() + σ('.') + identifier() + σ('>') + σ('#') + identifier() + σ('<') + identifier() + σ('.') + identifier() + σ('>') + σ('#') + identifier() + σ('<') + identifier() + σ('.') + identifier() + σ('>') + σ('#') + identifier() + stringLiteral() + σ('#') + identifier() + identifier() + σ('#') + identifier() + identifier() + identifier() + σ('#') + identifier() + pct_block() + η() +
σ('%parse-param') + σ('{') + σ('struct') + identifier() + σ('*') + identifier() + σ('}') + η() +
σ('%lex-param') + σ('{') + σ('struct') + identifier() + σ('*') + identifier() + σ('}') + η() +
σ('%define') + identifier() + σ('.') + identifier() + identifier() + η() +
σ('%expect') + integerLiteral() + η() +
η() +
identifier() + identifier() + identifier() + identifier() + σ(';') + identifier() + identifier() + identifier() + σ(';') + σ('struct') + identifier() + σ('*') + identifier() + σ(';') + pct_union() + η() +
η() +
identifier() + identifier() + identifier() + σ('(') + identifier() + σ('*') + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + identifier() + σ(')') + σ(';') + identifier() + identifier() + identifier() + σ('(') + σ('struct') + identifier() + σ('*') + identifier() + σ(',') + identifier() + identifier() + σ('*') + identifier() + σ(')') + σ(';') + identifier() + σ('struct') + identifier() + σ('*') + identifier() + σ('(') + identifier() + identifier() + σ(',') + identifier() + identifier() + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + identifier() + σ('*') + identifier() + σ(')') + identifier() + identifier() + σ(';') + σ('struct') + identifier() + σ('*') + identifier() + σ(';') + σ('for') + σ('(') + identifier() + σ('=') + identifier() + σ('-') + integerLiteral() + σ(';') + identifier() + σ('>=') + integerLiteral() + σ(';') + identifier() + σ('--') + σ(')') + σ('if') + σ('(') + identifier() + σ('[') + identifier() + σ(']') + σ('==') + identifier() + σ(')') + σ('goto') + identifier() + σ(';') + identifier() + σ('=') + σ('(') + σ('struct') + identifier() + σ('*') + σ(')') + identifier() + σ('(') + identifier() + σ('(') + σ('*') + identifier() + σ(')') + σ(')') + σ(';') + σ('if') + σ('(') + identifier() + σ('!=') + identifier() + σ(')') + identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + σ('for') + σ('(') + identifier() + σ('=') + identifier() + σ('-') + integerLiteral() + σ(';') + identifier() + σ('>=') + integerLiteral() + σ(';') + identifier() + σ('--') + σ(')') + identifier() + σ('->') + identifier() + σ('.') + identifier() + σ('[') + identifier() + σ(']') + σ('=') + identifier() + σ('[') + identifier() + σ(']') + σ(';') + identifier() + identifier() + σ(';') + identifier() + σ(':') + σ('for') + σ('(') + identifier() + σ('=') + identifier() + σ('-') + integerLiteral() + σ(';') + identifier() + σ('>=') + integerLiteral() + σ(';') + identifier() + σ('--') + σ(')') + identifier() + σ('(') + identifier() + σ('[') + identifier() + σ(']') + σ(')') + σ(';') + identifier() + identifier() + σ(';') + identifier() + identifier() + σ('struct') + identifier() + σ('*') + identifier() + σ('(') + identifier() + identifier() + identifier() + σ(')') + identifier() + identifier() + σ('(') + integerLiteral() + σ(',') + identifier() + σ(',') + identifier() + σ(')') + σ(';') + identifier() + identifier() + σ('struct') + identifier() + σ('*') + identifier() + σ('(') + identifier() + identifier() + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + σ('right') + σ(')') + σ('struct') + identifier() + σ('*') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(';') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('right') + σ(';') + identifier() + identifier() + σ('(') + integerLiteral() + σ(',') + identifier() + σ(',') + identifier() + σ(')') + σ(';') + identifier() + σ('struct') + identifier() + σ('*') + identifier() + σ('(') + identifier() + identifier() + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + σ('left') + σ(',') + σ('struct') + identifier() + σ('*') + σ('right') + σ(')') + σ('struct') + identifier() + σ('*') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(';') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('left') + σ(';') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + σ('right') + σ(';') + identifier() + identifier() + σ('(') + integerLiteral() + σ(',') + identifier() + σ(',') + identifier() + σ(')') + σ(';') + identifier() + identifier() + σ('struct') + identifier() + σ('*') + identifier() + σ('(') + identifier() + identifier() + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + identifier() + σ(',') + σ('struct') + identifier() + σ('*') + identifier() + σ(')') + σ('struct') + identifier() + σ('*') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(';') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + identifier() + σ(';') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + identifier() + σ(';') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('=') + identifier() + σ(';') + identifier() + identifier() + σ('(') + integerLiteral() + σ(',') + identifier() + σ(',') + identifier() + σ(')') + σ(';') + pct_block() + η() +
η() +
σ('%') + σ('right') + characterLiteral() + σ('%') + σ('left') + characterLiteral() + σ('%') + σ('left') + characterLiteral() + σ('%') + σ('left') + identifier() + σ('%') + σ('left') + identifier() + σ('%') + σ('left') + identifier() + σ('%') + σ('left') + identifier() + σ('/') + σ('*') + σ('*') + σ('/') + σ('%') + σ('*') + σ('/') + η() +
σ('%right') + characterLiteral() + pct_token() + η() +
pct_token() + η() +
pct_type() + identifier() + η() +
η() +
σ('%%') + η() +
η() +
σ('start') + σ(':') + identifier() + η() +
σ('{') + η() +
σ('if') + σ('(') + ζ('$#') + σ('==') + identifier() + σ(')') + η() +
identifier() + σ(';') + η() +
identifier() + σ('->') + identifier() + σ('=') + ζ('$#') + σ(';') + η() +
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
σ('if') + σ('(') + σ('(') + σ('$$') + σ('=') + identifier() + σ('(') + identifier() + σ(')') + σ(')') + σ('!=') + identifier() + σ(')') + η() +
σ('$$') + σ('->') + identifier() + σ('.') + identifier() + σ('=') + ζ('$#') + σ(';') + η() +
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
σ('if') + σ('(') + identifier() + σ('==') + identifier() + σ(')') + η() +
identifier() + σ(';') + η() +
η() +
σ('switch') + σ('(') + identifier() + σ('->') + identifier() + σ(')') + η() +
σ('{') + η() +
σ('case') + integerLiteral() + σ(':') + η() +
identifier() + σ('(') + identifier() + σ('->') + identifier() + σ('.') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(')') + σ(';') + η() +
σ('case') + integerLiteral() + σ(':') + η() +
identifier() + σ('(') + identifier() + σ('->') + identifier() + σ('.') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(')') + σ(';') + η() +
σ('case') + integerLiteral() + σ(':') + η() +
identifier() + σ('(') + identifier() + σ('->') + identifier() + σ('.') + identifier() + σ('[') + integerLiteral() + σ(']') + σ(')') + σ(';') + η() +
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
identifier() + identifier() + σ('*') + identifier() + σ('=') + identifier() + σ('->') + identifier() + σ(';') + η() +
identifier() + identifier() + σ(';') + η() +
η() +
σ('while') + σ('(') + integerLiteral() + σ(')') + η() +
σ('{') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('==') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + identifier() + σ(';') + η() +
σ('}') + η() +
η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('!=') + characterLiteral() + σ('&&') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('!=') + characterLiteral() + σ(')') + η() +
σ('break') + σ(';') + η() +
η() +
σ('++') + identifier() + σ(';') + η() +
σ('}') + η() +
η() +
identifier() + σ('=') + σ('*') + identifier() + σ('++') + σ(';') + η() +
σ('switch') + σ('(') + identifier() + σ(')') + η() +
σ('{') + η() +
σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + σ('case') + characterLiteral() + σ(':') + η() +
σ('{') + η() +
identifier() + identifier() + identifier() + identifier() + σ('=') + identifier() + σ('-') + characterLiteral() + σ(';') + η() +
σ('while') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('>=') + characterLiteral() + σ('&&') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('<=') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
identifier() + σ('*=') + integerLiteral() + σ(';') + η() +
identifier() + σ('+=') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('-') + characterLiteral() + σ(';') + η() +
σ('++') + identifier() + σ(';') + η() +
σ('}') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('}') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('==') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
σ('++') + identifier() + σ(';') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('}') + η() +
σ('else') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('==') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
σ('++') + identifier() + σ(';') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('}') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('==') + identifier() + σ(')') + η() +
σ('++') + identifier() + σ(';') + η() +
σ('else') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('==') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
σ('++') + identifier() + σ(';') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
σ('}') + η() +
σ('else') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('if') + σ('(') + identifier() + σ('[') + integerLiteral() + σ(']') + σ('==') + characterLiteral() + σ(')') + η() +
σ('{') + η() +
σ('++') + identifier() + σ(';') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
σ('}') + η() +
σ('else') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('break') + σ(';') + η() +
η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('case') + characterLiteral() + σ(':') + η() +
σ('--') + identifier() + σ(';') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('break') + σ(';') + η() +
η() +
σ('default') + σ(':') + η() +
identifier() + σ('=') + identifier() + σ(';') + η() +
σ('#') + σ('if') + identifier() + σ('!=') + integerLiteral() + η() +
σ('--') + identifier() + σ(';') + η() +
σ('#') + identifier() + η() +
σ('break') + σ(';') + η() +
σ('}') + η() +
η() +
identifier() + σ('->') + identifier() + σ('=') + identifier() + σ(';') + η() +
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