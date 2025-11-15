# Hash Tables: Building Efficient Data Structures from First Principles

## 🎯 Learning Objectives

By the end of this project, you will understand:
- The fundamental problem hash tables solve (O(1) lookup!)
- How hash functions work and what makes them good
- How to handle collisions (multiple keys hashing to same slot)
- The trade-offs between different collision resolution strategies
- Why hash tables are one of the most important data structures in CS

## 📚 First Principles Foundation

### The Lookup Problem

**PAUSE AND THINK:** Let's start with a real problem.

**Question 1:** You have a list of 1 million names and phone numbers. Someone asks you "What's Alice's phone number?"

If you store them in an array in random order, how many items might you need to check in the worst case?

<details>
<summary>Click after answering</summary>

**Answer:** All 1 million items (if Alice is last or not present)

**On average:** 500,000 items

**Time complexity:** O(n) - linear search

**Key Insight:** This gets slower as your data grows. Can we do better?
</details>

---

**Question 2:** What if the array was sorted? Could you find Alice faster?

<details>
<summary>Click after thinking</summary>

**Answer:** Yes! Use binary search:
- Check middle item
- If Alice is earlier, search first half
- If Alice is later, search second half
- Repeat

**Worst case:** log₂(1,000,000) ≈ 20 comparisons

**Time complexity:** O(log n) - much better!

**But can we do even better?**
</details>

---

### The Dream: O(1) Lookup

**Question 3:** Imagine you could magically convert a name directly into an array index. How many lookups would you need?

<details>
<summary>Click after answering</summary>

**Answer:** Just ONE!

```
index = magic_function("Alice")
phone = array[index]
```

**This is the hash table promise: O(1) average case lookup!**

**Key Insight:** If we can compute where data should be stored, we can find it instantly.
</details>

---

## 🔨 Project Overview

You'll build a **Hash Table from scratch** that:
1. Implements hash functions from first principles
2. Handles collisions gracefully
3. Dynamically resizes when needed
4. Achieves O(1) average case performance
5. Understands the trade-offs in hash table design

## 📖 Part 1: Hash Functions

### What Makes a Good Hash Function?

**Question 4:** A hash function converts a key (like "Alice") to an integer. What properties should it have?

Think about:
- Should "Alice" always hash to the same value?
- Should "Alice" and "Bob" hash to the same value?
- Should "Alice" and "alice" hash to the same value?

<details>
<summary>Click after thinking</summary>

**Essential properties:**
1. **Deterministic:** Same input always gives same output
2. **Uniform distribution:** Spreads values evenly across range
3. **Fast to compute:** Must be quick!

**Desirable properties:**
4. **Avalanche effect:** Small input change → big output change
5. **Minimize collisions:** Different inputs should rarely hash to same value

**Key Insight:** Perfect hash functions (no collisions) are impossible for general use, but we can get close!
</details>

---

### Building a Simple Hash Function

**Question 5:** Let's hash strings. Simplest approach - add up character ASCII values:

```python
def simple_hash(s):
    return sum(ord(c) for c in s)
```

What's wrong with this approach?

<details>
<summary>Click after thinking</summary>

**Problems:**
1. **Anagrams collide:** "listen" and "silent" have same hash
2. **Limited range:** For alphabet letters, max is roughly length × 122
3. **Patterns:** "aaa" and "bbb" are predictably spaced

**Key Insight:** We need to account for character POSITION, not just presence!
</details>

---

**Question 6:** Better approach - multiply each character by its position:

```python
def better_hash(s):
    total = 0
    for i, c in enumerate(s):
        total += ord(c) * (i + 1)
    return total
```

Is this good enough? What issues remain?

<details>
<summary>Click after thinking</summary>

**Improvement:** Anagrams no longer collide!

**Remaining issues:**
1. Still predictable patterns
2. Values can get HUGE (integer overflow in some languages)
3. Need to fit into array size

**Solution:** Use a prime number multiplier and modulo!
</details>

---

### The Polynomial Rolling Hash

**Question 7:** Industry-standard approach:

