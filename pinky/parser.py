from tokens import *
from model import *

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.curr = 0

  def advance(self):
    #TODO: consume the current token and advance to the next one
    pass

  def peek(self):
    #TODO: return the current token
    pass

  def is_next(self, expected_type):
    #TODO: check if the next token matches the expected type
    pass

  def expect(self, expected_type):
    #TODO: test if the current token is of the expected type, otherwise show error message
    pass

  def match(self, expected_type):
    #TODO: check if current token matches the expected type and return the token, otherwise returns False
    pass

  def previous_token(self):
    #TODO: return the previous token
    pass

  # <primary>  ::=  <integer> | <float> | '(' <expr> ')'
  def primary(self):
    if self.match(TOK_INTEGER): return Integer(int(self.previous_token().lexeme))
    if self.match(TOK_FLOAT): return Float(float(self.previous_token().lexeme))
    if self.match(TOK_LPAREN):
      expr = self.expr()
      if (not self.match(TOK_RPAREN)):
        raise SyntaxError(f'Error: ")" expected.')
      else:
        return Grouping(expr)

  # <unary>  ::=  ('+'|'-'|'~') <unary>  |  <primary>
  def unary(self):
    if self.match(TOK_NOT) or self.match(TOK_MINUS) or self.match(TOK_PLUS):
      op = self.previous_token()
      operand = self.unary()
      return UnOp(op, operand)
    return self.primary()

  # <factor>  ::=  <unary>
  def factor(self):
    return self.unary()

  # <term>  ::=  <factor> ( ('*'|'/') <factor> )*
  def term(self):
    expr = self.factor()
    while self.match(TOK_STAR) or self.match(TOK_SLASH):
      op = self.previous_token()
      right = self.factor()
      expr = BinOp(op, expr, right)
    return expr

  # <expr>  ::=  <term> ( ('+'|'-') <term> )*
  def expr(self):
    expr = self.term()
    while self.match(TOK_PLUS) or self.match(TOK_MINUS):
      op = self.previous_token()
      right = self.term()
      expr = BinOp(op, expr, right)
    return expr

  def parse(self):
    ast = self.expr()
    return ast
