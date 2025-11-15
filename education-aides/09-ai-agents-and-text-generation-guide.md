# AI Agents & Text Generation - Education Aide
## Understanding Modern NLP, Transformers, BERT, and LLMs

### Overview
This guide covers the Learn AI Agents and Text Generation projects, helping you understand transformer architectures, BERT models, language models, and practical AI/ML implementation.

---

## Part 1: The AI/ML Landscape

### What Are We Learning?

**Learn AI Agents/** - BERT model implementation and understanding
**Text Generation/** - Text generation with language models

**The Big Picture:**
```
Traditional NLP (pre-2017)
    ↓
Transformers (2017)
    ↓
BERT, GPT (2018-2019)
    ↓
Large Language Models (2020+)
    ↓
AI Agents (2023+)
```

---

## Part 2: Understanding Transformers

### The Revolution

**Question:** What made transformers so revolutionary?

<details>
<summary>Before and After Transformers</summary>

**Before (RNNs/LSTMs):**
```
Input: "The cat sat on the mat"

Processing:
Step 1: Process "The" → hidden state
Step 2: Process "cat" using previous hidden state
Step 3: Process "sat" using previous hidden state
...
Problem: Sequential! Can't parallelize!
```

**With Transformers:**
```
Input: "The cat sat on the mat"

Processing:
All words processed in PARALLEL!
Attention mechanism learns relationships
```

**Key Innovation: Self-Attention**
```
Query: "cat"
Looks at all other words:
- "The" (determiner) - 0.9 attention
- "sat" (verb) - 0.7 attention
- "on" (preposition) - 0.3 attention
- "mat" (noun) - 0.5 attention

Learns: "cat" is subject of "sat"
```
</details>

### Self-Attention Mechanism

**Question:** How does attention actually work?

<details>
<summary>Attention Mathematics</summary>

**Three Matrices:**
- **Q** (Query): What am I looking for?
- **K** (Key): What do I contain?
- **V** (Value): What information do I have?

**Formula:**
```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

**Example:**
```python
import numpy as np

# Word embeddings (simplified)
words = ["cat", "sat", "mat"]
embeddings = np.array([
    [0.2, 0.5, 0.1],  # cat
    [0.4, 0.1, 0.8],  # sat
    [0.3, 0.6, 0.2]   # mat
])

# Compute attention for "cat"
Q = embeddings[0]  # Query: cat
K = embeddings     # Keys: all words
V = embeddings     # Values: all words

# Attention scores
scores = Q @ K.T / np.sqrt(3)
attention = softmax(scores)
# Result: [0.4, 0.35, 0.25]  # How much to attend to each word

# Weighted combination
output = attention @ V
```

**Multi-Head Attention:**
```
Instead of one attention mechanism,
use multiple "heads" in parallel:

Head 1: Learns grammatical relationships
Head 2: Learns semantic relationships
Head 3: Learns positional relationships

Combine all heads for rich representation
```
</details>

---

## Part 3: Understanding BERT

### What is BERT?

**BERT = Bidirectional Encoder Representations from Transformers**

**Question:** What makes BERT "bidirectional"?

<details>
<summary>BERT Architecture</summary>

**Older Models (GPT-1):**
```
"The cat sat on the ___"
→ Predict next word using only LEFT context
```

**BERT:**
```
"The cat ___ on the mat"
→ Predict masked word using BOTH left AND right context!
```

**Training Method: Masked Language Modeling (MLM)**
```
Original: "The cat sat on the mat"
Masked:   "The cat [MASK] on the mat"
Task:     Predict [MASK] = "sat"

Also predicts: Is sentence B a continuation of sentence A?
```

**BERT Architecture:**
```
Input: "Hello World"
    ↓
Token Embeddings + Position Embeddings + Segment Embeddings
    ↓
[Transformer Encoder Block]
├── Multi-Head Self-Attention
├── Add & Normalize
├── Feed-Forward Network
└── Add & Normalize
    ↓ (Repeat 12 or 24 times)
Output: Contextualized embeddings
```

**Use Cases:**
1. **Text Classification**
   ```
   Input: "This movie is amazing!"
   Output: Sentiment = Positive
   ```

2. **Named Entity Recognition (NER)**
   ```
   Input: "John works at Google in California"
   Output:
   - John: PERSON
   - Google: ORGANIZATION
   - California: LOCATION
   ```

3. **Question Answering**
   ```
   Context: "BERT was released in 2018 by Google"
   Question: "When was BERT released?"
   Answer: "2018"
   ```
</details>

### Using BERT in Python

**Basic Implementation:**
```python
from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Encode text
text = "Hello, how are you?"
inputs = tokenizer(text, return_tensors='pt')

# Get embeddings
with torch.no_grad():
    outputs = model(**inputs)

# Last hidden state: contextualized embeddings
embeddings = outputs.last_hidden_state
print(embeddings.shape)  # [1, sequence_length, 768]
```

**Fine-tuning for Classification:**
```python
from transformers import BertForSequenceClassification, Trainer, TrainingArguments

# Load model for classification (2 classes: positive/negative)
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2
)

# Prepare dataset
train_dataset = ...  # Your labeled data

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    learning_rate=2e-5,
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()
```

---

## Part 4: Text Generation

### Language Models

**Question:** How do language models generate text?

<details>
<summary>Autoregressive Generation</summary>

**Process:**
```
1. Start with prompt: "The cat"
2. Predict next word: "sat" (probability: 0.6)
3. Append: "The cat sat"
4. Predict next: "on" (probability: 0.5)
5. Append: "The cat sat on"
6. Continue until [EOS] token or max length
```

**Probability Distribution:**
```
P(next word | "The cat") =
- "sat": 0.6
- "ran": 0.2
- "jumped": 0.1
- "meowed": 0.05
- other: 0.05
```

**Sampling Strategies:**

**1. Greedy (always pick highest probability):**
```python
def greedy_decode(model, prompt):
    for _ in range(max_length):
        probs = model(prompt)
        next_token = argmax(probs)
        prompt = append(prompt, next_token)
    return prompt
```
Problem: Repetitive, boring text

**2. Top-K Sampling:**
```python
def top_k_sample(model, prompt, k=50):
    probs = model(prompt)
    top_k_probs = top_k(probs, k)
    next_token = sample(top_k_probs)  # Random from top K
    return next_token
```

**3. Nucleus (Top-P) Sampling:**
```python
def nucleus_sample(model, prompt, p=0.9):
    probs = model(prompt)
    sorted_probs = sort(probs)
    cumsum = cumulative_sum(sorted_probs)
    # Take smallest set of tokens with cumulative prob > p
    nucleus = sorted_probs[cumsum <= p]
    next_token = sample(nucleus)
    return next_token
```

**4. Temperature:**
```python
def apply_temperature(logits, temperature=1.0):
    # temperature > 1: More random
    # temperature < 1: More focused
    # temperature = 0: Greedy
    return logits / temperature
```
</details>

### GPT Architecture

**GPT = Generative Pre-trained Transformer**

**Differences from BERT:**

| Aspect | BERT | GPT |
|--------|------|-----|
| Direction | Bidirectional | Left-to-right only |
| Task | Fill in blanks | Generate next word |
| Use | Understanding | Generation |
| Training | Masked LM | Causal LM |

**GPT Training:**
```
Text: "The quick brown fox jumps"

Training examples:
"The" → predict "quick"
"The quick" → predict "brown"
"The quick brown" → predict "fox"
"The quick brown fox" → predict "jumps"
```

---

## Part 5: Practical Implementation

### Project Structure

**Learn AI Agents/Project 1 & 2:**
```
project/
├── cache.py          # Model caching
├── requirements.txt  # Dependencies
├── mise.toml        # Tool configuration
└── notebooks/       # Jupyter notebooks
```

### Setting Up Environment

**Installation:**
```bash
cd "Learn AI Agents/Project 1"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Key libraries:
# - transformers: Hugging Face models
# - torch: PyTorch deep learning
# - datasets: Dataset loading
# - tokenizers: Fast tokenization
```

### Caching Models

**Study cache.py:**
```python
from transformers import AutoModel, AutoTokenizer

def cache_model(model_name):
    """Download and cache model for offline use"""
    print(f"Caching {model_name}...")

    # Download tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Download model
    model = AutoModel.from_pretrained(model_name)

    print(f"Cached to: {model.config._name_or_path}")

# Usage
cache_model('bert-base-uncased')
cache_model('gpt2')
```

**Why cache?**
- Faster subsequent loads
- Offline availability
- Version control
- Reproducibility

---

## Part 6: Hands-On Exercises

### Exercise 1: Sentiment Analysis with BERT

**Task:** Build a movie review sentiment classifier

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load pre-trained model
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2  # positive, negative
)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Prepare data
reviews = [
    "This movie was amazing!",
    "Terrible waste of time.",
    "Pretty good, I enjoyed it."
]
labels = [1, 0, 1]  # 1=positive, 0=negative

# Tokenize
inputs = tokenizer(reviews, padding=True, truncation=True, return_tensors='pt')

# Forward pass
outputs = model(**inputs, labels=torch.tensor(labels))
loss = outputs.loss
predictions = torch.argmax(outputs.logits, dim=1)

print(f"Loss: {loss.item()}")
print(f"Predictions: {predictions}")
```

### Exercise 2: Named Entity Recognition

**Task:** Extract entities from text

```python
from transformers import pipeline

# Load NER pipeline
ner = pipeline("ner", model="dslim/bert-base-NER")

# Extract entities
text = "Elon Musk founded SpaceX in California in 2002."
entities = ner(text)

for entity in entities:
    print(f"{entity['word']}: {entity['entity']}")
# Output:
# Elon: B-PER
# Musk: I-PER
# SpaceX: B-ORG
# California: B-LOC
# 2002: B-DATE
```

### Exercise 3: Text Generation

**Task:** Generate creative stories

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Generate text
prompt = "Once upon a time, in a galaxy far away,"
inputs = tokenizer(prompt, return_tensors='pt')

# Generate with different strategies
outputs = model.generate(
    inputs['input_ids'],
    max_length=100,
    num_return_sequences=3,
    temperature=0.8,
    top_k=50,
    top_p=0.95,
    do_sample=True
)

# Decode
for i, output in enumerate(outputs):
    text = tokenizer.decode(output, skip_special_tokens=True)
    print(f"\nGeneration {i+1}:\n{text}\n")
```

### Exercise 4: Question Answering

**Task:** Build Q&A system

```python
from transformers import pipeline

qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

context = """
BERT was introduced in 2018 by researchers at Google.
It revolutionized NLP by using bidirectional training of transformers.
The model achieved state-of-the-art results on 11 NLP tasks.
"""

questions = [
    "When was BERT introduced?",
    "Who created BERT?",
    "How many tasks did BERT excel at?"
]

for question in questions:
    result = qa(question=question, context=context)
    print(f"Q: {question}")
    print(f"A: {result['answer']} (score: {result['score']:.2f})\n")
```

---

## Part 7: Advanced Concepts

### Transfer Learning

**Concept:** Use pre-trained models as starting point

**Why it works:**
```
Pre-training (on billions of words):
    Learn general language understanding
        ↓
Fine-tuning (on your specific task):
    Adapt to your domain/task
        ↓
Much better results with less data!
```

**Example:**
```
Pre-trained BERT (knows English)
    ↓ Fine-tune on medical texts
Medical BERT (knows medical terminology)
    ↓ Fine-tune on diagnosis task
Diagnosis Model (predicts diseases)
```

### Attention Visualization

**Understanding what model learns:**
```python
from transformers import BertTokenizer, BertModel
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased', output_attentions=True)

text = "The cat sat on the mat"
inputs = tokenizer(text, return_tensors='pt')

outputs = model(**inputs)
attentions = outputs.attentions  # Tuple of attention matrices

# Visualize attention for layer 0, head 0
attention = attentions[0][0, 0].detach().numpy()

import matplotlib.pyplot as plt
import seaborn as sns

tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
sns.heatmap(attention, xticklabels=tokens, yticklabels=tokens)
plt.title("Attention Heatmap")
plt.show()
```

### Prompt Engineering for LLMs

**Zero-Shot:**
```
Classify sentiment: "This is terrible!"
Sentiment: negative
```

**Few-Shot:**
```
Classify sentiment:

Example: "I love this!" → positive
Example: "Waste of money" → negative
Example: "Pretty good" → positive

Classify: "This is terrible!"
Sentiment: negative
```

**Chain-of-Thought:**
```
Question: "Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 balls. How many tennis balls does he have now?"

Let's think step by step:
1. Roger starts with 5 balls
2. He buys 2 cans
3. Each can has 3 balls, so 2 cans = 2 × 3 = 6 balls
4. Total = 5 + 6 = 11 balls

Answer: 11 tennis balls
```

---

## Part 8: First Principles Summary

### Core NLP Concepts

**1. Embeddings:**
- Words → Vectors
- Similar meaning → Similar vectors
- Capture semantic relationships

**2. Attention:**
- Selective focus
- Learn what's important
- Capture long-range dependencies

**3. Transformers:**
- Parallel processing
- Self-attention mechanism
- Scalable architecture

### Model Types

**1. Encoders (BERT):**
- Understand context
- Bidirectional
- Best for: classification, NER, Q&A

**2. Decoders (GPT):**
- Generate text
- Left-to-right
- Best for: text generation, completion

**3. Encoder-Decoders (T5, BART):**
- Combine both
- Best for: translation, summarization

### Training Paradigms

**1. Pre-training:**
- Large corpus
- Self-supervised
- Learn general patterns

**2. Fine-tuning:**
- Task-specific data
- Supervised
- Adapt to task

**3. Prompt-based:**
- No fine-tuning needed
- Few/zero-shot learning
- Instruction following

---

## How to Use This Guide with Claude Code CLI

```bash
claude code

# Ask questions like:
"Explain how BERT's attention mechanism works"
"Help me implement Exercise 1 on sentiment analysis"
"What's the difference between BERT and GPT?"
"Walk me through fine-tuning BERT for my dataset"
"Explain temperature in text generation"
"How do I visualize attention weights?"
"Guide me through building a question-answering system"
"What's the best sampling strategy for creative writing?"
```

**Interactive Learning:**
- Understand transformer architecture
- Implement practical NLP applications
- Debug model training issues
- Optimize for your use case
- Explore state-of-the-art techniques
