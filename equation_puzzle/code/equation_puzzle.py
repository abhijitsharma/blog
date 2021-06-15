from lark import Lark, Tree
from itertools import product
from math import sqrt, factorial


def load_grammar():
    with open("equation_puzzle.lark", "r") as f:
        return f.read()


class Expression:
    VAR, PLUS, MINUS, MULT, DIV, SQRT, FACT, CUBEROOT, NOOP, NUMBER \
        = 'var', 'add', 'sub', 'mul', 'div', 'sqrt', 'fact', 'cuberoot', 'noop', 'number'
    ops = {VAR: 'var', PLUS: '+', MINUS: '-', MULT: '*', DIV: '/', SQRT: '√', FACT: '!', NOOP: '@', CUBEROOT: '∛'}

    def __init__(self, op, *args):
        """Op is a string and args are child Expression's or literal Strings (for a var)"""
        self.op = op
        self.args = args

    def is_unary(self):
        return len(self.args) == 1

    def _is_atom(self, types):
        return self.op in types

    def is_atom(self):
        return self._is_atom({Expression.VAR, Expression.NUMBER})

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
    assert len(tree.children) <= 2

    count = len(tree.children)

    left, right = None, None
    for i in range(count):
        n = tree.children[i]
        if isinstance(n, Tree):
            if i == 0:
                left = to_expression(n)
            elif i == 1:
                right = to_expression(n)
        else:
            return Expression(tree.data, n.value)

    if right is None and left is not None:
        return Expression(tree.data, left)
    elif count == 0 and (tree.data == 'true' or tree.data == 'false'):
        val = tree.data == 'true'
        # TODO remove condition
        return Expression(Expression.TRUEVAL, val)
    else:
        return Expression(tree.data, left, right)


def expr_eval(expression):
    if expression.is_atom():
        if expression.op == Expression.NUMBER:
            return int(expression.args[0])
    elif expression.is_unary():
        if expression.op == Expression.SQRT:
            return sqrt(expr_eval(expression.args[0]))
        elif expression.op == Expression.FACT:
            i = expr_eval(expression.args[0])
            # TODO limited factorial and improve
            if isinstance(i, int) and i < 10:
                return factorial(i)
            elif isinstance(i, float) and i.is_integer() and i < 10:
                return factorial(i)
        elif expression.op == Expression.CUBEROOT:
            i = expr_eval(expression.args[0])
            return i ** (1. / 3.)
        elif expression.op == Expression.NOOP:
            return expr_eval(expression.args[0])
    else:
        if expression.op == Expression.PLUS:
            return expr_eval(expression.args[0]) + expr_eval(expression.args[1])
        elif expression.op == Expression.MINUS:
            return expr_eval(expression.args[0]) - expr_eval(expression.args[1])
        elif expression.op == Expression.MULT:
            return expr_eval(expression.args[0]) * expr_eval(expression.args[1])
        elif expression.op == Expression.DIV:
            return expr_eval(expression.args[0]) / expr_eval(expression.args[1])


grammar = load_grammar()
prop_logic_parser = Lark(grammar, parser='lalr')
to_logic_tree = prop_logic_parser.parse


def test_permutation(numbers, exp_result):
    # h-0 (h-1(h-2 v-0 s-0 h-3 v-1) s-1 h-4 v-2)
    # √(√(√2 + √2) + √2)
    s_expr_fmt_l_tree = '{}({}({}{} {} {}{}) {} {}{})'

    # h-0 (h-1 v-0 s-0 h-2 (h-3 v-1 s-1 h-4 v-2))
    # √(√2 + √(√2 + √2))
    s_expr_fmt_r_tree = '{}({}{} {} {}({}{} {} {}{}))'
    bin_ops = ['+', '-', '*', '/']
    binary_p = list(product(bin_ops, repeat=2))
    unary_ops = ['√', '!', '@', '∛']
    unary_p = list(product(unary_ops, repeat=5))
    n = 0
    for u in unary_p:
        for b in binary_p:
            s = s_expr_fmt_r_tree.format(u[0], u[1], numbers[0], b[0], u[2], u[3], numbers[1], b[1], u[4], numbers[2])
            check_expr(s, exp_result)
            s = s_expr_fmt_l_tree.format(u[0], u[1], u[2], numbers[0], b[0], u[3], numbers[1], b[1], u[4], numbers[2])
            check_expr(s, exp_result)
            n = n + 1
    print(f'# of permutations {n * 2}')


def check_expr(s, exp_result):
    expression = parse(s)
    try:
        result = expr_eval(expression)
        # Clean the expression (remove noop)
        s_s = s.replace(expression.ops[Expression.NOOP], "")
        if result == exp_result:
            print(f'{s_s} = {result}')
    except:
        pass


def print_list(p):
    n = 0
    for j in list(p):
        print(j)
        n = n + 1
    print(f'# of permutations {n}')


def parse(s):
    return to_expression(to_logic_tree(s))


def test_parse():
    expression = parse("@(4 + √4)")
    result = expr_eval(expression)
    print(result)

    expression = parse("∛9")
    result = expr_eval(expression)
    print(result)

    expression = parse("!((!1 + !1)  + !1)")
    result = expr_eval(expression)
    print(result)


if __name__ == '__main__':
    # test_parse()
    test_permutation([1, 1, 1], 6)
    test_permutation([2, 2, 2], 6)
    test_permutation([3, 3, 3], 6)
    test_permutation([4, 4, 4], 6)
    test_permutation([5, 5, 5], 6)
    test_permutation([6, 6, 6], 6)
    test_permutation([7, 7, 7], 6)
    test_permutation([8, 8, 8], 6)
    test_permutation([9, 9, 9], 6)
