from lark import Lark, Tree


def load_grammar():
    with open("prop_logic.lark", "r") as f:
        return f.read()


class Expression:
    IMPLICATION, IFF, NEG, AND, OR, VAR = 'implication', 'iff', 'neg', 'and', 'or', 'var'
    ops = {IMPLICATION: '->', IFF: '<->', NEG: '~', AND: '&', OR: '|', VAR: 'var'}

    def __init__(self, op, *args):
        """Op is a string and args are Expression's or literal Strings (var)"""
        self.op = op
        self.args = args

    def is_unary(self):
        return len(self.args) == 1

    @property
    def _to_str(self):
        l = []
        if not self.is_unary():
            l += ['(']
        assert len(self.args) <= 2
        for i in range(len(self.args)):
            e = self.args[i]
            if isinstance(e, Expression):
                if i == 0:
                    if self.is_unary():
                        l += [self.ops[self.op]]
                        l += e._to_str
                    else:
                        l += e._to_str
                        l += [' ', self.ops[self.op], ' ']
                elif i == 1:
                    l += e._to_str
            else:
                l += ['%s' % (e,)]
        if not self.is_unary():
            l += [')']
        return l

    def to_str(self):
        """Returns a string representation of the Expression."""
        return ''.join(self._to_str)


def to_expression(tree: Tree) -> Expression:
    assert isinstance(tree, Tree)

    #    print(f'in _transform {tree} children {len(tree.children)}')
    assert len(tree.children) <= 2
    left, right = None, None
    for i in range(len(tree.children)):
        n = tree.children[i]
        #        print(f'type {type(n)}')
        if isinstance(n, Tree):
            if i == 0:
                left = to_expression(n)
            elif i == 1:
                right = to_expression(n)
        else:
            return Expression(tree.data, n.value)

    if right is None:
        return Expression(tree.data, left)
    else:
        return Expression(tree.data, left, right)


def to_cnf(expression: Expression) -> Expression:
    assert isinstance(expression, Expression)
    expression = _to_cnf(expression, eliminate_implication)
    expression = _to_cnf(expression, push_negation_inwards)
    expression = _to_cnf(expression, distribute_and_over_or)
    return expression


def _to_cnf(expression: Expression, func) -> Expression:
    assert isinstance(expression, Expression)
    assert func is not None

    expression = func(expression)

    left, right = None, None
    for i in range(len(expression.args)):
        n = expression.args[i]
        if isinstance(n, Expression):
            if i == 0:
                left = _to_cnf(n, func)
            elif i == 1:
                right = _to_cnf(n, func)
        else:
            return Expression(expression.op, n)

    if right is None:
        return func(Expression(expression.op, left))
    else:
        return func(Expression(expression.op, left, right))


def eliminate_implication(expression):
    assert isinstance(expression, Expression)
    if expression.op == Expression.IMPLICATION:
        return Expression(Expression.OR,
                          Expression(Expression.NEG, expression.args[0]), expression.args[1])
    elif expression.op == Expression.IFF:
        return Expression(Expression.OR,
                          Expression(Expression.OR,
                                     Expression(Expression.NEG, expression.args[0]), expression.args[1]),
                          Expression(Expression.OR,
                                     Expression(Expression.NEG, expression.args[1]), expression.args[0]))
    return expression


def push_negation_inwards(expression):
    assert isinstance(expression, Expression)
    if expression.op == Expression.NEG:
        # print(f'in push_negation {expression.to_str()}')
        child = expression.args[0]
        if isinstance(child, Expression):
            if child.op == Expression.OR:
                return Expression(Expression.AND,
                                  Expression(Expression.NEG, child.args[0]),
                                  Expression(Expression.NEG, child.args[1]))
            elif child.op == Expression.AND:
                return Expression(Expression.OR,
                                  Expression(Expression.NEG, child.args[0]),
                                  Expression(Expression.NEG, child.args[1]))
            elif child.op == Expression.NEG:
                return child.args[0]
    # print(f'in push_negation returning {expression.to_str()}')
    return expression


