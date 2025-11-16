# Miscellaneous Programming Projects

A curated collection of educational programming projects designed to teach computer science fundamentals from first principles. This repository contains everything from low-level systems programming to AI/ML applications, with comprehensive education guides for each project.

## Overview

This repository is organized into several categories of projects, each designed to teach specific computer science concepts through hands-on implementation:

### 📁 Project Categories

1. **Systems Programming** - OS concepts, processes, threads, shells
2. **Data Structures & Algorithms** - Hash tables, algorithms, complexity analysis
3. **Computer Architecture** - Building computers from NAND gates
4. **Enterprise Software** - Spring Boot, Kafka, microservices
5. **AI/ML** - Transformers, NLP, prompt engineering
6. **Challenging Projects** - Text editors, compilers, OSes, emulators, games

---

## 📚 Featured Projects

### Systems Programming & Operating Systems

#### [Count Primes](Count%20Primes/)
Learn concurrent programming by implementing prime number counting using processes and threads.
- **Topics:** fork(), pthread, process management
- **Languages:** C
- **Difficulty:** Intermediate

#### [Simple Shell](Simple%20Shell/)
Build a Unix shell from scratch to understand how command-line interfaces work.
- **Topics:** Process creation, I/O redirection, pipes
- **Languages:** C
- **Difficulty:** Intermediate

---

### Data Structures & Algorithms

#### [Hash Track](Hash%20Track/)
Implement a hash table with quadratic probing from first principles.
- **Topics:** Hash functions, collision resolution, templates
- **Languages:** C++
- **Difficulty:** Intermediate

---

### Computer Architecture

#### [Nand2Tetris](Nand2Tetris/)
Build a complete computer system from NAND gates to operating system.
- **Topics:** Logic gates, CPU, assembler, VM, compiler, OS
- **Languages:** HDL, Assembly, Jack, Python
- **Difficulty:** Advanced
- **Time:** 12+ weeks

---

### Computer Science First Principles

#### [CS First Principles](CS%20First%20Principles/)
Comprehensive curriculum covering fundamental CS concepts:
- Logic and Boolean algebra
- Number systems and encodings
- Computer architecture
- Operating systems
- Algorithms and data structures
- Programming language theory

---

### Enterprise Software Development

#### [Forage Midas](Forage%20Midas/)
Build a financial transaction processing system with Spring Boot and Kafka.
- **Topics:** Spring Boot, Kafka, JPA, microservices
- **Languages:** Java
- **Difficulty:** Intermediate

---

### Artificial Intelligence & Machine Learning

#### [Learn AI Agents](Learn%20AI%20Agents/)
Understand transformer architectures and build NLP models.
- **Topics:** BERT, transformers, attention mechanisms
- **Languages:** Python
- **Difficulty:** Advanced

#### [Prompt Engineering](Prompt%20Engineering/)
Master the art of communicating effectively with AI systems.
- **Topics:** Prompt design, few-shot learning, chain-of-thought
- **Difficulty:** Beginner

---

### Challenging Projects (From Austin Z. Henley's Blog)

