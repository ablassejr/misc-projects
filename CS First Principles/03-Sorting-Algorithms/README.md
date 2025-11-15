# Project 03: Sorting Algorithms from First Principles

## Overview

This project teaches you how to design and analyze algorithms by implementing sorting from first principles. You'll understand why different algorithms have different performance characteristics and how to choose the right one for your needs.

## What You'll Learn

- How to analyze algorithm complexity (Big O notation)
- The fundamental sorting algorithms and their trade-offs
- Divide-and-conquer algorithm design
- The theoretical limits of comparison-based sorting
- Non-comparison sorts for special cases
- How to choose the right algorithm for your data

## Files

- **GUIDE.md** - Interactive guide with deep algorithmic insights
- **sorting.py** - Implementation challenges for 8+ sorting algorithms

## Sorting Algorithms Covered

### Simple Sorts (O(n²))
- **Bubble Sort** - Understanding through bubbling
- **Insertion Sort** - How humans sort cards
- **Selection Sort** - Repeatedly selecting minimum

### Efficient Sorts (O(n log n))
- **Merge Sort** - Divide and conquer
- **Quick Sort** - Partition and conquer
- **Heap Sort** - Using data structures

### Special Case Sorts (O(n))
- **Counting Sort** - For integers in known range
- **Radix Sort** - Digit-by-digit sorting
- **Bucket Sort** - For uniformly distributed data

## How to Use

### Self-Guided Learning
1. Read `GUIDE.md` section by section
2. Answer questions to build intuition
3. Implement each algorithm in `sorting.py`
4. Compare performance on different data patterns
5. Complete the synthesis challenge

### Claude Code CLI Guided Mode
```bash
claude-code "Walk me through sorting algorithms from first principles. Start with bubble sort and help me understand why O(n²) happens."
```

## Prerequisites

- Basic Python knowledge
- Understanding of recursion
- Completed Projects 01-02 or equivalent

## Time Estimate

- Fast path: 4-5 hours
- Deep understanding: 8-10 hours
- Mastery (all challenges): 12-16 hours

## Key Concepts

### Algorithm Analysis
- Big O notation and growth rates
- Best, average, and worst-case analysis
- Amortized analysis
- Space complexity

### Algorithm Design Patterns
- Divide and conquer
- Greedy algorithms
- Using data structures
- In-place vs extra space

### Practical Considerations
- Stability
- Adaptivity
- Cache locality
- Constant factors

## Success Criteria

You've mastered this project when you can:
- Implement 8+ sorting algorithms from scratch
- Explain the time and space complexity of each
- Prove the O(n log n) lower bound for comparison sorts
- Choose the optimal algorithm for given constraints
- Analyze why theory and practice sometimes differ

## Experiments to Try

1. **Input Pattern Analysis**: Test each algorithm on:
   - Random data
   - Already sorted
   - Reverse sorted
   - Nearly sorted (90% sorted)
   - Many duplicates

2. **Size Scaling**: Measure how time grows with n

3. **Pivot Strategies**: Compare quicksort with different pivots

4. **Hybrid Algorithms**: Combine algorithms (e.g., quicksort + insertion sort)

## Extensions

- Implement parallel sorting algorithms
- Build interactive visualizations
- Analyze real-world data sorting
- Implement external sorting for data larger than memory

## Next Project

After mastering algorithm analysis, you're ready for **Project 04: Build an Interpreter**, where you'll learn how programming languages work from first principles.
