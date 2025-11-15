# Computer Science from First Principles

A comprehensive, hands-on curriculum designed to teach computer science from foundational concepts to advanced applications. Each project includes an interactive educational guide (GUIDE.md) that works with Claude Code CLI to walk you through thought processes and decisions.

## 🎯 Philosophy

This curriculum is built on the belief that:
- **Understanding beats memorization** - Know WHY, not just HOW
- **First principles matter** - Build from fundamental concepts
- **Questions precede answers** - Think before learning solutions
- **Implementation solidifies learning** - Code what you learn

## 📚 Curriculum Overview

The projects progress from foundational concepts to complex applications:

### Project 01: Binary Basics
**Foundation: How Computers Represent Data**
- Why binary? (transistors and reliability)
- Number systems and conversions
- Two's complement for negative numbers
- IEEE 754 floating-point representation
- Text encoding (ASCII, UTF-8)

**Time:** 4-10 hours | **Difficulty:** Beginner

### Project 02: Hash Tables from Scratch
**Foundation: Efficient Data Access**
- The O(1) lookup problem
- Hash functions and their properties
- Collision resolution strategies
- Dynamic resizing and amortized analysis
- Advanced applications (LRU cache, Bloom filters)

**Time:** 6-15 hours | **Difficulty:** Intermediate

### Project 03: Sorting Algorithms
**Foundation: Algorithm Design and Analysis**
- Big O notation and complexity analysis
- Simple sorts (O(n²))
- Divide-and-conquer (O(n log n))
- Non-comparison sorts (O(n))
- Choosing the right algorithm

**Time:** 8-16 hours | **Difficulty:** Intermediate

### Project 04: Build an Interpreter
**Foundation: How Code Executes**
- Lexical analysis (tokenization)
- Parsing and AST construction
- Evaluation and execution
- Variable scoping and closures
- Functions and recursion

**Time:** 15-25 hours | **Difficulty:** Advanced

### Project 05: TCP/IP Protocol Simulator
**Foundation: Network Communication**
- IP addressing and routing
- Reliable delivery over unreliable networks
- Flow control and congestion control
- The three-way handshake
- Real-world network conditions

**Time:** 20-30 hours | **Difficulty:** Advanced

## 🚀 How to Use This Curriculum

### Three Learning Modes

#### 1. Self-Guided Deep Learning
**Best for:** Those who want complete mastery
```
For each project:
1. Open the GUIDE.md file
2. Read each section carefully
3. Answer questions BEFORE revealing solutions
4. Implement the code challenges
5. Complete the synthesis project
6. Extend with your own ideas
```

#### 2. Claude Code CLI Guided Mode
**Best for:** Interactive, conversational learning
```bash
# Start a project
cd "CS First Principles/01-Binary-Basics"

# Ask Claude Code to guide you
claude-code "Walk me through the Binary Basics GUIDE.md. Ask me each question and wait for my answer before revealing solutions."

# Get help on specific topics
claude-code "Explain two's complement from first principles with examples"

# Review your implementation
claude-code "Review my binary_converter.py against the GUIDE.md requirements"
```

#### 3. Fast-Track Implementation
**Best for:** Experienced programmers who want to fill knowledge gaps
```
For each project:
1. Skim the GUIDE.md to identify concepts you don't know well
2. Focus deeply on those sections
3. Implement the challenging parts
4. Test against edge cases
```

### Recommended Path

**Complete Beginner:**
```
01 → 02 → 03 → 04 → 05
Take your time, answer all questions, do all extensions
Estimated total time: 100+ hours
```

**CS Student Filling Gaps:**
```
Start with any project where concepts are unclear
Focus on the GUIDE.md questions
Implement the parts you find challenging
Estimated time: 20-40 hours
```

**Interview Preparation:**
```
02 (Hash Tables) → 03 (Sorting) → Focus on analysis
Do all the performance comparisons
Estimated time: 15-25 hours
```

**Systems/Network Focus:**
```
01 (Binary) → 04 (Interpreter) → 05 (TCP/IP)
Understand how systems work end-to-end
Estimated time: 40-60 hours
```

## 💡 Educational Features

### Interactive Guides (GUIDE.md)

Each project includes a comprehensive guide with:
- **First principles explanations** - Why things work the way they do
- **Socratic questions** - Build intuition before revealing answers
- **Progressive difficulty** - Start simple, build complexity
- **Real-world connections** - See how concepts apply
- **Synthesis challenges** - Combine everything learned

### Implementation Challenges

Starter code files include:
- **Clear TODOs** - Know what to implement
- **Hints** - Get unstuck without spoilers
- **Test cases** - Verify correctness
- **Extensions** - Go deeper if interested

### Claude Code CLI Integration

The guides are specifically designed to work with Claude Code:
```bash
# Questions and guided learning
claude-code "Guide me through [topic] asking questions before showing answers"

# Implementation help
claude-code "Help me implement [function] following the first principles in GUIDE.md"

# Debugging
claude-code "My [implementation] isn't working. Debug it using first principles"

# Extensions
claude-code "Help me extend [project] with [feature]"
```

## 🎓 Learning Outcomes

After completing this curriculum, you will:

### Conceptual Understanding
- Understand how computers work from transistors to applications
- Explain complex topics from first principles
- Debug issues by reasoning from fundamentals
- Design systems with awareness of trade-offs

