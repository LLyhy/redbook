# Redbook (红宝书) - English Edition

> Solve algorithm problems with contradiction analysis — inspired by Mao Zedong's *On Contradiction* and *On Practice*.

## What is Redbook?

Redbook is a system prompt that transforms any AI into a Mao-style algorithm tutor. Instead of just giving you the answer, it analyzes every problem through the lens of **contradiction analysis** (矛盾分析法):

- Every algorithm problem is a **contradiction** between what you know (input) and what you want (output).
- Find the **main contradiction** first — why brute force doesn't work.
- Choose your weapon based on the contradiction — hash map, DP, backtracking, etc.
- **Verify** through practice — edge cases and complexity.

## Quick Start

### Option 1: Copy the System Prompt (Recommended)

Copy the contents of [REDBOOK_EN.md](./REDBOOK_EN.md) and paste it into ChatGPT/Claude/DeepSeek's custom instructions. **30 seconds and you're done.**

### Option 2: Use the CLI Tool

```bash
pip install redbook-cli
redbook config --api-key YOUR_DEEPSEEK_API_KEY
redbook analyze "Two Sum"
```

### Option 3: Fine-tune Your Own Model

Download [training_data_en.jsonl](./training_data_en.jsonl) and upload it to DeepSeek/OpenAI fine-tuning platforms.

## Mao Quotes → Algorithm Mapping

| Quote | Algorithm |
|-------|-----------|
| "Concentrate forces to destroy the enemy one by one" | Binary Search, Two Pointers |
| "A single spark can start a prairie fire" | Dynamic Programming |
| "Advance when the enemy retreats, retreat when the enemy advances" | Backtracking |
| "The masses are the creators of history" | Hash Map |
| "No investigation, no right to speak" | Problem Analysis, Debugging |

## Response Format

### Problem Solving
```
[Survey] Input / Output / Constraints
[Main Contradiction] Why brute force fails
[Solution] Logic from contradiction to approach
[Code]
[Verification] Edge cases / Complexity
```

### When You're Stuck
The AI will ONLY output `[Survey]` and ask: *"What would brute force look like? Where's the bottleneck?"*
No algorithm names, no code, no hints.

### Code Diagnosis
Layered diagnosis: Logic → Boundary → Tool → Efficiency. One layer at a time.

## Training Data

`training_data_en.jsonl` contains 50 high-quality English entries covering:
- Two Sum, Three Sum, Valid Parentheses, Reverse Linked List, Max Subarray
- Climbing Stairs, Number of Islands, LRU Cache, Merge Intervals
- Course Schedule, Word Break, Longest Palindromic Substring, Coin Change
- Subsets, Permutations

Each entry includes [Survey], [Main Contradiction], [Solution], and [Verification] with English Mao quotes.

## Files

| File | Description |
|------|-------------|
| `REDBOOK_EN.md` | English system prompt (~300 tokens) |
| `training_data_en.jsonl` | 50 English training entries |
| `README.md` | This documentation |

**Open Source · [LLyhy/redbook](https://github.com/LLyhy/redbook)**
