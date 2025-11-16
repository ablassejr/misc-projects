# Spreadsheet - Education Aide
## Building a Spreadsheet from First Principles

### Overview
This guide teaches you how to build a spreadsheet application like Excel or Google Sheets. You'll combine challenges from text editors (cell management) and compilers (formula parsing) into one powerful application.

---

## Part 1: Understanding Spreadsheets

### Question 1: What is a Spreadsheet?
**Think about this:** What makes a spreadsheet different from a text editor or database?

**Your Answer:** _[Write your thoughts]_

<details>
<summary>Spreadsheet Concept</summary>

A spreadsheet is:
- **Grid of cells** - Data organized in rows and columns
- **Formulas** - Cells can contain calculations
- **Auto-recalculation** - Changes propagate automatically
- **Functions** - Built-in operations (SUM, AVERAGE, IF)
- **Formatting** - Display numbers, dates, currency

**Example:**
```
    A         B        C
1   Item      Price    Quantity
2   Apple     1.50     10
3   Banana    0.80     15
4   Total     =B2*C2   =B3*C3
5   Sum       =SUM(C2:C4)
```

**Key insight:** Cell C4 depends on B2 and C2. When they change, C4 must recalculate!
</details>

### Question 2: Core Challenges
**Question:** What are the two main technical challenges?

<details>
<summary>Two Hard Problems</summary>

**1. Efficient cell storage** (like text editor problem)
- Need to store thousands of cells
- Most cells are empty (sparse matrix)
- Fast access by coordinate (A1, B2)

**2. Formula evaluation** (like compiler problem)
- Parse formula syntax: `=SUM(A1:A10) + B2 * 2`
- Build expression tree
- Evaluate with cell references
- Handle dependencies
- Detect circular references

**This project combines both!**
</details>

---

## Part 2: Cell Storage

### Naive Approach

**Question:** How would you store cell data?

**Your Answer:** _[Describe your approach]_

<details>
<summary>2D Array Approach</summary>

```python
# Naive approach: 2D array
cells = [[None for _ in range(100)] for _ in range(100)]

# Set cell A1 (row 0, col 0)
cells[0][0] = "Hello"

# Get cell B2
value = cells[1][1]
```

**Problems:**
1. **Wastes memory** - Stores empty cells
2. **Fixed size** - Can't go beyond 100x100
3. **Sparse data** - Most cells are empty

**Example:** 1,000,000 cell grid with only 100 cells used wastes 99.99% of memory!
</details>

### Better Approach: Hash Map

**Question:** How do you store sparse data efficiently?

<details>
<summary>Dictionary/Hash Map Storage</summary>

```python
class Spreadsheet:
    def __init__(self):
        self.cells = {}  # Dictionary: "A1" -> Cell

    def set_cell(self, ref, value):
        """Set cell value"""
        self.cells[ref] = Cell(ref, value)

    def get_cell(self, ref):
        """Get cell value"""
        return self.cells.get(ref, Cell(ref, ""))

class Cell:
    def __init__(self, ref, value):
        self.ref = ref        # "A1"
        self.value = value    # Raw value: "=A2+1" or "Hello"
        self.result = None    # Computed result

# Usage
sheet = Spreadsheet()
sheet.set_cell("A1", "5")
sheet.set_cell("A2", "10")
sheet.set_cell("A3", "=A1+A2")

# Only 3 entries in dictionary, not 1 million!
```

**Advantages:**
- Only stores non-empty cells
- Grows dynamically
- Fast lookup: O(1) average case

**Used by:** Most spreadsheet implementations
</details>

---

## Part 3: Cell References

### Understanding Coordinates

**Question:** How do you convert "A1" to row/column numbers?

<details>
<summary>Cell Reference Parsing</summary>

