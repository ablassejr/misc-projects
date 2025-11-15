# Git Tools - Education Aide
## Understanding Command-Line Interface Development in C

### Overview
This guide walks you through building a command-line tool router for Git and GitHub CLI, covering argument parsing, enums, and program design.

---

## Part 1: Understanding the Problem

### What Are We Building?

**Goal:** A CLI tool (`gt`) that routes commands to either `git` or `gh` (GitHub CLI).

**Usage Examples:**
```bash
$ gt git status
$ gt gh pr list
$ gt git commit -m "message"
```

**Question:** Why build a router instead of just using `git` and `gh` directly?

**Your Thoughts:** _[Think about use cases]_

<details>
<summary>Potential Use Cases</summary>

**Reasons to build CLI routers:**
1. **Unified interface** - One command for multiple tools
2. **Add logging** - Track all git/gh commands
3. **Add authentication** - Centralized auth handling
4. **Aliases and shortcuts** - Custom command abbreviations
5. **Company-specific workflows** - Enforce policies
6. **Learning** - Understand CLI tool design!

**Real-world examples:**
- `hub` - GitHub wrapper for git
- `gh` - GitHub's official CLI
- `meta` - Meta-repo management tool
</details>

---

## Part 2: Command-Line Arguments

### The main() Function Signature

**Study the code (gt.c:9-11):**
```cpp
int main(int argc, char *argv[]) {
  char *filename = argv[0];
  char *command = argv[1];
```

**Question:** What are `argc` and `argv`?

**Your Understanding:** _[Explain in your own words]_

<details>
<summary>Understanding Command-Line Arguments</summary>

**When you run:**
```bash
$ gt git status
```

**The OS passes:**
```c
argc = 3                    // Argument count
argv[0] = "gt"             // Program name
argv[1] = "git"            // First argument
argv[2] = "status"         // Second argument
argv[3] = NULL             // Null terminator
```

**Visual Model:**
```
Command: ./gt git status

┌──────┬────────────┐
│ argc │     3      │
├──────┼────────────┤
│argv  │ ┌────────┐ │
│  [0] │ │  "gt"  │ │
│  [1] │ │  "git" │ │
│  [2] │ │"status"│ │
│  [3] │ │  NULL  │ │
│      │ └────────┘ │
└──────┴────────────┘
```

**Important Points:**
- `argv[0]` is always the program name
- `argc` counts all arguments including program name
- `argv[argc]` is always NULL
- Array of C strings (char pointers)
</details>

### Argument Parsing

**Critical Question:** What happens if user runs `gt` with no arguments?

**Study this code:**
```c
char *command = argv[1];  // Accessing argv[1]
```

**Your Analysis:** _[Is this safe?]_

<details>
<summary>Buffer Overflow / Segmentation Fault</summary>

**The Problem:**
```bash
$ gt
# argc = 1
# argv[0] = "gt"
# argv[1] = ???  ← Accessing beyond array!
```

**Result:** Segmentation fault!

**Safe Approach:**
```c
int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <git|gh> <command> [args...]\n", argv[0]);
        return 1;
    }

    char *tool = argv[1];
    // Now safe to access argv[1]
```

**Better: Check all required args:**
```c
if (argc < 3) {
    fprintf(stderr, "Usage: %s <git|gh> <command> [args...]\n", argv[0]);
    fprintf(stderr, "Example: %s git status\n", argv[0]);
    return 1;
}

char *tool = argv[1];
char *command = argv[2];
```
</details>

---

## Part 3: Enumerations in C

### Understanding Enums

**Study the code (gt.c:7):**
```c
enum GitTool { GH, GIT };
```

**Question:** What is an enum and why use it?

