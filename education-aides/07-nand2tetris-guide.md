# Nand2Tetris - Education Aide
## Building a Modern Computer From First Principles

### Overview
Nand2Tetris is one of the most comprehensive computer science learning experiences available. This guide will help you navigate the course and understand how to build a complete computer system from NAND gates up to high-level applications.

---

## Part 1: The Big Picture

### What is Nand2Tetris?

**Question:** Is it really possible to build an entire computer from a single logic gate?

**Your Thought:** _[Think about what a computer needs]_

<details>
<summary>The Journey</summary>

**Yes! The course takes you through 13 projects:**

```
Hardware Layer (Projects 1-5):
NAND gate → Basic gates → ALU → Memory → CPU → Computer

Software Layer (Projects 6-13):
Assembler → VM → Compiler → Operating System → Applications
```

**The Abstraction Stack:**
```
Applications (Tetris, etc.)
       ↕
Operating System (Jack OS)
       ↕
High-Level Language (Jack)
       ↕
Compiler
       ↕
Virtual Machine
       ↕
Assembly Language
       ↕
Machine Language
       ↕
Computer Architecture (Hack)
       ↕
Logic Gates
       ↕
NAND gate (given as primitive)
```

**Core Philosophy:** Each layer builds on the previous, using only what you've already built.
</details>

---

## Part 2: Hardware Projects (1-5)

### Project 1: Boolean Logic

**Fundamental Question:** How do you build all logic gates from just NAND?

**Your Challenge:** _[How would you make an AND gate from NAND?]_

<details>
<summary>Boolean Algebra Basics</summary>

**The NAND gate is universal:**
```
NAND(a, b) = NOT(AND(a, b))

Truth table:
a | b | NAND
--|---|-----
0 | 0 |  1
0 | 1 |  1
1 | 0 |  1
1 | 1 |  0
```

**Building other gates:**

**NOT gate from NAND:**
```
NOT(a) = NAND(a, a)

If a=0: NAND(0,0) = 1 ✓
If a=1: NAND(1,1) = 0 ✓
```

**AND gate from NAND:**
```
AND(a, b) = NOT(NAND(a, b))
          = NAND(NAND(a, b), NAND(a, b))
```

**OR gate from NAND:**
```
OR(a, b) = NAND(NOT(a), NOT(b))
         = NAND(NAND(a, a), NAND(b, b))
```

**XOR gate:**
```
XOR(a, b) = (a AND NOT(b)) OR (NOT(a) AND b)
```

**HDL (Hardware Description Language):**
```
CHIP And {
    IN a, b;
    OUT out;

    PARTS:
    Nand(a=a, b=b, out=nandOut);
    Nand(a=nandOut, b=nandOut, out=out);
}
```
</details>

### Project 2: Boolean Arithmetic

**Goal:** Build an ALU (Arithmetic Logic Unit)

**Question:** How do computers actually add numbers?

<details>
<summary>Binary Addition</summary>

**Half Adder (adds 2 bits):**
```
Inputs: a, b
Outputs: sum, carry

Truth table:
a | b | sum | carry
--|---|-----|------
0 | 0 |  0  |  0
0 | 1 |  1  |  0
1 | 0 |  1  |  0
1 | 1 |  0  |  1    ← carry!

sum = XOR(a, b)
carry = AND(a, b)
```

**Full Adder (adds 3 bits - includes carry-in):**
```
sum = XOR(XOR(a, b), carry_in)
carry_out = OR(AND(a, b), AND(carry_in, XOR(a, b)))
```

**16-bit Adder:**
```
Chain 16 full adders together!
Each carry_out feeds into next carry_in
```

