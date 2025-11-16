# Text Editor - Education Aide
## Building a Text Editor from First Principles

### Overview
This guide walks you through understanding how text editors work internally, from simple character arrays to sophisticated data structures like ropes and piece tables. You'll learn the same concepts used in VS Code, Sublime, Vim, and Emacs.

---

## Part 1: Understanding the Problem

### Question 1: What Does a Text Editor Need to Do?
**Think about this:** Before we dive into code, what operations does a text editor need to support?

**Your Answer:** _[List the operations you think are essential]_

<details>
<summary>Essential Operations</summary>

A text editor must efficiently support:
1. **Display text** - Show the document content
2. **Navigate** - Move cursor around (arrow keys, Home, End, Page Up/Down)
3. **Insert** - Add characters at cursor position
4. **Delete** - Remove characters (Backspace, Delete key)
5. **Select** - Highlight regions of text
6. **Copy/Paste** - Duplicate text
7. **Save/Load** - Persist to files
8. **Undo/Redo** - Reverse changes

**Advanced operations:**
- Search and replace
- Syntax highlighting
- Multiple cursors
- Auto-complete
</details>

### Question 2: The Naive Approach
**Think about this:** What's the simplest way to store text in memory?

**Your Answer:** _[Describe your approach]_

<details>
<summary>Simple Approach - Array of Characters</summary>

The most obvious approach:
```c
char buffer[1000000];  // Fixed-size array
int cursor_position = 0;
```

**Try to answer:** What are the problems with this approach?

<details>
<summary>Problems with Array Approach</summary>

1. **Fixed size** - Must know maximum size ahead of time
2. **Insertion is O(n)** - Must shift all characters after cursor
3. **Deletion is O(n)** - Must shift characters to fill gap
4. **Wastes memory** - Allocates full size even for small files

Example of insertion problem:
```
Insert 'X' at position 2 in "HELLO"
Before: H E L L O _ _ _ _
After:  H E X L L O _ _ _
         ↑ ↑ ↑ ↑ ↑
         Must shift: L, L, O (3 characters)
```

For a 1MB file, inserting one character at the start requires shifting 1 million characters!
</details>
</details>

---

## Part 2: Better Data Structures

### The Gap Buffer

**Conceptual Question:** What if we keep a gap (empty space) where the cursor is?

**Your Answer:** _[Think about how this helps]_

<details>
<summary>Gap Buffer Concept</summary>

Keep an empty gap in the buffer at the cursor position:

```
Text: "HELLO WORLD"
Cursor after "HELLO" (before space)

Buffer representation:
H E L L O _ _ _ _ _   W O R L D
          ↑ cursor   ↑
        gap_start  gap_end
```

**Operations:**
- **Insert:** Place character at gap_start, increment gap_start
- **Delete:** Decrement gap_start (backspace) or increment gap_end (delete key)
- **Move cursor:** Move the gap to new position

**Time Complexity:**
- Insert at cursor: **O(1)** ✓
- Delete at cursor: **O(1)** ✓
- Move cursor: **O(n)** (must move gap)

**Try to answer:** When is gap buffer ideal? When is it bad?

<details>
<summary>Answer</summary>

**Ideal for:**
- Sequential editing (typing, backspacing)
- Most text editing is local to cursor position
- Used by: **Emacs**

**Bad for:**
- Jumping around the document (moves the gap)
- Multiple cursors
- Very large files

**Real-world performance:** Excellent for typical editing patterns!
</details>
</details>

### Implementation Exercise

**Exercise:** Implement a simple gap buffer

<details>
<summary>Gap Buffer Implementation in C</summary>

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *buffer;
    int gap_start;
    int gap_end;
    int size;
} GapBuffer;

GapBuffer* create_gap_buffer(int initial_size) {
    GapBuffer *gb = malloc(sizeof(GapBuffer));
    gb->buffer = malloc(initial_size);
    gb->gap_start = 0;
    gb->gap_end = initial_size;
    gb->size = initial_size;
    return gb;
}

