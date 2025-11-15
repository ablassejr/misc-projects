# Build an Interpreter: Understanding How Code Executes from First Principles

## 🎯 Learning Objectives

By the end of this project, you will understand:
- How programming languages work "under the hood"
- The stages of code execution: lexing, parsing, evaluation
- How to design and implement a language from scratch
- Abstract syntax trees (ASTs) and their importance
- Variable scopes, functions, and closures
- The difference between interpretation and compilation

## 📚 First Principles Foundation

### From Text to Execution

**PAUSE AND THINK:** When you write `print(2 + 3)`, how does the computer know what to do?

**Question 1:** The computer only understands binary (machine code). What steps must happen to get from text to execution?

<details>
<summary>Click after thinking</summary>

**High-level steps:**
1. **Read the text:** "print(2 + 3)"
2. **Understand the structure:** It's a function call with an argument
3. **Evaluate the argument:** 2 + 3 = 5
4. **Execute the function:** Print 5
5. **Convert to machine instructions:** Binary operations

**Key Insight:** Every programming language performs these transformations!
</details>

---

**Question 2:** Why is `2 + 3 * 4` equal to 14 and not 20?

<details>
<summary>Click after answering</summary>

**Answer:** Operator precedence! Multiplication before addition.

**But who enforces this?** The language parser!

**Key Insight:** Languages have rules that must be encoded in the interpreter/compiler.
</details>

---

### The Interpreter Pipeline

**Question 3:** An interpreter typically has three main stages:
1. **Lexer** (Tokenizer): Breaks text into tokens
2. **Parser**: Organizes tokens into structure
3. **Evaluator**: Executes the structure

For the code `x = 5 + 3`, what would each stage produce?

<details>
<summary>Click after thinking</summary>

**Lexer output (tokens):**
```
[IDENTIFIER("x"), EQUALS, NUMBER(5), PLUS, NUMBER(3)]
```

**Parser output (AST - Abstract Syntax Tree):**
```
Assignment
├── variable: "x"
└── value: BinaryOp
    ├── left: 5
    ├── operator: +
    └── right: 3
```

**Evaluator:**
```
1. Evaluate right side: 5 + 3 = 8
2. Assign to variable x
```

**Key Insight:** Each stage transforms representation to something easier to process!
</details>

---

## 🔨 Project Overview

You'll build **TinyLang**, a simple but complete programming language with:
1. Arithmetic expressions: `2 + 3 * 4`
2. Variables: `x = 10`
3. Conditionals: `if x > 5 then ... else ...`
4. Functions: `func add(a, b) { return a + b }`
5. Recursion and scoping

## 📖 Part 1: Lexical Analysis (Tokenization)

### What Is a Token?

**Question 4:** Consider the code: `age = 42`

As a human, you recognize three "words": "age", "=", and "42". But to a computer, it's just characters: 'a', 'g', 'e', ' ', '=', ' ', '4', '2'.

How do we group characters into meaningful units?

<details>
<summary>Click after designing</summary>

**Answer:** Pattern matching!

- **Identifier:** Letter followed by letters/digits/underscores
- **Number:** One or more digits (maybe with decimal point)
- **Operator:** =, +, -, *, /, ==, !=, <, >, etc.
- **Whitespace:** Spaces, tabs, newlines (usually ignored)

**Result:**
```python
[
    Token(type='IDENTIFIER', value='age'),
    Token(type='EQUALS', value='='),
    Token(type='NUMBER', value=42)
]
```

**Key Insight:** Tokenization simplifies the input into categories!
</details>

---

**Question 5:** Why tokenize before parsing? Why not parse characters directly?

<details>
<summary>Click after considering</summary>

**Reasons:**
1. **Separation of concerns:** Lexer handles character patterns, parser handles language grammar
2. **Performance:** Token stream is smaller than character stream
3. **Error handling:** Easier to report "unexpected token" than "unexpected character"
4. **Whitespace handling:** Lexer can skip whitespace once

**Key Insight:** Each stage simplifies the problem for the next stage!
</details>

---

**Question 6:** How do you tokenize `>=` vs `>` and `=`?

Consider: `if x >= 5` vs `if x > y = 10`

<details>
<summary>Click after thinking</summary>

**Challenge:** Need lookahead!

