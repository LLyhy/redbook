# 红宝书 · AI 算法助手

用毛主席矛盾分析法在 VS Code 里分析算法题。

---

## 安装

### 方式一：从本地安装

1. 打开 VS Code
2. 按 `Ctrl+Shift+P`，输入 `Extensions: Install from VSIX...`
3. 如果没有 `.vsix`，先安装 `vsce`：
   ```bash
   npm install -g @vscode/vsce
   cd d:\游戏\.trae\skills\redbook\vscode
   vsce package
   ```
4. 选择生成的 `.vsix` 文件安装

### 方式二：开发模式运行

```bash
cd d:\游戏\.trae\skills\redbook\vscode
code --extensionDevelopmentPath=.
```

---

## 配置

安装后，需要设置 DeepSeek API Key：

### 方式一：命令面板

1. `Ctrl+Shift+P` → 输入 `红宝书: 设置 API Key`
2. 在弹出的输入框中粘贴你的 DeepSeek API Key

### 方式二：设置文件

打开 VS Code 设置 (`Ctrl+,`)，搜索 `redbook`，填入以下配置：

| 配置项 | 说明 | 默认值 |
|-------|------|--------|
| `redbook.apiKey` | DeepSeek API Key | (空) |
| `redbook.apiEndpoint` | API 端点 | `https://api.deepseek.com/chat/completions` |
| `redbook.model` | 模型名称 | `deepseek-chat` |

> 获取 API Key：前往 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册并创建 API Key。

---

## 使用

### 命令列表

| 命令 | 快捷键（可自定义） | 说明 |
|-----|------------------|------|
| `红宝书: 分析此题` | 无（建议绑定） | 用矛盾分析法完整解题 |
| `红宝书: 引导思考` | 无（建议绑定） | 只做调查，不直接给答案 |
| `红宝书: 诊断代码` | 无（建议绑定） | 逐层诊断代码错误 |
| `红宝书: 设置 API Key` | 无 | 配置 API Key |

### 三种模式

#### 1. 解题模式 —— `红宝书: 分析此题`

选中题目文字（或打开题目文件），运行命令。红宝书会：

```
【调查】输入 输出 约束
【主要矛盾】为什么暴力不行
【解法】从矛盾到思路
【代码】
【实践检验】边界 复杂度
```

#### 2. 引导模式 —— `红宝书: 引导思考`

当你**没思路**时使用。红宝书**只做调查**，不直接给答案。它会问：

> "输入是一个数组，输出是两个下标。暴力枚举每对组合是 O(n²)，n 最大 10^5，你觉得暴力能过吗？"

#### 3. 诊断模式 —— `红宝书: 诊断代码`

选中你的错误代码，运行命令。红宝书按 4 层矛盾逐层诊断：

```
1. 逻辑矛盾 → 思路根本不对
      ↓ 如果逻辑正确
2. 边界矛盾 → 空数组、单元素、极值
      ↓ 如果边界正确
3. 工具矛盾 → 数据结构选错了
      ↓ 如果工具正确
4. 效率矛盾 → O(n²) 过不了大数据
```

**一次只诊断一层**，确认后再深入。

---

## 自定义快捷键

推荐绑定快捷键到 `keybindings.json`：

```json
[
  {
    "key": "ctrl+shift+alt+a",
    "command": "redbook.analyze",
    "when": "editorTextFocus"
  },
  {
    "key": "ctrl+shift+alt+g",
    "command": "redbook.guide",
    "when": "editorTextFocus"
  },
  {
    "key": "ctrl+shift+alt+d",
    "command": "redbook.explainCode",
    "when": "editorTextFocus"
  }
]
```

---

## 语录映射

| 语录 | 算法 | 矛盾 |
|-----|------|------|
| 集中优势兵力，各个击破 | 二分查找 / 双指针 | 每次消灭一半 |
| 星星之火，可以燎原 | 动态规划 | dp[0]蔓延到dp[n] |
| 敌进我退，敌退我进 | 回溯算法 | 前进和后退的对立统一 |
| 牵一发而动全身 | 链表操作 | 局部改变影响全局 |
| 群众路线 | 哈希表 | 发动每个元素帮你查找 |
| 没有调查就没有发言权 | 审题 | 先分析再动手 |
| 前途是光明的，道路是曲折的 | 栈和队列 | 处理顺序的对立 |
| 抓住主要矛盾 | 二叉树 | 抓住 root，递归自然成立 |

---

## 常见问题

**Q: 为什么返回"API Key 未设置"？**

A: 运行 `红宝书: 设置 API Key`，或在设置中填入 `redbook.apiKey`。

**Q: 可以用其他模型吗？**

A: 可以。修改 `redbook.apiEndpoint` 和 `redbook.model` 配置项，支持任何兼容 OpenAI Chat Completions 格式的 API。

**Q: 红宝书和普通 ChatGPT 有什么区别？**

A: 红宝书遵循严格的矛盾分析法协议——解题格式固定、没思路绝不直接给答案、诊断逐层递进、语录对应具体算法。它不是通用聊天，是专门的算法教练。

---

## 许可

MIT
