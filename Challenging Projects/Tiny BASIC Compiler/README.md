# Compiler - Tiny BASIC

## Overview
Build a compiler for a simple BASIC-like language to understand how programming languages work from source code to execution.

## The Challenge
"**The recursive descent parsing technique is beautiful!**" - Implementing a complete compiler teaches you lexical analysis, parsing, semantic analysis, and code generation.

## Core Features to Implement

### Phase 1: Lexer (Lexical Analysis)
- [ ] Tokenize source code
- [ ] Recognize keywords (IF, THEN, WHILE, etc.)
- [ ] Identify operators (+, -, *, /, =, <, >)
- [ ] Parse numbers and identifiers
- [ ] Handle whitespace and comments

### Phase 2: Parser (Syntax Analysis)
- [ ] Build Abstract Syntax Tree (AST)
- [ ] Implement recursive descent parser
- [ ] Handle expressions with proper precedence
- [ ] Parse control structures (IF/THEN, WHILE)
- [ ] Error reporting with line numbers

### Phase 3: Semantic Analysis
- [ ] Type checking
- [ ] Variable declaration checking
- [ ] Scope resolution
- [ ] Detect undefined variables

### Phase 4: Code Generation
- [ ] Generate target code (can be another language!)
- [ ] Optimize simple expressions
- [ ] Handle control flow
- [ ] Generate executable output

## Tiny BASIC Language Features

### Minimum Features
```basic
LET X = 5
LET Y = X + 3
PRINT Y

IF X < 10 THEN PRINT "Small"

LET I = 0
WHILE I < 5 DO
    PRINT I
    LET I = I + 1
END
```

### Recommended Features
- Variables (integer or floating-point)
- Arithmetic operators (+, -, *, /)
- Comparison operators (<, >, =, <=, >=, <>)
- IF/THEN statements
- WHILE/DO loops
- PRINT statement
- INPUT statement
- GOTO and GOSUB (optional, for classic BASIC feel)

## Key Concepts

### Lexical Analysis (Tokenization)
- Read source character by character
- Group into meaningful tokens
- Classify tokens (keyword, identifier, number, operator)

### Parsing
- **Recursive Descent:** Hand-written parser following grammar rules
- **Grammar:** BNF (Backus-Naur Form) notation
- **Precedence:** Handle operator precedence correctly
  - Multiplication/Division before Addition/Subtraction
  - Parentheses override precedence

### Abstract Syntax Tree (AST)
- Tree representation of program structure
- Each node represents a construct
- Makes analysis and code generation easier

### Code Generation Strategies
- **Transpile to C/Python/JavaScript:** Easier than assembly
- **Generate bytecode:** For a simple VM
- **Direct interpretation:** Walk the AST (technically an interpreter)
- **Assembly/machine code:** Most challenging but educational

## Learning Objectives
- Understanding compiler pipeline
- Implementing lexers and parsers
- Working with grammars and formal languages
- Building ASTs
- Code generation techniques
- Error handling and reporting
- Optimization basics

## Technology Suggestions

### Language Choice
- **C/C++:** Traditional, full control
- **Python:** Rapid prototyping, easy to start
- **Rust:** Modern, safe, great error handling
- **Java:** Good structure, plenty of resources
- **OCaml/Haskell:** Functional approach, pattern matching

### Tools (Optional)
- **Lex/Flex:** Lexer generator (but hand-writing is more educational)
- **Yacc/Bison:** Parser generator (again, hand-writing teaches more)
- **ANTLR:** Modern parser generator
- **LLVM:** If you want to generate optimized machine code

## Implementation Tips

1. **Start with the Lexer:** Get tokenization working first
2. **Test Incrementally:** Test each phase independently
3. **Use Examples:** Have a suite of test programs
4. **Error Messages Matter:** Good errors help debugging
5. **Build Up Grammar:** Start simple, add features gradually

## Milestones

### Milestone 1: Calculator
- Tokenize arithmetic expressions
- Parse with correct precedence
- Evaluate expressions
- Example: `2 + 3 * 4` should equal `14`

### Milestone 2: Variables and Print
```basic
LET X = 5
LET Y = X + 3
PRINT Y
```

### Milestone 3: Conditionals
```basic
IF X > 0 THEN PRINT "Positive"
IF X < 0 THEN PRINT "Negative"
```

### Milestone 4: Loops
```basic
LET I = 0
WHILE I < 10 DO
    PRINT I
    LET I = I + 1
END
```

### Milestone 5: Full Compiler
- All features working
- Good error messages
- Generates executable code
- Test suite passing

## Sample Grammar (Simplified)

```
program     → statement*
statement   → assignment | print | if | while
assignment  → "LET" identifier "=" expression
print       → "PRINT" expression
if          → "IF" comparison "THEN" statement
while       → "WHILE" comparison "DO" statement* "END"
comparison  → expression ("<" | ">" | "=") expression
expression  → term (("+" | "-") term)*
term        → factor (("*" | "/") factor)*
factor      → number | identifier | "(" expression ")"
```

## Resources
- [Crafting Interpreters](https://craftinginterpreters.com/) - Excellent free book
- [Let's Build a Compiler](https://compilers.iecc.com/crenshaw/) - Classic tutorial
- [Dragon Book](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools) - Comprehensive reference
- [Write You a Haskell](http://dev.stephendiehl.com/fun/) - Haskell implementation
- [Tiny BASIC specification](https://en.wikipedia.org/wiki/Tiny_BASIC) - Original spec

## Extensions
- **Functions:** User-defined functions with parameters
- **Arrays:** Support for array variables
- **Strings:** String type and operations
- **File I/O:** Read/write files
- **Debugging info:** Generate source maps
- **Optimization:** Constant folding, dead code elimination
- **Type system:** Static typing with type inference
- **Standard library:** Built-in functions (SIN, COS, SQRT)
- **REPL:** Interactive mode
- **Better errors:** Show context, suggestions

## Target Platforms

### Transpile to High-Level Language (Easiest)
- Generate Python, JavaScript, or C code
- Let existing compiler handle optimization

### Virtual Machine (Intermediate)
- Design simple bytecode format
- Write interpreter for bytecode
- Good balance of challenge and practicality

### x86/ARM Assembly (Hardest)
- Learn assembly language
- Handle calling conventions
- Deal with register allocation
- Most educational but time-consuming

## Common Pitfalls
- Not handling operator precedence correctly
- Poor error messages (cryptic errors frustrate users)
- Memory leaks in AST construction
- Not testing edge cases
- Making grammar too complex too quickly

## Estimated Time
- **Basic calculator:** 1 week
- **Simple compiler (transpiler):** 2-4 weeks
- **Full-featured compiler:** 2-3 months
- **Optimizing compiler:** 6+ months

---

*From Austin Z. Henley's "Challenging Projects Every Programmer Should Try"*
