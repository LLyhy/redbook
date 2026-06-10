# 红宝书微调操作指南

## 平台地址
- DeepSeek: https://platform.deepseek.com/fine-tuning
- 硅基流动（备选）: https://siliconflow.cn/fine-tuning

## 操作步骤

### 1. 打开平台
访问 https://platform.deepseek.com/fine-tuning

### 2. 创建微调任务
点击「创建微调任务」
- 模型：deepseek-chat
- 训练数据：上传 `finetune/training_data.jsonl`（1000 条）
- 轮次：3 epochs
- 验证集：自动分割 10%

### 3. 等待完成（约 1-2 小时）
1000 条数据 × 3 epochs ≈ 1-2 小时

### 4. 获取模型 ID
微调完成后得到一个模型 ID，格式类似：
`ft-20241201-xxxxxxxx`

### 5. 调用微调模型
```python
import requests
resp = requests.post(
    "https://api.deepseek.com/chat/completions",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "ft-20241201-xxxxxxxx",  # 微调后的模型ID
        "messages": [{"role": "user", "content": "分析两数之和"}]
    }
)
```

### 6. 验证效果
微调后的模型应该天生就是红宝书人格，
即使不带系统提示词也会用矛盾分析法回答。

## 费用估算
- DeepSeek 微调：约 ¥5-10 / 1000 条
- 硅基流动：约 ¥2-5 / 1000 条

## 结果记录
微调完成后，将模型 ID 记录在此：

**模型 ID：** `（待填入）`
**平台：** `（待填入）`
**费用：** `（待填入）`
**效果：** `（待填入）`