**Your Understanding:** _[How is this different from #define?]_

<details>
<summary>Enum Fundamentals</summary>

**An enum creates a new type with named constants:**

```c
enum GitTool { GH, GIT };
// GH = 0
// GIT = 1
```

**Behind the scenes:**
```c
// Compiler translates to integers
enum GitTool { GH = 0, GIT = 1 };
```

**Alternative Approaches:**

**#define (bad):**
```c
#define GH 0
#define GIT 1
// No type checking!
```

**const int (better):**
```c
const int GH = 0;
const int GIT = 1;
// Type checking, but uses memory
```

**enum (best for this):**
```c
enum GitTool { GH, GIT };
enum GitTool tool;  // Type-safe variable
// Compiler can optimize, no memory if not stored
```

**Benefits of enum:**
1. **Type safety** - Can't assign wrong values
2. **Readability** - `tool = GIT` vs `tool = 1`
3. **Debugger support** - Shows names not numbers
4. **Compiler optimization** - Can be compile-time constants

**Custom Values:**
```c
enum HttpStatus {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
};
```
</details>

### Using Enums

**Study the code (gt.c:16-18):**
```c
strcmp(argv[1], "git") == 0  ? tool = GIT
: strcmp(argv[1], "gh") == 0 ? tool = GH
                             : exit(1);
```

**Question:** Is this good code style?

**Your Opinion:** _[Evaluate readability and safety]_

<details>
<summary>Code Style Analysis</summary>

**Problems with the ternary chain:**
1. **Hard to read** - Ternary operators nested
2. **No error message** - Silent `exit(1)`
3. **Inconsistent** - Why check "git" first, then "gh"?
4. **Format** - Unconventional formatting

**Better Approach - if/else:**
```c
enum GitTool tool;

if (strcmp(argv[1], "git") == 0) {
    tool = GIT;
} else if (strcmp(argv[1], "gh") == 0) {
    tool = GH;
} else {
    fprintf(stderr, "Error: Unknown tool '%s'\n", argv[1]);
    fprintf(stderr, "Supported tools: git, gh\n");
    return 1;
}
```

**Even Better - Function:**
```c
enum GitTool parse_tool(const char *name) {
    if (strcmp(name, "git") == 0) return GIT;
    if (strcmp(name, "gh") == 0) return GH;

    fprintf(stderr, "Error: Unknown tool '%s'\n", name);
    fprintf(stderr, "Supported tools: git, gh\n");
    exit(1);
}

// Usage:
enum GitTool tool = parse_tool(argv[1]);
```

**Advanced - Lookup Table:**
```c
struct ToolMapping {
    const char *name;
    enum GitTool tool;
};

struct ToolMapping tools[] = {
    {"git", GIT},
    {"gh", GH},
    {NULL, 0}
};

enum GitTool parse_tool(const char *name) {
    for (int i = 0; tools[i].name != NULL; i++) {
        if (strcmp(name, tools[i].name) == 0) {
            return tools[i].tool;
        }
    }
    fprintf(stderr, "Unknown tool: %s\n", name);
    exit(1);
}
```
</details>

---

## Part 4: The Switch Statement

**Study the code (gt.c:19-26):**
```c
switch (tool) {
case GIT:
  printf("Using Git tool\n");
  break;
case GH:
  printf("Using GitHub CLI tool\n");
  break;
}
```

**Question:** What happens if you forget `break`?

**Your Prediction:** _[Trace the execution]_

<details>
<summary>Fall-through Behavior</summary>

**Without break:**
```c
switch (tool) {
case GIT:
  printf("Using Git tool\n");
  // No break! Falls through to next case
case GH:
  printf("Using GitHub CLI tool\n");
  // No break! Falls through (but nothing after)
}
```

**Result if tool == GIT:**
```
Using Git tool
Using GitHub CLI tool    ← Also executes!
```

**This is called "fall-through" and is usually a bug!**

**Intentional Fall-through (valid use):**
```c
switch (ch) {
case 'a':
case 'e':
case 'i':
case 'o':
case 'u':
    printf("Vowel\n");
    break;
default:
    printf("Consonant\n");
    break;
}
```

**Modern C: Annotate intentional fall-through:**
```c
switch (value) {
case 1:
    setup();
    __attribute__((fallthrough));  // Intentional
case 2:
    process();
    break;
}
```
</details>

### Default Case

**Question:** Should we add a `default` case?

**Your Thought:** _[Is it needed here?]_

<details>
<summary>Default Case Discussion</summary>

**Current code:**
```c
switch (tool) {
case GIT:
    printf("Using Git tool\n");
    break;
case GH:
    printf("Using GitHub CLI tool\n");
    break;
// No default!
}
```

**Question:** Can `tool` have a value other than GIT or GH?

**Answer:** Not in this code! We only assign GIT or GH (or exit).

**But consider:**
```c
enum GitTool tool = 99;  // Invalid but compiles!
switch (tool) {
    case GIT: /* ... */ break;
    case GH: /* ... */ break;
    // Silently does nothing!
}
```

**Best Practice - Always add default:**
```c
switch (tool) {
case GIT:
    printf("Using Git tool\n");
    break;
case GH:
    printf("Using GitHub CLI tool\n");
    break;
default:
    fprintf(stderr, "Internal error: Invalid tool\n");
    exit(1);
}
```

**Why?**
- Catches programming errors
- Makes intent clear
- Compiler warnings if enum expanded but switch not updated
</details>

---

## Part 5: Actually Executing Commands

### The Missing Piece

**Question:** The current code just prints messages. How do we actually execute `git` or `gh`?

**Your Implementation:** _[How would you call the real git/gh?]_

<details>
<summary>System Call Options</summary>

**Option 1: system() (simple but limited):**
```c
#include <stdlib.h>

switch (tool) {
case GIT:
    system("git status");  // Hardcoded!
    break;
}
```

**Problems:**
- Hardcoded command
- Can't pass user arguments
- Security risk (command injection)

**Option 2: Build command string (dangerous!):**
```c
char command[1024];
sprintf(command, "git %s", argv[2]);  // Buffer overflow risk!
system(command);  // Command injection risk!
```

**Option 3: execvp() (best!):**
```c
#include <unistd.h>

switch (tool) {
case GIT:
    execvp("git", &argv[1]);  // Pass all args starting from "git"
    perror("execvp failed");
    exit(1);
    break;
}
```

**Complete Implementation:**
```c
int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <git|gh> <command> [args...]\n", argv[0]);
        return 1;
    }

    enum GitTool tool;
    if (strcmp(argv[1], "git") == 0) {
        tool = GIT;
    } else if (strcmp(argv[1], "gh") == 0) {
        tool = GH;
    } else {
        fprintf(stderr, "Unknown tool: %s\n", argv[1]);
        return 1;
    }

    // Execute the appropriate command
    // argv[1] is "git" or "gh"
    // argv[2..] are the actual command and arguments
    execvp(argv[1], &argv[1]);

    // Only reaches here if execvp fails
    perror("execvp failed");
    return 1;
}
```

**How it works:**
```
User runs: gt git status

argv = ["gt", "git", "status", NULL]

execvp("git", &argv[1])
       ↑       ↑
       |       Points to ["git", "status", NULL]
       Program to execute

Result: Replaces current process with "git status"
```
</details>

---

## Part 6: Hands-On Exercises

### Exercise 1: Add Error Handling
**Task:** Add proper error handling for missing arguments.

**Test cases:**
```bash
$ gt                    # No arguments
$ gt git                # No command
$ gt python status      # Invalid tool
```

### Exercise 2: Add Logging
**Task:** Log all commands to a file before executing.

**Implementation:**
```c
void log_command(int argc, char *argv[]) {
    FILE *log = fopen(".gt_history", "a");
    if (!log) return;

    time_t now = time(NULL);
    fprintf(log, "[%s] ", ctime(&now));

    for (int i = 0; i < argc; i++) {
        fprintf(log, "%s ", argv[i]);
    }
    fprintf(log, "\n");
    fclose(log);
}
```

### Exercise 3: Add Help Command
**Task:** Implement `gt help` to show usage information.

**Implementation:**
```c
void show_help(const char *program) {
    printf("Usage: %s <tool> <command> [args...]\n\n", program);
    printf("Supported tools:\n");
    printf("  git    - Git version control\n");
    printf("  gh     - GitHub CLI\n\n");
    printf("Examples:\n");
    printf("  %s git status\n", program);
    printf("  %s gh pr list\n", program);
}

// In main:
if (argc == 2 && strcmp(argv[1], "help") == 0) {
    show_help(argv[0]);
    return 0;
}
```

### Exercise 4: Add More Tools
**Task:** Extend to support more tools (npm, docker, kubectl, etc.)

**Design:**
```c
enum Tool {
    GIT,
    GH,
    NPM,
    DOCKER,
    KUBECTL
};

struct ToolInfo {
    const char *name;
    enum Tool type;
    const char *description;
};

const struct ToolInfo SUPPORTED_TOOLS[] = {
    {"git", GIT, "Git version control"},
    {"gh", GH, "GitHub CLI"},
    {"npm", NPM, "Node package manager"},
    {"docker", DOCKER, "Container platform"},
    {"kubectl", KUBECTL, "Kubernetes CLI"},
    {NULL, 0, NULL}
};
```

### Exercise 5: Add Aliases
**Task:** Support command aliases (e.g., `gt g s` → `git status`)

**Design:**
```c
struct Alias {
    const char *short_cmd;
    const char **expansion;
};

// "g s" → "git status"
const char *git_status[] = {"git", "status", NULL};

struct Alias aliases[] = {
    {"g s", git_status},
    {NULL, NULL}
};
```

---

## Part 7: First Principles Summary

### Core Concepts

**1. Command-Line Arguments:**
```c
int main(int argc, char *argv[])
// argc: argument count
// argv: argument vector (array of strings)
```

**2. Enumerations:**
```c
enum Type { VALUE1, VALUE2 };
// Named integer constants
// Type-safe, readable, debuggable
```

**3. String Comparison:**
```c
strcmp(s1, s2)
// Returns 0 if equal
// < 0 if s1 < s2
// > 0 if s1 > s2
```

**4. Program Execution:**
```c
execvp(program, args)
// Replace current process
// Search PATH for program
// Pass arguments as array
```

**5. Error Handling:**
```c
if (error_condition) {
    fprintf(stderr, "Error: %s\n", message);
    return error_code;
}
```

### Design Patterns

**CLI Tool Router Pattern:**
```
1. Parse arguments
2. Validate input
3. Determine tool/command
4. Execute with appropriate tool
5. Handle errors
```

**Safety Checklist:**
- Check `argc` before accessing `argv`
- Validate all user input
- Handle all error cases
- Provide helpful error messages
- Don't trust user data (sanitize!)

---

## How to Use This Guide with Claude Code CLI

```bash
claude code

# Ask questions like:
"Explain argc and argv with examples"
"Why use enums instead of #define?"
"Help me implement Exercise 2 on logging"
"What's the difference between system() and execvp()?"
"How do I handle command-line arguments safely?"
"Walk me through adding support for Docker commands"
```
