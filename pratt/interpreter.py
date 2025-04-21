from defs import *
from utils import *
from model import *
from tokens import *
import codecs

class Interpreter:
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
        else:
          runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      elif node.op.token_type == TOK_MINUS:
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
          return (TYPE_NUMBER, leftval - rightval)
        else:
          runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      elif node.op.token_type == TOK_STAR:
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
          return (TYPE_NUMBER, leftval * rightval)
        else:
          runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      elif node.op.token_type == TOK_SLASH:
        if rightval == 0:
          runtime_error(f'Division by zero.', node.line)
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
          return (TYPE_NUMBER, leftval / rightval)
        else:
          runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      elif node.op.token_type == TOK_CARET:
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
          return (TYPE_NUMBER, leftval ** rightval)
        else:
          runtime_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

    elif isinstance(node, UnOp):
      operandtype, operandval = self.interpret(node.operand)
      if node.op.token_type == TOK_MINUS:
        if operandtype == TYPE_NUMBER:
          return (TYPE_NUMBER, -operandval)
        else:
          runtime_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)

      if node.op.token_type == TOK_PLUS:
        if operandtype == TYPE_NUMBER:
          return (TYPE_NUMBER, operandval)
        else:
          runtime_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)