```python
def polynomial_hash(s, prime=31, table_size=1000):
    hash_value = 0
    for c in s:
        hash_value = (hash_value * prime + ord(c)) % table_size
    return hash_value
```

Why use a prime number (like 31)?

<details>
<summary>Click after thinking</summary>

**Answer:** Primes reduce patterns and collisions!

- Prime numbers have no common factors with table size
- This spreads values more uniformly
- Mathematically proven to reduce clustering

**Why 31 specifically?**
- Small enough to avoid overflow
- 31 × n = 32 × n - n = (n << 5) - n (fast bitshift!)
- Empirically tested and works well

**Key Insight:** Good hash functions use properties from number theory!
</details>

---

### 💻 Implementation Challenge 1

In `hash_table.py`, implement:
- `simple_hash()` - the bad version
- `polynomial_hash()` - the good version
- `test_hash_distribution()` - compare their collision rates

**Experiment:** Hash 1000 random words. Which function has fewer collisions?

---

## 📖 Part 2: Handling Collisions

### The Pigeonhole Principle

**Question 8:** You have an array of size 100, but need to store 1000 items.

By the pigeonhole principle, what's guaranteed to happen?

<details>
<summary>Click after thinking</summary>

**Answer:** At least some slots will have multiple items (collisions)!

**Mathematical certainty:** Can't avoid all collisions with more items than slots.

**Key Insight:** We MUST have a collision resolution strategy!
</details>

---

### Strategy 1: Separate Chaining

**Question 9:** Instead of storing values directly in the array, what if each array slot holds a list of items?

```
Array:
[0] → []
[1] → [("Alice", "555-0001")]
[2] → [("Bob", "555-0002"), ("Charlie", "555-0003")]  ← collision!
[3] → []
...
```

What's the worst-case lookup time if everything hashes to the same slot?

<details>
<summary>Click after thinking</summary>

**Answer:** O(n) - degrades to a linked list!

**Average case:** O(1 + α) where α = n/m (load factor)
- n = number of items
- m = array size
- α = average items per slot

**Key Insight:** Performance degrades gracefully as table fills up.
</details>

---

**Question 10:** If you have 100 slots and 75 items (load factor α = 0.75), how many items do you expect to check on average?

<details>
<summary>Click after calculating</summary>

**Answer:** 1.75 items on average

**Calculation:** 1 (array lookup) + 0.75 (avg chain length)

**Strategy:** Keep load factor < 0.75 for good performance!

**Key Insight:** When α gets too high, resize the array!
</details>

---

### Strategy 2: Open Addressing (Linear Probing)

**Question 11:** Instead of chains, what if we just look for the next empty slot?

```python
def insert(key, value):
    index = hash(key) % size
    while table[index] is not None:
        index = (index + 1) % size  # Try next slot
    table[index] = (key, value)
```

What problem might this cause?

<details>
<summary>Click after thinking</summary>

**Problem:** Primary clustering!

- Occupied slots form contiguous blocks
- Blocks grow larger over time
- Longer search times in clustered regions

**Example:**
```
[_, _, X, X, X, X, X, _, _]  ← Hard to insert near this cluster!
```

**Key Insight:** The collision resolution strategy affects performance!
</details>

---

**Question 12:** For open addressing, how do you delete an item without breaking lookups?

<details>
<summary>Click after thinking deeply</summary>

**Problem:** Can't just set slot to None!

**Example:**
```
Insert "Alice" at index 5
Insert "Bob" at index 5 → collision → goes to index 6
Delete "Alice" → set index 5 to None
Search for "Bob":
  - Hash to index 5
  - See None
  - Conclude "Bob" not present ← WRONG!
```

**Solution:** Use a "tombstone" marker:
- Mark deleted slots as DELETED (not None)
- During search, skip DELETED slots
- During insert, can reuse DELETED slots

**Key Insight:** Delete is tricky with open addressing!
</details>

---

### Strategy 3: Double Hashing

**Question 13:** Instead of linear probing (+1, +2, +3...), use a second hash function:

```python
probe_sequence = (hash1(key) + i * hash2(key)) % size
```

Why does this reduce clustering?

