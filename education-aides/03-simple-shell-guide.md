# Simple Shell (ablash) - Education Aide
## Understanding Operating System Concepts and Shell Implementation

### Overview
This guide will walk you through building a Unix shell from first principles, covering process management, I/O redirection, command parsing, and concurrent execution.

---

## Part 1: What is a Shell?

### The Big Picture

**Question:** When you type `ls -la` in a terminal, what actually happens?

**Your Thought Process:** _[Think about the chain of events]_

<details>
<summary>The Shell's Role</summary>

**The Shell is:**
- An interface between user and operating system
- A command interpreter
- A programming environment

**Process Flow:**
```
User types: ls -la
     ↓
Shell reads input
     ↓
Shell parses: command="ls", args=["-la"]
     ↓
Shell creates new process (fork)
     ↓
Child process executes "ls" program
     ↓
Parent shell waits for completion
     ↓
Results displayed to user
```

**Famous Shells:**
- sh (Bourne Shell) - Original Unix shell
- bash (Bourne Again Shell) - Most common Linux shell
- zsh (Z Shell) - Modern, feature-rich
- ablash (Your shell!) - Learning implementation
</details>

### Core Shell Responsibilities

**Question:** What features should a basic shell provide?

**Your List:** _[Write down shell features you use]_

<details>
<summary>Essential Shell Features</summary>

**1. Command Execution**
```bash
$ ls
$ cat file.txt
$ python script.py
```

**2. Argument Passing**
```bash
$ ls -la /home/user
$ gcc -o program program.c
```

**3. I/O Redirection**
```bash
$ cat < input.txt          # Input from file
$ ls > output.txt          # Output to file
$ grep "error" < log.txt > errors.txt
```

**4. Concurrent Execution**
```bash
$ long_running_task &      # Run in background
```

**5. Command History**
```bash
$ !!                       # Repeat last command
```

**6. Built-in Commands**
```bash
$ cd /home/user           # Change directory
$ exit                    # Exit shell
```

**Advanced Features (not in our implementation):**
- Pipes: `ls | grep txt`
- Environment variables: `echo $PATH`
- Job control: `Ctrl+Z`, `fg`, `bg`
- Command substitution: `$(command)`
- Scripting: loops, conditionals, functions
</details>

---

## Part 2: Understanding Processes

### The Process Model

**Fundamental Question:** What is a process?

**Your Definition:** _[Explain in your own words]_

<details>
<summary>Process Fundamentals</summary>

**A Process is:**
- A program in execution
- Has its own memory space (code, data, stack, heap)
- Has unique Process ID (PID)
- Has state (running, waiting, terminated)
- Has resources (open files, CPU time, etc.)

**Memory Layout:**
```
High Address
┌─────────────────┐
│  Command Args   │
│  Environment    │
├─────────────────┤
│     Stack       │  ← Grows down
│       ↓         │
│                 │
│       ↑         │
│     Heap        │  ← Grows up
├─────────────────┤
│  Uninitialized  │
│  Data (BSS)     │
├─────────────────┤
│  Initialized    │
│  Data           │
├─────────────────┤
│  Text (Code)    │
└─────────────────┘
Low Address
```
</details>

### The fork() System Call

**Core Concept:** `fork()` creates a copy of the current process.

**Study this code:**
```c
pid_t pid = fork();

if (pid == 0) {
    // Child process
    printf("I'm the child! PID: %d\n", getpid());
} else if (pid > 0) {
    // Parent process
    printf("I'm the parent! Child PID: %d\n", pid);
} else {
    // Fork failed
    perror("fork failed");
}
```

**Critical Thinking Questions:**

**Q1:** After `fork()`, how many processes exist?

**Your Answer:** _[Think carefully]_

<details>
<summary>Answer</summary>
**Two processes** - the original (parent) and the copy (child).

Both execute the code after the `fork()` call, but with different return values!
</details>

**Q2:** What memory is shared between parent and child?

