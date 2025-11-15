# Project 04: Build an Interpreter from First Principles

## Overview

This project teaches you how programming languages work by building a complete interpreter from scratch. You'll understand the journey from text to execution and gain deep insights into language design.

## What You'll Learn

- The three stages of interpretation: lexing, parsing, and evaluation
- How to design and implement a programming language
- Abstract Syntax Trees (ASTs) and their importance
- Variable scoping and closures
- How functions work under the hood
- The foundations of compilers and interpreters

## Language Features

**TinyLang** supports:
- Arithmetic and logical expressions
- Variables and assignment
- Control flow (if/else, while, for)
- Functions with closures
- Recursion
- Built-in functions
- REPL for interactive use

## Files

- **GUIDE.md** - Comprehensive guide to building an interpreter
- **tinylang.py** - Implementation challenges for the complete interpreter

## Architecture

### Stage 1: Lexer (Tokenizer)
```
"x = 2 + 3" → [IDENTIFIER(x), EQUALS, NUMBER(2), PLUS, NUMBER(3)]
```
Breaks source code into meaningful tokens.

### Stage 2: Parser
```
[tokens] → BinaryOp(
              left=Number(2),
              op='+',
              right=Number(3)
           )
```
Builds an Abstract Syntax Tree from tokens.

### Stage 3: Evaluator
```
AST → Execute and produce results
```
Walks the tree and executes the program.

## How to Use

### Self-Guided Learning
1. Work through `GUIDE.md` sequentially
2. Implement each component in `tinylang.py`
3. Test each stage independently
4. Build up to the complete interpreter
5. Extend with your own features

### Claude Code CLI Guided Mode
```bash
claude-code "Walk me through building an interpreter from first principles. Help me understand lexical analysis first."
```

## Prerequisites

- Strong Python knowledge
- Understanding of recursion
- Completed Projects 01-03 or equivalent
- Willingness to think deeply about language design

## Time Estimate

- Fast path: 8-10 hours
- Deep understanding: 15-20 hours
- Mastery (with extensions): 25+ hours

## Development Approach

### Incremental Development
1. **Start simple:** Arithmetic expressions only
2. **Add variables:** Store and retrieve values
3. **Add control flow:** If statements, loops
4. **Add functions:** Define and call functions
5. **Add scoping:** Nested scopes and closures
6. **Polish:** Error handling, REPL, debugging

### Testing Strategy
- Test each component independently
- Use simple examples first
- Build up complexity gradually
- Test edge cases (empty input, errors, etc.)

## Example Programs

### Arithmetic
```
2 + 3 * 4  # 14
(2 + 3) * 4  # 20
2 ** 3  # 8
```

### Variables
```
x = 10
y = x + 5
print(y)  # 15
```

### Functions
```
func add(a, b) {
    return a + b
}

result = add(5, 3)
print(result)  # 8
```

### Recursion
```
func factorial(n) {
    if n <= 1 {
        return 1
    } else {
        return n * factorial(n - 1)
    }
}

print(factorial(5))  # 120
```

### Closures
```
func makeCounter() {
    count = 0
    func increment() {
        count = count + 1
        return count
    }
    return increment
}

counter = makeCounter()
print(counter())  # 1
print(counter())  # 2
```

## Success Criteria

You've mastered this project when you can:
- Explain the interpreter pipeline from first principles
- Implement a complete working interpreter
- Debug issues at each stage (lexer, parser, evaluator)
- Design and add new language features
- Understand how real programming languages work
- Explain closures and lexical scoping with examples

## Common Challenges

1. **Operator precedence:** Use grammar hierarchy
2. **Scoping:** Use environment chains with parent pointers
3. **Recursion:** Handle return values with exceptions
4. **Error messages:** Track line/column numbers throughout
5. **Closures:** Capture environment when function is defined

## Extensions

Once you have the basic interpreter working:
- Add classes and objects
- Implement a module system
- Add type checking (optional or static)
- Build a debugger (step through execution)
- Optimize with bytecode compilation
- Add garbage collection
- Implement tail call optimization

## Resources in GUIDE.md

- Detailed explanations of each stage
- Questions to build understanding
- Design considerations
- Trade-offs in language design
- Best practices

## Next Project

After understanding how code executes, you're ready for **Project 05: TCP/IP Protocol Simulator**, where you'll learn how computers communicate over networks from first principles.