def distribute_and_over_or(expression):
    assert isinstance(expression, Expression)
    # print(f'in distribute_and_over_or {expression.to_str()}')
    if expression.op == Expression.OR:
        left = expression.args[0]
        right = expression.args[1]
        # (a & b) | (c & d) = (a | c) & (a | d) & (b | c) & (b | d)
        # print(f'in distribute_and_over_or left {left.to_str()} right {right.to_str()}')
        if left.op == Expression.AND and right.op == Expression.AND:
            l0, l1, r0, r1 = left.args[0], left.args[1], right.args[0], right.args[1]
            return Expression(Expression.AND,
                              Expression(Expression.AND,
                                         distribute_and_over_or(Expression(Expression.OR, l0, r0)),
                                         distribute_and_over_or(Expression(Expression.OR, l0, r1))),
                              Expression(Expression.AND,
                                         distribute_and_over_or(Expression(Expression.OR, l1, r0)),
                                         distribute_and_over_or(Expression(Expression.OR, l1, r1))))
        # (a = Exp other than AND) | (b & c) = (a | b) & (a | c)
        elif right.op == Expression.AND:
            # print(f'in distribute_and_over_or right.op = AND {right.to_str()}')
            r0, r1 = right.args[0], right.args[1]
            return Expression(Expression.AND,
                              distribute_and_over_or(Expression(Expression.OR, left, r0)),
                              distribute_and_over_or(Expression(Expression.OR, left, r1)))
        elif left.op == Expression.AND:
            # print(f'in distribute_and_over_or left.op = AND {left.to_str()}')
            l0, l1 = left.args[0], left.args[1]
            return Expression(Expression.AND,
                              distribute_and_over_or(Expression(Expression.OR, l0, right)),
                              distribute_and_over_or(Expression(Expression.OR, l1, right)))
    return expression


grammar = load_grammar()
prop_logic_parser = Lark(grammar, parser='lalr')
to_logic_tree = prop_logic_parser.parse


def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(to_logic_tree(s))


