"""
裸写版：不用任何 Agent 框架，手动实现"工具调用循环"
目的：让你看清楚 LLM 和工具之间到底在干嘛

整个流程 5 步：
  1. 告诉 LLM 有哪些工具
  2. 发用户问题
  3. LLM 回复"我要调某工具"
  4. 我们真的去执行那个工具
  5. 把工具结果塞回去，让 LLM 给最终回答
"""
import json
import os
from openai import OpenAI

# ===== 配置 DeepSeek（伪装成 OpenAI 客户端）=====
client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)
MODEL = "deepseek-chat"


# ===== 第 1 步：定义真实的工具函数 =====
def get_weather(city: str) -> str:
    """假装查天气（实际项目可以调真的天气 API）"""
    print(f"   🔧 [工具被调用] get_weather(city='{city}')")
    fake_data = {"东京": "晴天 20℃", "北京": "雾霾 15℃", "上海": "下雨 18℃"}
    return fake_data.get(city, f"{city} 的天气：晴天 22℃（默认）")


def calculator(expression: str) -> str:
    """计算数学表达式"""
    print(f"   🔧 [工具被调用] calculator(expression='{expression}')")
    try:
        result = eval(expression)  # 学习用，真实项目不要用 eval
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"


# ===== 第 2 步：写工具说明书（给 LLM 看的）=====
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某个城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，如 东京"}
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，如 3+5*2",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"}
                },
                "required": ["expression"],
            },
        },
    },
]

# 工具名 → 真实函数的映射表（dispatch table）
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "calculator": calculator,
}


# ===== 第 3 步：手写"工具调用循环" =====
def run_agent(user_question: str):
    print(f"\n👤 用户: {user_question}")

    # 对话历史
    messages = [
        {"role": "system", "content": "你是一个有用的助手，可以使用工具帮用户。"},
        {"role": "user", "content": user_question},
    ]

    # ⭐ 关键：循环！因为 LLM 可能连续调多个工具
    for turn in range(5):  # 最多循环 5 次防死循环
        print(f"\n--- 第 {turn + 1} 轮 ---")

        # 发请求给 LLM，带上工具说明书
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS_SCHEMA,
        )
        msg = response.choices[0].message
        messages.append(msg)  # 把 LLM 的回复加到历史

        # 如果 LLM 没要调工具，说明它要直接回答了
        if not msg.tool_calls:
            print(f"🤖 LLM 最终回答: {msg.content}")
            return msg.content

        # 否则，LLM 要调工具——我们去执行每个工具
        print(f"🤖 LLM 决定调用 {len(msg.tool_calls)} 个工具")
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            # 派发到真实函数
            func = TOOL_FUNCTIONS[func_name]
            result = func(**func_args)
            print(f"   ✅ 结果: {result}")

            # 把工具结果塞回对话历史
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    print("⚠️  达到最大循环次数")


if __name__ == "__main__":
    # 测试 1：单个工具
    run_agent("东京今天天气怎么样？")

    # 测试 2：需要算数
    # run_agent("帮我算一下 (15 + 27) * 3 等于多少")

    # 测试 3：需要先后调用多个工具（挑战！）
    # run_agent("北京天气怎么样？另外帮我算 100/4")