**ALU Operations:**
- Add (a + b)
- Subtract (a - b, using two's complement)
- AND (a & b)
- OR (a | b)
- NOT (negation)
- Zero check
- Negative check
</details>

### Project 3: Memory

**Question:** How do you store a bit?

<details>
<summary>Sequential Logic</summary>

**The Clock:**
```
Time: ___↑___↓___↑___↓___↑___↓___
        Cycle 1  Cycle 2  Cycle 3
```

**DFF (Data Flip-Flop) - primitive:**
```
OUT(t) = IN(t-1)
Stores previous input value
```

**Bit (1-bit register):**
```
if (load) then OUT(t) = IN(t-1)
else OUT(t) = OUT(t-1)  ← Remembers!
```

**Register (16-bit storage):**
```
16 Bit chips in parallel
```

**RAM (Random Access Memory):**
```
RAM8: 8 registers
RAM64: 8 RAM8 chips
RAM512: 8 RAM64 chips
RAM4K: 8 RAM512 chips
RAM16K: 4 RAM4K chips

Uses address to select which register to read/write
```

**Key Insight:** Memory holds state across clock cycles!
</details>

### Project 4: Machine Language

**Transition to software!**

**Question:** What is machine language?

<details>
<summary>The Hack Language</summary>

**A-instruction (Address):**
```
@value    →  Set A register to value
@100      →  A = 100
@sum      →  A = address of variable 'sum'
```

**C-instruction (Compute):**
```
dest = comp ; jump

Examples:
D=A          → D register = A register
D=D+1        → Increment D
M=D          → Memory[A] = D
D;JGT        → If D > 0, jump to address in A
```

**Example Program (sum 1 to 10):**
```assembly
// sum = 0
@sum
M=0

// i = 1
@i
M=1

(LOOP)
  // if i > 10 goto END
  @i
  D=M
  @10
  D=D-A
  @END
  D;JGT

  // sum = sum + i
  @i
  D=M
  @sum
  M=M+D

  // i = i + 1
  @i
  M=M+1

  // goto LOOP
  @LOOP
  0;JMP

(END)
  @END
  0;JMP    // Infinite loop (halt)
```
</details>

### Project 5: Computer Architecture

**The culmination of hardware: build the Hack computer!**

**Components:**
```
┌─────────────────────────────────┐
│         Hack Computer           │
├─────────────────────────────────┤
│  ┌─────┐  ┌────┐  ┌──────────┐ │
│  │ CPU │──│ROM │  │  Screen  │ │
│  └──┬──┘  └────┘  └──────────┘ │
│     │                           │
│  ┌──┴───┐    ┌──────────────┐  │
│  │ RAM  │    │  Keyboard    │  │
│  └──────┘    └──────────────┘  │
└─────────────────────────────────┘
```

**CPU Design:**
- Decode instruction
- Execute computation
- Update registers
- Handle jumps

**Your Task:** Wire everything together using the chips you've built!

---

## Part 3: Software Projects (6-13)

### Project 6: Assembler

**Goal:** Translate assembly (.asm) → machine code (.hack)

**Question:** What does an assembler do?

<details>
<summary>Two-Pass Assembly</summary>

**Pass 1: Build symbol table**
```
Scan for labels:
(LOOP)  → LOOP = current address
@sum    → sum = next available variable address
```

**Pass 2: Translate instructions**
```
@100     → 0000000001100100  (A-instruction)
D=M      → 1111110000010000  (C-instruction)
```

**Binary Encoding:**
```
A-instruction: 0 + 15-bit value
C-instruction: 111 + comp + dest + jump
```

**Implementation (your choice of language):**
```python
def assemble(asm_file):
    # Pass 1: symbols
    symbol_table = parse_labels(asm_file)

    # Pass 2: translate
    machine_code = []
    for line in asm_file:
        if is_a_instruction(line):
            machine_code.append(translate_a(line))
        else:
            machine_code.append(translate_c(line))

    return machine_code
```
</details>

### Project 7-8: Virtual Machine

**Goal:** Implement a VM translator (VM code → Assembly)

**Question:** Why have a virtual machine?

<details>
<summary>Stack-Based VM</summary>

**VM Commands:**
```
push constant 7    // Push 7 onto stack
push constant 8
add                // Pop two, push sum
pop temp 0         // Pop to temp variable
```

**Stack Model:**
```
      ┌───┐
      │ 15│  ← SP (stack pointer)
      ├───┤
      │ 8 │
      ├───┤
      │ 7 │
      ├───┤
      │...│
      └───┘
```

**Memory Segments:**
- argument: function arguments
- local: function local variables
- static: static variables
- constant: constants
- this/that: heap access
- pointer: this/that pointers
- temp: temp storage

**Why VM?**
- Platform independence
- Easier compilation target
- Optimization opportunities
</details>

### Project 9: High-Level Language

**Goal:** Write a program in Jack (Java-like language)

**Example Jack Program:**
```jack
class Main {
    function void main() {
        var int sum, i;
        let sum = 0;
        let i = 1;

        while (i < 11) {
            let sum = sum + i;
            let i = i + 1;
        }

        do Output.printInt(sum);
        return;
    }
}
```

**Features:**
- Object-oriented
- Classes and methods
- Primitive types (int, boolean, char)
- Arrays
- Strings

### Project 10-11: Compiler

**Goal:** Build Jack compiler (Jack → VM code)

**Compilation Stages:**
```
Jack Source Code
       ↓
Lexical Analysis (Tokenizer)
       ↓
Syntax Analysis (Parser)
       ↓
Code Generation (VM Code)
       ↓
VM Code
```

**Tokenizer:**
```jack
let x = 10;

Tokens:
KEYWORD: let
IDENTIFIER: x
SYMBOL: =
INT_CONST: 10
SYMBOL: ;
```

**Parser (builds parse tree):**
```
letStatement
├── keyword: let
├── identifier: x
├── symbol: =
├── expression
│   └── intConstant: 10
└── symbol: ;
```

**Code Generator:**
```
push constant 10
pop local 0       // Assuming x is local 0
```

### Project 12: Operating System

**Goal:** Implement OS in Jack

**Modules to implement:**
- **Math**: multiply, divide, sqrt
- **Memory**: alloc, deAlloc (heap management)
- **Screen**: drawPixel, drawLine, drawRectangle
- **Output**: printChar, printString
- **Keyboard**: keyPressed, readChar, readLine
- **String**: new, length, charAt
- **Array**: new
- **Sys**: init, halt, wait

**Example - Math.multiply:**
```jack
/** Returns the product of x and y. */
function int multiply(int x, int y) {
    var int sum, shiftedX, i;
    let sum = 0;
    let shiftedX = x;
    let i = 0;

    while (i < 16) {
        if (~((y & (1 << i)) = 0)) {
            let sum = sum + shiftedX;
        }
        let shiftedX = shiftedX + shiftedX;
        let i = i + 1;
    }

    return sum;
}
```

### Project 13: Applications

**Goal:** Write applications (games, etc.)

**Example: Tetris, Snake, Pong**

---

## Part 4: Learning Strategy

### How to Approach Each Project

**1. Read the Chapter**
- Understand the theory
- Study the API
- Review examples

**2. Design Before Coding**
- Sketch architecture
- Plan data structures
- Think about edge cases

**3. Implement Incrementally**
- Build simplest component first
- Test thoroughly
- Add complexity gradually

**4. Use the Hardware Simulator**
- Test each chip
- Use provided test scripts
- Debug with built-in tools

**5. Reflect**
- What did you learn?
- How does this connect to real computers?
- What would you do differently?

### Study Group Pattern

**Week 1:** Hardware (Projects 1-3)
- Day 1-2: Boolean logic
- Day 3-4: Arithmetic
- Day 5-7: Memory

**Week 2:** Hardware + Assembly (Projects 4-5)
- Day 1-3: Machine language
- Day 4-7: Computer architecture

**Week 3:** Software Tools (Projects 6-8)
- Day 1-3: Assembler
- Day 4-7: VM translator

**Week 4-5:** Compiler (Projects 9-11)
**Week 6:** OS + Applications (Projects 12-13)

---

## Part 5: Key Concepts and First Principles

### Digital Logic Fundamentals

**1. Boolean Algebra:**
- Everything is 0 or 1
- Basic operations: AND, OR, NOT
- Universal gates: NAND, NOR

**2. Abstraction:**
- Build complex from simple
- Hide implementation details
- Interface vs. implementation

**3. Composition:**
- Combine chips to build larger chips
- Hierarchical design
- Modularity

### Computer Architecture Principles

**1. Von Neumann Architecture:**
- Shared memory for data and instructions
- Fetch-Decode-Execute cycle
- Sequential execution

**2. Memory Hierarchy:**
- Registers (fastest)
- RAM (main memory)
- Storage (slowest)

**3. Instruction Set Architecture (ISA):**
- Interface between hardware and software
- A-instructions (addressing)
- C-instructions (computation)

### Software Engineering Principles

**1. Compilation:**
- High-level → Low-level
- Multiple stages
- Optimization opportunities

**2. Abstraction Layers:**
- Each layer provides services to layer above
- Uses services from layer below
- Independence and modularity

**3. Virtual Machines:**
- Platform independence
- Simplified compilation
- Runtime flexibility

---

## Part 6: Hands-On Exercises

### Exercise 1: Design a MUX
**Task:** Design a multiplexer using only NAND gates

**Specification:**
```
MUX(a, b, sel):
  if sel == 0: out = a
  if sel == 1: out = b
```

### Exercise 2: Optimize ALU
**Task:** Reduce the number of gates in the ALU design

**Consider:**
- Common subexpressions
- Gate reuse
- Critical path

### Exercise 3: Write Assembly Program
**Task:** Write Hack assembly for binary search

**Requirements:**
- Search sorted array
- Return index or -1
- Handle edge cases

### Exercise 4: Extend the VM
**Task:** Add new VM command

**Example:** `pow` - compute power
```
push constant 2
push constant 10
pow              // 2^10 = 1024
```

### Exercise 5: Jack Program
**Task:** Implement a linked list in Jack

**Methods:**
- append(value)
- remove(index)
- get(index)
- size()

---

## Part 7: Real-World Connections

### How Nand2Tetris Relates to Real Computers

**Differences:**
- Real CPUs: pipelining, superscalar, out-of-order execution
- Real memory: caches, virtual memory, MMU
- Real ISAs: x86, ARM, RISC-V (more complex)

**Similarities:**
- Same fundamental principles
- Same abstraction layers
- Same compilation process

### Modern Applications

**Hardware Design:**
- FPGAs programmed with HDL
- ASIC design uses similar principles
- Logic simulation and verification

**Compilers:**
- Same multi-stage process
- IR (intermediate representation) like VM code
- Optimization passes

**Virtual Machines:**
- JVM (Java Virtual Machine)
- Python interpreter
- WebAssembly

---

## How to Use This Guide with Claude Code CLI

```bash
claude code

# Ask questions like:
"Explain how to build an OR gate from NAND gates"
"Walk me through Project 3 on memory systems"
"Help me debug my ALU implementation"
"Explain the difference between A and C instructions"
"How does the assembler symbol table work?"
"Guide me through implementing the VM stack operations"
"Help me understand the Jack compilation process"
"Review my OS Math.multiply implementation"
```

**Interactive Learning:**
- Work through projects step-by-step
- Get explanations of difficult concepts
- Debug hardware and software implementations
- Explore connections to real-world systems
- Discuss design decisions and trade-offs
