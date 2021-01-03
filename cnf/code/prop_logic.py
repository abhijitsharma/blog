from lark import Lark

l = Lark('''
?start: iff

?iff: implication
    | iff "<->" implication -> iff

?implication: or
    | implication "->" or -> implication

?or: and
    | or "v" and -> or

?and: negation
    | and "^" negation -> and
    
?negation: "~" expression -> neg
    | expression 

?expression: "(" iff ")" 
    | NAME -> var

%import common.CNAME -> NAME
%import common.WS_INLINE
%ignore WS_INLINE
''')

print(l.parse("a ^ b"))