void insert_char(GapBuffer *gb, char c) {
    if (gb->gap_start == gb->gap_end) {
        // Gap is full, need to resize
        int old_size = gb->size;
        gb->size *= 2;
        char *new_buffer = malloc(gb->size);

        // Copy text before gap
        memcpy(new_buffer, gb->buffer, gb->gap_start);

        // Copy text after gap
        int text_after = old_size - gb->gap_end;
        memcpy(new_buffer + gb->size - text_after,
               gb->buffer + gb->gap_end,
               text_after);

        gb->gap_end = gb->size - text_after;
        free(gb->buffer);
        gb->buffer = new_buffer;
    }

    gb->buffer[gb->gap_start++] = c;
}

void delete_char(GapBuffer *gb) {
    if (gb->gap_start > 0) {
        gb->gap_start--;  // Backspace
    }
}

void move_gap(GapBuffer *gb, int position) {
    if (position < gb->gap_start) {
        // Move gap left
        int distance = gb->gap_start - position;
        memmove(gb->buffer + gb->gap_end - distance,
                gb->buffer + position,
                distance);
        gb->gap_end -= distance;
        gb->gap_start = position;
    } else if (position > gb->gap_start) {
        // Move gap right
        int distance = position - gb->gap_start;
        memmove(gb->buffer + gb->gap_start,
                gb->buffer + gb->gap_end,
                distance);
        gb->gap_start += distance;
        gb->gap_end += distance;
    }
}

void print_gap_buffer(GapBuffer *gb) {
    // Print text before gap
    fwrite(gb->buffer, 1, gb->gap_start, stdout);

    // Print text after gap
    int text_after = gb->size - gb->gap_end;
    fwrite(gb->buffer + gb->gap_end, 1, text_after, stdout);
    printf("\n");
}

int main() {
    GapBuffer *gb = create_gap_buffer(10);

    // Type "HELLO"
    insert_char(gb, 'H');
    insert_char(gb, 'E');
    insert_char(gb, 'L');
    insert_char(gb, 'L');
    insert_char(gb, 'O');

    print_gap_buffer(gb);  // Output: HELLO

    delete_char(gb);       // Delete 'O'
    print_gap_buffer(gb);  // Output: HELL

    insert_char(gb, 'P');  // Add 'P'
    print_gap_buffer(gb);  // Output: HELLP

    return 0;
}
```

**Understanding Question:** What happens when you insert_char and the gap is full?

<details>
<summary>Answer</summary>
The buffer is resized (doubled), and the text is copied to the new buffer with a larger gap. This is similar to how dynamic arrays (std::vector) work.
</details>
</details>

---

## Part 3: The Rope Data Structure

### Conceptual Understanding

**Question:** What if we use a tree where each leaf holds a string fragment?

**Your Answer:** _[Think about advantages]_

<details>
<summary>Rope Concept</summary>

A **rope** is a binary tree where:
- **Leaf nodes** contain actual text (strings)
- **Internal nodes** store the total length of text in left subtree

Example: "Hello_World" as a rope:
```
        [11]              (total length)
       /    \
     [6]     [5]          (left subtree length)
     |        |
  "Hello_"  "World"       (actual text)
```

**Operations:**
- **Index [i]:** Traverse tree to find character at position i
- **Insert:** Split at position, create new node
- **Delete:** Split, remove middle, concatenate
- **Concatenate:** Create new root with two subtrees

**Time Complexity:**
- All operations: **O(log n)** on balanced tree
- Much better than O(n) for arrays!

**Used by:** VS Code (Monaco Editor), Xi Editor
</details>

### Rope Implementation Question

**Question:** How do you find character at index i in a rope?

**Your Answer:** _[Write algorithm in pseudocode]_

<details>
<summary>Rope Indexing Algorithm</summary>

```python
def get_char_at_index(node, index):
    if node.is_leaf():
        return node.text[index]

    left_length = node.left.weight

    if index < left_length:
        # Character is in left subtree
        return get_char_at_index(node.left, index)
    else:
        # Character is in right subtree
        return get_char_at_index(node.right, index - left_length)