def test():
    _test("a", "a")
    _test("~a", "~a")
    _test("a -> b", "(~a | b)")
    _test("a <-> b", "((~a | b) | (~b | a))")
    _test("a -> b -> c", "((a | c) & (~b | c))")
    _test("~(~a)", "a")
    _test("~(~(~a))", "~a")
    _test("~(c | d)", "(~c & ~d)")
    _test("~(~c | ~d)", "(c & d)")
    _test("~(b | ~(c | d))", "(~b & (c | d))")
    _test("~(a | ~(b | ~(c | d)))", "(~a & ((b | ~c) & (b | ~d)))")
    _test("~(a -> ~(b -> ~(c -> d)))", "(a & ((~b | c) & (~b | ~d)))")
    _test("~(a -> b)", "(a & ~b)")
    _test("~(a | ~b | (c -> d))", "((~a & b) & (c & ~d))")
    _test("(a & b) | (c & d)", "(((a | c) & (a | d)) & ((b | c) & (b | d)))")
    _test("a | (c & d)", "((a | c) & (a | d))")
    _test("(c & d) | a", "((c | a) & (d | a))")
    _test("(a | b) | (c & d)", "(((a | b) | c) & ((a | b) | d))")
    _test("((a | b) & (a | c)) | (d & e)",
          "((((a | b) | d) & ((a | b) | e)) & (((a | c) | d) & ((a | c) | e)))")
    _test("((a & b) | (c & (d | g)))", "(((a | c) & (a | (d | g))) & ((b | c) & (b | (d | g))))")
    _test("(c & ((d & e) | g))", "(c & ((d | g) & (e | g)))")
    _test("a | (c & (d & e))", "((a | c) & ((a | d) & (a | e)))")
    _test("a | (c & (d | g))", "((a | c) & (a | (d | g)))")
    _test("(c & ((d & e) | g))", "(c & ((d | g) & (e | g)))")
    _test("((a & b) | (c & ((d & e) & g)))",
          "(((a | c) & (((a | d) & (a | e)) & (a | g))) & ((b | c) & (((b | d) & (b | e)) & (b | g))))")
    _test("a | (((d & e) | g))", "((a | (d | g)) & (a | (e | g)))")
    _test("a | (c & ((d & e) | g))", "((a | c) & ((a | (d | g)) & (a | (e | g))))")
    _test("((a & b) | (c & ((d & e) | g)))",
          "(((a | c) & ((a | (d | g)) & (a | (e | g)))) & ((b | c) & ((b | (d | g)) & (b | (e | g)))))")
    _test("((a & b) | (c & (d & e)))",
          "(((a | c) & ((a | d) & (a | e))) & ((b | c) & ((b | d) & (b | e))))")
    _test("((a & b) | (c & (d | g)))",
          "(((a | c) & (a | (d | g))) & ((b | c) & (b | (d | g))))")
    _test("((a & b) | (c -> (d | g)))",
          "((a | (~c | (d | g))) & (b | (~c | (d | g))))")
    _test("(a | (d | (e & g)))", "((a | (d | e)) & (a | (d | g)))")
    _test("(a | (((d | h) & (d | g)) & ((e | h) & (e | g))))",
          "(((a | (d | h)) & (a | (d | g))) & ((a | (e | h)) & (a | (e | g))))")
    _test("(a | ((d & e) | (h & g)))",
          "(((a | (d | h)) & (a | (d | g))) & ((a | (e | h)) & (a | (e | g))))")
    _test("~(a | ~((d & e) | ~(h & g)))",
          "(~a & ((d | (~h | ~g)) & (e | (~h | ~g))))")
    _test("((a & b) | ((d & e) | (h & g)))",
          "((((a | (d | h)) & (a | (d | g))) & ((a | (e | h)) & (a | (e | g)))) & (((b | (d | h)) & (b | (d | g))) & ((b | (e | h)) & (b | (e | g)))))")
    _test("((a & b) | (c & ((d & e) | (h & g))))",
          "(((a | c) & (((a | (d | h)) & (a | (d | g))) & ((a | (e | h)) & (a | (e | g))))) & ((b | c) & (((b | (d | h)) & (b | (d | g))) & ((b | (e | h)) & (b | (e | g))))))")
    _test("((((a & b) | (c & d)) & e) | (((n & g) | (h & i)) & ((j & k) | (l & m))))",
          "((((((((a | c) | (n | h)) & ((a | c) | (n | i))) & (((a | d) | (n | h)) & ((a | d) | (n | i)))) & ((((a | c) | (g | h)) & ((a | c) | (g | i))) & (((a | d) | (g | h)) & ((a | d) | (g | i))))) & (((((b | c) | (n | h)) & ((b | c) | (n | i))) & (((b | d) | (n | h)) & ((b | d) | (n | i)))) & ((((b | c) | (g | h)) & ((b | c) | (g | i))) & (((b | d) | (g | h)) & ((b | d) | (g | i)))))) & ((((((a | c) | (j | l)) & ((a | c) | (j | m))) & (((a | d) | (j | l)) & ((a | d) | (j | m)))) & ((((a | c) | (k | l)) & ((a | c) | (k | m))) & (((a | d) | (k | l)) & ((a | d) | (k | m))))) & (((((b | c) | (j | l)) & ((b | c) | (j | m))) & (((b | d) | (j | l)) & ((b | d) | (j | m)))) & ((((b | c) | (k | l)) & ((b | c) | (k | m))) & (((b | d) | (k | l)) & ((b | d) | (k | m))))))) & ((((e | (n | h)) & (e | (n | i))) & ((e | (g | h)) & (e | (g | i)))) & (((e | (j | l)) & (e | (j | m))) & ((e | (k | l)) & (e | (k | m))))))")


def _test(s, e):
    expression = to_expression(to_logic_tree(s))
    cnf_expression = to_cnf(expression)
    print(">>>>>>>")
    _s = cnf_expression.to_str()
    print(f's: "{s}" \ncnf: "{_s}" \nexpected "{e}"')
    print(">>>>>>>")
    assert _s == e


# TODO fix T, F
# print(prop_logic_tree("a & b | T").pretty())


if __name__ == '__main__':
    test()
    # main()
