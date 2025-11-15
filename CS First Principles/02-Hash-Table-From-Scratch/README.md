# Project 02: Hash Tables from Scratch

## Overview

This project teaches you how to build one of the most important data structures in computer science from first principles. You'll understand why hash tables achieve O(1) average-case lookup and how to handle the challenges that arise.

## What You'll Learn

- **The fundamental problem**: How to achieve constant-time lookup
- How hash functions work and what makes them good
- Different collision resolution strategies and their trade-offs
- Dynamic resizing and amortized analysis
- Advanced applications: Sets, LRU caches, Bloom filters
- The mathematics behind hash table performance

## Files

- **GUIDE.md** - Interactive educational guide with questions and deep explanations
- **hash_table.py** - Implementation challenges for multiple hash table variants

## How to Use

### Self-Guided Learning
1. Read through `GUIDE.md` section by section
2. Answer each question before revealing solutions
3. Implement the corresponding functions in `hash_table.py`
4. Test and compare different implementations
5. Complete the spell checker synthesis project

### Claude Code CLI Guided Mode
```bash
claude-code "Walk me through the Hash Table project step by step. Ask me the questions from GUIDE.md and help me implement each part."
```

## Prerequisites

- Basic Python knowledge
- Understanding of arrays and linked lists
- Completed Project 01 (Binary Basics) or equivalent knowledge

## Time Estimate

- Fast path: 3-4 hours
- Deep understanding: 6-8 hours
- Mastery (with all challenges): 10-15 hours

## Key Concepts Covered

### Part 1: Hash Functions
- Properties of good hash functions
- Simple vs polynomial hashing
- Distribution analysis

### Part 2: Collision Resolution
- Separate chaining
- Open addressing (linear probing)
- Double hashing
- Trade-offs and performance

### Part 3: Dynamic Resizing
- Load factor analysis
- Amortized time complexity
- Rehashing strategies

### Part 4: Advanced Applications
- Hash sets
- LRU caches (hash table + linked list)
- Bloom filters (probabilistic data structures)

### Part 5: Real-World Application
- Build a spell checker
- Performance analysis
- Design decisions

## Success Criteria

You've mastered this project when you can:
- Explain why hash tables achieve O(1) average case from first principles
- Implement a production-quality hash table from scratch
- Choose appropriate collision resolution strategies
- Analyze performance using load factor
- Explain the trade-offs in hash table design
- Build advanced data structures using hash tables as primitives

## Testing Your Implementation

```python
# Test hash functions
python hash_table.py

# Compare collision strategies
# Implement benchmark_collision_strategies() and run

# Build spell checker
# Implement test_spell_checker() and run
```

## Common Pitfalls

1. **Forgetting to rehash during resize** - Hash values depend on table size!
2. **Deletion in open addressing** - Must use tombstones
3. **Infinite loops in probing** - Ensure table never completely full
4. **Poor hash function** - Leads to clustering and poor performance

## Extensions

Once you've completed the basic project:
- Implement Robin Hood hashing
- Build a concurrent hash table with locks
- Experiment with different hash functions (MurmurHash, etc.)
- Analyze hash table performance with real-world data

## Next Project

After understanding hash tables, you're ready for **Project 03: Sorting Algorithms**, where you'll learn how to efficiently organize data and analyze algorithm complexity.
