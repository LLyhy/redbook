import os
import re
import requests
import discord
from discord.ext import commands

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

REDBOOK_SYSTEM_PROMPT = (
    "你是红宝书，以毛主席《矛盾论》《实践论》为方法论分析算法问题。"
    "核心人格：任何算法问题本质是矛盾（已知vs所求），先找主要矛盾再选解法，"
    "语录必须对应具体算法，简洁务实不搞形式主义。"
    "解题格式：【调查】输入/输出/约束→【主要矛盾】一句话→【解法】逻辑推导→【代码】→【检验】边界/复杂度。"
    "用户说没思路：只做调查不给答案，禁止提任何算法名称。"
    "诊断代码：逻辑→边界→工具→效率，一次只诊断一层。"
    "语录映射：集中优势兵力→二分/双指针，星星之火→DP，敌进我退→回溯，群众路线→哈希表。"
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def should_respond(message_content):
    content = message_content.strip()
    if re.search(r"@红宝书", content):
        return True
    if content.startswith("红宝书"):
        return True
    return False


def is_guide_mode(message_content):
    content = message_content.strip()
    guide_keywords = ["没思路", "引导", "不会做", "做不来", "怎么想", "想不出来"]
    for kw in guide_keywords:
        if kw in content:
            return True
    return False


def clean_message(message_content):
    content = message_content.strip()
    content = re.sub(r"<@!?\d+>", "", content)
    content = re.sub(r"@红宝书", "", content)
    content = content.replace("红宝书", "", 1).strip()
    return content


def call_deepseek(user_message, guide_mode=False):
    if not DEEPSEEK_API_KEY:
        return (
            "❌ 未设置 DEEPSEEK_API_KEY 环境变量。\n"
            "请在运行 bot 前设置: `set DEEPSEEK_API_KEY=sk-...` (Windows) 或 `export DEEPSEEK_API_KEY=sk-...` (Linux/Mac)"
        )

    if guide_mode:
        full_user_message = (
            "我没思路，请只做调查，不要给答案，不要提任何算法名称，不要写代码。\n\n" + user_message
        )
    else:
        full_user_message = user_message

    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + DEEPSEEK_API_KEY,
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": REDBOOK_SYSTEM_PROMPT},
                    {"role": "user", "content": full_user_message},
                ],
                "temperature": 0.6,
                "max_tokens": 4096,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "⏰ API 请求超时，请稍后重试。"
    except requests.exceptions.RequestException as e:
        return "❌ API 请求失败: " + str(e)
    except (KeyError, IndexError, TypeError) as e:
        return "❌ API 响应格式异常: " + str(e)


def split_long_message(text, max_length=1900):
    if len(text) <= max_length:
        return [text]

    parts = []
    lines = text.split("\n")
    current = ""
    in_code_block = False

    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block

        if len(current) + len(line) + 1 > max_length:
            if in_code_block:
                current += "```"
                in_code_block = False
            parts.append(current)
            current = line
            if line.startswith("```"):
                in_code_block = True
        else:
            current += ("\n" if current else "") + line

    if current:
        parts.append(current)

    return parts


@bot.event
async def on_ready():
    print(f"📕 红宝书已上线: {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content
    if not should_respond(content):
        return

    guide_mode = is_guide_mode(content)
    user_message = clean_message(content)

    if not user_message:
        user_message = "请出一道算法题"

    async with message.channel.typing():
        reply = call_deepseek(user_message, guide_mode)
        for part in split_long_message(reply):
            await message.channel.send(part)


if __name__ == "__main__":
    if not DISCORD_BOT_TOKEN:
        print("❌ 错误: 未设置 DISCORD_BOT_TOKEN 环境变量")
        print(
            "请设置: set DISCORD_BOT_TOKEN=你的token (Windows) 或 export DISCORD_BOT_TOKEN=你的token (Linux/Mac)"
        )
        exit(1)
    if not DEEPSEEK_API_KEY:
        print("⚠️  警告: 未设置 DEEPSEEK_API_KEY 环境变量")
        print("bot 将启动，但调用 API 时会提示设置密钥")
    bot.run(DISCORD_BOT_TOKEN)
