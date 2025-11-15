# Hash Track - Education Aide
## Understanding Hash Tables and Collision Resolution

### Overview
This guide will walk you through understanding hash tables, one of the most important data structures in computer science, and specifically how quadratic probing resolves collisions.

---

## Part 1: The Fundamental Problem

### Question 1: The Search Problem
**Imagine:** You have 1,000,000 student records. Given a student ID, how do you find their record quickly?

**Approach 1 - Linear Search:**
```
for each record:
    if record.id == target_id:
        return record
```
**Time Complexity:** O(n) - might check all 1,000,000 records!

**Approach 2 - Binary Search (sorted array):**
**Time Complexity:** O(log n) - much better! But...
**Problem:** Inserting new records is O(n) - have to maintain sorted order

**Question:** Is there a way to get O(1) average case for both search AND insert?

**Your Thought:** _[Think before revealing the answer]_

<details>
<summary>The Hash Table Solution</summary>

**Answer:** YES! Hash tables provide O(1) average case for:
- Search
- Insert
- Delete

**The Magic:** Use the data itself to determine where it should be stored!
</details>

---

## Part 2: Understanding Hash Functions

### What is Hashing?

**Core Idea:** Transform data into an array index.

**Example:**
```
Student ID: 123456
Hash Function: ID % 101 = 83
Store at index 83!
```

**Visual Model:**
```
Student ID    Hash Function         Array Index
─────────────────────────────────────────────────
  123456  ──►  123456 % 101  ──►      83
  234567  ──►  234567 % 101  ──►      63
  345678  ──►  345678 % 101  ──►      93
```

### Properties of Good Hash Functions

**Question:** What makes a hash function "good"?

**Your Ideas:** _[List properties you think are important]_

<details>
<summary>Essential Properties</summary>

**1. Deterministic:**
- Same input ALWAYS produces same output
- `hash(123456)` must always return same index

**2. Uniform Distribution:**
- Spread values evenly across array
- Minimize collisions

**3. Fast to Compute:**
- O(1) time complexity
- No complex calculations

