from lark import Lark, Tree, Token


def load_grammar():
    with open("prop_logic.lark", "r") as f:
        return f.read()


class Expression:
    ops = {'implication': '->', 'iff': '<->', 'neg': '~', 'and': '&', 'or': '|'}

    def __init__(self, op, *args):
        "Op is a string and args are Expressions"
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
        """Returns an indented string representation of the tree.
        """
        return ''.join(self._to_str)

    def is_unary(self):
        return len(self.args) == 1


def to_expression(tree: Tree) -> Expression:
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
    print(to_expression(to_logic_tree("a -> b")).to_str())
    print(to_expression(to_logic_tree("~(a -> b)")).to_str())
    print(to_expression(to_logic_tree("~a")).to_str())
    print(to_expression(to_logic_tree("a -> b -> c")).to_str())
    print(to_expression(to_logic_tree("~(a | ~b | (c -> d))")).to_str())


# TODO fix T, F
# print(prop_logic_tree("a & b | T").pretty())


if __name__ == '__main__':
    test()
    # main()