**Algorithm:**
```python
if current_char == '>':
    if next_char == '=':
        return Token('GREATER_EQUAL', '>=')
    else:
        return Token('GREATER', '>')
```

**Key Insight:** Tokenizers need to peek ahead to resolve ambiguity!
</details>

---

### 💻 Implementation Challenge 1

Implement a `Lexer` class that:
- Tokenizes arithmetic: `+`, `-`, `*`, `/`, `(`, `)`
- Handles numbers (integers and floats)
- Handles identifiers and keywords (`if`, `else`, `func`, etc.)
- Skips whitespace and comments
- Reports line numbers for error messages

**Test it:**
```python
code = "x = 2 + 3 * (4 - 1)"
tokens = Lexer(code).tokenize()
```

---

## 📖 Part 2: Parsing (Building the AST)

### What Is an Abstract Syntax Tree?

**Question 7:** The expression `2 + 3 * 4` should be evaluated as `2 + (3 * 4)` due to precedence.

How do you represent this structure in code?

<details>
<summary>Click after designing</summary>

**Answer:** A tree!

```
    +
   / \
  2   *
     / \
    3   4
```

**In code:**
```python
BinaryOp(
    left=Number(2),
    operator='+',
    right=BinaryOp(
        left=Number(3),
        operator='*',
        right=Number(4)
    )
)
```

**Key Insight:** Tree structure naturally represents operator precedence!
</details>

---

**Question 8:** How do you build this tree from a flat list of tokens?

**Hint:** This is one of the core challenges in computer science!

<details>
<summary>Click after thinking deeply</summary>

**Main approaches:**

1. **Recursive Descent Parsing:**
   - Write a function for each grammar rule
   - Functions call each other recursively
   - Natural and intuitive

2. **Operator Precedence Parsing:**
   - Use precedence table
   - Efficient for expressions

3. **Parser Generators (like yacc):**
   - Specify grammar formally
   - Tool generates parser

**We'll use recursive descent - it's clearest for learning!**

**Key Insight:** Language grammar maps to parser code structure!
</details>

---

### Grammar and Recursive Descent

**Question 9:** Here's a simple expression grammar:

```
expression := term (('+' | '-') term)*
term       := factor (('*' | '/') factor)*
factor     := NUMBER | '(' expression ')'
```

Why is `expression` defined in terms of `term`, not the other way around?

<details>
<summary>Click after analyzing</summary>

**Answer:** Precedence!

- `expression` is lowest precedence (handles + and -)
- `term` is higher precedence (handles * and /)
- `factor` is highest (handles numbers and parentheses)

**Parsing `2 + 3 * 4`:**
1. `expression` finds `+`, splits into terms
2. First term is just `2`
3. Second term finds `*`, splits into factors `3` and `4`
4. Result: `2 + (3 * 4)` ✓

**Key Insight:** Grammar rules encode operator precedence!
</details>

---

**Question 10:** How do you handle left vs right associativity?

`2 - 3 - 4` should be `(2 - 3) - 4` = -5, not `2 - (3 - 4)` = 3

<details>
<summary>Click after considering</summary>

**Answer:** Loop structure!

**Left-associative** (subtraction, division):
```python
def expression():
    result = term()
    while current_token in ['+', '-']:
        op = current_token
        advance()
        right = term()
        result = BinaryOp(result, op, right)  # Left becomes new left
    return result
```

**Right-associative** (exponentiation):
```python
def factor():
    left = atom()
    if current_token == '**':
        op = current_token
        advance()
        right = factor()  # Recursive call for right-associativity!
        return BinaryOp(left, op, right)
    return left
```

**Key Insight:** Iteration gives left-associativity, recursion gives right-associativity!
</details>

---

### 💻 Implementation Challenge 2

Implement a `Parser` class that:
- Parses arithmetic expressions with correct precedence
- Handles parentheses
- Builds an AST from tokens
- Provides clear error messages with line numbers

**Test it:**
```python
tokens = Lexer("2 + 3 * 4").tokenize()
ast = Parser(tokens).parse()
# Should produce: BinaryOp(2, '+', BinaryOp(3, '*', 4))
```

---

## 📖 Part 3: Evaluation (Executing the AST)

### Walking the Tree

**Question 11:** Given this AST:
```
    +
   / \
  2   *
     / \
    3   4
```

How do you evaluate it to get 14?

<details>
<summary>Click after thinking</summary>

