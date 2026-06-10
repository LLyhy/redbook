# 红宝书模型微调指南

## 你的数据

- 文件：`finetune/training_data.jsonl`
- 格式：100 条红宝书风格 Q&A
- 覆盖：算法解题（50条）+ 知识点（25条）+ 原著解读（25条）

## DeepSeek 微调步骤

### 1. 登录 DeepSeek 平台
打开 https://platform.deepseek.com → 注册/登录

### 2. 充值
右上角「充值」，10 块钱够用

### 3. 创建数据集
左侧菜单 → 「数据集」 → 「上传数据集」
- 选择文件：`finetune/training_data.jsonl`
- 格式选：**对话格式 (messages)**

### 4. 创建微调任务
左侧菜单 → 「微调」 → 「创建微调任务」
- 基础模型：选 deepseek-chat（最新版）
- 数据集：选刚上传的 training_data
- 学习率：默认 1e-5 即可
- Epochs：3-5（100条数据建议 5 epoch）
- 点击「开始训练」

### 5. 等待训练
通常 10-30 分钟完成

### 6. 使用你的模型
训练完成后获得模型 ID，通过 API 调用：
```python
from openai import OpenAI

client = OpenAI(
    api_key="你的deepseek-api-key",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="你的微调模型ID",
    messages=[{"role": "user", "content": "分析一下两数之和"}]
)
print(response.choices[0].message.content)
```

结果就是红宝书风格的回答，不需要额外的系统提示词。

## 其他模型微调

同样的 JSONL 文件可用于：

| 平台 | 微调文档 |
|-----|---------|
| OpenAI | https://platform.openai.com/docs/guides/fine-tuning |
| DeepSeek | https://platform.deepseek.com |
| 硅基流动 | https://siliconflow.cn (支持 Qwen/DeepSeek 等开源模型微调) |
| 阿里百炼 | https://bailian.console.aliyun.com |

格式都一样，上传同样的 `training_data.jsonl` 即可。

## 费用估算

- DeepSeek 微调 100 条数据：约 0.5-2 元
- 推理费用：约 1 元/百万 tokens
- 你充的 10 块钱完成微调后还能用很久

## 问题排查

| 问题 | 解决 |
|-----|------|
| 上传失败 | 检查 JSON 格式是否每行完整 |
| 训练失败 | 减少 epoch 或检查数据格式 |
| 结果不好 | 增加 epoch 到 5-8，或增加数据量到 200 条 |
| 风格不够强 | epoch 设高一点（8-10）让模型更牢固地学习红宝书人格 |