**Your Answer:** _[What gets copied?]_

<details>
<summary>Memory Model</summary>

**Before fork():**
```
Process (PID 100)
Memory: [variables, code, stack]
```

**After fork():**
```
Parent (PID 100)              Child (PID 101)
Memory: [variables, code]     Memory: [COPY of variables, code]
```

**Key Points:**
- Child gets **copy** of parent's memory
- Changes in child don't affect parent
- Changes in parent don't affect child
- Code is the same, but they execute independently

**Copy-on-Write Optimization:**
Modern OSes don't actually copy memory until one process writes to it.
</details>

**Q3:** What is inherited by the child?

<details>
<summary>Inheritance</summary>

**Child Inherits:**
- Code (text segment)
- Data (initialized and uninitialized)
- Stack
- Heap
- Open file descriptors (important for I/O redirection!)
- Environment variables
- Working directory
- Signal handlers

**Child Gets New:**
- Process ID (PID)
- Parent Process ID (PPID)
- Resource utilization (CPU time resets to 0)
- Pending signals (cleared)
</details>

---

## Part 3: The exec Family of System Calls

### Replacing Process Image

**The Problem:** `fork()` creates a copy of the current process. How do we run a different program (like `ls` or `cat`)?

**The Solution:** `exec()` family of system calls.

**Study the shell code (ablash.c:112-116):**
```c
if (execvp(cmd[0], cmd) == -1)
{
    perror("Error executing command");
    exit(1);
}
```

**Question:** What does `execvp()` do?

**Your Understanding:** _[What happens to the process?]_

<details>
<summary>The exec Transformation</summary>

**execvp() replaces the current process with a new program:**

```
Before execvp("ls", ["-la"]):
┌─────────────────────┐
│  Shell Child        │
│  Code: shell code   │
│  Data: shell vars   │
└─────────────────────┘

After execvp("ls", ["-la"]):
┌─────────────────────┐
│  Same Process       │
│  Code: ls program!  │
│  Data: ls vars      │
└─────────────────────┘
```

**Key Points:**
- Same PID, different program!
- Shell code is **gone**, replaced by ls code
- If exec succeeds, it never returns!
- If exec fails, returns -1 and original code continues
</details>

### The exec Family

**There are several exec variants:**

```c
int execl(const char *path, const char *arg, ...);
int execlp(const char *file, const char *arg, ...);
int execle(const char *path, const char *arg, ..., char *const envp[]);
int execv(const char *path, char *const argv[]);
int execvp(const char *file, char *const argv[]);
int execve(const char *path, char *const argv[], char *const envp[]);
```

**Question:** Why use `execvp()` instead of others?

**Your Analysis:** _[Compare the options]_

<details>
<summary>Choosing the Right exec</summary>

**Naming Convention:**
- `l` - Arguments as list: `exec("ls", "-l", "-a", NULL)`
- `v` - Arguments as vector (array): `exec("ls", argv)`
- `p` - Search PATH for executable
- `e` - Pass custom environment

**Why execvp() is perfect for shells:**
1. **v**: We already have arguments in an array (`cmd[]`)
2. **p**: Searches PATH so user doesn't need full path (`ls` vs `/bin/ls`)

**Example:**
```c
char *cmd[] = {"ls", "-la", NULL};

// Without p: Need full path
execv("/bin/ls", cmd);  // Must know exact location

// With p: Searches PATH
execvp("ls", cmd);  // Searches /bin, /usr/bin, etc.
```
</details>

---

## Part 4: Command Execution in ablash

### The Fork-Exec Pattern

**Study the executeCommand function (ablash.c:77-122):**

```c
void executeCommand(int isConcurrent)
{
  pid_t pid = fork();

  if (pid > 0)
  {
    // Parent process
    if (!isConcurrent)
    {
      wait(NULL);  // Wait for child
    }
    else {
      printf("executing concurrently\n");
    }
  }
  else if (pid == 0)
  {
    // Child process
    if (execvp(cmd[0], cmd) == -1)
    {
      perror("Error executing command");
      exit(1);
    }
  }
  else
  {
    perror("Fork failed");
  }
}
```

