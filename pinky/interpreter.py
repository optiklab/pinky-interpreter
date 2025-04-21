from utils import *
from model import *
from tokens import *

###############################################################################
# Constants for different runtime value types
###############################################################################
TYPE_NUMBER = 'TYPE_NUMBER'  # Default to 64-bit float
TYPE_STRING = 'TYPE_STRING'  # String managed by the host language
TYPE_BOOL   = 'TYPE_BOOL'    # true | false

class Interpreter:
  def __init__(self):
    pass

  def interpret(self, node):
    if isinstance(node, Integer):
      return (TYPE_NUMBER, float(node.value))

    elif isinstance(node, Float):
      return (TYPE_NUMBER, float(node.value))

    elif isinstance(node, Grouping):
      return self.interpret(node.value)

    elif isinstance(node, BinOp):
      lefttype, leftval  = self.interpret(node.left)
      righttype, rightval = self.interpret(node.right)
      if node.op.token_type == TOK_PLUS:
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
          return (TYPE_NUMBER, leftval + rightval)
        elif lefttype == TYPE_STRING or righttype == TYPE_STRING:
          return (TYPE_STRING, str(leftval) + str(rightval))
        else:
          runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      #################################################
      # TODO:
      # Complete the type checks for binops and unops
      #################################################

      elif node.op.token_type == TOK_MINUS:
        return leftval - rightval
      elif node.op.token_type == TOK_STAR:
        return leftval * rightval
      elif node.op.token_type == TOK_SLASH:
        return leftval / rightval

    elif isinstance(node, UnOp):
      operand = self.interpret(node.operand)
      if node.op.token_type == TOK_PLUS:
        return +operand
      elif node.op.token_type == TOK_MINUS:
        return -operand
      #if node.op.token_type == TOK_NOT:
      #  return not operand