```python
def parse_cell_ref(ref):
    """Convert 'A1' to (row, col) tuple"""
    # Separate letters and numbers
    col_str = ""
    row_str = ""

    for char in ref:
        if char.isalpha():
            col_str += char
        else:
            row_str += char

    # Convert column letters to number
    # A=0, B=1, ..., Z=25, AA=26, AB=27, etc.
    col = 0
    for char in col_str:
        col = col * 26 + (ord(char.upper()) - ord('A'))

    row = int(row_str) - 1  # Rows start at 1

    return (row, col)

# Test
print(parse_cell_ref("A1"))   # (0, 0)
print(parse_cell_ref("B2"))   # (1, 1)
print(parse_cell_ref("Z1"))   # (0, 25)
print(parse_cell_ref("AA1"))  # (0, 26)
print(parse_cell_ref("AB1"))  # (0, 27)

def cell_ref_to_string(row, col):
    """Convert (row, col) to 'A1' format"""
    result = ""

    # Convert column number to letters
    col += 1  # Make 1-based
    while col > 0:
        col -= 1
        result = chr(ord('A') + (col % 26)) + result
        col //= 26

    result += str(row + 1)
    return result

print(cell_ref_to_string(0, 0))   # A1
print(cell_ref_to_string(0, 26))  # AA1
```
</details>

### Relative vs Absolute References

**Question:** What happens when you copy a formula?

<details>
<summary>Reference Types</summary>

**Relative reference (A1):**
```
Cell B1: =A1
Copy B1 to C1: =B1  (reference shifts right)
Copy B1 to B2: =A2  (reference shifts down)
```

**Absolute reference ($A$1):**
```
Cell B1: =$A$1
Copy B1 to C1: =$A$1  (stays same)
Copy B1 to B2: =$A$1  (stays same)
```

**Mixed references:**
```
$A1  - Column absolute, row relative
A$1  - Row absolute, column relative
```

**Implementation:**
```python
class CellRef:
    def __init__(self, col, row, col_abs=False, row_abs=False):
        self.col = col
        self.row = row
        self.col_absolute = col_abs
        self.row_absolute = row_abs

    def offset(self, delta_row, delta_col):
        """Create new reference with offset"""
        new_row = self.row if self.row_absolute else self.row + delta_row
        new_col = self.col if self.col_absolute else self.col + delta_col
        return CellRef(new_col, new_row, self.col_absolute, self.row_absolute)

    def __str__(self):
        col_str = ('$' if self.col_absolute else '') + num_to_col(self.col)
        row_str = ('$' if self.row_absolute else '') + str(self.row + 1)
        return col_str + row_str

# Parse "$A$1"
def parse_ref(ref_str):
    col_abs = ref_str[0] == '$'
    if col_abs:
        ref_str = ref_str[1:]

    # Find where numbers start
    i = 0
    while i < len(ref_str) and ref_str[i].isalpha():
        i += 1

    col_str = ref_str[:i]
    row_str = ref_str[i:]

    row_abs = row_str[0] == '$'
    if row_abs:
        row_str = row_str[1:]

    col = col_to_num(col_str)
    row = int(row_str) - 1

    return CellRef(col, row, col_abs, row_abs)
```
</details>

---

## Part 4: Formula Parsing

### Understanding Formula Syntax

**Question:** How do you parse `=SUM(A1:A10) + B2 * 2`?

<details>
<summary>Formula Grammar</summary>

**Grammar (simplified):**
```
formula     → "=" expression
expression  → term (("+" | "-") term)*
term        → factor (("*" | "/") factor)*
factor      → number | cell_ref | function_call | "(" expression ")"
function    → IDENTIFIER "(" arguments ")"
arguments   → expression ("," expression)*
range       → cell_ref ":" cell_ref
```

**Tokenization:**
```
Input:  =SUM(A1:A10) + B2 * 2

Tokens:
  [EQUALS]
  [IDENTIFIER, "SUM"]
  [LPAREN]
  [CELL_REF, "A1"]
  [COLON]
  [CELL_REF, "A10"]
  [RPAREN]
  [PLUS]
  [CELL_REF, "B2"]
  [MULTIPLY]
  [NUMBER, 2]
```
</details>

### Building the Formula Parser

<details>
<summary>Formula Parser Implementation</summary>