**Trace This Example:**
```
User types: ls -la
```

**Your Trace:** _[Step through what happens]_

<details>
<summary>Execution Trace</summary>

**Step-by-step:**

```
1. Shell parses input: cmd[0]="ls", cmd[1]="-la", cmd[2]=NULL

2. Shell calls fork()
   ┌─────────────┐
   │ Shell (PID) │
   └──────┬──────┘
          │ fork()
          ├──────────┬──────────┐
   ┌──────▼──────┐ ┌─▼─────────┐
   │ Parent      │ │ Child     │
   │ pid = 1234  │ │ pid = 0   │
   └─────────────┘ └───────────┘

3. Parent: pid > 0
   → Executes: wait(NULL)
   → Blocks until child completes

4. Child: pid == 0
   → Executes: execvp("ls", ["-la"])
   → Becomes ls program
   → Runs ls -la
   → Exits

5. Parent: wait() returns
   → Displays prompt again
   → Ready for next command
```
</details>

### The wait() System Call

**Question:** What happens if parent doesn't call `wait()`?

**Your Prediction:** _[Think about process lifecycle]_

<details>
<summary>Understanding wait()</summary>

**Without wait():**
```c
pid_t pid = fork();
if (pid == 0) {
    execvp(cmd[0], cmd);
} else {
    // Parent continues immediately!
    printf("lash⚟ ");  // Shows prompt before child finishes
}
```

**Result:**
```bash
lash⚟ ls
lash⚟ file1.txt
file2.txt
file3.txt
```
Prompt appears before output! Confusing!

**With wait():**
```c
if (pid > 0) {
    wait(NULL);  // Wait for child to finish
    printf("lash⚟ ");
}
```

**Result:**
```bash
lash⚟ ls
file1.txt
file2.txt
file3.txt
lash⚟
```
Clean output!

**Zombie Processes:**
If child exits but parent never calls `wait()`:
- Child becomes "zombie" (terminated but not reaped)
- Takes up PID and process table entry
- `wait()` cleans this up
</details>

**Advanced:** What does `wait(NULL)` return?

<details>
<summary>wait() Return Value and Status</summary>

```c
int status;
pid_t child_pid = wait(&status);

if (child_pid == -1) {
    perror("wait failed");
}

// Check how child exited
if (WIFEXITED(status)) {
    int exit_code = WEXITSTATUS(status);
    printf("Child exited with code %d\n", exit_code);
}

if (WIFSIGNALED(status)) {
    int signal = WTERMSIG(status);
    printf("Child killed by signal %d\n", signal);
}
```

**In ablash:** `wait(NULL)` ignores exit status (just waits for any child).
</details>

---

## Part 5: Input Parsing

### The Challenge of Parsing

**Question:** How do you convert user input string into separate arguments?

**Example:**
```
Input: "ls -la /home/user"
Desired: cmd[0]="ls", cmd[1]="-la", cmd[2]="/home/user", cmd[3]=NULL
```

**Your Approach:** _[How would you solve this?]_

<details>
<summary>Tokenization Approach</summary>

**Using strtok():**
```c
char input[] = "ls -la /home/user";
char *token = strtok(input, " ");

while (token != NULL) {
    // token points to next word
    printf("%s\n", token);
    token = strtok(NULL, " ");
}

Output:
ls
-la
/home/user
```

**How strtok() works:**
1. First call: `strtok(input, " ")` - pass string
2. Subsequent calls: `strtok(NULL, " ")` - pass NULL to continue
3. Returns NULL when no more tokens
4. **Important:** Modifies original string! (inserts '\0' characters)
</details>

### Analyzing the input() Function

**Study ablash.c:125-195:**

