# Spreadsheet Application

## Overview
Build a spreadsheet application like Excel or Google Sheets to combine challenges from text editors and compilers - efficient cell storage and formula evaluation.

## The Challenge
This project **combines the challenges of writing a text editor and a compiler**:
- Text editor: Managing cells and their content efficiently
- Compiler: Parsing and evaluating formulas with cell references

## Core Features to Implement

### Phase 1: Basic Grid
- [ ] Display grid of cells
- [ ] Cell selection and navigation
- [ ] Edit cell contents
- [ ] Display values in cells
- [ ] Resize columns and rows

### Phase 2: Data Types
- [ ] Numbers (integer and float)
- [ ] Text/strings
- [ ] Dates
- [ ] Booleans
- [ ] Type detection and formatting

### Phase 3: Formulas
- [ ] Formula parser (starting with =)
- [ ] Basic operators (+, -, *, /)
- [ ] Cell references (A1, B2)
- [ ] Formula evaluation
- [ ] Display formula vs value

### Phase 4: Functions
- [ ] SUM, AVERAGE, MIN, MAX
- [ ] COUNT, COUNTA
- [ ] IF statements
- [ ] Mathematical functions (SQRT, POWER)
- [ ] String functions (CONCAT, LEFT, RIGHT)

### Phase 5: Advanced Features
- [ ] Cell ranges (A1:B10)
- [ ] Absolute/relative references ($A$1, $A1, A$1)
- [ ] Auto-recalculation
- [ ] Dependency tracking
- [ ] Circular reference detection
- [ ] Copy/paste with formula adjustment
- [ ] File save/load

### Expert Features
- [ ] Charts and graphs
- [ ] Conditional formatting
- [ ] Data validation
- [ ] Pivot tables
- [ ] Multiple sheets
- [ ] Macros/scripting
- [ ] Real-time collaboration

## Key Concepts

### Cell Storage
- **2D Array:** Simple but wastes memory for sparse sheets
- **Hash Map:** Key is "A1", "B2", value is cell content
- **Compressed Column Storage:** For very large sparse sheets
- **R-Tree:** For spatial queries

### Formula Evaluation

#### Parsing Formulas
```
=SUM(A1:A10) + B2 * 2

Tokens: [SUM, (, A1:A10, ), +, B2, *, 2]
AST:
    +
   / \
  SUM  *
  /    / \
 A1:A10 B2 2
```

#### Dependency Graph
- Track which cells depend on which
- Recalculate in correct order
- Detect circular dependencies
- Optimize by only recalculating changed cells

### Formula Language Grammar

```
formula     → "=" expression
expression  → term (("+" | "-") term)*
term        → factor (("*" | "/") factor)*
factor      → number | string | cell_ref | function_call | "(" expression ")"
function    → identifier "(" arguments ")"
arguments   → expression ("," expression)*
cell_ref    → column row | range
range       → cell_ref ":" cell_ref
```

## Learning Objectives
- Grid data structure design
- Formula parsing and evaluation
- Dependency graph management
- Cell reference resolution
- Type system implementation
- Event-driven updates
- User interface design
- File format handling (CSV, custom format)

## Technology Suggestions

### Language
- **JavaScript:** Easy UI with HTML canvas or tables
- **Python:** Good for logic, use tkinter/Qt for UI
- **C++:** Qt for professional-looking UI
- **Rust:** egui or iced for GUI
- **Java:** Swing or JavaFX

### Architecture
- **Model-View-Controller:** Separate data from display
- **Observer Pattern:** Cells notify dependents of changes
- **Command Pattern:** For undo/redo functionality

## Implementation Tips

1. **Start Small:** 10×10 grid with just text
2. **Add Navigation:** Arrow keys, mouse clicks
3. **Implement Editing:** Click to edit, Enter to confirm
4. **Add Numbers:** Parse and format numbers
5. **Simple Formulas:** Just +, -, *, / first
6. **Cell References:** A1, B2 notation
7. **Functions:** Start with SUM
8. **Dependency Tracking:** Recalculate dependent cells
9. **Advanced Features:** Once basics are solid

## Milestones