```python
class FormulaLexer:
    def __init__(self, formula):
        self.formula = formula
        self.pos = 0
        self.current_char = formula[0] if formula else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.formula):
            self.current_char = self.formula[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return float(result) if '.' in result else int(result)

    def identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def cell_ref(self):
        result = ''
        # Handle absolute references: $A$1, $A1, A$1
        if self.current_char == '$':
            result += self.current_char
            self.advance()

        while self.current_char and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        if self.current_char == '$':
            result += self.current_char
            self.advance()

        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return result

    def next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token('NUMBER', self.number())

            if self.current_char.isalpha() or self.current_char == '$':
                # Could be cell ref or function name
                ref = self.cell_ref()
                # Check if function call (followed by '(')
                if self.current_char == '(':
                    return Token('FUNCTION', ref)
                else:
                    return Token('CELL_REF', ref)

            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')

            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')

            if self.current_char == '*':
                self.advance()
                return Token('MULTIPLY', '*')

            if self.current_char == '/':
                self.advance()
                return Token('DIVIDE', '/')

            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')

            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')

            if self.current_char == ':':
                self.advance()
                return Token('COLON', ':')

            if self.current_char == ',':
                self.advance()
                return Token('COMMA', ',')

            raise Exception(f'Invalid character: {self.current_char}')

        return Token('EOF', None)
```
</details>

### Evaluating Formulas

<details>
<summary>Formula Evaluator</summary>

```python
class FormulaEvaluator:
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet

    def evaluate(self, formula):
        """Evaluate a formula string"""
        if not formula.startswith('='):
            # Not a formula, just return the value
            try:
                return float(formula)
            except:
                return formula

        # Parse and evaluate
        lexer = FormulaLexer(formula[1:])  # Skip '='
        parser = FormulaParser(lexer)
        ast = parser.parse()
        return self.eval_node(ast)

    def eval_node(self, node):
        """Recursively evaluate AST node"""
        if isinstance(node, NumberNode):
            return node.value

        elif isinstance(node, CellRefNode):
            cell = self.spreadsheet.get_cell(node.ref)
            # Recursively evaluate the cell
            return self.evaluate(cell.value)

        elif isinstance(node, BinOpNode):
            left = self.eval_node(node.left)
            right = self.eval_node(node.right)

            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                return left / right

        elif isinstance(node, FunctionNode):
            return self.eval_function(node.name, node.args)

        elif isinstance(node, RangeNode):
            return self.get_range(node.start, node.end)

    def eval_function(self, name, args):
        """Evaluate built-in functions"""
        if name == 'SUM':
            total = 0
            for arg in args:
                value = self.eval_node(arg)
                if isinstance(value, list):
                    total += sum(value)
                else:
                    total += value
            return total

        elif name == 'AVERAGE':
            values = []
            for arg in args:
                value = self.eval_node(arg)
                if isinstance(value, list):
                    values.extend(value)
                else:
                    values.append(value)
            return sum(values) / len(values) if values else 0

        elif name == 'IF':
            condition = self.eval_node(args[0])
            if condition:
                return self.eval_node(args[1])
            else:
                return self.eval_node(args[2]) if len(args) > 2 else 0

        # Add more functions...

    def get_range(self, start_ref, end_ref):
        """Get all values in a range like A1:A10"""
        start_row, start_col = parse_cell_ref(start_ref)
        end_row, end_col = parse_cell_ref(end_ref)

        values = []
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                ref = cell_ref_to_string(row, col)
                cell = self.spreadsheet.get_cell(ref)
                value = self.evaluate(cell.value)
                try:
                    values.append(float(value))
                except:
                    pass  # Skip non-numeric

        return values
```
</details>

---

## Part 5: Dependency Graph

### The Dependency Problem

**Question:** What if A1 = A2 + 1 and A2 = A3 * 2?

<details>
<summary>Dependency Chain</summary>

**Problem:** When A3 changes, both A2 and A1 must recalculate!

**Dependency graph:**
```
A3 → A2 → A1

A3 changes → recalc A2 → recalc A1
```

**Algorithm:**
1. Track which cells depend on which
2. When cell changes, recalculate dependents
3. Use topological sort for order

**Implementation:**
```python
class DependencyGraph:
    def __init__(self):
        self.dependents = {}  # cell → set of cells that depend on it

    def add_dependency(self, cell, depends_on):
        """cell depends on depends_on"""
        if depends_on not in self.dependents:
            self.dependents[depends_on] = set()
        self.dependents[depends_on].add(cell)

    def get_dependents(self, cell):
        """Get all cells that depend on cell"""
        return self.dependents.get(cell, set())

    def get_all_dependents(self, cell):
        """Get all transitive dependents"""
        visited = set()
        to_visit = [cell]

        while to_visit:
            current = to_visit.pop()
            if current in visited:
                continue
            visited.add(current)

            for dependent in self.get_dependents(current):
                to_visit.append(dependent)

        return visited

# Usage
deps = DependencyGraph()
deps.add_dependency('A1', 'A2')  # A1 depends on A2
deps.add_dependency('A2', 'A3')  # A2 depends on A3

# A3 changes
to_recalc = deps.get_all_dependents('A3')
# Returns: {'A2', 'A1'}
```
</details>