```c
void input()
{
  fgets(buf, 100, stdin);  // Read line from user

  // Handle '&' for concurrent execution
  if ((ampersand = strchr(buf, '&')) != NULL)
  {
    *ampersand = '\0';  // Remove '&' from command
    isConcurrent = 1;
  }

  // Handle history command
  if (!strcmp(buf, "!!\n"))
  {
    if (strlen(hisBuf) == 0)
    {
      printf("No commands in history.\n");
      buf[0] = '\0';
    }
    strcpy(buf, hisBuf);
  }

  strcpy(hisBuf, buf);  // Save to history

  // Parse into tokens
  strcpy(buf, strtok(buf, "\n"));
  arg = strtok(buf, " ");
  i = 0;
  while (arg != NULL && i < 100 / 2)
  {
    cmd[i] = arg;

    // Check for redirection
    if (strcmp(cmd[i], "<") == 0)
    {
      isRedirect = 1;
      glts = '<';
    }
    else if (strcmp(cmd[i], ">") == 0)
    {
      isRedirect = 1;
      glts = '>';
    }

    i++;
    arg = strtok(NULL, " ");
  }
}
```

**Critical Analysis Questions:**

**Q1:** Why use `fgets()` instead of `scanf()`?

<details>
<summary>fgets vs scanf</summary>

**fgets():**
```c
fgets(buf, 100, stdin);
// Reads entire line (up to 100 chars)
// Includes newline character
// Safe from buffer overflow
```

**scanf():**
```c
scanf("%s", buf);
// Reads until whitespace
// Can't get full command with spaces
// Vulnerable to buffer overflow
```

**For shell:** Need entire line including spaces, so `fgets()` is correct choice!
</details>

**Q2:** What is the bug in `strcpy(buf, strtok(buf, "\n"))`?

<details>
<summary>Dangerous strtok Usage</summary>

**The line:**
```c
strcpy(buf, strtok(buf, "\n"));
```

**Problem:** Undefined behavior!
- `strtok` modifies `buf`
- `strcpy` writes to `buf`
- Source and destination overlap!

**Safer approach:**
```c
char *newline = strchr(buf, '\n');
if (newline) *newline = '\0';  // Just remove newline
```

**Why it "works" anyway:** Implementation-dependent. Might work on some systems, fail on others.
</details>

---

## Part 6: I/O Redirection

### Understanding File Descriptors

**Fundamental Concept:** In Unix, everything is a file!

**Question:** What is a file descriptor?

**Your Understanding:** _[What does "0", "1", "2" mean?]_

<details>
<summary>File Descriptor Table</summary>

**Every process has a file descriptor table:**

```
┌─────┬──────────────────┐
│ FD  │  Points To       │
├─────┼──────────────────┤
│  0  │  stdin (keyboard)│  Standard Input
│  1  │  stdout(terminal)│  Standard Output
│  2  │  stderr(terminal)│  Standard Error
│  3  │  (available)     │
│  4  │  (available)     │
│ ... │                  │
└─────┴──────────────────┘
```

**Example:**
```c
int fd = open("file.txt", O_RDONLY);
// fd might be 3 (first available descriptor)

read(fd, buffer, 100);   // Read from file.txt
write(1, buffer, 100);   // Write to stdout
```

**Key Insight:** Programs don't know if fd 0 is keyboard or file! This enables redirection.
</details>

### The dup2() System Call

**Study the handleRedirect function (ablash.c:199-232):**

```c
void handleRedirect(char *redirectSign, char *commandString[])
{
  int fd;
  switch (*redirectSign)
  {
  case '<':
    fd = open(filename, O_RDWR);
    if (fd == -1)
    {
      perror("Error opening file for input");
      exit(1);
    }
    dup2(fd, STDIN_FILENO);  // Redirect stdin to file
    close(fd);
    break;

  case '>':
    fd = open(filename, O_RDWR);
    if (fd == -1)
    {
      perror("Error opening file for output");
      exit(1);
    }
    dup2(fd, STDOUT_FILENO);  // Redirect stdout to file
    close(fd);
    break;
  }

  execvp(commandString[0], commandString);
}
```

