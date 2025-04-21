############################################################
#
# Thie file generates LLVM IR for a subset of the language.
#
# Limitations:
#
#  1. This uses Numba/llvmlite to generate LLVM IR code.
#
#  2. We do not implement functions. Our language does not
#     have type annotations, which makes it cumbersome to
#     figure out the function's return type before runtime.
#
#  3. We do not handle child scope blocks. All variables
#     are globals and are stored with the help of a simple
#     environment dictionary inside our LLVM module.
#
#  4. We only handle numbers and booleans. Strings are not
#     implemented in this LLVM module.
#
#  5. To compile correctly, you must include an external
#     .c file called helpers.c, which contains some print
#     functions to print numbers and booleans.
#
############################################################

import sys
from defs import *
from utils import *
from tokens import *
from lexer import *
from parser import *
from llvmlite import ir

############################################################
# Declare shorter aliases for common LLVM types
############################################################
void = ir.VoidType()
f64  = ir.DoubleType()
i32  = ir.IntType(32)
i8   = ir.IntType(8)
i1   = ir.IntType(1)

class LLVMModule:
  #TODO: This class contains some important information about our LLVM module
  #TODO: We can also include an "environment" to store variables and their content

  self.vars = {}

  def get_var(self, name):
    # TODO:
    pass

  def set_var(self, name, vartype, value):
    # TODO:
    pass


class LLVMGenerator:
  def generate():
    #TODO:
    pass
  def generate_main(self, node):
    #TODO: generate the main module (with the main function inside)
    generate(...recursively for all nodes of the AST)
    pass

############################################################
# Main function that invokes the LLVM IR Generator
############################################################
if __name__ == '__main__':
  if len(sys.argv) != 2:
    raise SystemExit('Usage: python3.11 llvm.py <filename>')
  filename = sys.argv[1]

  with open(filename) as file:
    source = file.read()
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    llvmgen = LLVMGenerator()
    mainll = llvmgen.generate_main(ast)

    with open('main.ll', 'w') as file:
      file.write(str(mainll.module))

    print(str(mainll.module))

    print("*** LLVM IR generated into main.ll ***")
