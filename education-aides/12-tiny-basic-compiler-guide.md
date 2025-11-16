# Tiny BASIC Compiler - Education Aide
## Building a Compiler from First Principles

### Overview
This guide teaches you how compilers work by building one for a simple BASIC-like language. You'll learn lexical analysis, parsing, semantic analysis, and code generation - the same techniques used in GCC, Clang, and V8.

---

## Part 1: What is a Compiler?

### Question 1: High-Level Understanding
**Think about this:** What does a compiler do?

**Your Answer:** _[Write your understanding]_

<details>
<summary>Compiler Pipeline</summary>

A compiler translates source code into executable code through stages:

```
Source Code
    ↓
[Lexer] → Tokens
    ↓
[Parser] → Abstract Syntax Tree (AST)
    ↓
[Semantic Analyzer] → Validated AST
    ↓
[Code Generator] → Target Code
```

**Example:**
```basic
LET X = 5 + 3
```

**After lexer:**
```
[LET] [IDENTIFIER:X] [=] [NUMBER:5] [+] [NUMBER:3]
```

**After parser (AST):**
```
Assignment
  ├─ Variable: X
  └─ BinaryOp: +
      ├─ Number: 5
      └─ Number: 3
```

**After code gen (Python target):**
```python
X = 5 + 3
```
</details>

### Question 2: Why Build a Compiler?
**Reflection:** What will you learn?

<details>
<summary>Learning Objectives</summary>

1. **Pattern recognition** - Tokenizing text
2. **Recursive thinking** - Parsing nested structures
3. **Tree manipulation** - Working with ASTs
4. **Error handling** - Meaningful error messages
5. **Language design** - Understanding syntax choices

**Applications beyond compilers:**
- JSON/XML parsers
- Configuration file processors
- Domain-specific languages (DSLs)
- Query languages
- Markup processors
</details>

---

## Part 2: Lexical Analysis (Tokenization)

### Understanding Tokens

**Question:** What is a token?

**Your Answer:** _[Define token]_

<details>
<summary>Token Concept</summary>

A **token** is a meaningful unit in source code:

```basic
LET X = 5 + 3 * Y
```

**Tokens:**
1. `LET` - Keyword
2. `X` - Identifier
3. `=` - Operator
4. `5` - Number literal
5. `+` - Operator
6. `3` - Number literal
7. `*` - Operator
8. `Y` - Identifier

**Token structure:**
```python
class Token:
    def __init__(self, type, value, line):
        self.type = type      # TOKEN_NUMBER, TOKEN_PLUS, etc.
        self.value = value    # Actual value: 5, "+", "X"
        self.line = line      # For error messages
```

**Whitespace is ignored** - spaces, tabs, newlines between tokens don't matter (usually).
</details>

### Building a Lexer

**Exercise:** Write a lexer for simple arithmetic

<details>
<summary>Simple Lexer Implementation</summary>

```python
import re

class TokenType:
    NUMBER = 'NUMBER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    EOF = 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

    def advance(self):
        """Move to next character"""
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self):
        """Parse a number (integer or float)"""
        result = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return float(result) if '.' in result else int(result)

    def get_next_token(self):
        """Lexical analyzer (tokenizer)"""
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.number())

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            raise Exception(f'Invalid character: {self.current_char}')

        return Token(TokenType.EOF, None)

# Test it!
lexer = Lexer("3 + 5 * (2 - 1)")
token = lexer.get_next_token()
while token.type != TokenType.EOF:
    print(token)
    token = lexer.get_next_token()

# Output:
# Token(NUMBER, 3)
# Token(PLUS, +)
# Token(NUMBER, 5)
# Token(MULTIPLY, *)
# Token(LPAREN, ()
# Token(NUMBER, 2)
# Token(MINUS, -)
# Token(NUMBER, 1)
# Token(RPAREN, ))
```

**Try it:** Add support for identifiers (variable names)

<details>
<summary>Solution</summary>

```python
class TokenType:
    # ... existing types ...
    IDENTIFIER = 'IDENTIFIER'

class Lexer:
    # ... existing methods ...

    def identifier(self):
        """Parse identifier or keyword"""
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char:
            # ... existing checks ...

            if self.current_char.isalpha():
                return Token(TokenType.IDENTIFIER, self.identifier())

            raise Exception(f'Invalid character: {self.current_char}')

        return Token(TokenType.EOF, None)
```
</details>
</details>