These projects are inspired by [Austin Z. Henley's "Challenging Projects Every Programmer Should Try"](https://austinhenley.com/blog/challengingprojects.html).

#### [Text Editor](Challenging%20Projects/Text%20Editor/)
Build a text editor to understand data structures like gap buffers, ropes, and piece tables.
- **Topics:** Text buffers, undo/redo, cursor management
- **Difficulty:** Intermediate to Advanced
- **Time:** 2-8 weeks

#### [Space Invaders](Challenging%20Projects/Space%20Invaders/)
Create a 2D game to learn game development fundamentals.
- **Topics:** Game loop, collision detection, entity management
- **Difficulty:** Beginner to Intermediate
- **Time:** 1-4 weeks

#### [Tiny BASIC Compiler](Challenging%20Projects/Tiny%20BASIC%20Compiler/)
Build a compiler for a simple BASIC-like language.
- **Topics:** Lexing, parsing, AST, code generation
- **Difficulty:** Intermediate to Advanced
- **Time:** 2-12 weeks

#### [Mini Operating System](Challenging%20Projects/Mini%20Operating%20System/)
Write a minimal OS from scratch including bootloader and kernel.
- **Topics:** Bootloader, memory management, scheduling, interrupts
- **Difficulty:** Advanced
- **Time:** 3-12+ months

#### [Spreadsheet](Challenging%20Projects/Spreadsheet/)
Create a spreadsheet application with formulas and functions.
- **Topics:** Formula parsing, dependency graphs, cell references
- **Difficulty:** Intermediate to Advanced
- **Time:** 2-8 weeks

#### [Console Emulator](Challenging%20Projects/Console%20Emulator/)
Emulate a video game console (CHIP-8, Game Boy, or NES).
- **Topics:** CPU emulation, memory mapping, graphics rendering
- **Difficulty:** Intermediate (CHIP-8) to Advanced (Game Boy/NES)
- **Time:** 1 week (CHIP-8) to 6+ months (advanced consoles)

---

## 🎓 Education Aides

Every project includes comprehensive educational resources in the [`education-aides/`](education-aides/) directory:

- **Interactive Q&A format** - Questions to think about before revealing answers
- **First principles explanations** - Concepts explained from the ground up
- **Code examples** - Real implementations you can study and run
- **Exercises** - Hands-on practice problems
- **Progressive difficulty** - From beginner to advanced

### How to Use Education Aides

```bash
# Navigate to the repository
cd /path/to/misc-projects

# Start Claude Code CLI
claude code

# Ask questions like:
"Walk me through the Text Editor education aide"
"Explain gap buffers from the Text Editor guide"
"Help me understand lexical analysis in the compiler guide"
"I'm stuck on Part 3 of the Mini OS guide, explain interrupts"
```

---

## 🗺️ Learning Paths

Choose a learning path based on your goals:

### Path 1: Systems Programmer (4-6 weeks)
```
Week 1-2: Simple Shell + Count Primes
Week 3: Reversal
Week 4-6: Nand2Tetris (Hardware + Software)
```
**Skills:** OS concepts, concurrent programming, computer architecture

### Path 2: Software Engineer (3-4 weeks)
```
Week 1: Hash Track + Git Tools
Week 2-3: Forage Midas
Week 4: Review and build projects
```
**Skills:** Data structures, enterprise development, Spring Boot, Kafka

### Path 3: AI/ML Engineer (3-4 weeks)
```
Week 1: Prompt Engineering
Week 2-3: AI Agents & Text Generation
Week 4: Build AI application
```
**Skills:** NLP, transformers, BERT, GPT, prompt engineering

### Path 4: Complete Computer Scientist (10-12 weeks)
```
Weeks 1-3: Systems (Simple Shell, Count Primes, Reversal)
Weeks 4-5: Data Structures (Hash Track, Git Tools)
Weeks 6-8: Computer Architecture (Nand2Tetris)
Weeks 9-10: Enterprise Software (Forage Midas)
Weeks 11-12: AI/ML (Prompt Engineering, AI Agents)
```
**Skills:** Full stack, from hardware to AI

### Path 5: Challenging Projects (12-24 weeks)
```
Week 1-2: Space Invaders - Game development basics
Week 3-5: Text Editor - Data structures
Week 6-9: Tiny BASIC Compiler - Language implementation
Week 10-13: Spreadsheet - Combining concepts
Week 14-17: Console Emulator - Start with CHIP-8
Week 18-24: Mini OS - Advanced systems programming
```
**Skills:** Systems programming, compilers, game dev, emulation, OS internals

**Description:** This path follows Austin Z. Henley's "Challenging Projects Every Programmer Should Try" - projects that teach fundamental computer science concepts through hands-on implementation.

---

## 🎯 Project Difficulty Levels

### Beginner
- Git Tools
- Reversal
- Prompt Engineering
- Space Invaders

### Intermediate
- Count Primes
- Hash Track
- Simple Shell
- Forage Midas
- Text Editor
- CHIP-8 Emulator
- Spreadsheet
- Tiny BASIC Compiler

### Advanced
- Nand2Tetris
- AI Agents & Text Generation
- Mini Operating System
- Game Boy/NES Emulator

---

## 🛠️ Technologies Covered

| Technology | Projects |
|------------|----------|
| **C** | Count Primes, Simple Shell, Git Tools, Mini OS |
| **C++** | Hash Track, Reversal, Text Editor |
| **Python** | Nand2Tetris, AI Agents, Space Invaders, Compilers, Emulators |
| **Java** | Forage Midas |
| **Assembly** | Nand2Tetris, Mini OS |
| **Spring Boot** | Forage Midas |
| **Kafka** | Forage Midas |
| **Transformers/NLP** | AI Agents |

---

## 📖 Key Skills Matrix

| Project | C/C++ | Java | Python | OS | Data Struct | Arch | AI/ML | Game Dev | Compilers |
|---------|-------|------|--------|----|-----------  |------|-------|----------|-----------|
| Count Primes | ✓✓ | | | ✓✓ | | | | | |
| Hash Track | ✓✓ | | | | ✓✓✓ | | | | |
| Simple Shell | ✓✓✓ | | | ✓✓✓ | | | | | |
| Reversal | ✓✓ | | | | | | | | |
| Git Tools | ✓ | | | ✓ | | | | | |
| Prompt Engineering | | | | | | | ✓✓ | | |
| Nand2Tetris | | | ✓ | ✓ | ✓ | ✓✓✓ | | | |
| Forage Midas | | ✓✓✓ | | | ✓ | | | | |
| AI Agents | | | ✓✓✓ | | | | ✓✓✓ | | |
| Text Editor | ✓✓ | | ✓✓ | | ✓✓✓ | | | | |
| Space Invaders | ✓ | | ✓✓ | | ✓ | | | ✓✓✓ | |
| Tiny BASIC | ✓✓ | | ✓✓ | | ✓✓ | | | | ✓✓✓ |
| Mini OS | ✓✓✓ | | | ✓✓✓ | ✓ | ✓✓✓ | | | |
| Spreadsheet | | | ✓✓ | | ✓✓ | | | | ✓✓ |
| Console Emulator | ✓✓ | | ✓✓ | | ✓ | ✓✓✓ | | | |

**Legend:** ✓ = Basic, ✓✓ = Intermediate, ✓✓✓ = Advanced

---

## 🚀 Getting Started

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd misc-projects
   ```

2. **Choose a project based on your skill level:**
   - **New to programming?** Start with Git Tools or Reversal
   - **Have experience?** Try Simple Shell or Text Editor
   - **Want a challenge?** Build a Mini OS or emulator

3. **Read the education guide:**
   ```bash
   # Each project has a corresponding guide
   cat education-aides/10-text-editor-guide.md
   ```

4. **Use Claude Code CLI for interactive learning:**
   ```bash
   claude code
   # Then ask: "Walk me through the Text Editor project"
   ```

---

## 💡 Learning Tips

### 1. Active Learning
- Don't just read - **implement**
- Try to answer questions before expanding details
- Modify examples to test understanding
- Break things intentionally to learn debugging

### 2. First Principles Thinking
- Ask "why" at every level
- Understand the problem before the solution
- Connect concepts across projects
- Build mental models

### 3. Spaced Repetition
- Review concepts after 1 day, 3 days, 1 week
- Teach concepts to others (or explain to Claude)
- Create your own examples
- Write blog posts about what you learned

### 4. Project Integration
- Combine concepts from multiple projects
- Example: Use hash table in shell implementation
- Example: Build CLI tool for AI model
- Example: Create microservice using learned patterns

---

## 📚 Additional Resources

### Books
- **Systems Programming:** "The Linux Programming Interface" - Michael Kerrisk
- **Algorithms:** "Introduction to Algorithms" - CLRS
- **Computer Architecture:** "Computer Organization and Design" - Patterson & Hennessy
- **Compilers:** "Crafting Interpreters" - Bob Nystrom
- **OS Development:** "Operating Systems: Three Easy Pieces" - Remzi & Andrea
- **Spring Boot:** "Spring Boot in Action" - Craig Walls
- **NLP:** "Speech and Language Processing" - Jurafsky & Martin

### Online Courses
- MIT 6.824: Distributed Systems
- Stanford CS231n: CNNs for Visual Recognition
- Fast.ai: Practical Deep Learning
- Nand2Tetris Course (Coursera)

### Practice Platforms
- LeetCode (data structures & algorithms)
- HackerRank (various)
- Kaggle (ML/AI)
- OSDev.org (OS development)

---

## 🤝 Contributing

Contributions are welcome! Whether it's:
- Bug fixes
- New projects
- Improved education guides
- Additional examples
- Better explanations

Please feel free to open an issue or submit a pull request.

---

## 📄 License

These education aides and projects are provided as-is for educational purposes. Original project code is subject to their respective licenses.

---

## 🙏 Acknowledgments

- **Nand2Tetris:** Created by Noam Nisan and Shimon Schocken
- **Prompt Engineering Tutorial:** Anthropic
- **Forage Midas:** JPMC Forage Program
- **Challenging Projects (Text Editor, Space Invaders, Compiler, OS, Spreadsheet, Emulator):** Inspired by [Austin Z. Henley's blog post](https://austinhenley.com/blog/challengingprojects.html) "Challenging Projects Every Programmer Should Try"
- All other projects are educational implementations

---

## 🎯 Project Status

| Project | Status | Documentation | Tests |
|---------|--------|---------------|-------|
| Count Primes | ✅ Complete | ✅ Full guide | ⚠️ Partial |
| Hash Track | ✅ Complete | ✅ Full guide | ⚠️ Partial |
| Simple Shell | ✅ Complete | ✅ Full guide | ⚠️ Partial |
| Reversal | ✅ Complete | ✅ Full guide | ⚠️ Partial |
| Git Tools | ✅ Complete | ✅ Full guide | ⚠️ Partial |
| Prompt Engineering | ✅ Complete | ✅ Full guide | N/A |
| Nand2Tetris | ✅ Complete | ✅ Full guide | ✅ Complete |
| Forage Midas | ✅ Complete | ✅ Full guide | ✅ Complete |
| AI Agents | ✅ Complete | ✅ Full guide | ⚠️ Partial |
| Text Editor | 📁 Starter | ✅ Full guide | ❌ Not started |
| Space Invaders | 📁 Starter | ✅ Full guide | ❌ Not started |
| Tiny BASIC Compiler | 📁 Starter | ✅ Full guide | ❌ Not started |
| Mini OS | 📁 Starter | ✅ Full guide | ❌ Not started |
| Spreadsheet | 📁 Starter | ✅ Full guide | ❌ Not started |
| Console Emulator | 📁 Starter | ✅ Full guide | ❌ Not started |
| CS First Principles | ✅ Complete | ✅ Full curriculum | N/A |

---

**Happy Learning! Remember: Understanding beats memorization. Build from first principles.**

---

*Last Updated: 2025*
*Use `claude code` to get interactive help with any project*
