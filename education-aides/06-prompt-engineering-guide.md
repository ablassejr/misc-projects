# Prompt Engineering - Education Aide
## Understanding How to Communicate Effectively with AI

### Overview
This repository contains comprehensive interactive tutorials on prompt engineering for Claude AI. This guide will help you navigate the materials and understand the first principles of effective AI communication.

---

## Part 1: What is Prompt Engineering?

### The Fundamental Concept

**Question:** Why does the way you ask a question to an AI matter?

**Your Thought:** _[Think about human communication]_

<details>
<summary>Understanding Prompts</summary>

**A prompt is:**
- Your instruction or question to an AI
- The entire input context the AI receives
- The "programming language" for AI

**Why it matters:**
```
Poor Prompt:
"Tell me about dogs"
→ Generic, unfocused response

Good Prompt:
"Explain the key differences between Golden Retrievers and Labrador Retrievers in terms of temperament, exercise needs, and grooming requirements. Format as a comparison table."
→ Specific, structured, actionable response
```

**Core Insight:** AI models are incredibly capable, but they need clear direction to produce the output you want.
</details>

---

## Part 2: Course Structure

### Learning Path

The repository contains two main tutorial paths:

**1. AmazonBedrock/** - Interactive Jupyter notebooks using AWS Bedrock API
**2. Anthropic 1P/** - Exercises using Anthropic's direct API

### The 9 Chapters

**Beginner (Chapters 1-3):**
1. Basic Prompt Structure
2. Being Clear and Direct
3. Assigning Roles

**Intermediate (Chapters 4-7):**
4. Separating Data from Instructions
5. Formatting Output & Speaking for Claude
6. Precognition (Thinking Step by Step)
7. Using Examples

**Advanced (Chapters 8-9):**
8. Avoiding Hallucinations
9. Complex Prompts (Real-world use cases)

**Appendix:**
- Prompt Chaining
- Tool Use
- Search & Retrieval

---

## Part 3: Core Principles

### Principle 1: Clear Structure

**Question:** What makes a prompt "well-structured"?

<details>
<summary>Prompt Anatomy</summary>

**Basic Structure:**
```xml
<role>
You are an expert Python developer.
</role>

<task>
Write a function to calculate fibonacci numbers.
</task>

<requirements>
- Use recursion
- Include docstring
- Handle edge cases (n<0, n=0, n=1)
- Include time complexity comment
</requirements>

<format>
Return only the code, no explanation.
</format>
```

**Why structure matters:**
- AI can clearly identify different components
- Reduces ambiguity
- Easier to iterate and improve
- More consistent results
</details>

### Principle 2: Specificity

**Question:** What's more specific and why?

**Option A:** "Write some code"
**Option B:** "Write a Python function named `calculate_average` that takes a list of numbers and returns their mean"

<details>
<summary>The Power of Specificity</summary>

**Option B is better because it specifies:**
- Language (Python)
- Structure (function)
- Name (`calculate_average`)
- Input (list of numbers)
- Output (mean/average)

**Specificity spectrum:**
```
Vague ← → Specific

"Code" < "Python code" < "Python function" < "Python function with typing" < "Python function with typing, docstrings, and unit tests"
```

**Rule:** Be as specific as your requirements demand, but no more.
</details>

### Principle 3: Examples (Few-Shot Learning)

**Question:** When should you provide examples?

<details>
<summary>Example-Based Learning</summary>

**Zero-Shot (no examples):**
```
Extract the name and email from this text:
"John Smith - john@email.com"
```

**Few-Shot (with examples):**
```
Extract the name and email from text.

Examples:
Input: "John Smith - john@email.com"
Output: {"name": "John Smith", "email": "john@email.com"}

Input: "Jane Doe <jane@example.org>"
Output: {"name": "Jane Doe", "email": "jane@example.org"}

Now extract from:
"Bob Jones (bob.jones@company.com)"
```

**When to use examples:**
- Complex or unusual formatting
- Domain-specific patterns
- Subtle distinctions
- Consistent style needed

**Format Patterns:**
```
INPUT: example input
OUTPUT: example output

INPUT: another input
OUTPUT: another output

INPUT: actual input to process
```
</details>

### Principle 4: Step-by-Step Thinking

**Question:** Why ask AI to "think step by step"?

<details>
<summary>Chain of Thought Reasoning</summary>

**Without thinking:**
```
Prompt: "Is 127 a prime number?"
Response: "Yes"
```
(Might be wrong! No reasoning shown)

**With thinking:**
```
Prompt: "Is 127 a prime number? Think step by step."

Response:
Let me check if 127 is prime:

1. A prime number is only divisible by 1 and itself
2. I need to check divisibility up to √127 ≈ 11.3
3. Checking:
   - 127 ÷ 2 = 63.5 (not divisible)
   - 127 ÷ 3 = 42.33... (not divisible)
   - 127 ÷ 5 = 25.4 (not divisible)
   - 127 ÷ 7 = 18.14... (not divisible)
   - 127 ÷ 11 = 11.54... (not divisible)
4. No divisors found

Yes, 127 is prime.
```

**Benefits:**
- More accurate results
- Explainable reasoning
- Catches errors
- Shows work like a tutor
</details>

---

## Part 4: Navigating the Tutorials

### How to Use the Jupyter Notebooks

**Setup (for AmazonBedrock/ version):**
```bash
cd "Prompt Engineering/AmazonBedrock"

# Install dependencies
pip install boto3 anthropic

# Configure AWS credentials
aws configure

# Launch Jupyter
jupyter notebook
```

**Recommended Order:**
1. Start with `01_Basic_Prompt_Structure.ipynb`
2. Complete exercises before moving to next chapter
3. Experiment in the playground areas
4. Check answer key when stuck
5. Try variations of prompts

### Interactive Learning Pattern

**For each chapter:**

1. **Read** the concept explanation
2. **Predict** what prompt will work
3. **Test** your prompt in the playground
4. **Compare** with provided examples
5. **Iterate** to improve
6. **Complete** exercises
7. **Reflect** on what you learned

---

## Part 5: Key Techniques from Each Chapter

### Chapter 1: Basic Prompt Structure

**Core Lesson:** Clear task definition

**Pattern:**
```
[Context] I have a dataset of customer reviews

[Task] Classify each review as positive, negative, or neutral

[Output Format] Return as JSON array
```

### Chapter 2: Being Clear and Direct

**Core Lesson:** Avoid ambiguity

**Poor:**
```
Tell me about the file
```

**Better:**
```
Analyze this Python file and list:
1. All function names
2. Number of lines of code
3. External dependencies
4. Potential security issues
```

### Chapter 3: Assigning Roles

**Core Lesson:** Set expertise context

**Pattern:**
```
You are a senior security engineer with 10 years of experience in penetration testing.

Review this authentication code and identify vulnerabilities.
```

**Why roles work:**
- Activates relevant training data
- Sets appropriate tone/depth
- Guides response style

### Chapter 4: Separating Data from Instructions

**Core Lesson:** Use delimiters

**Pattern:**
```
Summarize the following article in 3 bullet points:

<article>
[Long article text here...]
</article>

Focus on the main scientific findings.
```

**Benefits:**
- Clear boundaries
- Prevents injection attacks
- Easier to parse
- More reliable

### Chapter 5: Formatting Output

**Core Lesson:** Specify exact format

**Example:**
```
Generate a user profile in JSON format with these exact fields:
{
  "name": string,
  "age": number,
  "email": string,
  "interests": array of strings,
  "premium": boolean
}
```

### Chapter 6: Thinking Step by Step (Precognition)

**Core Lesson:** Request intermediate reasoning

**Pattern:**
```
Solve this problem step by step:

<problem>
A train leaves Station A at 60 mph...
</problem>

Show all work before giving the final answer.
```

### Chapter 7: Using Examples

**Core Lesson:** Show, don't just tell

**Pattern:**
```
Convert casual text to formal:

Example 1:
Input: "hey, can u send me the report?"
Output: "Hello, could you please send me the report?"

Example 2:
Input: "thx for the help!"
Output: "Thank you for your assistance."

Convert:
Input: "gonna be late, sorry!"
```

### Chapter 8: Avoiding Hallucinations

**Core Lesson:** Request citations and admit uncertainty

**Pattern:**
```
Answer the following question about historical events.

Rules:
- Only use information you're certain about
- If unsure, say "I don't have confident information about this"
- Don't make up dates, names, or details
- Cite your reasoning

Question: [...]
```

### Chapter 9: Complex Prompts

**Core Lesson:** Combine all techniques

**Real-world example:**
```xml
<role>
You are a financial analyst with expertise in risk assessment.
</role>

<task>
Analyze the following company data and provide investment recommendation.
</task>

<data>
<financial_metrics>
Revenue: $50M
Profit Margin: 15%
Debt-to-Equity: 0.8
</financial_metrics>

<market_context>
Industry growth: 12% YoY
Competitive position: #3 in market
</market_context>
</data>

<requirements>
1. Assess financial health
2. Evaluate market position
3. Identify risks
4. Provide clear recommendation (Buy/Hold/Sell)
</requirements>

<format>
Structure as:
## Financial Health
[Analysis]

## Market Position
[Analysis]

## Risk Factors
- [List]

## Recommendation
[Buy/Hold/Sell with reasoning]
</format>

<constraints>
- Be conservative in assessment
- Highlight any data gaps
- No speculation beyond provided data
</constraints>
```

---

## Part 6: Hands-On Exercises

### Exercise 1: Improve This Prompt

**Poor Prompt:**
```
Write code for sorting
```

**Your Improved Version:** _[Rewrite to be specific]_

<details>
<summary>Improved Version</summary>

```
Write a Python function that implements the quicksort algorithm.

Requirements:
- Function name: quicksort
- Input: List of integers
- Output: Sorted list (ascending order)
- Include docstring with time complexity
- Include 3 test cases
- Handle edge case of empty list

Example usage:
quicksort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
→ [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
```
</details>

### Exercise 2: Add Examples

**Task:** Improve this prompt with examples

```
Extract product names and prices from e-commerce descriptions.
```

**Your Version:** _[Add 2-3 examples]_

### Exercise 3: Role Assignment

**Task:** Choose the best role for this task

```
Task: Debug complex async JavaScript promises
```

**What role should you assign?**

### Exercise 4: Error Analysis

**Find issues in this prompt:**
```
You're the best coder ever! Write me perfect code that solves everything and never has bugs! Make it fast and good!
```

**What's wrong?** _[List all issues]_

---

## Part 7: Common Pitfalls

### Pitfall 1: Over-Politeness

**Ineffective:**
```
If you wouldn't mind, and if it's not too much trouble, could you perhaps maybe help me with...
```

**Effective:**
```
Analyze this code and identify bugs:
[code]
```

### Pitfall 2: Hidden Assumptions

**Unclear:**
```
Convert the date
```
(Which date? From what format? To what format?)

**Clear:**
```
Convert this date from MM/DD/YYYY to ISO 8601 format:
"12/25/2023" → "2023-12-25"
```

### Pitfall 3: Vague Constraints

**Vague:**
```
Make it short
```

**Specific:**
```
Summarize in exactly 50 words or less
```

### Pitfall 4: Multiple Tasks in One

**Confusing:**
```
Analyze this code and also explain sorting algorithms and write me a better version and document it.
```

**Better - Separate:**
```
Step 1: Analyze this code and identify issues
Step 2: Suggest improvements
Step 3: Implement improved version
Step 4: Add documentation
```

---

## Part 8: Advanced Techniques

### Technique 1: Prompt Chaining

**Pattern:** Break complex tasks into sequential prompts

```
Prompt 1: "Analyze these customer reviews and extract main themes"
→ Get themes

Prompt 2: "For each theme [from above], count how many reviews mentioned it"
→ Get counts

Prompt 3: "Create a prioritized action plan based on the most common themes"
→ Get action plan
```

### Technique 2: Self-Consistency

**Pattern:** Ask for multiple approaches

```
Solve this problem in three different ways, then compare the results:
[problem]
```

### Technique 3: Constitutional AI

**Pattern:** Add principles

```
Answer this question while adhering to these principles:
1. Be accurate (say "I don't know" if unsure)
2. Be helpful (provide context and examples)
3. Be harmless (don't suggest dangerous actions)

Question: [...]
```

---

## Part 9: Testing and Iteration

### Evaluation Framework

**Test your prompts against:**

1. **Accuracy** - Correct information?
2. **Completeness** - All requirements met?
3. **Consistency** - Same input → same output?
4. **Format** - Matches specified format?
5. **Tone** - Appropriate style?

### Iteration Process

```
1. Write initial prompt
2. Test with sample input
3. Identify issues in output
4. Refine prompt
5. Test again
6. Repeat until satisfied
```

**Tracking Changes:**
```
Version 1: "Summarize the article"
→ Too vague, got rambling summary

Version 2: "Summarize the article in 3 bullet points"
→ Better structure, but missed key points

Version 3: "Summarize the article in 3 bullet points focusing on: main argument, supporting evidence, conclusion"
→ Perfect!
```

---

## Part 10: Real-World Applications

### Use Case 1: Code Review

```
<role>Senior Python developer reviewing pull request</role>

<task>Review this code for:
- Security vulnerabilities
- Performance issues
- Code style (PEP 8)
- Logic errors
- Missing edge cases
</task>

<code>
[paste code here]
</code>

<format>
For each issue found:
- Line number
- Issue type
- Description
- Suggested fix
</format>
```

### Use Case 2: Data Analysis

```
You are a data analyst. Analyze this sales data and provide insights.

<data>
[CSV or JSON data]
</data>

Provide:
1. Summary statistics
2. Trends identified
3. Anomalies or outliers
4. Actionable recommendations

Format findings as a business report.
```

### Use Case 3: Content Generation

```
Create a technical blog post about [topic].

Target audience: Intermediate developers
Length: 800-1000 words
Tone: Professional but conversational
Structure:
- Introduction with hook
- 3-4 main sections with code examples
- Conclusion with key takeaways

Include:
- Practical examples
- Common pitfalls
- Best practices
```

---

## How to Use This Guide with Claude Code CLI

```bash
claude code

# Ask questions like:
"Walk me through Chapter 3 on role assignment"
"Help me improve this prompt: [your prompt]"
"Explain when to use few-shot vs zero-shot prompting"
"What's wrong with this prompt and how can I fix it?"
"Show me examples of effective prompt chaining"
"Help me create a prompt for [your specific task]"
```

**Interactive Learning:**
- Share your prompts for feedback
- Ask for explanations of techniques
- Request examples for specific use cases
- Get help debugging ineffective prompts
- Explore advanced patterns
