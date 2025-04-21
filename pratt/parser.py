from utils import *
from tokens import *
from model import *

bp = {
  '*': 2,
  '/': 2,
  '+': 1,
  '-': 1,
}

class PrattParser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.curr = 0

  def advance(self):
    token = self.tokens[self.curr]
    self.curr = self.curr + 1
    return token

  def peek(self):
    return self.tokens[self.curr]

  def is_next(self, expected_type):
    if self.curr >= len(self.tokens):
      return False
    return self.peek().token_type == expected_type

  def expect(self, expected_type):
    if self.curr >= len(self.tokens):
      parse_error(f'Found {self.previous_token().lexeme!r} at the end of parsing', self.previous_token().line)
    elif self.peek().token_type == expected_type:
      token = self.advance()
      return token
    else:
      parse_error(f'Expected {expected_type!r}, found {self.peek().lexeme!r}.', self.peek().line)

  def previous_token(self):
    return self.tokens[self.curr - 1]

  def match(self, expected_type):
    if self.curr >= len(self.tokens):
      return False
    if self.peek().token_type != expected_type:
      return False
    self.curr = self.curr + 1
    return True

  def nud(self):
    if self.match(TOK_INTEGER):
      return Integer(int(self.previous_token().lexeme), line=self.previous_token().line)
    if self.match(TOK_FLOAT):
      return Float(float(self.previous_token().lexeme), line=self.previous_token().line)

  def led(self, left):
    if self.match(TOK_PLUS) or self.match(TOK_MINUS) or self.match(TOK_STAR) or self.match(TOK_SLASH):
      op = self.previous_token()
      right = self.expr()
      return BinOp(op, left, right, line=op.line)

  def expr(self, rbp=0):
    left = self.nud()
    while self.curr < len(self.tokens):
      left = self.led(left)
    return left

  def parse(self):
    ast = self.expr(rbp=0)
    return ast
