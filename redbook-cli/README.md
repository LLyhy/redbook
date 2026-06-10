# 红宝书 CLI (Redbook CLI)

> Command-line tool for algorithm analysis using contradiction methodology (矛盾分析法)

## Installation

```bash
pip install redbook-cli
```

Or from source:

```bash
git clone https://github.com/LLyhy/redbook.git
cd redbook/skills/redbook/redbook-cli
pip install -e .
```

## Prerequisites

- Python 3.8+
- A [DeepSeek API Key](https://platform.deepseek.com/api_keys) (free to apply)

## Quick Start

```bash
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
redbook analyze "Given an array of integers, find two numbers that sum to a target"
```

## Commands

### `redbook analyze <problem>`

Analyze an algorithm problem with the full contradiction analysis framework.

```bash
redbook analyze "Find the longest palindromic substring in a string"
```

Outputs: [Survey] → [Main Contradiction] → [Solution] → [Code] → [Verification]

### `redbook guide <problem>`

Use when you're stuck. The AI will ONLY survey the problem and guide you to find the contradiction yourself — no algorithm names, no code, no hints.

```bash
redbook guide "Merge k sorted linked lists"
```

### `redbook diagnose <code>`

Diagnose buggy code layer by layer: Logic → Boundary → Tool → Efficiency.

```bash
redbook diagnose "def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]"
```

### `redbook config`

Configure API key, model, and endpoint.

```bash
redbook config --api-key sk-xxxxxxxxxxxxxxxx
redbook config --model deepseek-chat
redbook config                                   # Show current config
```

### `redbook philosophy <concept>`

Explore a philosophical concept with the [Original] [Meaning] [Algorithm Insight] format.

```bash
redbook philosophy "On Contradiction"
redbook philosophy "Mass Line"
```

## Configuration

Configuration is stored in `~/.redbook/config.json`:

```json
{
  "api_key": "sk-xxxxxxxxxxxxxxxx",
  "model": "deepseek-chat",
  "api_url": "https://api.deepseek.com/chat/completions"
}
```

You can also set the API key via environment variable:

```bash
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

## Philosophy

The Redbook CLI treats algorithm problems as contradictions:

| Command | Contradiction Stage |
|---------|-------------------|
| `analyze` | Full analysis: identify contradiction → resolve it → verify |
| `guide` | Help you discover the contradiction yourself |
| `diagnose` | Find the contradiction in broken code, layer by layer |
| `philosophy` | Study the theory behind the methodology |

## License

MIT · [LLyhy/redbook](https://github.com/LLyhy/redbook)
