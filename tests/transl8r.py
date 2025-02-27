class token(object):
    def __init__(self, name, expr, patr):
        self.name = name
        self.expr = expr
        self.patr = patr
        self.seen = dict()

