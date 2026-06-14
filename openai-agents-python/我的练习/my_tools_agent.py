"""
阶段 2 练习：工具与多轮
学习目标：
  1. 用 @function_tool 装饰器把普通函数变成 Agent 的工具
  2. 观察 Agent 如何"决定"调用哪个工具
  3. 看 Agent 在多轮调用中怎么串联多个工具

跑法（在 openai-agents-python 目录下）：
  DEEPSEEK_API_KEY="你的新key" uv run python 我的练习/my_tools_agent.py
"""
import asyncio
import os
from datetime import datetime

from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)

# ===== 1. 配置 DeepSeek（跟 hello world 一样）=====
client = AsyncOpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY", ""),
)
set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)


# ===== 2. 定义 3 个工具 =====
# ⭐ 关键：@function_tool 这一行让 SDK 自动把这个函数变成"Agent 能调的工具"
# ⭐ docstring（三引号注释）和参数类型 = LLM 看到的"工具说明书"，写得越清楚 Agent 用得越准

@function_tool
def get_weather(city: str) -> str:
    """查询某个城市的当前天气。

    Args:
        city: 城市名，如 "东京"、"北京"
    """
    print(f"   🔧 [工具被调用] get_weather(city='{city}')")
    # 假数据（真实项目可以调用真的天气 API）
    fake_data = {
        "东京": "晴天，气温 20℃，微风",
        "北京": "雾霾，气温 15℃，无风",
        "上海": "下雨，气温 18℃，东风",
        "纽约": "多云，气温 12℃",
    }
    return fake_data.get(city, f"{city} 今天晴天，气温 22℃（默认）")


@function_tool
def calculator(expression: str) -> str:
    """计算数学表达式。

    Args:
        expression: 数学表达式，如 "3 + 5 * 2" 或 "(15 + 27) / 3"
    """
    print(f"   🔧 [工具被调用] calculator(expression='{expression}')")
    try:
        # 注意：eval 在生产环境危险，这里只是学习用
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算失败: {e}"


@function_tool
def get_current_time() -> str:
    """获取当前的日期和时间。"""
    print(f"   🔧 [工具被调用] get_current_time()")
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# ===== 3. 创建 Agent，把工具列表塞给它 =====
agent = Agent(
    name="全能助手",
    instructions=(
        "你是一个有用的助手。"
        "用户问到天气、数学、时间的时候，要使用对应的工具来获取真实信息，"
        "不要自己编造。回答用中文。"
    ),
    model="deepseek-chat",
    tools=[get_weather, calculator, get_current_time],  # ⭐ 三个工具都给它
)


# ===== 4. 跑几个测试 =====
async def test(question: str):
    """跑一次 Agent 并打印结果"""
    print("\n" + "=" * 60)
    print(f"👤 用户: {question}")
    print("-" * 60)
    result = await Runner.run(agent, question)
    print(f"\n🤖 最终回答: {result.final_output}")


async def main():
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("❌ 请先设置 DEEPSEEK_API_KEY 环境变量")
        return

    # 测试 1：单工具——只需要查天气
    await test("北京今天天气怎么样？")

    # 测试 2：单工具——只需要算数
    await test("帮我算一下 (15 + 27) * 3 等于多少")

    # 测试 3：⭐ 多工具——需要 Agent 自己决定调多个
    await test("北京今天天气怎么样？另外帮我算 100 除以 4，再告诉我现在几点了")


if __name__ == "__main__":
    asyncio.run(main())