**Answer:** Post-order traversal (children before parent)!

```python
def evaluate(node):
    if node is Number:
        return node.value
    elif node is BinaryOp:
        left = evaluate(node.left)   # Evaluate left child
        right = evaluate(node.right)  # Evaluate right child
        return apply_op(left, node.operator, right)
```

**Execution:**
1. evaluate(2) → 2
2. evaluate(3) → 3
3. evaluate(4) → 4
4. apply_op(3, '*', 4) → 12
5. apply_op(2, '+', 12) → 14

**Key Insight:** Recursion naturally handles tree traversal!
</details>

---

**Question 12:** How do you add variables? Consider: `x = 5; y = x + 3`

<details>
<summary>Click after designing</summary>

**Answer:** Environment (symbol table)!

```python
class Environment:
    def __init__(self):
        self.variables = {}

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        raise NameError(f"Variable '{name}' not defined")
```

**Evaluation:**
```python
def evaluate(node, env):
    if node is Assignment:
        value = evaluate(node.value, env)
        env.set(node.name, value)
        return value
    elif node is Variable:
        return env.get(node.name)
    # ... other cases
```

**Key Insight:** Environment maps variable names to values!
</details>

---

### 💻 Implementation Challenge 3

Implement an `Evaluator` class that:
- Evaluates arithmetic expressions
- Handles variable assignment and lookup
- Implements comparison operators (`<`, `>`, `==`, etc.)
- Implements logical operators (`and`, `or`, `not`)

---

## 📖 Part 4: Control Flow

### If Statements

**Question 13:** For `if x > 5 then print("big") else print("small")`, what does the AST look like?

<details>
<summary>Click after designing</summary>

**AST:**
```
IfStatement
├── condition: BinaryOp(Variable(x), '>', Number(5))
├── then_branch: FunctionCall('print', [String("big")])
└── else_branch: FunctionCall('print', [String("small")])
```

**Evaluation:**
```python
def evaluate(node, env):
    if node is IfStatement:
        condition_value = evaluate(node.condition, env)
        if condition_value:
            return evaluate(node.then_branch, env)
        else:
            return evaluate(node.else_branch, env)
```

**Key Insight:** Control flow is just conditional evaluation of branches!
</details>

---

### Loops

**Question 14:** How would you implement `while x < 10 { x = x + 1 }`?

<details>
<summary>Click after thinking</summary>

**Evaluation:**
```python
def evaluate(node, env):
    if node is WhileStatement:
        while evaluate(node.condition, env):
            evaluate(node.body, env)
        return None
```

**Question:** What if the body never changes the condition?

**Answer:** Infinite loop! (This is a feature, not a bug - same as real languages)

**Key Insight:** Loops are just repeated conditional execution!
</details>

---

### 💻 Implementation Challenge 4

Implement:
- If-else statements
- While loops
- For loops (syntactic sugar for while)
- Break and continue statements

---

## 📖 Part 5: Functions and Scope

### Function Definitions and Calls

**Question 15:** For `func add(a, b) { return a + b }`, what information needs to be stored?

<details>
<summary>Click after thinking</summary>

**Function object needs:**
```python
class Function:
    def __init__(self, params, body, env):
        self.params = params      # ['a', 'b']
        self.body = body          # AST of function body
        self.closure_env = env    # Environment where defined
```

**Why store environment?**

For closures! (See next question)

**Key Insight:** Functions are values that can be stored and passed around!
</details>

---

**Question 16:** What should this code print?

```python
x = 10

func makeAdder() {
    func adder(y) {
        return x + y
    }
    return adder
}

f = makeAdder()
x = 20
print(f(5))  # What prints?
```

<details>
<summary>Click after thinking deeply</summary>

**Answer:** Depends on scoping rules!

**Lexical scoping (most languages):** Prints 15
- Function remembers environment where defined
- x = 10 when makeAdder was called

**Dynamic scoping (rare):** Prints 25
- Function uses environment where called
- x = 20 when f(5) is called

**We'll implement lexical scoping - it's more intuitive!**

**Key Insight:** Closures "close over" their defining environment!
</details>

---

**Question 17:** How do you implement function calls with proper scoping?

<details>
<summary>Click after designing</summary>

**Answer:** Create new environment for each call!

