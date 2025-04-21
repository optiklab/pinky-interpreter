from model import *
from tokens import *
from utils import *

###############################################################################
# Constants for different runtime value types
###############################################################################
TYPE_NUMBER = 'TYPE_NUMBER'  # Default to 64-bit float
TYPE_STRING = 'TYPE_STRING'  # String managed by the host language
TYPE_BOOL   = 'TYPE_BOOL'    # true | false

class Compiler:
  def __init__(self):
    self.code = []

  def emit(self, instruction):
    self.code.append(instruction)

  def compile(self, node):
    if isinstance(node, Integer):
      value = (TYPE_NUMBER, float(node.value))
      self.emit(('PUSH', value))

    if isinstance(node, Float):
      value = (TYPE_NUMBER, float(node.value))
      self.emit(('PUSH', value))

    #TODO: emit instructions for booleans and strings...

    if isinstance(node, BinOp):
      self.compile(node.left)
      self.compile(node.right)
      if node.op.token_type == TOK_PLUS:
        self.emit(('ADD',))
      if node.op.token_type == TOK_MINUS:
        self.emit(('SUB',))
      #TODO: *, /, ^, %, etc.

    if isinstance(node, PrintStmt):
      self.compile(node.value)
      if node.end == '':
        self.emit(('PRINT',))
      else:
        self.emit(('PRINTLN',))

    if isinstance(node, Stmts):
      for stmt in node.stmts:
        self.compile(stmt)

  def compile_code(self, node):
    #TODO: Create the global parent environment
    self.compile(node)
    return self.code
