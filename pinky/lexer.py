from tokens import *

class Lexer:
  def __init__(self, source):
    self.source = source
    self.start = 0
    self.curr = 0
    self.line = 1
    self.tokens = []

  def advance(self):
    ch = self.source[self.curr]
    self.curr = self.curr + 1
    return ch

  def peek(self):
    return self.source[self.curr]

  def lookahead(self, n=1):
    if self.curr >= len(self.source):
      return '\0'
    return self.source[self.curr + n]

  def match(self, expected):
    if self.curr >= len(self.source):
      return False
    if self.source[self.curr] != expected:
      return False
    self.curr = self.curr + 1 # If it is a match, we also consume that char
    return True

  def handle_number(self):
    while self.peek().isdigit():
      self.advance()
    if self.peek() == '.' and self.lookahead().isdigit():
      self.advance() # consume the '.'
      while self.peek().isdigit():
        self.advance()
      self.add_token(TOK_FLOAT)
    else:
      self.add_token(TOK_INTEGER)

  def add_token(self, token_type):
    self.tokens.append(Token(token_type, self.source[self.start:self.curr], self.line))

  def tokenize(self):
    while self.curr < len(self.source):
      self.start = self.curr
      ch = self.advance()
      if ch == '\n': self.line = self.line + 1
      elif ch == ' ': pass
      elif ch == '\t': pass
      elif ch == '\r': pass
      elif ch == '#':
        while self.peek() != '\n' and not(self.curr >= len(self.source)):
          self.advance()
      elif ch == '(': self.add_token(TOK_LPAREN)
      elif ch == ')': self.add_token(TOK_RPAREN)
      elif ch == '{': self.add_token(TOK_LCURLY)
      elif ch == '}': self.add_token(TOK_RCURLY)
      elif ch == '[': self.add_token(TOK_LSQUAR)
      elif ch == ']': self.add_token(TOK_RSQUAR)
      elif ch == '.': self.add_token(TOK_DOT)
      elif ch == ',': self.add_token(TOK_COMMA)
      elif ch == '+': self.add_token(TOK_PLUS)
      elif ch == '-': self.add_token(TOK_MINUS)
      elif ch == '*': self.add_token(TOK_STAR)
      elif ch == '^': self.add_token(TOK_CARET)
      elif ch == '/': self.add_token(TOK_SLASH)
      elif ch == ';': self.add_token(TOK_SEMICOLON)
      elif ch == '?': self.add_token(TOK_QUESTION)
      elif ch == '%': self.add_token(TOK_MOD)
      elif ch == '=':
        if self.match('='):
          self.add_token(TOK_EQ)
      elif ch == '~':
        self.add_token(TOK_NE if self.match('=') else TOK_NOT)
      elif ch == '<':
        self.add_token(TOK_LE if self.match('=') else TOK_LT)
      elif ch == '>':
        self.add_token(TOK_GE if self.match('=') else TOK_GT)
      elif ch == ':':
        self.add_token(TOK_ASSIGN if self.match('=') else TOK_COLON)
      elif ch.isdigit():
        self.handle_number()
      #TODO: handle_string() --> "something" or 'something'
    return self.tokens