**Question:** What does `dup2(fd, STDIN_FILENO)` do?

**Your Mental Model:** _[Visualize the file descriptor table]_

<details>
<summary>Understanding dup2()</summary>

**Before dup2():**
```
┌─────┬──────────────────┐
│ FD  │  Points To       │
├─────┼──────────────────┤
│  0  │  stdin (keyboard)│
│  1  │  stdout(terminal)│
│  2  │  stderr(terminal)│
│  3  │  input.txt       │  ← fd from open()
└─────┴──────────────────┘
```

**After dup2(fd, STDIN_FILENO):**
```
┌─────┬──────────────────┐
│ FD  │  Points To       │
├─────┼──────────────────┤
│  0  │  input.txt!      │  ← Now points to file!
│  1  │  stdout(terminal)│
│  2  │  stderr(terminal)│
│  3  │  input.txt       │
└─────┴──────────────────┘
```

**After close(fd):**
```
┌─────┬──────────────────┐
│ FD  │  Points To       │
├─────┼──────────────────┤
│  0  │  input.txt       │  ← Still points to file!
│  1  │  stdout(terminal)│
│  2  │  stderr(terminal)│
│  3  │  (closed)        │
└─────┴──────────────────┘
```

**Result:** Any `read(0, ...)` now reads from input.txt instead of keyboard!

**After execvp():** New program (e.g., cat) inherits fd 0 pointing to file, so it reads from file automatically!
</details>

### Redirection Example Trace

**Command:** `cat < input.txt > output.txt`

**Your Trace:** _[Step through the execution]_

<details>
<summary>Complete Trace</summary>

```
1. Parse: cmd = ["cat", "<", "input.txt", ">", "output.txt", NULL]
   isRedirect = 1
   filename will be set during parsing

2. Fork child process

3. Child process:

   a) Open input.txt:
      fd = open("input.txt", O_RDWR)  → fd = 3

   b) Redirect stdin:
      dup2(3, 0)  → fd 0 now points to input.txt
      close(3)

   c) Open output.txt:
      fd = open("output.txt", O_RDWR)  → fd = 3 (reused)

   d) Redirect stdout:
      dup2(3, 1)  → fd 1 now points to output.txt
      close(3)

   e) Execute cat:
      execvp("cat", ["cat", NULL])

   f) cat program runs:
      - Reads from fd 0 (input.txt)
      - Writes to fd 1 (output.txt)
      - Doesn't know about redirection!

4. Parent process:
   wait() for child to complete

Result: input.txt contents copied to output.txt
```
</details>

**Bug in ablash:** What's wrong with using `O_RDWR` for output redirection?

<details>
<summary>File Open Modes</summary>

**The bug:**
```c
case '>':
    fd = open(filename, O_RDWR);  // ❌ Wrong flags!
```

**Problem:**
- `O_RDWR`: Open for reading and writing
- But file might not exist!
- Should create file if it doesn't exist
- Should truncate file if it does exist

**Correct:**
```c
fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
//                  Write     Create    Truncate  Permissions
```

**Flags explained:**
- `O_RDONLY`: Read only (< input)
- `O_WRONLY`: Write only (> output)
- `O_RDWR`: Read and write
- `O_CREAT`: Create file if doesn't exist
- `O_TRUNC`: Truncate file to 0 bytes (clear it)
- `0644`: Permissions (rw-r--r--)
</details>

---

## Part 7: Concurrent Execution

### Background Processes

**Study concurrent execution (ablash.c:84-91):**

```c
if (pid > 0)
{
  // Parent process
  if (!isConcurrent)
  {
    wait(NULL);  // Wait for child
  }
  else {
    printf("executing concurrently\n");
    // Don't wait! Continue immediately
  }
}
```

**Question:** What's the difference between `ls` and `ls &`?

**Your Understanding:** _[Think about when shell returns]_

