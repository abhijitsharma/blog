from lark import Lark, Transformer, v_args


def load_grammar():
    with open("prop_logic.lark", "r") as f:
        return f.read()


@v_args(inline=True)  # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    number = float

    def __init__(self):
        super().__init__()
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)


# prop_logic_parser = Lark(grammar, parser='lalr', transformer=CalculateTree())
grammar = load_grammar()
prop_logic_parser = Lark(grammar, parser='lalr')
prop_logic_tree = prop_logic_parser.parse


def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(prop_logic_tree(s))


def test():
    print(prop_logic_tree("a -> b"))

    # print(prop_logic_tree("a & b").pretty())
    # print(prop_logic_tree("~(a | ~b | (c -> d))").pretty())
    # print(prop_logic_tree("a & b | T").pretty())


if __name__ == '__main__':
    test()
    # main()
