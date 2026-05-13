import json

# ── 真正执行的 Python 函数 ──────────────────────────────
def get_weather(city: str) -> str:
    # 这里是模拟数据，真实项目会调用天气 API
    fake_data = {
        "北京": "晴，25°C",
        "上海": "多云，22°C",
        "广州": "小雨，28°C",
    }
    result = fake_data.get(city, f"没有 {city} 的天气数据")
    return json.dumps({"city": city, "weather": result}, ensure_ascii=False)


def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return json.dumps({"expression": expression, "result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── 告诉 AI "有哪些工具可以用" 的描述 ─────────────────
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某个城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，例如：北京"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算一个数学表达式，例如 2+3*4",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"}
                },
                "required": ["expression"]
            }
        }
    }
]

# ── 工具名 → 函数 的映射表 ─────────────────────────────
TOOL_MAP = {
    "get_weather": get_weather,
    "calculate": calculate,
}
