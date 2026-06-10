import json, os

input_path = os.path.join(os.path.dirname(__file__), "..", "finetune", "training_data.jsonl")
output_path = os.path.join(os.path.dirname(__file__), "..", "finetune", "training_data_qwen.jsonl")

system_prompt = "你是红宝书，用矛盾分析法分析算法问题。解题格式：【调查】输入/输出/约束→【主要矛盾】一句话→【解法】→【代码】→【检验】。语录：集中优势兵力→二分/双指针 星星之火→DP 敌进我退→回溯 群众路线→哈希表"

count = 0
with open(input_path, "r", encoding="utf-8-sig") as fin, open(output_path, "w", encoding="utf-8") as fout:
    for line in fin:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            print(f"Skip bad line at entry {count}")
            continue
        msgs = data.get("messages", [])

        user_msg = ""
        assistant_msg = ""
        for m in msgs:
            if m["role"] == "user":
                user_msg = m["content"]
            elif m["role"] == "assistant":
                assistant_msg = m["content"]

        if not user_msg or not assistant_msg:
            continue

        # HuggingFace SFT format: system + user -> assistant
        # Qwen uses <|im_start|> tokens but we'll use standard format
        entry = {
            "instruction": user_msg,
            "input": "",
            "output": assistant_msg,
            "system": system_prompt,
            "history": []
        }

        fout.write(json.dumps(entry, ensure_ascii=False) + "\n")
        count += 1

print(f"Converted {count} entries")
print(f"Output: {output_path}")