```python
def evaluate(node, env):
    if node is FunctionCall:
        func = evaluate(node.name, env)
        args = [evaluate(arg, env) for arg in node.arguments]

        # Create new environment for function execution
        call_env = Environment(parent=func.closure_env)

        # Bind parameters to arguments
        for param, arg in zip(func.params, args):
            call_env.set(param, arg)

        # Execute function body in new environment
        return evaluate(func.body, call_env)
```

**Key Insight:** Each function call gets its own local scope!
</details>

---

### 💻 Implementation Challenge 5

Implement:
- Function definitions
- Function calls with arguments
- Return statements
- Recursive functions (should work automatically!)
- Nested scopes with closures

---

## 📖 Part 6: Advanced Features

### First-Class Functions

**Question 18:** If functions are values, they can be:
- Assigned to variables
- Passed as arguments
- Returned from functions

This enables powerful patterns. Can you think of use cases?

<details>
<summary>Click after thinking</summary>

**Examples:**

**Passing functions (callbacks):**
```python
func map(f, list) {
    result = []
    for item in list {
        result.append(f(item))
    }
    return result
}

doubled = map(func(x) { return x * 2 }, [1, 2, 3])
```

**Returning functions (currying):**
```python
func multiply(a) {
    return func(b) {
        return a * b
    }
}

double = multiply(2)
print(double(5))  # 10
```

**Key Insight:** First-class functions enable functional programming!
</details>

---

### Error Handling

**Question 19:** What kinds of errors can occur, and where?

<details>
<summary>Click after categorizing</summary>

**Errors by stage:**

1. **Lexer errors:** Invalid characters, unterminated strings
2. **Parser errors:** Unexpected tokens, invalid syntax
3. **Runtime errors:** Division by zero, undefined variables, type errors

**Good error messages need:**
- Location (line and column number)
- Context (what was being parsed/evaluated)
- Suggestion (what was expected)

**Example:**
```
Error at line 5, column 10:
    x = y + z
           ^
NameError: Variable 'z' is not defined
```

**Key Insight:** Good errors are crucial for usability!
</details>

---

### 💻 Implementation Challenge 6

Implement:
- Anonymous/lambda functions
- Lists/arrays with indexing
- Dictionaries/maps
- String operations
- Comprehensive error handling

---

## 🎓 Final Synthesis Challenge

### Build a Complete Language

Create **TinyLang** with:

1. **All basic features:**
   - Arithmetic, comparisons, logic
   - Variables and scoping
   - Control flow (if, while, for)
   - Functions and recursion

2. **Standard library:**
   - Built-in functions (print, len, range, etc.)
   - String methods
   - List operations

3. **Advanced features:**
   - Classes and objects (bonus!)
   - Modules/imports (bonus!)
   - Error handling (try/catch)

4. **Development tools:**
   - REPL (Read-Eval-Print Loop)
   - File execution
   - Debugger (step through AST evaluation)

**Design Questions:**
- What syntax feels natural?
- What should be built-in vs library?
- How do you balance simplicity and power?

---

## 🧪 Testing Your Understanding

Answer these to verify your grasp of first principles:

1. **Stages:** Explain the role of lexer, parser, and evaluator. Why three stages?

2. **AST:** Why use a tree instead of evaluating tokens directly?

3. **Scope:** Explain lexical scoping with an example involving closures.

4. **Performance:** Where are the bottlenecks in a tree-walking interpreter?

5. **Compilation:** How would a compiler differ from your interpreter?

---

## 📚 Further Exploration

Once you've completed this project, you understand:
- How programming languages work internally
- The relationship between syntax and semantics
- How to design and implement language features
- The foundations of compilers and interpreters

**Next steps:**
- How do computers communicate? (Project 05: TCP/IP Protocol)
- Build a compiler (translate to bytecode or machine code)
- Implement optimizations (constant folding, etc.)
- Study type systems (static vs dynamic typing)

---

## 💡 How to Use This Guide with Claude Code CLI

```bash
# Interactive walkthrough
claude-code "Guide me through building an interpreter from first principles. Start with lexical analysis."

# Debug implementations
claude-code "My parser isn't handling precedence correctly. Help me understand the grammar from GUIDE.md"

# Extend language
claude-code "Help me add classes to my TinyLang interpreter following the first principles approach"
```

---

**Remember:** Every programming language you've ever used works on these same principles. Understanding interpreters deeply makes you a better programmer in ANY language!