```

**Trace example:** Find character at index 7 in "Hello_World" rope:
```
1. At root [11]: index 7 >= 6 (left weight), go right with index 7-6=1
2. At leaf "World": return "World"[1] = 'o'
```

**Time:** O(log n) for balanced tree - much faster than linear search!
</details>

### Rope Insert Algorithm

**Exercise:** How would you insert "BEAUTIFUL_" at position 6 in "Hello_World"?

<details>
<summary>Rope Insert Strategy</summary>

**Steps:**
1. Split at position 6: "Hello_" and "World"
2. Create new node for "BEAUTIFUL_"
3. Concatenate: "Hello_" + "BEAUTIFUL_" + "World"

**Visual:**
```
Before:
        [11]
       /    \
     [6]     [5]
     |        |
  "Hello_"  "World"

After insert "BEAUTIFUL_" at 6:
              [21]
            /      \
          [16]      [5]
         /    \      |
       [6]   [10]  "World"
        |      |
    "Hello_" "BEAUTIFUL_"

Result: "Hello_BEAUTIFUL_World"
```

**Key insight:** No copying of "Hello_" or "World" - just tree restructuring!
</details>

---

## Part 4: The Piece Table

### Understanding Piece Tables

**Question:** What if we never modify the original text, only track changes?

**Your Answer:** _[Think about how this could work]_

<details>
<summary>Piece Table Concept</summary>

A **piece table** has three components:

1. **Original buffer** - Never modified, contains original file
2. **Add buffer** - Contains all added text
3. **Piece descriptor table** - Sequence of pieces pointing to buffers

**Example:** Start with "HELLO WORLD"

Original buffer: `"HELLO WORLD"`
Add buffer: (empty)
Pieces: `[(original, 0, 11)]`  // (buffer, offset, length)

**After inserting "BEAUTIFUL " at position 6:**

Original buffer: `"HELLO WORLD"` (unchanged!)
Add buffer: `"BEAUTIFUL "`
Pieces: `[(original, 0, 6), (add, 0, 10), (original, 6, 5)]`

Reading the text: Concatenate pieces:
- Piece 1: original[0:6] = "HELLO "
- Piece 2: add[0:10] = "BEAUTIFUL "
- Piece 3: original[6:11] = "WORLD"
- Result: "HELLO BEAUTIFUL WORLD"

**Advantages:**
- Original file never modified (great for undo!)
- Efficient for large files
- Multiple views can share original buffer

**Used by:** VS Code, Microsoft Word
</details>

### Piece Table for Undo/Redo

**Question:** Why is piece table perfect for undo/redo?

**Your Answer:** _[Think about how undo would work]_

<details>
<summary>Undo/Redo with Piece Tables</summary>

**Key insight:** Undo/Redo is just managing piece table states!

```
Initial state:
Pieces: [(original, 0, 11)]  // "HELLO WORLD"

After insert "BEAUTIFUL " at 6:
Pieces: [(original, 0, 6), (add, 0, 10), (original, 6, 5)]

Undo:
Pieces: [(original, 0, 11)]  // Just restore previous pieces!

Redo:
Pieces: [(original, 0, 6), (add, 0, 10), (original, 6, 5)]
```

**Implementation:**
- Save piece table snapshots on undo stack
- Undo = pop stack, restore pieces
- No need to reverse operations!
- Add buffer keeps growing (can be garbage collected later)

**Why this is brilliant:**
- O(1) undo/redo (just swap piece table)
- Handles complex multi-cursor edits easily
- Memory efficient (share buffers)
</details>

---

## Part 5: Building Your First Editor

### Milestone 1: Array-Based Editor

**Exercise:** Implement basic editor with array of lines

<details>
<summary>Simple Line-Based Editor (Python)</summary>

```python
class SimpleEditor:
    def __init__(self):
        self.lines = [""]
        self.cursor_row = 0
        self.cursor_col = 0

    def insert_char(self, char):
        line = self.lines[self.cursor_row]
        self.lines[self.cursor_row] = (
            line[:self.cursor_col] + char + line[self.cursor_col:]
        )
        self.cursor_col += 1

    def delete_char(self):
        if self.cursor_col > 0:
            line = self.lines[self.cursor_row]
            self.lines[self.cursor_row] = (
                line[:self.cursor_col-1] + line[self.cursor_col:]
            )
            self.cursor_col -= 1

    def insert_newline(self):
        line = self.lines[self.cursor_row]
        # Split current line
        self.lines[self.cursor_row] = line[:self.cursor_col]
        self.lines.insert(self.cursor_row + 1, line[self.cursor_col:])
        self.cursor_row += 1
        self.cursor_col = 0

    def move_cursor(self, delta_row, delta_col):
        self.cursor_row = max(0, min(len(self.lines)-1,
                                      self.cursor_row + delta_row))
        max_col = len(self.lines[self.cursor_row])
        self.cursor_col = max(0, min(max_col,
                                      self.cursor_col + delta_col))

    def display(self):
        for i, line in enumerate(self.lines):
            if i == self.cursor_row:
                # Show cursor position
                print(line[:self.cursor_col] + '|' + line[self.cursor_col:])
            else:
                print(line)
        print(f"Cursor: ({self.cursor_row}, {self.cursor_col})")

