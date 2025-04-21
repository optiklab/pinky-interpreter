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

############################################################
# A simple dictionary to map Pinky types to LLVM IR types
############################################################
typemap = {
  TYPE_NUMBER: f64,
  TYPE_BOOL: i1,
}

############################################################
# LLVM module containing an environment/dict for vars
############################################################
class LLVMModule:
  def __init__(self):
    self.module = ir.Module("pinky_subset")
    self.function = ir.Function(self.module, ir.FunctionType(i32, []), "main")
    self.block = self.function.append_basic_block()
    self.builder = ir.IRBuilder(self.block)

    self.print_i32 = ir.Function(self.module, ir.FunctionType(void, [i32]), name="print_i32")
    self.print_f64 = ir.Function(self.module, ir.FunctionType(void, [f64]), name="print_f64")
    self.print_i1  = ir.Function(self.module, ir.FunctionType(void, [i1]),  name="print_i1")

    self.vars = {}

  def get_var(self, name):
    vartype, llvmptr = self.vars.get(name)
    if vartype is not None:
      return (vartype, self.builder.load(llvmptr))
    else:
      return None

  def set_var(self, name, pinkytype, value):
    llvmtype = typemap[pinkytype]
    if self.vars.get(name) is not None:
      vartype, llvmptr = self.vars[name]
      self.builder.store(value, llvmptr)
    else:
      llvmptr = self.builder.alloca(llvmtype)
      self.builder.store(value, llvmptr)
      self.vars[name] = (pinkytype, llvmptr)

