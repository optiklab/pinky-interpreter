from utils import *
from tokens import *
from model import *

class Parser:
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
    self.curr = self.curr + 1 # If it is a match, we return True and also comsume that token
    return True

  # <primary>  ::=  <integer> | <float> | '(' <expr> ')'
  def primary(self):
    if self.match(TOK_INTEGER): return Integer(int(self.previous_token().lexeme), line=self.previous_token().line)
    if self.match(TOK_FLOAT): return Float(float(self.previous_token().lexeme), line=self.previous_token().line)
    if self.match(TOK_LPAREN):
      expr = self.expr()
      if (not self.match(TOK_RPAREN)):
        parse_error(f'Error: ")" expected.', self.previous_token().line)
      else:
        return Grouping(expr, line=self.previous_token().line)

  # <unary>  ::=  ('+'|'-'|'~') <unary>  |  <primary>
  def unary(self):
    if self.match(TOK_NOT) or self.match(TOK_MINUS) or self.match(TOK_PLUS):
      op = self.previous_token()
      operand = self.unary()
      return UnOp(op, operand, line=self.previous_token().line)
    return self.primary()

  # <multiplication>  ::=  <unary> ( ('*'|'/') <unary> )*
  def multiplication(self):
    expr = self.unary()
    while self.match(TOK_STAR) or self.match(TOK_SLASH):
      op = self.previous_token()
      right = self.unary()
      expr = BinOp(op, expr, right, self.previous_token().line)
    return expr

  # <addition>  ::=  <multiplication> ( ('+'|'-') <multiplication> )*
  def addition(self):
    expr = self.multiplication()
    while self.match(TOK_PLUS) or self.match(TOK_MINUS):
      op = self.previous_token()
      right = self.multiplication()
      expr = BinOp(op, expr, right, line=self.previous_token().line)
    return expr

  def expr(self):
    return self.addition()

  def parse(self):
    ast = self.expr()
    return ast