### Circular Reference Detection

**Question:** What if A1 = A2 and A2 = A1?

<details>
<summary>Detecting Cycles</summary>

```python
class CircularReferenceError(Exception):
    pass

def has_cycle(graph, start):
    """Detect if there's a cycle starting from start"""
    visited = set()
    recursion_stack = set()

    def dfs(node):
        visited.add(node)
        recursion_stack.add(node)

        for neighbor in graph.get_dependents(node):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in recursion_stack:
                return True  # Cycle detected!

        recursion_stack.remove(node)
        return False

    return dfs(start)

# Check before evaluating
if has_cycle(deps, 'A1'):
    raise CircularReferenceError("Circular reference detected!")
```

**Error display:**
```
Cell A1: =A2
Cell A2: =A1
Result: #CIRCULAR!
```
</details>

---

## Part 6: User Interface

### Terminal-Based UI

<details>
<summary>Simple Text UI</summary>

```python
class SpreadsheetUI:
    def __init__(self):
        self.sheet = Spreadsheet()
        self.cursor_row = 0
        self.cursor_col = 0

    def display(self):
        # Print column headers
        print("    ", end="")
        for col in range(10):
            print(f"{chr(ord('A') + col):>8}", end="")
        print()

        # Print rows
        for row in range(20):
            print(f"{row+1:3} ", end="")
            for col in range(10):
                ref = cell_ref_to_string(row, col)
                cell = self.sheet.get_cell(ref)
                value = str(cell.result if cell.result is not None else cell.value)

                # Highlight cursor
                if row == self.cursor_row and col == self.cursor_col:
                    print(f"[{value:>6}]", end="")
                else:
                    print(f" {value:>6} ", end="")
            print()

    def run(self):
        while True:
            self.display()
            print(f"\nCursor: {cell_ref_to_string(self.cursor_row, self.cursor_col)}")
            print("Commands: arrow keys, e=edit, q=quit")

            cmd = input("> ")

            if cmd == 'q':
                break
            elif cmd == 'e':
                self.edit_cell()
            # Handle arrow keys...

    def edit_cell(self):
        ref = cell_ref_to_string(self.cursor_row, self.cursor_col)
        current = self.sheet.get_cell(ref).value
        new_value = input(f"Edit {ref} [{current}]: ")
        self.sheet.set_cell(ref, new_value)
        self.sheet.recalculate()
```
</details>

---

## Learning Projects

### Project 1: Basic Grid (1 week)
- [ ] 10x10 grid display
- [ ] Navigate with arrow keys
- [ ] Edit cells
- [ ] Display text and numbers

### Project 2: Formulas (2 weeks)
- [ ] Parse simple formulas (A1+A2)
- [ ] Evaluate expressions
- [ ] Cell references
- [ ] Auto-recalculation

### Project 3: Functions (2 weeks)
- [ ] SUM, AVERAGE
- [ ] COUNT, MIN, MAX
- [ ] IF function
- [ ] Range support (A1:A10)

### Project 4: Advanced (3 weeks)
- [ ] Dependency tracking
- [ ] Circular reference detection
- [ ] Copy/paste with formula adjustment
- [ ] Save/load files

---

## Resources

- [Spreadsheet Implementation](https://lord.io/spreadsheets/)
- [Building a Reactive Spreadsheet](https://jrsinclair.com/articles/2019/elegant-error-handling-with-the-js-either-monad/)
- Study: LibreOffice Calc, Ethercalc (open source)

---

**Key Takeaways:**

1. **Hash map storage** - Efficient for sparse data
2. **Formula parsing** - Like building a compiler
3. **Dependency graph** - Critical for auto-update
4. **Start simple** - Text/numbers first, formulas later

---

*"A spreadsheet is a compiler with a UI!"*