### Milestone 1: Static Grid
- Display grid
- Navigate with arrow keys
- Edit cells
- Store text and numbers

### Milestone 2: Basic Formulas
```
A1: 5
A2: 10
A3: =A1 + A2    (displays 15)
```

### Milestone 3: Functions
```
A1: 1
A2: 2
A3: 3
A4: =SUM(A1:A3)    (displays 6)
```

### Milestone 4: Auto-Update
```
A1: 5
A2: =A1 * 2        (displays 10)
(Change A1 to 7)
A2: (automatically updates to 14)
```

### Milestone 5: Complete Application
- Multiple sheets
- Save/load files
- Charts
- Advanced functions
- Professional UI

## Example Cell Reference System

### Relative References (A1)
```
If A1 contains: =B1
Copy A1 to A2: =B2  (reference adjusts)
```

### Absolute References ($A$1)
```
If A1 contains: =$B$1
Copy A1 to A2: =$B$1  (reference stays same)
```

### Mixed References ($A1 or A$1)
```
$A1: Column absolute, row relative
A$1: Row absolute, column relative
```

## Dependency Graph Example

```
A1: 5
A2: =A1 * 2
A3: =A1 + A2
B1: =A2 + 10

Dependency graph:
A1 → A2 → A3
A2 → B1

Evaluation order when A1 changes:
1. A1
2. A2 (depends on A1)
3. A3 (depends on A2)
4. B1 (depends on A2)
```

## Resources
- [Spreadsheet Implementation](https://lord.io/spreadsheets/) - Architecture discussion
- [Building a Reactive Spreadsheet](https://jrsinclair.com/articles/2019/elegant-error-handling-with-the-js-either-monad/) - Functional approach
- [Formula Parsing](https://www.codeproject.com/Articles/1214409/Formula-Parser) - Implementation guide
- [Topological Sort](https://en.wikipedia.org/wiki/Topological_sorting) - For dependency resolution

## Extensions
- **Import/Export:** Excel (.xlsx), CSV, Google Sheets
- **Charts:** Line, bar, pie, scatter plots
- **Conditional Formatting:** Color cells based on rules
- **Data Validation:** Dropdown lists, number ranges
- **Pivot Tables:** Data summarization
- **Macros:** Record and playback actions
- **JavaScript API:** Scriptable spreadsheet
- **Web App:** Real-time collaboration
- **Database Connection:** Import from SQL
- **Add-ins/Plugins:** Extend functionality
- **Mobile App:** Touch-friendly interface
- **Version History:** Track changes over time

## Common Pitfalls
- Circular dependency crashes (A1=B1, B1=A1)
- Not handling formula errors gracefully (#DIV/0!, #REF!)
- Inefficient recalculation (recalculating entire sheet)
- Memory usage with large sheets
- Copy/paste not adjusting references correctly
- Floating-point precision issues
- Race conditions in async recalculation

## File Format Considerations

### Simple CSV
```csv
Name,Age,Score
Alice,25,95
Bob,30,87
```

### Custom Format (JSON)
```json
{
  "sheets": [
    {
      "name": "Sheet1",
      "cells": {
        "A1": {"value": "Name", "type": "string"},
        "B1": {"value": "Age", "type": "string"},
        "A2": {"formula": "=UPPER(\"Alice\")", "value": "ALICE"}
      }
    }
  ]
}
```

### Excel XLSX
- Use library (OpenPyXL for Python, Apache POI for Java)
- ZIP file containing XML documents
- Complex format, use existing libraries

## Estimated Time
- **Basic grid with editing:** 1-2 weeks
- **With simple formulas:** 3-4 weeks
- **With functions and dependencies:** 2-3 months
- **Excel-like features:** 6-12 months
- **Google Sheets competitor:** 1-2 years with team

## Real-World Examples to Study
- **Pyspread:** Python-based spreadsheet
- **Ethercalc:** Web-based collaborative spreadsheet
- **SC-IM:** Terminal-based spreadsheet (vim-like)
- **LibreOffice Calc:** Open-source Excel alternative
- **TinySheet:** Minimal JavaScript implementation

---

*From Austin Z. Henley's "Challenging Projects Every Programmer Should Try"*
