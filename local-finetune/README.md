# 红宝书 本地微调指南

## 你的硬件
- CPU: i7-12800HX (24核)
- RAM: 15.7 GB  
- GPU: 无独立显卡
- **结论：跑不了大模型微调，但有两个方案**

---

## 方案一：Google Colab（推荐 ⭐）

完全免费，T4 GPU (16GB 显存)，30 分钟出结果。

### 操作步骤（3 步）

**第 1 步：转化数据格式**
```bash
python local-finetune/convert_data.py
```
会在 `finetune/` 下生成 `training_data_qwen.jsonl`。

**第 2 步：上传到 Colab**
1. 打开 https://colab.research.google.com/
2. 文件 → 上传笔记本 → 选 `local-finetune/colab_redbook.ipynb`
3. 左边文件夹图标 → 上传 `finetune/training_data_qwen.jsonl`
4. 菜单栏 → 运行时 → 更改运行时类型 → T4 GPU

**第 3 步：运行**
- 按顺序点每个单元格的 ▶ 按钮
- 或者 运行时 → 全部运行
- 约 20 分钟后，下载 `redbook-merged/` 文件夹

### 模型选择
| 模型 | 大小 | 速度 | 效果 | 显存 |
|-----|------|------|------|------|
| Qwen2.5-1.5B | 1.5B | 快(15min) | 可用的红宝书风格 | 4GB |
| Qwen2.5-7B | 7B | 慢(40min) | 更智能 | 8GB |

在笔记本的 `[2/5]` 单元格改 `MODEL_NAME` 即可切换。

### 微调后使用
```python
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained('./redbook-lora')
FastLanguageModel.for_inference(model)

# 回答问题
messages = [{"role": "user", "content": "分析两数之和"}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
# ... 生成回复 ...
```

---

## 方案二：CPU 微调（慢但能跑）

使用 Qwen2.5-0.5B（最小模型），完全在本地 CPU 上微调。

### 安装
```bash
pip install unsloth transformers datasets accelerate
```

### 运行
```bash
python local-finetune/cpu_finetune.py
```

### 预计耗时
- Qwen2.5-0.5B：约 4-6 小时（1000 条数据）
- 优点：不依赖网络，不依赖 Google
- 缺点：模型很小，效果有限

---

## 常见问题

**Q: Colab 会断连吗？**
A: 免费版约 2-4 小时断一次。我们 20 分钟就能跑完，不会断。

**Q: 微调要钱吗？**
A: Colab + T4 GPU 完全免费。除非你买 Colab Pro（更快但没必要）。

**Q: 微调后的模型怎么用？**
A: 下载 `redbook-merged` 文件夹，用 unsloth 或 transformers 加载即可。可以在本地 CPU 上推理（1.5B 模型约 2GB 内存）。

**Q: 能不能微调成 API？**
A: 部署到 HuggingFace Spaces（免费）或 RunPod 即可变成 API。