<details>
<summary>Foreground vs Background</summary>

**Foreground (ls):**
```
lash⚟ ls
file1.txt  ← Output from ls
file2.txt
file3.txt
lash⚟     ← Prompt after ls completes
```

**Process flow:**
```
Shell → fork() → wait() → (blocked) → ls exits → wait() returns → prompt
```

**Background (ls &):**
```
lash⚟ ls &
executing concurrently
lash⚟     ← Prompt appears immediately!
file1.txt
file2.txt
file3.txt
```

**Process flow:**
```
Shell → fork() → continue → prompt
              ↓
           Child runs ls concurrently
```

**Use cases for background:**
- Long-running tasks
- Servers/daemons
- Tasks you want to start and forget
</details>

**Problem:** What happens to zombie processes from background jobs?

<details>
<summary>Zombie Problem</summary>

**The issue:**
```c
if (isConcurrent) {
    // Don't wait!
    // Child will exit eventually...
    // But no one calls wait()!
    // → ZOMBIE PROCESS!
}
```

**Solution 1:** Signal handler
```c
#include <signal.h>

void sigchld_handler(int sig) {
    while (waitpid(-1, NULL, WNOHANG) > 0);  // Reap any dead children
}

int main() {
    signal(SIGCHLD, sigchld_handler);
    // Now when child exits, handler automatically reaps it
}
```

**Solution 2:** Periodically check for dead children
```c
waitpid(-1, NULL, WNOHANG);  // Non-blocking wait
```

**ablash doesn't implement this** - background processes become zombies!
</details>

---

## Part 8: Command History

### The History Feature

**Study the history implementation (ablash.c:139-150):**

```c
static char hisBuf[100 / 2 + 1];  // Global history buffer

// In input() function:
if (!strcmp(buf, "!!\n"))
{
  if (strlen(hisBuf) == 0)
  {
    printf("No commands in history.\n");
    buf[0] = '\0';
  }
  strcpy(buf, hisBuf);
}

strcpy(hisBuf, buf);  // Save current command
```

**Question:** How would you improve this history implementation?

**Your Ideas:** _[List improvements]_

<details>
<summary>History Limitations and Improvements</summary>

**Current Limitations:**
1. Only stores ONE command (last command only)
2. Lost when shell exits (not persistent)
3. No way to view history
4. No numbered recall (like `!5`)

**Improvement 1: History Array**
```c
#define HISTORY_SIZE 100
char history[HISTORY_SIZE][MAX_LINE];
int history_count = 0;

void add_to_history(char *command) {
    strcpy(history[history_count % HISTORY_SIZE], command);
    history_count++;
}

void execute_history_number(int n) {
    if (n >= history_count || n < 0) {
        printf("No such command\n");
        return;
    }
    strcpy(buf, history[n]);
}
```

**Improvement 2: Persistent History**
```c
void save_history() {
    FILE *f = fopen(".ablash_history", "w");
    for (int i = 0; i < history_count; i++) {
        fprintf(f, "%s\n", history[i]);
    }
    fclose(f);
}

void load_history() {
    FILE *f = fopen(".ablash_history", "r");
    if (!f) return;

    while (fgets(history[history_count], MAX_LINE, f)) {
        history_count++;
    }
    fclose(f);
}
```

**Improvement 3: History Commands**
```c
// In main loop:
if (!strcmp(cmd[0], "history")) {
    for (int i = 0; i < history_count; i++) {
        printf("%4d  %s\n", i, history[i]);
    }
    continue;  // Don't execute
}

if (cmd[0][0] == '!') {
    int n = atoi(cmd[0] + 1);  // "!5" → 5
    execute_history_number(n);
}
```
</details>

---

## Part 9: Built-in Commands

### Why Built-in Commands?

**Question:** Why does `cd` need to be a built-in command?

**Try this:**
```c
// What if cd was external program?
if (strcmp(cmd[0], "cd") == 0) {
    executeCommand(0);  // Fork and exec cd program
}
```