---

## Part 3: Parsing - Building the AST

### Understanding Grammars

**Question:** What rules define valid syntax?

<details>
<summary>Grammar Notation (BNF)</summary>

**Backus-Naur Form (BNF)** defines syntax rules:

```
expression → term ((PLUS | MINUS) term)*
term → factor ((MULTIPLY | DIVIDE) factor)*
factor → NUMBER | LPAREN expression RPAREN
```

**Reading the grammar:**
- `→` means "is defined as"
- `|` means "or"
- `*` means "zero or more"
- `+` means "one or more"
- `( )` groups items

**Example:** `3 + 5 * 2`

Following the grammar:
1. **expression** → term (PLUS term)
2. **term** → factor (no operators)
3. **factor** → 3
4. Then PLUS
5. **term** → factor MULTIPLY factor
6. **factor** → 5
7. **factor** → 2

**Why this structure?** It enforces operator precedence:
- Multiplication binds tighter than addition
- `3 + 5 * 2` parses as `3 + (5 * 2)`, not `(3 + 5) * 2`
</details>

### Recursive Descent Parsing

**Question:** How do you turn grammar rules into code?

**Answer:** Each grammar rule becomes a function!

<details>
<summary>Parser Implementation</summary>

```python
class AST:
    pass

class Number(AST):
    def __init__(self, value):
        self.value = value

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        """Consume a token of given type"""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : NUMBER | LPAREN expression RPAREN"""
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node

    def term(self):
        """term : factor ((MULTIPLY | DIVIDE) factor)*"""
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expression(self):
        """expression : term ((PLUS | MINUS) term)*"""
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expression()

# Test it!
lexer = Lexer("3 + 5 * 2")
parser = Parser(lexer)
ast = parser.parse()

# AST structure:
#     BinOp(+)
#      /      \
#   Num(3)  BinOp(*)
#            /      \
#         Num(5)  Num(2)
```

**Beautiful, isn't it?** Each function calls others recursively, building the tree from bottom up!
</details>

### Visualizing the AST

**Exercise:** Print the AST in readable form

<details>
<summary>AST Printer</summary>

```python
def print_ast(node, indent=0):
    """Pretty-print the AST"""
    spacing = "  " * indent

    if isinstance(node, Number):
        print(f"{spacing}Number({node.value})")

    elif isinstance(node, BinOp):
        print(f"{spacing}BinOp({node.op.value})")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

# Test
lexer = Lexer("3 + 5 * 2")
parser = Parser(lexer)
ast = parser.parse()
print_ast(ast)

# Output:
# BinOp(+)
#   Number(3)
#   BinOp(*)
#     Number(5)
#     Number(2)
```
</details>

---

## Part 4: Interpretation (Walking the AST)

### Evaluating Expressions

**Question:** How do you execute the AST?

<details>
<summary>Interpreter (Tree Walker)</summary>

```python
class Interpreter:
    def visit(self, node):
        """Dispatch to appropriate visitor method"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Number(self, node):
        return node.value

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == TokenType.PLUS:
            return left + right
        elif node.op.type == TokenType.MINUS:
            return left - right
        elif node.op.type == TokenType.MULTIPLY:
            return left * right
        elif node.op.type == TokenType.DIVIDE:
            return left / right

    def interpret(self, tree):
        return self.visit(tree)

# Test the complete pipeline!
text = "7 + 3 * (10 / (12 / (3 + 1) - 1))"
lexer = Lexer(text)
parser = Parser(lexer)
interpreter = Interpreter()
result = interpreter.interpret(parser.parse())
print(f"{text} = {result}")

# Output: 7 + 3 * (10 / (12 / (3 + 1) - 1)) = 22.0
```

**Congratulations!** You just built a working calculator compiler!
</details>

---

## Part 5: Adding Variables (Symbol Table)

### Understanding Scope

**Question:** How do compilers track variable names?

<details>
<summary>Symbol Table</summary>

A **symbol table** maps variable names to values/types:

