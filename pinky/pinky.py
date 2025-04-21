import sys
from utils import *
from tokens import *
from lexer import *
from parser import *

if __name__ == '__main__':
  if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 pinky.py <filename>')
  filename = sys.argv[1]

  with open(filename) as file:
    source = file.read()

    print(f'***************************************')
    print(f'SOURCE:')
    print(f'***************************************')
    print(source)

    print(f'***************************************')
    print(f'LEXER:')
    print(f'***************************************')
    tokens = Lexer(source).tokenize()
    for tok in tokens: print(tok)

    print()
    print(f'***************************************')
    print(f'PARSED AST:')
    print(f'***************************************')
    ast = Parser(tokens).parse()
    print_pretty_ast(ast)