**Your Analysis:** _[What would go wrong?]_

<details>
<summary>The cd Problem</summary>

**If cd was external:**

```
Shell (PID 1000, cwd=/home/user)
    ↓ fork()
Child (PID 1001, cwd=/home/user)
    ↓ execvp("cd", ["/tmp"])
cd program (PID 1001, cwd=/tmp)  ← Changes ITS directory
    ↓ exits
Shell (PID 1000, cwd=/home/user)  ← Still in /home/user!
```

**The problem:** Child process changes its own directory, but that doesn't affect parent!

**Solution:** Implement cd as built-in:
```c
if (strcmp(cmd[0], "cd") == 0) {
    if (chdir(cmd[1]) != 0) {
        perror("cd failed");
    }
    // Don't fork! Change shell's directory directly
    continue;  // Skip executeCommand()
}
```

**Other commands that must be built-in:**
- `exit` - Must terminate the shell itself
- `export` - Must modify shell's environment
- `alias` - Must be remembered by shell
- `cd` - Must change shell's working directory
</details>

### Implementing exit

**Study ablash.c:236-251:**

```c
int exitCheck()
{
  if (cmd[0] == NULL)
  {
    return false;
  }
  if (!strcmp(cmd[0], "exit"))
  {
    system("clear");
    return true;
  }
  else
  {
    return false;
  }
}
```

**Question:** Is using `system("clear")` a good idea?

<details>
<summary>Avoiding system()</summary>

**Problem with system():**
- Spawns a shell to execute command
- Inefficient
- Security risk (command injection if user input)
- Overkill for simple tasks

**Better alternatives:**
```c
// Option 1: ANSI escape codes
printf("\033[2J\033[H");  // Clear screen and move cursor to home

// Option 2: Use terminfo library
#include <curses.h>
#include <term.h>
putp(tigetstr("clear"));

// Option 3: Direct system call
execl("/usr/bin/clear", "clear", NULL);
```

**For exit:** Just return from main() or call `exit(0)`, no need to clear!
</details>

---

## Part 10: Hands-On Exercises

### Exercise 1: Fix the Bugs
**Task:** Fix all bugs in ablash.c

**Bugs to fix:**
1. Input redirection should use `O_RDONLY`
2. Output redirection should use `O_WRONLY | O_CREAT | O_TRUNC`
3. Implement proper zombie reaping for background processes
4. Fix dangerous `strcpy(buf, strtok(buf, "\n"))`
5. Handle edge cases (NULL command, empty input)

### Exercise 2: Implement Pipes
**Task:** Add support for pipes: `ls | grep txt`

**Hints:**
1. Use `pipe()` system call to create pipe
2. Use `dup2()` to redirect stdout of first command to pipe write end
3. Use `dup2()` to redirect stdin of second command to pipe read end
4. Fork twice (one for each command)

**Skeleton:**
```c
int pipefd[2];
pipe(pipefd);  // pipefd[0] = read end, pipefd[1] = write end

if (fork() == 0) {
    // First command
    dup2(pipefd[1], STDOUT_FILENO);
    close(pipefd[0]);
    close(pipefd[1]);
    execvp(cmd1[0], cmd1);
}

if (fork() == 0) {
    // Second command
    dup2(pipefd[0], STDIN_FILENO);
    close(pipefd[0]);
    close(pipefd[1]);
    execvp(cmd2[0], cmd2);
}

close(pipefd[0]);
close(pipefd[1]);
wait(NULL);
wait(NULL);
```

### Exercise 3: Implement Environment Variables
**Task:** Add support for `export VAR=value` and `$VAR` expansion.

**Steps:**
1. Parse export command
2. Use `setenv()` to set environment variable
3. Before exec, scan command for `$VAR` and replace with value
4. Use `getenv()` to retrieve values

### Exercise 4: Add Job Control
**Task:** Implement `jobs`, `fg`, `bg` commands.