```python
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def set(self, name, value):
        self.symbols[name] = value

    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        raise Exception(f'Undefined variable: {name}')

# Extend lexer for keywords
class TokenType:
    # ... existing ...
    LET = 'LET'
    IDENTIFIER = 'IDENTIFIER'
    ASSIGN = 'ASSIGN'

# Extend AST
class Assign(AST):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Variable(AST):
    def __init__(self, name):
        self.name = name

# Extend interpreter
class Interpreter:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_Assign(self, node):
        value = self.visit(node.value)
        self.symbol_table.set(node.name, value)
        return value

    def visit_Variable(self, node):
        return self.symbol_table.get(node.name)

# Now we can do:
# LET X = 5
# LET Y = X + 3
# PRINT Y  → 8
```
</details>

---

## Part 6: Control Flow (IF, WHILE)

### Implementing Conditionals

<details>
<summary>IF Statement</summary>

**Grammar:**
```
if_stmt → IF comparison THEN statement
comparison → expression (LT | GT | EQ) expression
```

**AST Nodes:**
```python
class If(AST):
    def __init__(self, condition, then_stmt):
        self.condition = condition
        self.then_stmt = then_stmt

class Comparison(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

# Interpreter
class Interpreter:
    def visit_If(self, node):
        if self.visit(node.condition):
            self.visit(node.then_stmt)

    def visit_Comparison(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == TokenType.LT:
            return left < right
        elif node.op.type == TokenType.GT:
            return left > right
        elif node.op.type == TokenType.EQ:
            return left == right

# Example:
# IF X > 5 THEN PRINT X
```
</details>

### Loops

<details>
<summary>WHILE Loop</summary>

```python
class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body  # List of statements

# Interpreter
def visit_While(self, node):
    while self.visit(node.condition):
        for stmt in node.body:
            self.visit(stmt)

# Example:
# LET I = 0
# WHILE I < 10 DO
#     PRINT I
#     LET I = I + 1
# END
```
</details>

---

## Part 7: Code Generation

### Transpiling to Python

**Question:** Instead of interpreting, can we generate Python code?

<details>
<summary>Code Generator</summary>

```python
class CodeGenerator:
    def __init__(self):
        self.code = []
        self.indent_level = 0

    def emit(self, code):
        indent = "    " * self.indent_level
        self.code.append(indent + code)

    def visit_Number(self, node):
        return str(node.value)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"({left} {node.op.value} {right})"

    def visit_Assign(self, node):
        value = self.visit(node.value)
        self.emit(f"{node.name} = {value}")

    def visit_Print(self, node):
        value = self.visit(node.value)
        self.emit(f"print({value})")

    def visit_If(self, node):
        condition = self.visit(node.condition)
        self.emit(f"if {condition}:")
        self.indent_level += 1
        self.visit(node.then_stmt)
        self.indent_level -= 1

    def generate(self, tree):
        for stmt in tree:
            self.visit(stmt)
        return "\n".join(self.code)

# Input BASIC:
# LET X = 5
# IF X > 3 THEN PRINT X

# Generated Python:
# X = 5
# if (X > 3):
#     print(X)
```

**Now you can execute it!**
```python
generated_code = code_gen.generate(ast)
exec(generated_code)
```
</details>

---

## Learning Projects

### Project 1: Calculator (1 week)
- [ ] Tokenize arithmetic
- [ ] Parse with precedence
- [ ] Evaluate expressions
- [ ] Support parentheses

### Project 2: Variables (1 week)
- [ ] LET statements
- [ ] Symbol table
- [ ] Variable references
- [ ] PRINT statement

### Project 3: Control Flow (2 weeks)
- [ ] IF/THEN
- [ ] WHILE loops
- [ ] Comparison operators
- [ ] Multiple statements

### Project 4: Functions (2 weeks)
- [ ] Function definitions
- [ ] Parameters
- [ ] Return values
- [ ] Local scope

---

## Resources

- [Crafting Interpreters](https://craftinginterpreters.com/) - The best book
- [Let's Build a Compiler](https://compilers.iecc.com/crenshaw/) - Classic tutorial
- [Dragon Book](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools) - Reference

---

**Next Steps:** Start with the calculator, then add features!

*"The recursive descent parsing technique is beautiful!" - Austin Henley*
