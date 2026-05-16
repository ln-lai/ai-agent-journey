import json
import os

MEMORY_FILE = "memory.json"

def _load() -> dict:
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data: dict):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def remember(key: str, value: str) -> str:
    data = _load()
    data[key] = value
    _save(data)
    return json.dumps({"status": "已记住", "key": key, "value": value}, ensure_ascii=False)


def recall(key: str) -> str:
    data = _load()
    if key in data:
        return json.dumps({"key": key, "value": data[key]}, ensure_ascii=False)
    return json.dumps({"key": key, "value": "没有找到这条记忆"}, ensure_ascii=False)


def recall_all() -> str:
    data = _load()
    if not data:
        return json.dumps({"memories": "暂无记忆"}, ensure_ascii=False)
    return json.dumps({"memories": data}, ensure_ascii=False)
