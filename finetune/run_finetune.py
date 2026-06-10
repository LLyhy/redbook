import requests, json, time, os

API_KEY = "sk-2a912b23b3aa4db681b1a9dd8767ecf5"
BASE_URL = "https://api.deepseek.com"

def upload_file(path):
    print(f"[1/4] Uploading training data: {path}")
    with open(path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/files",
            headers={"Authorization": f"Bearer {API_KEY}"},
            files={"file": ("training_data.jsonl", f, "application/jsonl"),
                   "purpose": (None, "fine-tune")}
        )
    data = resp.json()
    print(f"  Response: {json.dumps(data, ensure_ascii=False)[:200]}")
    return data.get("id")

def create_job(file_id, model="deepseek-chat"):
    print(f"[2/4] Creating fine-tuning job...")
    resp = requests.post(
        f"{BASE_URL}/fine_tuning/jobs",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": model,
            "training_file": file_id,
            "hyperparameters": {"n_epochs": 3}
        }
    )
    data = resp.json()
    print(f"  Response: {json.dumps(data, ensure_ascii=False)[:300]}")
    return data.get("id")

def wait_for_job(job_id, poll_interval=30):
    print(f"[3/4] Waiting for job {job_id} to complete...")
    while True:
        resp = requests.get(
            f"{BASE_URL}/fine_tuning/jobs/{job_id}",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        data = resp.json()
        status = data.get("status", "unknown")
        print(f"  Status: {status} | {time.strftime('%H:%M:%S')}")

        if status in ("succeeded", "failed", "cancelled"):
            return data

        if status == "running":
            steps = data.get("trained_tokens", 0)
            print(f"  Trained tokens: {steps}")

        time.sleep(poll_interval)

def get_final_model(job_data):
    print(f"[4/4] Final result:")
    status = job_data.get("status")
    print(f"  Status: {status}")
    if status == "succeeded":
        model_id = job_data.get("fine_tuned_model")
        print(f"  Model ID: {model_id}")
        print(f"\n  Use with: model='{model_id}' in API calls")
        return model_id
    else:
        print(f"  Error: {job_data.get('error', 'unknown')}")
        return None

def main():
    data_path = os.path.join(os.path.dirname(__file__), "training_data.jsonl")
    print("=" * 60)
    print("红宝书 DeepSeek Fine-Tuning")
    print("=" * 60)

    file_id = upload_file(data_path)
    if not file_id:
        print("ERROR: Failed to upload file")
        return
    print(f"  File ID: {file_id}")

    job_id = create_job(file_id)
    if not job_id:
        print("ERROR: Failed to create job")
        return
    print(f"  Job ID: {job_id}")

    result = wait_for_job(job_id)
    model_id = get_final_model(result)

    if model_id:
        result_path = os.path.join(os.path.dirname(__file__), "FINE_TUNE_RESULT.txt")
        with open(result_path, "w") as f:
            f.write(f"model_id={model_id}\njob_id={job_id}\nstatus=succeeded\n")
        print(f"\n  Result saved to FINE_TUNE_RESULT.txt")

    return model_id

if __name__ == "__main__":
    main()
