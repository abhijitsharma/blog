from lark import Lark, Tree, Token


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

    @property
    def _to_str(self):
        l = ['(']
        # TODO assert self.args <= 2
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
        l += [')']
        return l

    def to_str(self):
        """Returns a string representation of the Expression."""
        return ''.join(self._to_str)

    def is_unary(self):
        return len(self.args) == 1


def to_expression(tree: Tree) -> Expression:
    assert isinstance(tree, Tree)

    #    print(f'in _transform {tree} children {len(tree.children)}')
    # TODO assert tree.children <= 2
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
    return expression


def _to_cnf(expression: Expression, func) -> Expression:
    assert isinstance(expression, Expression)
    # print(f'in to_cnf {expression.to_str()}')
    expression = func(expression)

    left, right = None, None
    for i in range(len(expression.args)):
        n = expression.args[i]
        if isinstance(n, Expression):
            if i == 0:
                left = to_cnf(n)
                # print(f'left {left.to_str()}')
            elif i == 1:
                right = to_cnf(n)
                # print(f'right {right.to_str()}')
        else:
            return Expression(expression.op, n)

    if right is None:
        return Expression(expression.op, left)
    else:
        return Expression(expression.op, left, right)


def eliminate_implication(expression):
    assert isinstance(expression, Expression)
    if expression.op == Expression.IMPLICATION:
        return Expression(Expression.OR, Expression(Expression.NEG, expression.args[0]), expression.args[1])
    return expression


def push_negation_inwards(expression):
    assert isinstance(expression, Expression)
    # print(f'in push_negation {expression.to_str()}')
    if expression.op == Expression.NEG:
        child = expression.args[0]
        # print(f'in push_negation:child {child.to_str()}')
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
    _test("a")
    _test("~a")
    _test("a -> b")
    _test("a -> b -> c")
    _test("a -> b")
    _test("~(~a)")
    _test("~(a -> b)")
    _test("~(a | ~b | (c -> d))")


def _test(s):
    expression = to_expression(to_logic_tree(s))
    cnf_expression = to_cnf(expression)
    print(">>>>>>>")
    print(f's: "{s}" \nexp: "{expression.to_str()}" \ncnf: "{cnf_expression.to_str()}"')
    print(">>>>>>>")

# TODO fix T, F
# print(prop_logic_tree("a & b | T").pretty())


if __name__ == '__main__':
    test()
    # main()