# Test it
editor = SimpleEditor()
editor.insert_char('H')
editor.insert_char('e')
editor.insert_char('l')
editor.insert_char('l')
editor.insert_char('o')
editor.display()

# Output:
# Hello|
# Cursor: (0, 5)
```

**Question:** What's the time complexity of insert_char?

<details>
<summary>Answer</summary>
O(n) where n is line length - we create a new string by concatenating three parts. Python strings are immutable, so this requires copying.

**Better approach:** Use a list of characters or a gap buffer per line.
</details>
</details>

### Milestone 2: Terminal UI with curses

**Question:** How do text editors handle keyboard input and screen rendering?

<details>
<summary>Terminal-Based Editor with curses (Python)</summary>

```python
import curses

def main(stdscr):
    curses.curs_set(1)  # Show cursor
    stdscr.clear()

    lines = [""]
    cursor_row = 0
    cursor_col = 0

    while True:
        # Display
        stdscr.clear()
        for i, line in enumerate(lines):
            stdscr.addstr(i, 0, line)

        # Move cursor to position
        stdscr.move(cursor_row, cursor_col)
        stdscr.refresh()

        # Get key
        key = stdscr.getch()

        if key == ord('q') and curses.keyname(key) == b'q':
            break
        elif key == curses.KEY_UP:
            cursor_row = max(0, cursor_row - 1)
            cursor_col = min(cursor_col, len(lines[cursor_row]))
        elif key == curses.KEY_DOWN:
            cursor_row = min(len(lines) - 1, cursor_row + 1)
            cursor_col = min(cursor_col, len(lines[cursor_row]))
        elif key == curses.KEY_LEFT:
            cursor_col = max(0, cursor_col - 1)
        elif key == curses.KEY_RIGHT:
            cursor_col = min(len(lines[cursor_row]), cursor_col + 1)
        elif key == curses.KEY_BACKSPACE or key == 127:
            if cursor_col > 0:
                line = lines[cursor_row]
                lines[cursor_row] = line[:cursor_col-1] + line[cursor_col:]
                cursor_col -= 1
        elif key == ord('\n'):
            line = lines[cursor_row]
            lines[cursor_row] = line[:cursor_col]
            lines.insert(cursor_row + 1, line[cursor_col:])
            cursor_row += 1
            cursor_col = 0
        elif 32 <= key <= 126:  # Printable characters
            char = chr(key)
            line = lines[cursor_row]
            lines[cursor_row] = line[:cursor_col] + char + line[cursor_col:]
            cursor_col += 1

curses.wrapper(main)
```

**Understanding:** This creates a basic text editor in the terminal!
- Arrow keys move cursor
- Type to insert characters
- Backspace deletes
- Enter creates new line
- Press 'q' to quit
</details>

---

## Part 6: Advanced Features

### Undo/Redo with Command Pattern

**Question:** How do you implement multi-level undo/redo?

<details>
<summary>Command Pattern for Undo/Redo</summary>

**Concept:** Each edit is a command object that can be undone/redone

```python
class Command:
    def execute(self):
        pass

    def undo(self):
        pass

class InsertCommand(Command):
    def __init__(self, editor, position, text):
        self.editor = editor
        self.position = position
        self.text = text

    def execute(self):
        self.editor.insert(self.position, self.text)

    def undo(self):
        self.editor.delete(self.position, len(self.text))