############################################################
# Class to visit all nodes of the AST generating their IR
############################################################
class LLVMGenerator:
  def generate(self, node, module):
    if isinstance(node, Integer):
      return (TYPE_NUMBER, ir.Constant(f64, float(node.value)))

    if isinstance(node, Float):
      return (TYPE_NUMBER, ir.Constant(f64, float(node.value)))

    if isinstance(node, Bool):
      return (TYPE_BOOL, ir.Constant(i1, int(node.value)))

    if isinstance(node, String):
      compile_error(f"Strings are not implemented in our current LLVM IR generator.", node.line)

    if isinstance(node, Grouping):
      return self.generate(node.value, module)

    if isinstance(node, Identifier):
      value = module.get_var(node.name)
      if value is None:
        compile_error(f'Undeclared identifier {node.name!r}', node.line)
      if value[1] is None:
        compile_error(f'Uninitialized identifier {node.name!r}', node.line)
      return value

    if isinstance(node, Assignment) or isinstance(node, LocalAssignment):
      righttype, rightval = self.generate(node.right, module)
      module.set_var(node.left.name, righttype, rightval)

    if isinstance(node, BinOp):
      lefttype, leftval = self.generate(node.left, module)
      righttype, rightval = self.generate(node.right, module)
      if node.op.token_type == TOK_PLUS:
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
          return (TYPE_NUMBER, module.builder.fadd(leftval, rightval))
        else:
          compile_error(f"Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.", node.op.line)

      if node.op.token_type == TOK_MINUS:
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
          return (TYPE_NUMBER, module.builder.fsub(leftval, rightval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      if node.op.token_type == TOK_STAR:
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
          return (TYPE_NUMBER, module.builder.fmul(leftval, rightval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      if node.op.token_type == TOK_SLASH:
        if rightval == 0:
          compile_error(f'Division by zero.', node.line)
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
          return (TYPE_NUMBER, module.builder.fdiv(leftval, rightval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      if node.op.token_type == TOK_MOD:
        if lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER:
          return (TYPE_NUMBER, module.builder.frem(leftval, rightval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      if node.op.token_type == TOK_CARET:
        # TODO: Implement exponent operator using a sequence of multiplications
        pass

      if node.op.token_type == TOK_GT:
        if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER):
          return (TYPE_BOOL, module.builder.fcmp_ordered('>', leftval, rightval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      if node.op.token_type == TOK_GE:
        if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER):
          return (TYPE_BOOL, module.builder.fcmp_ordered('>=', leftval, rightval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      if node.op.token_type == TOK_LT:
        if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER):
          return (TYPE_BOOL, module.builder.fcmp_ordered('<', leftval, rightval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      if node.op.token_type == TOK_LE:
        if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER):
          return (TYPE_BOOL, module.builder.fcmp_ordered('<=', leftval, rightval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      if node.op.token_type == TOK_EQEQ:
        if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER):
          return (TYPE_BOOL, module.builder.fcmp_ordered('==', leftval, rightval))
        elif (lefttype == TYPE_BOOL and righttype == TYPE_BOOL):
          return (TYPE_BOOL, module.builder.icmp_signed('==', leftval, rightval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

      if node.op.token_type == TOK_NE:
        if (lefttype == TYPE_NUMBER and righttype == TYPE_NUMBER):
          return (TYPE_BOOL, module.builder.fcmp_ordered('!=', leftval, rightval))
        elif (lefttype == TYPE_BOOL and righttype == TYPE_BOOL):
          return (TYPE_BOOL, module.builder.icmp_signed('!=', leftval, rightval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} between {lefttype} and {righttype}.', node.op.line)

    if isinstance(node, UnOp):
      operandtype, operandval = self.generate(node.operand, module)
      if node.op.token_type == TOK_MINUS:
        if operandtype == TYPE_NUMBER:
          return (TYPE_NUMBER, module.builder.fneg(operandval))
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)

      if node.op.token_type == TOK_PLUS:
        if operandtype == TYPE_NUMBER:
          return (TYPE_NUMBER, operandval)
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)

      elif node.op.token_type == TOK_NOT:
        if operandtype == TYPE_BOOL:
          return (TYPE_BOOL, module.builder.not_(operandval)) # Bitwise complement
        else:
          compile_error(f'Unsupported operator {node.op.lexeme!r} with {operandtype}.', node.op.line)

    if isinstance(node, LogicalOp):
      lefttype, leftval = self.generate(node.left, module)
      righttype, rightval = self.generate(node.right, module)
      if node.op.token_type == TOK_OR:
        return (TYPE_BOOL, module.builder.or_(leftval, rightval))  # Bitwise OR
      elif node.op.token_type == TOK_AND:
        return (TYPE_BOOL, module.builder.and_(leftval, rightval)) # Bitwise AND

    if isinstance(node, Stmts):
      for stmt in node.stmts:
        self.generate(stmt, module)

    if isinstance(node, PrintStmt):
      exprtype, exprval = self.generate(node.value, module)
      if exprtype == TYPE_NUMBER:
        module.builder.call(module.print_f64, [exprval])  # Call external "print_f64" function declared in a C file
      if exprtype == TYPE_BOOL:
        module.builder.call(module.print_i1, [exprval])  # Call external "print_i1" function declared in a C file

    if isinstance(node, IfStmt):
      testtype, testval = self.generate(node.test, module)
      if testtype != TYPE_BOOL:
        compile_error("Condition test is not a boolean expression.", node.line)
      # Create LLVM blocks/labels for then, else, and exit
      then_label = module.function.append_basic_block()
      else_label = module.function.append_basic_block()
      exit_label = module.function.append_basic_block()
      # Test
      module.builder.cbranch(testval, then_label, else_label)
      # Then
      module.builder.position_at_end(then_label)
      self.generate(node.then_stmts, module)
      module.builder.branch(exit_label)
      module.builder.position_at_end(else_label)
      # Else
      if node.else_stmts:
        self.generate(node.else_stmts, module)
      module.builder.branch(exit_label)
      # Exit
      module.builder.position_at_end(exit_label)

    if isinstance(node, WhileStmt):
      #TODO:
      pass

    if isinstance(node, FuncDecl):
      compile_error(f"Function declarations are not implemented in the current LLVM IR generator.", node.line)

    if isinstance(node, FuncCall):
      compile_error(f"Function calls are not implemented in the current LLVM IR generator.", node.line)

  def generate_main(self, node):
    module = LLVMModule()
    self.generate(node, module)
    module.builder.ret(ir.Constant(i32, 0)) # manually adding a return 0 at the end of our main function
    return module

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
