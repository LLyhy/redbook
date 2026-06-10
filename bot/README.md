# 红宝书 · Discord 机器人

用矛盾分析法分析算法问题的 Discord 机器人。

## 功能

- 监听 `@红宝书` 或 `红宝书` 开头的消息
- 调用 DeepSeek API，用矛盾论分析算法问题
- 两种模式：
  - **正常分析**：完整分析（调查→矛盾→解法→代码→检验）
  - **引导模式**：用户说"没思路"/"引导"时，只做调查不给答案

## 部署步骤

### 1. 创建 Discord 应用

1. 打开 [Discord Developer Portal](https://discord.com/developers/applications)
2. 点击右上角 **New Application**，输入名称"红宝书"
3. 左侧菜单点击 **Bot** → **Add Bot** → **Yes, do it!**
4. 在 **Privileged Gateway Intents** 中开启 **MESSAGE CONTENT INTENT**（必须）
5. 点击 **Reset Token** → **Copy**，保存这个 token

### 2. 邀请机器人到服务器

1. 左侧菜单点击 **OAuth2** → **URL Generator**
2. Scopes 勾选 **bot**
3. Bot Permissions 勾选：
   - Send Messages
   - Read Messages/View Channels
   - Read Message History
4. 复制生成的 URL，在浏览器中打开，选择要添加的服务器

### 3. 获取 DeepSeek API Key

1. 打开 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册/登录后，进入 **API Keys** 页面
3. 创建一个新 key 并复制

### 4. 运行机器人

**Windows (PowerShell):**
```powershell
$env:DISCORD_BOT_TOKEN = "你的DiscordBotToken"
$env:DEEPSEEK_API_KEY = "sk-你的DeepSeekKey"
pip install -r requirements.txt
python bot.py
```

**Linux / Mac:**
```bash
export DISCORD_BOT_TOKEN="你的DiscordBotToken"
export DEEPSEEK_API_KEY="sk-你的DeepSeekKey"
pip install -r requirements.txt
python bot.py
```

启动成功后，控制台显示 `📕 红宝书已上线: 红宝书#xxxx`。

### 5. 使用示例

在 Discord 频道中发送：

```
@红宝书 分析这道：给定一个整数数组，找出和为target的两个数的下标
```

```
红宝书 没思路
```

```
@红宝书 引导我一下，这道题：判断链表是否有环
```

## 注意事项

- `deepseek-chat` 模型每次调用约消耗 token，注意用量
- 引导模式下系统提示中已加入"不要给答案"，依赖模型遵守
- 长回复会自动分段发送（每段 < 1900 字符）

## 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `DISCORD_BOT_TOKEN` | ✅ | Discord 机器人 Token |
| `DEEPSEEK_API_KEY` | ✅ | DeepSeek API Key |