**4. Minimize Collisions:**
- Different inputs should ideally map to different indices
- (But collisions are inevitable - we'll handle them!)

**Common Hash Functions:**
```c
// Division method (used in this project)
int hash(int key, int tableSize) {
    return key % tableSize;
}

// Multiplication method
int hash(int key, int tableSize) {
    double A = 0.6180339887;  // (√5 - 1) / 2
    return (int)(tableSize * (key * A - (int)(key * A)));
}
```
</details>

### The Collision Problem

**Question:** What happens when two different keys hash to the same index?

**Example:**
```
Student ID: 123456  → 123456 % 101 = 83
Student ID: 123557  → 123557 % 101 = 83  // Collision!
```

**Visual:**
```
Array Index 83:
┌────┐
│ ?? │  ← Who goes here? Both IDs hash to 83!
└────┘
```

**Your Solution:** _[How would you handle this?]_

<details>
<summary>Collision Resolution Strategies</summary>

**1. Chaining (Separate Chaining):**
```
Index 83:  [123456] → [123557] → NULL
           (Linked list of colliding items)
```
**Pros:** Simple, never "full"
**Cons:** Extra memory for pointers, cache-unfriendly

**2. Open Addressing (this project uses this!):**
- Linear Probing: Check next slot: 83, 84, 85, 86...
- Quadratic Probing: Check quadratically: 83, 84, 87, 94, 105...
- Double Hashing: Use second hash function

**Pros:** Better cache locality, no extra pointers
**Cons:** Can become "full", clustering issues
</details>

---

## Part 3: Quadratic Probing Deep Dive

### How Quadratic Probing Works

**Formula:**
```
index = (hashIndex + i²) % tableSize

where i = 0, 1, 2, 3, ...
```

**Sequence:**
```
i = 0:  (hashIndex + 0²) % tableSize = hashIndex
i = 1:  (hashIndex + 1²) % tableSize = hashIndex + 1
i = 2:  (hashIndex + 2²) % tableSize = hashIndex + 4
i = 3:  (hashIndex + 3²) % tableSize = hashIndex + 9
i = 4:  (hashIndex + 4²) % tableSize = hashIndex + 16
```

**Question:** Why is this better than linear probing?

**Your Analysis:** _[Compare with linear probing: hashIndex, hashIndex+1, hashIndex+2...]_

<details>
<summary>Quadratic vs Linear Probing</summary>

**Linear Probing Problem - Primary Clustering:**
```
Filled: [X][X][X][X][X][ ][ ]
New insertion: High probability of extending the cluster!
Result: Long chains of occupied slots
```

**Quadratic Probing Advantage:**
```
Filled: [X][ ][X][ ][ ][X][ ]
New insertion: Jumps over filled slots more effectively
Result: Less clustering, better distribution
```

**Trade-off:** Quadratic probing is more complex but distributes better.
</details>

### The Hash Track Implementation

**Study this code from hashT.h (lines 75-102):**

```cpp
template <class elemType>
void hashT<elemType>::insert(int hashIndex, const elemType& rec)
{
    int pCount;
    int inc;

    pCount = 0;
    inc = 1;

    while (indexStatusList[hashIndex] == 1
        && HTable[hashIndex] != rec && pCount < HTSize / 2)
    {
        pCount++;
        hashIndex = (hashIndex + inc) % HTSize;
        inc = inc + 2;
    }

    if (indexStatusList[hashIndex] != 1)
    {
        HTable[hashIndex] = rec;
        indexStatusList[hashIndex] = 1;
        length++;
    }
    else if (HTable[hashIndex] == rec)
        std::cerr << "Error: No duplicates are allowed.\n";
    else
        std::cerr << "Error: The table is full. "
        << "Unable to resolve the collision.\n";
}
```

### Critical Analysis Questions

**Question 1:** How does `inc = inc + 2` implement quadratic probing?

**Your Analysis:** _[Trace through the values of inc]_

<details>
<summary>Understanding the Implementation</summary>

**Trace:**
```
Iteration  pCount  inc  Offset from original hashIndex
─────────────────────────────────────────────────────
    0        0      1         0
    1        1      1         1  (0 + 1)
    2        2      3         4  (1 + 3)
    3        3      5         9  (4 + 5)
    4        4      7        16  (9 + 7)
```

**The Pattern:**
```
inc sequence: 1, 3, 5, 7, 9, 11, ...
offset sequence: 0, 1, 4, 9, 16, 25, ... (perfect squares!)
```

**Mathematical Insight:**
```
1 = 1
1 + 3 = 4 = 2²
1 + 3 + 5 = 9 = 3²
1 + 3 + 5 + 7 = 16 = 4²

Sum of first n odd numbers = n²
```

This clever implementation achieves quadratic probing by adding successive odd numbers!
</details>

**Question 2:** What is the purpose of `indexStatusList`?

**Your Thought:** _[Why not just check if HTable[i] is empty?]_

<details>
<summary>The Three States</summary>

**The Problem:**
```
Insert 42 at index 5
Delete 42
Insert 99 (hashes to 5)
Search for 42?
```

**Without Status Tracking:**
```
If we just mark deleted slots as "empty", search might stop too early!
```

**The Solution - Three States:**
```c
indexStatusList[i] == 0   // Empty (never used)
indexStatusList[i] == 1   // Occupied (currently has data)
indexStatusList[i] == -1  // Deleted (had data, now removed)
```

**Why This Matters:**
```
Array: [42][99][--][ ]
Status: [1][1][-1][0]

Searching for 99:
- Start at index 0 (42), not a match
- Check index 1 (99), found it!

If we treated deleted (-1) as empty (0):
- Start at index 0 (42), not a match
- Check index 1... looks empty?
- Might miss 99 if it was pushed further by collision!
```

**Search must continue through deleted slots!**
</details>

**Question 3:** Why stop at `pCount < HTSize / 2`?

**Your Analysis:** _[What happens if we keep searching forever?]_

<details>
<summary>Theoretical Limit</summary>

**Theorem:** With quadratic probing and a prime table size, you're guaranteed to visit at least half the table.

**Practical Implication:**
- If we've checked HTSize/2 positions and found no empty slot
- The table is too full (load factor too high)
- Should resize or report error

**Load Factor:** λ = n / m (items / table size)
- λ < 0.5: Good performance
- λ > 0.5: Performance degrades
- λ > 0.75: Serious performance issues

**Question:** Why not check the entire table?

**Answer:** Quadratic probing may not visit all slots! Better to fail fast and resize.
</details>

---

## Part 4: Template Programming in C++

### Understanding Templates

**Study the class declaration:**
```cpp
template <class elemType>
class hashT
{
private:
    elemType* HTable;
    int* indexStatusList;
    int length;
    int HTSize;
};
```

**Question:** What problem do templates solve?

**Your Understanding:** _[Why not just use a specific type like int?]_

<details>
<summary>The Power of Generic Programming</summary>

**Without Templates:**
```cpp
class IntHashTable {
    int* HTable;
    // Only works for integers!
};

class StringHashTable {
    string* HTable;
    // Duplicate code for strings!
};

class StudentHashTable {
    Student* HTable;
    // Duplicate code again!
};
```

**With Templates:**
```cpp
template <class elemType>
class hashT {
    elemType* HTable;
    // Works for ANY type!
};

// Usage:
hashT<int> intTable(101);
hashT<string> stringTable(101);
hashT<Student> studentTable(101);
```

**Benefits:**
1. **Code Reuse:** Write once, use for any type
2. **Type Safety:** Compiler checks types at compile time
3. **Performance:** No runtime overhead (unlike inheritance)
4. **Flexibility:** Users can use with custom types
</details>

### Template Implementation Details

**Important:** Template implementations must be in header files!

**Question:** Why can't we put template code in .cpp files like normal code?

**Your Thought:** _[Think about the compilation process]_

<details>
<summary>Compilation Model</summary>

**Normal Class:**
```
MyClass.h  ─┐
            ├─► Compile separately ─► Link ─► Executable
MyClass.cpp ┘
```

**Template Class:**
```
Templates are not compiled until used!
Compiler needs full definition at instantiation point.
```

**Example:**
```cpp
// main.cpp
#include "hashT.h"

int main() {
    hashT<int> table(101);  // Compiler generates hashT<int> HERE
                            // Needs complete implementation!
}
```

**Solution:** Put everything in .h file so it's available when needed.
</details>

---

## Part 5: Memory Management

### Constructor Analysis

**Study the constructor (lines 162-172):**
```cpp
template <class elemType>
hashT<elemType>::hashT(int size) : HTSize(size)
{
    HTable = new elemType[HTSize];
    indexStatusList = new int[HTSize];

    for (int i = 0; i < HTSize; i++)
        indexStatusList[i] = 0;

    length = 0;
}
```

**Question 1:** What is `: HTSize(size)` syntax?

<details>
<summary>Member Initializer List</summary>

**Two ways to initialize:**
```cpp
// Method 1: In constructor body
hashT(int size) {
    HTSize = size;  // Assignment
}

// Method 2: Initializer list (better!)
hashT(int size) : HTSize(size) {
    // HTSize is constructed with value 'size'
}
```

**Why Initializer Lists are Better:**
1. More efficient (construct once vs construct then assign)
2. Required for const members
3. Required for references
4. Required for members without default constructors
</details>

**Question 2:** What's the memory layout?

**Your Visualization:** _[Draw the memory]_

<details>
<summary>Memory Model</summary>

```
hashT object (on stack or heap):
┌─────────────────────┐
│ HTable     ─────────┼──► [elemType][elemType][...][elemType]
│                     │     HTSize elements (on heap)
│ indexStatusList ────┼──► [int][int][int][...][int]
│                     │     HTSize elements (on heap)
│ length = 0          │
│ HTSize = 101        │
└─────────────────────┘

indexStatusList initialized to 0 (empty):
[0][0][0][0][0]...[0]
```

**Important:** We have dynamic allocation! Must free in destructor.
</details>

### Destructor Analysis

**Study the destructor (lines 174-179):**
```cpp
template <class elemType>
hashT<elemType>::~hashT()
{
    delete[] HTable;
    delete[] indexStatusList;
}
```

**Question:** Why `delete[]` instead of `delete`?

<details>
<summary>Array vs Single Object Deletion</summary>

**delete vs delete[]:**
```cpp
// Single object
elemType* obj = new elemType;
delete obj;  // Correct

// Array
elemType* arr = new elemType[100];
delete[] arr;  // Correct - calls destructors for all elements

// ❌ WRONG:
elemType* arr = new elemType[100];
delete arr;  // Undefined behavior! Only deletes first element
```

**Rule:** Match allocation with deallocation:
- `new` → `delete`
- `new[]` → `delete[]`
</details>

---

## Part 6: Search Implementation

**Study the search function (lines 104-119):**

```cpp
template <class elemType>
void hashT<elemType>::search(int& hashIndex, const elemType& rec,
    bool& found) const
{
    int inc = 1;

    while ((indexStatusList[hashIndex] == 1 ||
        indexStatusList[hashIndex] == -1)
        && HTable[hashIndex] != rec)
    {
        hashIndex = (hashIndex + inc) % HTSize;
        inc = inc + 2;
    }

    found = HTable[hashIndex] == rec;
}
```

### Critical Thinking Questions

**Question 1:** Why pass `hashIndex` by reference?

**Your Answer:** _[Think about the function's purpose]_

<details>
<summary>Multiple Return Values</summary>

**The function returns TWO pieces of information:**
1. `found` (bool) - Was the item found?
2. `hashIndex` (int&) - WHERE was it found?

**Usage:**
```cpp
int index = calculateHash(key);
bool found;
search(index, key, found);

if (found) {
    // index now contains the location!
    retrieve(index, result);
}
```

**Alternative Modern Design:**
```cpp
struct SearchResult {
    bool found;
    int index;
};

SearchResult search(int hashIndex, const elemType& rec) const {
    // Return struct instead of reference parameters
}
```
</details>

**Question 2:** Why check deleted slots `(indexStatusList[hashIndex] == -1)` during search?

**Trace This Scenario:**
```
1. Insert 42 at index 5
2. Collision! Insert 99 at index 6
3. Delete 42 (mark index 5 as -1)
4. Search for 99?
```

**Your Trace:** _[Step through the search]_

<details>
<summary>The Answer</summary>

```
Initial: [42][99]
Status:  [1][1]

After deleting 42:
Array:   [42][99]
Status:  [-1][1]

Searching for 99:
- Start at index 5 (hashIndex for 99)
- Index 5 is deleted (-1), not empty (0)
- Must continue searching! 99 might have been pushed here by collision
- Check index 6
- Found it!

If we stopped at deleted slots:
- Would incorrectly report "not found"
```

**Key Insight:** Deleted slots might have caused other items to probe further. Must continue through them during search!
</details>

---

## Part 7: Remove Implementation

**Study the remove function (lines 138-151):**

```cpp
template <class elemType>
void hashT<elemType>::remove(int hashIndex, const elemType& rec)
{
    if (indexStatusList[hashIndex] == 1 && HTable[hashIndex] == rec)
        indexStatusList[hashIndex] = -1;
    else {
        bool found = false;
        search(hashIndex, rec, found);
        if (found)
            indexStatusList[hashIndex] = -1;
        else
            std::cerr << "Error: " << rec << " not found in hash table.\n";
    }
}
```

**Question:** Why not actually delete the data, just mark as -1?

**Your Understanding:** _[What happens to the data in HTable?]_

<details>
<summary>Lazy Deletion</summary>

**What happens:**
```cpp
Before remove:
HTable[5] = 42
indexStatusList[5] = 1

After remove:
HTable[5] = 42  // Still there!
indexStatusList[5] = -1  // But marked as deleted
```

**Why this works:**
1. **Search:** Checks status list, ignores deleted items
2. **Insert:** Can overwrite deleted slots
3. **Performance:** No need to move data

**Trade-off:**
- **Pro:** Fast deletion O(1)
- **Con:** Memory not actually freed until table is destroyed
- **Con:** Deleted slots still take space

**Advanced:** Some implementations periodically "rehash" to reclaim space from deleted items.
</details>

---

## Part 8: Table Size and Prime Numbers

**Notice:** Default table size is 101 (a prime number).

**Question:** Why use a prime number for table size?

**Your Hypothesis:** _[Think about division and modulo]_

<details>
<summary>Mathematical Reasoning</summary>

**Problem with Composite Numbers:**
```
Table size = 100
Hash values with common factors cluster!

If keys are multiples of 10:
10 % 100 = 10
20 % 100 = 20
110 % 100 = 10  // Collision!
120 % 100 = 20  // Collision!
```

**Prime Numbers:**
- No common factors (except 1)
- Better distribution
- Quadratic probing works better

**Quadratic Probing Theorem:**
If table size is prime and load factor < 0.5, quadratic probing will find an empty slot (if one exists).

**Common Prime Table Sizes:**
```
53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, ...
```

**Pattern:** Each is roughly double the previous (for resizing)
</details>

---

## Part 9: Hands-On Exercises

### Exercise 1: Trace Insertions
**Task:** Manually trace quadratic probing with these operations:

```
Table size: 11 (prime)
Hash function: key % 11

Operations:
1. Insert 23  (23 % 11 = 1)
2. Insert 34  (34 % 11 = 1)  // Collision!
3. Insert 45  (45 % 11 = 1)  // Collision!
4. Insert 56  (56 % 11 = 1)  // Collision!
5. Insert 12  (12 % 11 = 1)  // Collision!
```

**Your Trace:**
```
Index:  [0][1][2][3][4][5][6][7][8][9][10]
Data:   [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
Status: [0][0][0][0][0][0][0][0][0][0][0]

After insert 23:
...

After insert 34:
...
```

<details>
<summary>Solution</summary>

```
After insert 23:
Index:  [0][1][2][3][4][5][6][7][8][9][10]
Data:   [ ][23][ ][ ][ ][ ][ ][ ][ ][ ][ ]
Status: [0][1][0][0][0][0][0][0][0][0][0]

After insert 34:
Hash index = 1 (occupied)
Probe: (1 + 1) % 11 = 2 ✓ empty
Index:  [0][1][2][3][4][5][6][7][8][9][10]
Data:   [ ][23][34][ ][ ][ ][ ][ ][ ][ ][ ]
Status: [0][1][1][0][0][0][0][0][0][0][0]

After insert 45:
Hash index = 1 (occupied, != 45)
Probe: (1 + 1) % 11 = 2 (occupied, != 45)
Probe: (1 + 4) % 11 = 5 ✓ empty
Index:  [0][1][2][3][4][5][6][7][8][9][10]
Data:   [ ][23][34][ ][ ][45][ ][ ][ ][ ][ ]
Status: [0][1][1][0][0][1][0][0][0][0][0]

After insert 56:
Hash index = 1 (occupied)
Probes: 2 (occupied), 5 (occupied), 10, wraps to 6 ✓ empty
Index:  [0][1][2][3][4][5][6][7][8][9][10]
Data:   [ ][23][34][ ][ ][45][56][ ][ ][ ][ ]
Status: [0][1][1][0][0][1][1][0][0][0][0]

After insert 12:
Hash index = 1 (occupied)
Probes: 2, 5, 10, 6 (occupied), then (1 + 16) % 11 = 6...
Then (1 + 25) % 11 = 4 ✓ empty
Index:  [0][1][2][3][4][5][6][7][8][9][10]
Data:   [ ][23][34][ ][12][45][56][ ][ ][ ][ ]
Status: [0][1][1][0][1][1][1][0][0][0][0]
```
</details>

### Exercise 2: Implement Linear Probing
**Task:** Modify the insert function to use linear probing instead of quadratic.

**Hint:** Change how `hashIndex` is updated.

### Exercise 3: Add Resizing
**Task:** Implement a resize function that doubles the table size (to next prime) when load factor exceeds 0.5.

**Steps:**
1. Calculate next prime number
2. Create new larger table
3. Rehash all existing items
4. Update pointers

### Exercise 4: Performance Analysis
**Task:** Compare performance of linear vs quadratic probing.

**Metrics to measure:**
- Average number of probes for insertion
- Average number of probes for search
- Clustering patterns

**Test with:**
- Random data
- Sequential data (1, 2, 3, 4, ...)
- Patterned data (10, 20, 30, ...)

---

## Part 10: First Principles Summary

### Core Concepts Learned

**1. Hash Tables:**
- Trade space for time
- Average O(1) operations
- Require good hash functions
- Must handle collisions

**2. Collision Resolution:**
- **Chaining:** Linked lists at each slot
- **Open Addressing:** Find another slot
  - Linear probing: +1, +2, +3, ...
  - Quadratic probing: +1², +2², +3², ...
  - Double hashing: Use second hash function

**3. Load Factor:**
```
λ = n / m = (number of elements) / (table size)

λ < 0.5: Excellent performance
λ = 0.7: Good performance
λ > 0.8: Degraded performance
λ = 1.0: Table full (open addressing fails!)
```

**4. Template Programming:**
- Generic, reusable code
- Type-safe
- Compile-time instantiation
- Implementation in headers

**5. Memory Management:**
- Constructor allocates
- Destructor deallocates
- Match new[] with delete[]
- Avoid memory leaks

### Design Trade-offs

**Chaining vs Open Addressing:**

| Aspect | Chaining | Open Addressing |
|--------|----------|-----------------|
| Memory | Extra pointers | Compact |
| Cache | Poor locality | Good locality |
| Load Factor | Can exceed 1.0 | Must stay < 1.0 |
| Deletion | Easy | Complex (tombstones) |

**When to Use Hash Tables:**
- Need fast lookups
- Order doesn't matter
- Have good hash function
- Know approximate size

**When NOT to Use:**
- Need sorted order (use BST)
- Need range queries (use BST)
- Small dataset (array might be faster)
- Many deletions (chaining might be better)

---

## Part 11: Advanced Topics

### 1. Universal Hashing
**Idea:** Randomly select hash function from a family to prevent worst-case attack.

### 2. Perfect Hashing
**Idea:** If dataset is known and static, can construct collision-free hash function.

### 3. Cuckoo Hashing
**Idea:** Use two hash functions, "kick out" existing items if collision occurs.

### 4. Robin Hood Hashing
**Idea:** Steal from the rich (items close to their ideal position) to give to the poor.

---

## How to Use This Guide with Claude Code CLI

```bash
# Start interactive session
claude code

# Ask questions like:
"Explain how quadratic probing differs from linear probing"
"Walk me through Exercise 1 step by step"
"Why do we use prime numbers for hash table sizes?"
"Help me implement the resize function for Exercise 3"
"Compare the pros and cons of chaining vs open addressing"
"Trace a search operation with deleted slots"
```

**Interactive Learning:**
- Ask for clarification on any concept
- Request visual diagrams
- Get hints for exercises before seeing solutions
- Discuss real-world applications
- Explore advanced topics