<details>
<summary>Click after thinking</summary>

**Answer:** Different keys probe different sequences!

- "Alice" might probe: 5, 8, 11, 14...
- "Bob" might probe: 5, 12, 19, 26...

**Requirements for hash2:**
- Must never return 0 (else probe doesn't move!)
- Should be relatively prime to table size

**Common choice:** `hash2(key) = prime - (key % prime)`

**Key Insight:** Better distribution, but more computation!
</details>

---

### 💻 Implementation Challenge 2

Implement all three collision resolution strategies:
- Separate chaining (linked lists)
- Linear probing (open addressing)
- Double hashing

Compare their performance with different load factors!

---

## 📖 Part 3: Dynamic Resizing

### When to Resize

**Question 14:** Your hash table has 100 slots and 80 items (α = 0.8).

Should you resize? What's the trade-off?

<details>
<summary>Click after considering</summary>

**Arguments for resizing:**
- Performance degrading (longer chains/probes)
- α > 0.75 is generally considered high

**Arguments against:**
- Resizing is expensive (must rehash everything)
- Maybe more deletes coming?

**Common strategy:** Resize when α > 0.75

**Key Insight:** Amortized analysis shows resizing is still O(1) average!
</details>

---

**Question 15:** When resizing, should you double the size (100 → 200) or add a fixed amount (100 → 150)?

<details>
<summary>Click after thinking about growth patterns</summary>

**Answer:** Double it!

**Why?**
- Doubling: Resize operations decrease in frequency
  - Resize at sizes: 1, 2, 4, 8, 16, 32, 64, 128...
  - Total copies to reach n items: n + n/2 + n/4 + ... ≈ 2n
  - Amortized O(1) per insert!

- Adding fixed amount: Resize more frequently
  - Resize at sizes: 100, 150, 200, 250...
  - Total copies grows as O(n²)!

**Key Insight:** Doubling gives amortized constant time!
</details>

---

**Question 16:** When resizing from size 100 to size 200, can you just copy items to the same indices?

<details>
<summary>Click after thinking</summary>

**Answer:** NO! Must REHASH everything!

**Why?**
```python
old_index = hash(key) % 100
new_index = hash(key) % 200  # Different!
```

**Process:**
1. Create new larger array
2. For each item in old array:
   - Recalculate hash with new size
   - Insert into new array
3. Replace old array with new array

**Key Insight:** Resizing is O(n), but amortized cost is O(1)!
</details>

---

### 💻 Implementation Challenge 3

Implement:
- Dynamic resizing when load factor exceeds threshold
- Rehashing all items during resize
- Shrinking when load factor gets too low (< 0.25)

Measure the amortized cost of insertions!

---

## 📖 Part 4: Advanced Hash Table Features

### The Power of Hash Tables

**Question 17:** Hash tables enable many powerful data structures. How would you implement a Set using a hash table?

<details>
<summary>Click after designing</summary>

**Answer:** Hash table with keys only (no values)!

```python
class Set:
    def __init__(self):
        self.table = HashTable()

    def add(self, item):
        self.table.insert(item, None)

    def contains(self, item):
        return self.table.search(item) is not None
```

**Key operations:**
- add: O(1)
- contains: O(1)
- remove: O(1)

**Key Insight:** Sets are just hash tables with keys only!
</details>

---

**Question 18:** How would you implement a LRU (Least Recently Used) Cache with O(1) operations?

<details>
<summary>Click after thinking about data structures</summary>

**Answer:** Hash table + doubly linked list!

```
Hash table: Maps keys to linked list nodes
Linked list: Maintains order (most recent at front)
```

**Operations:**
- Get(key): O(1) hash lookup, move node to front
- Put(key, value): O(1) insert/update, move to front
- Evict LRU: O(1) remove from tail

**Key Insight:** Hash tables combine with other structures for powerful hybrids!
</details>

---

### Security Considerations

**Question 19:** If an attacker knows your hash function, they could craft keys that all hash to the same value, causing O(n) operations.

How can you defend against this?

<details>
<summary>Click after considering security</summary>

**Solutions:**

1. **Randomized hash functions:** Use a random seed
   ```python
   hash_value = (key * random_seed) % size
   ```

2. **Cryptographic hashes:** SHA-256, etc. (but slower!)

3. **Universal hashing:** Choose hash function randomly from a family

**Real-world example:** Python randomizes string hashing since 3.3!

**Key Insight:** Algorithm choice has security implications!
</details>

---

### 💻 Implementation Challenge 4

Implement:
- A Set class using your hash table
- A simple LRU cache
- Randomized hashing with a random seed

---

## 📖 Part 5: Hash Table Variations

### Perfect Hashing

**Question 20:** If you know ALL keys in advance, you can construct a perfect hash function (zero collisions).

How is this possible?

<details>
<summary>Click after thinking</summary>

**Answer:** Two-level hashing!

**Level 1:** Hash n items into n buckets (expect collisions)
**Level 2:** For each bucket with k items, create perfect hash table of size k²

**Math:** With k² slots for k items, probability of collision is < 1/2
- Try random hash functions until one works

**Trade-off:** Uses more space for guaranteed O(1) worst-case

**Key Insight:** With constraints, you can eliminate collisions entirely!
</details>

---

### Bloom Filters

**Question 21:** Sometimes you just need to answer "Is X in the set?" and you can tolerate false positives.

How could multiple hash functions help?

<details>
<summary>Click after designing</summary>

**Bloom Filter:**
- Bit array of size m
- k different hash functions
- Insert: Set k bits to 1
- Query: Check if all k bits are 1

**Properties:**
- Can have false positives (bits set by other items)
- NEVER false negatives (if item was added, bits are definitely set)
- Extremely space-efficient

**Use case:** Checking if passwords are in breach database!

**Key Insight:** Probabilistic data structures trade accuracy for efficiency!
</details>

---

### 💻 Implementation Challenge 5

Implement:
- A simple Bloom filter
- Test false positive rate vs. number of hash functions
- Compare space usage to regular hash table

---

## 🎓 Final Synthesis Challenge

### Build a Spell Checker

Create a spell checker that:
1. Loads a dictionary of 100,000+ words into a hash table
2. Checks if a word is spelled correctly in O(1) time
3. Suggests corrections using:
   - Edit distance 1 (insert, delete, replace, transpose)
   - Phonetic similarity
4. Analyzes performance with different hash table configurations

**Design Questions:**
- Which collision resolution strategy works best?
- What load factor gives best performance?
- How do you handle case-insensitivity?
- Can a Bloom filter help with the "definitely not a word" case?

---

## 🧪 Testing Your Understanding

Answer these to verify your grasp of first principles:

1. **Why O(1)?** Explain from first principles why hash tables achieve O(1) average case.

2. **Collision analysis:** With m slots and n items, what's the probability of zero collisions? (Hint: birthday paradox!)

3. **Load factor:** Why does performance degrade as load factor increases?

4. **Hash function quality:** How would you measure if a hash function distributes uniformly?

5. **Space-time trade-off:** Hash tables use more space than arrays. What do you get in return?

---

## 📚 Further Exploration

Once you've completed this project, you understand:
- How to achieve O(1) lookup through clever indexing
- The trade-offs in hash table design
- How hash functions work mathematically
- Why hash tables are ubiquitous in software

**Next steps:**
- How do we efficiently sort data? (Project 03: Sorting Algorithms)
- How do we turn text into executable code? (Project 04: Interpreters)
- How do computers communicate over networks? (Project 05: TCP/IP)

---

## 💡 How to Use This Guide with Claude Code CLI

```bash
# Interactive walkthrough
claude-code "Guide me through the Hash Table GUIDE.md, asking questions and checking my understanding"

# Compare implementations
claude-code "Help me analyze the performance differences between chaining and linear probing in my hash_table.py"

# Debug issues
claude-code "My hash table has too many collisions. Review my hash function against the GUIDE.md principles"
```

---

**Remember:** Hash tables are one of the most important data structures in all of computer science. Understanding them from first principles helps you use them effectively and debug when things go wrong!