**Requirements:**
1. Keep list of background jobs with PIDs
2. `jobs` - display all background jobs
3. `fg %1` - bring job 1 to foreground
4. `bg %1` - continue stopped job in background
5. Handle Ctrl+Z (SIGTSTP) to stop foreground job

**Advanced:** Use `tcsetpgrp()` for proper terminal control.

---

## Part 11: First Principles Summary

### Core Operating System Concepts

**1. Process Management:**
- `fork()` - Create new process (copy)
- `exec()` - Replace process image
- `wait()` - Synchronize with child
- Zombie processes and reaping

**2. File Descriptors:**
- Every process has descriptor table
- 0 = stdin, 1 = stdout, 2 = stderr
- `open()`, `close()`, `read()`, `write()`
- `dup2()` - Redirect file descriptors

**3. I/O Redirection:**
- `<` - Input from file (fd 0)
- `>` - Output to file (fd 1)
- `2>` - Error to file (fd 2)
- Pipes connect processes

**4. Shell Mechanics:**
- Read-Parse-Execute loop
- Tokenization and argument parsing
- Foreground vs background execution
- Built-in vs external commands

### Design Patterns

**The Fork-Exec Pattern:**
```c
pid_t pid = fork();
if (pid == 0) {
    // Child: setup (redirect I/O, etc.)
    execvp(program, args);
    // Only reaches here if exec fails
    perror("exec failed");
    exit(1);
} else {
    // Parent: wait or continue
    wait(NULL);
}
```

**Why this pattern?**
- Separates process creation from program loading
- Allows setup between fork and exec (I/O redirection!)
- Parent can monitor child

### Common Pitfalls

**1. Forgetting to wait():**
```c
fork();
// Child exits → zombie!
```

**2. Closing wrong file descriptors:**
```c
dup2(fd, 0);
// Forgot to close(fd) → file descriptor leak!
```

**3. Buffer overflow:**
```c
char buf[100];
scanf("%s", buf);  // ❌ Unsafe!
fgets(buf, 100, stdin);  // ✓ Safe
```

**4. Modifying string literals:**
```c
char *s = "hello";
s[0] = 'H';  // ❌ Segmentation fault!

char s[] = "hello";
s[0] = 'H';  // ✓ OK
```

### Performance Considerations

**1. Fork is expensive:**
- Copies entire address space (copy-on-write helps)
- Consider threads for lightweight concurrency

**2. Context switching:**
- Too many processes → thrashing
- Balance parallelism with overhead

**3. I/O buffering:**
- `fflush()` when needed
- Understand when output appears

---

## Part 12: Advanced Topics

### Signal Handling
```c
#include <signal.h>

void sigint_handler(int sig) {
    printf("\nCaught Ctrl+C! Not exiting.\n");
    printf("lash⚟ ");
    fflush(stdout);
}

signal(SIGINT, sigint_handler);
```

### Job Control
- Process groups
- Foreground/background job management
- Terminal control with `tcsetpgrp()`

### Advanced Parsing
- Handle quotes: `echo "hello world"`
- Escape characters: `echo hello\ world`
- Variable expansion: `echo $HOME`
- Command substitution: `echo $(date)`

### Process Relationships
- Process groups (setpgid)
- Session leaders (setsid)
- Controlling terminal
- Daemon processes

---

## How to Use This Guide with Claude Code CLI

```bash
claude code

# Ask questions like:
"Explain the fork-exec pattern step by step"
"Why do we need to call wait() after fork()?"
"Walk me through Exercise 2 on implementing pipes"
"Help me understand file descriptor redirection"
"What's the difference between execl and execvp?"
"Trace the execution of: cat < input.txt > output.txt"
"How do I implement signal handling for Ctrl+C?"
```

**Interactive Learning:**
- Request visual diagrams of process trees
- Ask for memory layout visualizations
- Get hints for exercises
- Discuss design trade-offs
- Explore advanced topics
