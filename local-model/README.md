# 红宝书本地模式

用你电脑运行一个真正的红宝书 AI。

---

## 方案 A：Python 服务器（推荐 ⭐ 无需下载任何模型）

**无需任何外部下载，1 秒启动。**

```bash
cd local-model
python server.py
```

打开 http://localhost:8787 直接对话。

原理：本地 Python 服务器自己就是红宝书——接收你的问题，注入红宝书人格，调用 DeepSeek API，返回结果。你的浏览器聊天页也可以连到它。

---

## 方案 B：Ollama（需要下载 ~2GB 模型）

真正的本地模型，断网也能用，但不依赖任何 API。

### 第一步：安装 Ollama
打开 https://ollama.com 下载安装。

### 第二步：运行安装脚本
```powershell
cd local-model
.\setup.ps1
```
会自动下载 qwen2.5:3b 模型并创建红宝书模型。

### 第三步：使用
```bash
ollama run redbook
```

---

## 聊天页接入

打开 https://llyhy.github.io/redbook/chat/ → 设置：
- 选择「本地红宝书 (Ollama)」→ 自动连 localhost:11434
- 或在「API 端点」填 `http://localhost:8787/v1/chat/completions` → 连 Python 服务器
