# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a custom Unix shell implementation called "ablashell" (displayed as "lash⚟" prompt). It's an operating systems concepts project that implements a basic command-line shell with support for process management, command history, I/O redirection, and concurrent execution.

## Build Commands

```bash
# Build the shell
make

# Run the shell
./ablashell
```

The Makefile compiles `ablashell.c` and `utilities.c` into the `ablashell` executable using gcc.

## Architecture

The codebase follows a modular architecture with two main components:

### Main Shell (`ablashell.c`)
- Entry point and main execution loop
- Handles the shell prompt display and main control flow
- Manages the command history buffer (stores last command for `!!` history recall)
- Coordinates between input parsing and command execution
- Uses `input()` to parse user commands and `executeCommand()` to run them
- The shell continues running until the "exit" command is received

### Utilities Module (`utilities.c` / `utilities.h`)
Core shell functionality split into four main functions:

1. **`input()`** (utilities.c:44-130)
   - Parses user input into command arguments
   - Detects special operators: `&` (concurrent execution), `<` (input redirect), `>` (output redirect)
   - Handles `!!` history command by repeating the last command from `hisBuf`
   - Returns a flags array indicating concurrent execution and redirection status
   - Tokenizes commands using `strtok()` and populates the args array

2. **`executeCommand()`** (utilities.c:8-41)
   - Forks a child process to execute commands using `execvp()`
   - Parent process behavior depends on concurrent flag:
     - If `isConcurrent` is false: waits for child to complete (`wait()`)
     - If `isConcurrent` is true: continues immediately (background execution)
   - Sets `childFlag` to indicate when running in child process context

3. **`handleRedirect()`** (utilities.c:134-176)
   - Manages I/O redirection for commands
   - Forks a new process to handle the redirection
   - Uses `dup2()` to redirect STDIN or STDOUT to specified file
   - `<` redirects file input to command's stdin
   - `>` redirects command's stdout to file (creates/truncates with 0644 permissions)

4. **`exitCheck()`** (utilities.c:180-191)
   - Simple check for the "exit" command
   - Clears the terminal before exiting

## Key Implementation Details

- **Process Management**: The shell uses `fork()` to create child processes and `execvp()` to execute commands
- **Concurrent Execution**: Commands ending with ` &` run in background without parent waiting
- **Command History**: Limited to one command stored in `historyBuffer`, accessible via `!!`
- **Child Flag Pattern**: `childFlag` pointer is used to ensure child processes exit after command execution and don't continue the shell loop
- **Redirection Flow**: When redirect symbols are detected, `handleRedirect()` is called directly from `input()`, bypassing normal `executeCommand()` flow
