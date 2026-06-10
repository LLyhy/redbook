# 红宝书 (RedBook)

> 用毛主席《矛盾论》《实践论》分析算法问题

**[🔗 在线体验](https://llyhy.github.io/redbook/chat/)** ｜ [📋 复制系统提示词](https://github.com/LLyhy/redbook/blob/main/finetune/REDBOOK_SHORT.md) ｜ [📊 下载训练数据](https://github.com/LLyhy/redbook/blob/main/finetune/training_data.jsonl)

---

## ⚡ 30 秒看懂红宝书

**它是什么：** 一套让任何 AI 用矛盾分析法回答算法问题的工具链。

**怎么用：** 复制 300 字符提示词 → 粘贴到 ChatGPT/DeepSeek → AI 变成红宝书人格。

**核心思想：** 任何算法题本质是一个矛盾（已知条件 vs 所求结果）。先找主要矛盾，再选解法。

**效果：**

```
👤 用户：分析一下两数之和

🧠 红宝书：
  【调查】输入整数数组 nums，目标 target。输出两个下标。
  【主要矛盾】暴力 O(n²)，查找补数太慢。
  【解法】哈希表——群众路线。遍历时查 target-num 见过没。O(n)。
  【检验】O(n)/O(n)，通过。
```

---

## 📦 项目包含

| 模块 | 说明 |
|-----|------|
| 🧠 系统提示词 | 300 token 短版 + 400 token 标准版，实测 DeepSeek 100% 命中率 |
| 📊 训练数据 | 500 条 JSONL，覆盖 LeetCode Top 200+ 经典题的红宝书风格解析 |
| 💬 在线聊天 | 单页 HTML，填入 API Key 即用 → **[点我体验](https://llyhy.github.io/redbook/chat/)** |
| 📖 电子书 | 矛盾论基础 → 数据结构篇 → 算法篇 → 学习路径 |
| 🔌 浏览器插件 | LeetCode 侧栏自动分析，分析/引导双模式 |
| 🤖 Discord Bot | 部署到群，@红宝书 即问即答 |

---

## 🗣 语录 → 算法对照

| 语录 | 算法 | 用法 |
|-----|------|------|
| "集中优势兵力，各个击破" | 二分查找、双指针 | 每次消灭一半，两端夹击 |
| "星星之火，可以燎原" | 动态规划 | dp[0] 是火，推到 dp[n] 是燎原 |
| "敌进我退，敌退我进" | 回溯算法 | 做选择（进），撤销（退） |
| "人民群众是历史的创造者" | 哈希表 | 发动元素 O(1) 查找 |
| "牵一发而动全身" | 链表操作 | 改一个指针影响全局 |
| "没有调查就没有发言权" | 审题、调试 | 先搞清输入输出再动手 |

---

## 🚀 快速开始

**方式一：复制提示词（推荐）**

打开 [REDBOOK_SHORT.md](https://github.com/LLyhy/redbook/blob/main/finetune/REDBOOK_SHORT.md)，复制全部内容，粘贴到 ChatGPT/DeepSeek/Kimi 的自定义指令中。**30 秒搞定。**

**方式二：在线聊天**

访问 **[https://llyhy.github.io/redbook/chat/](https://llyhy.github.io/redbook/chat/)**，填入你的 DeepSeek API Key（[免费申请](https://platform.deepseek.com/api_keys)），直接对话。

**方式三：微调专属模型**

下载 [training_data.jsonl](https://github.com/LLyhy/redbook/blob/main/finetune/training_data.jsonl)，上传到 DeepSeek/OpenAI 微调平台，获得天生就是红宝书人格的模型。

---

## 📊 实测数据

三版系统提示词在 DeepSeek API 上的四轮测试（解题/没思路/诊断/哲学）：

| 版本 | 命中率 | Token |
|-----|--------|-------|
| v3 短版 | 100% | ~308 |
| v3 标准版 | 100% | ~395 |
| v2 旧版 | 100% | ~1577 |

v3 用 1/5 的 token 达到同样效果，省下的就是 API 费用。

---

## 📁 仓库结构

```
├── index.html                ← 在线体验入口
├── chat/
│   └── index.html            ← 聊天页面
├── ebook/
│   └── README.md             ← 电子书
├── extension/                ← 浏览器插件
├── bot/                      ← Discord Bot
├── finetune/
│   ├── training_data.jsonl    ← 500 条训练数据
│   ├── REDBOOK_SHORT.md       ← 300-token 短版提示词
│   └── REDBOOK_SYSTEM_PROMPT.md ← 完整版提示词
├── SKILL.md                  ← Trae IDE Skill 定义
└── PROMO_ARTICLE.md          ← 推广文章
```

---

**开源 · [LLyhy/redbook](https://github.com/LLyhy/redbook)**