### Technical Skills
- Implement fundamental data structures and algorithms
- Analyze time and space complexity
- Build interpreters and understand language design
- Understand network protocols and distributed systems

### Problem-Solving Abilities
- Break complex problems into manageable parts
- Choose appropriate tools and algorithms
- Optimize for different constraints
- Think critically about engineering decisions

## 📖 Project Structure

Each project directory contains:
```
01-Project-Name/
├── README.md          # Project overview and quick reference
├── GUIDE.md          # Comprehensive educational guide
└── implementation.py  # Starter code with TODOs
```

### README.md
- Quick overview
- Key concepts
- Prerequisites
- Time estimates
- Success criteria

### GUIDE.md
- First principles explanations
- Questions to build intuition
- Progressive challenges
- Synthesis projects
- Extension ideas

### Implementation Files
- Well-structured starter code
- Clear TODOs
- Hints and suggestions
- Test cases

## 🛠️ Prerequisites

### Required
- **Programming experience** - Basic Python knowledge
- **Curiosity** - Willingness to think deeply
- **Patience** - Learning from first principles takes time

### Helpful But Not Required
- Basic math (algebra, logarithms)
- Command line familiarity
- Previous CS coursework

### Setup
```bash
# Clone the repository
git clone [repository-url]

# Navigate to the curriculum
cd "misc-projects/CS First Principles"

# Start with any project
cd 01-Binary-Basics

# Read the guide
cat GUIDE.md

# Or use Claude Code CLI for interactive guidance
claude-code "Walk me through this project step by step"
```

## 🌟 Success Stories

What you can build after this curriculum:
- **Your own programming language** - You'll understand lexing, parsing, and evaluation
- **Network applications** - You'll know how data travels across the internet
- **Efficient algorithms** - You'll analyze and optimize code
- **System-level tools** - You'll understand how software interacts with hardware

## 🤝 How to Get the Most Out of This

### Do
✅ Answer questions before revealing solutions
✅ Implement code even if it seems simple
✅ Test edge cases and break your code
✅ Extend projects with your own ideas
✅ Explain concepts to others (or to Claude Code!)

### Don't
❌ Skip the questions and just read answers
❌ Copy code without understanding
❌ Rush through to "finish" projects
❌ Give up when stuck (ask for hints instead)

## 🔄 Iteration and Practice

Computer science concepts require practice:
- **First pass:** Understand the concepts
- **Second pass:** Implement from scratch without reference
- **Third pass:** Optimize and extend
- **Fourth pass:** Teach others or write about it

## 📈 Progress Tracking

Track your understanding:
```
For each project, rate your understanding (1-5):
□ Can explain the first principles
□ Can implement from scratch
□ Can debug issues
□ Can optimize performance
□ Can teach others

5/5 = Mastery
3-4/5 = Good understanding
1-2/5 = Review needed
```

## 🎯 Next Steps After Completion

Once you've completed this curriculum:
- **Build projects** - Apply what you learned
- **Study theory** - Dive into textbooks with strong foundation
- **Contribute to open source** - You understand how things work now!
- **Create your own projects** - Design from first principles
- **Teach others** - Solidify your understanding

## 📚 Additional Resources

While this curriculum is self-contained, you might enjoy:
- **Books:** "Structure and Interpretation of Computer Programs", "The Algorithm Design Manual"
- **Courses:** MIT OpenCourseWare, Stanford CS courses
- **Practice:** LeetCode, Project Euler
- **Community:** Computer Science Discord servers, Reddit r/learnprogramming

## 🙏 Philosophy on Learning

This curriculum embodies these principles:
1. **First principles > memorization**
2. **Understanding > implementation**
3. **Questions > answers**
4. **Practice > theory**
5. **Depth > breadth**

Take your time. Think deeply. Build solidly.

## 📞 Getting Help

When stuck:
1. **Re-read the question** - Often the answer is there
2. **Try simple examples** - Build intuition
3. **Ask Claude Code CLI** - "Help me understand [concept] from first principles"
4. **Implement a simpler version** - Then build up
5. **Take a break** - Fresh perspective helps

## 🚦 Getting Started

```bash
# Start with Project 01
cd "01-Binary-Basics"

# Choose your mode:

# Self-guided:
less GUIDE.md

# Interactive with Claude Code:
claude-code "I want to learn binary representation from first principles. Guide me through GUIDE.md, asking questions and checking my understanding."

# Then implement:
python binary_converter.py
```

---

**Remember:** Computer science is about understanding how to solve problems with computation. These projects teach you to think like a computer scientist, not just to code. Take your time, think deeply, and enjoy the journey from first principles to mastery!

## 📋 Quick Reference

| Project | Core Concept | Key Insight | Time |
|---------|--------------|-------------|------|
| 01 | Binary Representation | All data is numbers with interpretation | 4-10h |
| 02 | Hash Tables | Hash functions enable O(1) lookup | 6-15h |
| 03 | Sorting | Algorithm analysis guides design | 8-16h |
| 04 | Interpreters | Code is data that can be interpreted | 15-25h |
| 05 | TCP/IP | Reliability can be built on unreliable foundations | 20-30h |

**Total estimated time:** 50-100+ hours for complete mastery

Start anywhere, learn everything! 🚀
