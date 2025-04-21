import sys
from utils import *
from tokens import *
from lexer import *
from parser import *
from interpreter import *

VERBOSE = False

if __name__ == '__main__':
  if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 pinky.py <filename>')
  filename = sys.argv[1]

  with open(filename) as file:
    source = file.read()
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    if VERBOSE:
      print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
      print(f'{Colors.GREEN}SOURCE:{Colors.WHITE}')
      print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
      print(source)

      print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
      print(f'{Colors.GREEN}TOKENS:{Colors.WHITE}')
      print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
      for tok in tokens: print(tok)

      print()
      print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
      print(f'{Colors.GREEN}AST:{Colors.WHITE}')
      print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
      print_pretty_ast(ast)

      print()
      print(f'{Colors.GREEN}***************************************{Colors.WHITE}')
      print(f'{Colors.GREEN}INTERPRETER:{Colors.WHITE}')
      print(f'{Colors.GREEN}***************************************{Colors.WHITE}')

    interpreter = Interpreter()
    interpreter.interpret_ast(ast)
