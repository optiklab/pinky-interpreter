from model import *
from tokens import *

class Interpreter:
  def __init__(self):
    pass

  def interpret(self, node):
    if isinstance(node, Integer):
      return float(node.value)

    elif isinstance(node, Float):
      return float(node.value)

    elif isinstance(node, Grouping):
      return self.interpret(node.value)

    elif isinstance(node, BinOp):
      leftval  = self.interpret(node.left)
      rightval = self.interpret(node.right)
      if node.op.token_type == TOK_PLUS:
        return leftval + rightval
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