class DeleteCommand(Command):
    def __init__(self, editor, position, length):
        self.editor = editor
        self.position = position
        self.length = length
        self.deleted_text = None

    def execute(self):
        self.deleted_text = self.editor.get_text(
            self.position, self.length
        )
        self.editor.delete(self.position, self.length)

    def undo(self):
        self.editor.insert(self.position, self.deleted_text)

class Editor:
    def __init__(self):
        self.text = ""
        self.undo_stack = []
        self.redo_stack = []

    def execute_command(self, command):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()  # Clear redo after new command

    def undo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)

    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.undo_stack.append(command)

# Usage
editor = Editor()
editor.execute_command(InsertCommand(editor, 0, "Hello"))
editor.execute_command(InsertCommand(editor, 5, " World"))
editor.undo()  # Remove " World"
editor.redo()  # Add " World" back
```
</details>

### Syntax Highlighting

**Question:** How do editors colorize code?

<details>
<summary>Basic Syntax Highlighting Approach</summary>

**Tokenization + Coloring:**

```python
import re

def highlight_python(line):
    # Simple regex-based highlighter
    keywords = r'\b(def|class|if|else|for|while|return|import)\b'
    strings = r'(\".*?\"|\'.*?\')'
    comments = r'(#.*$)'
    numbers = r'\b\d+\b'

    # Replace with ANSI color codes
    line = re.sub(keywords, r'\033[94m\1\033[0m', line)  # Blue
    line = re.sub(strings, r'\033[92m\1\033[0m', line)   # Green
    line = re.sub(comments, r'\033[90m\1\033[0m', line)  # Gray
    line = re.sub(numbers, r'\033[93m\1\033[0m', line)   # Yellow

    return line

# Test
code = "def hello(): # function"
print(highlight_python(code))
```

**Modern approach:** Use Tree-sitter for accurate parsing
- Builds syntax tree
- Handles nested structures
- Used by Atom, Neovim, GitHub
</details>

---

## Part 7: Learning Projects

### Project 1: Build Minimal Editor (1 week)
**Requirements:**
- [ ] Display text file
- [ ] Arrow key navigation
- [ ] Insert/delete characters
- [ ] Save to file
- [ ] Works in terminal

### Project 2: Add Advanced Editing (2 weeks)
**Requirements:**
- [ ] Undo/redo (10 levels)
- [ ] Copy/paste
- [ ] Search (find text)
- [ ] Line numbers
- [ ] Status bar

### Project 3: Optimize for Large Files (2 weeks)
**Requirements:**
- [ ] Implement gap buffer or rope
- [ ] Handle 1MB+ files smoothly
- [ ] Lazy loading (don't load entire file)
- [ ] Efficient rendering (only visible lines)

### Project 4: Syntax Highlighting (1 week)
**Requirements:**
- [ ] Detect file type
- [ ] Tokenize code
- [ ] Colorize keywords, strings, comments
- [ ] Support at least 2 languages

---

## Resources

### Books
- "The Craft of Text Editing" by Craig A. Finseth (free online)
- "Build Your Own Text Editor" - kilo tutorial (C)

### Articles
- [Text Editor Data Structures](https://www.averylaird.com/programming/the%20text%20editor/2017/09/30/the-piece-table)
- [Rope Science](https://xi-editor.io/docs/rope_science_00.html)
- [VS Code Text Buffer Reimplementation](https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation)

### Open Source Editors to Study
- **kilo** - 1000 line editor in C
- **nano** - Small, simple editor
- **micro** - Modern terminal editor (Go)
- **xi-editor** - Modern architecture (Rust)

---

## Key Takeaways

1. **Data structure matters:** Choice of buffer representation affects performance
2. **Trade-offs exist:** Gap buffer fast for local edits, rope better for random access
3. **Undo/redo design:** Piece tables make this natural
4. **Start simple:** Array of lines works fine for learning
5. **Optimize later:** Profile before optimizing

---

**Next Challenge:** Build a basic editor this weekend, then improve it iteratively!

*Happy editing!*
