"""
阶段 3 练习 1：路由模式（Routing / Handoff）

学习目标：
  1. 理解 handoff 和 tool 的区别
  2. 实现"分诊 → 转交专科"的多 Agent 协作
  3. 观察对话权如何从一个 Agent 转到另一个

场景：电商客服分诊
  - 分诊 Agent：判断用户问的是退款/技术/物流，转给对应专家
  - 退款专家：只懂退款流程
  - 技术专家：只懂产品技术问题
  - 物流专家：只懂物流查询

跑法（在 openai-agents-python 目录下）：
  DEEPSEEK_API_KEY="你的key" uv run python 我的练习/my_routing_agent.py
"""
import asyncio
import os

from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)

# ===== 配置 DeepSeek =====
client = AsyncOpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY", ""),
)
set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

MODEL = "deepseek-chat"


# ===== 1. 定义 3 个"专科"Agent =====

refund_agent = Agent(
    name="refund_agent",
    instructions=(
        "你是退款专员。只回答退款相关问题。"
        "退款流程：申请→审核 3 天→原路退回 5-7 个工作日。"
        "如果用户问其他问题，告诉他你只负责退款。"
    ),
    model=MODEL,
)

tech_agent = Agent(
    name="tech_agent",
    instructions=(
        "你是技术支持专员。只回答产品使用、bug、功能问题。"
        "回答时要专业、有耐心。"
        "如果用户问其他问题，告诉他你只负责技术问题。"
    ),
    model=MODEL,
)

logistics_agent = Agent(
    name="logistics_agent",
    instructions=(
        "你是物流专员。只回答快递、发货、配送相关问题。"
        "常见快递公司：顺丰、京东、圆通、中通。"
        "如果用户问其他问题，告诉他你只负责物流。"
    ),
    model=MODEL,
)


# ===== 2. 定义"分诊"Agent =====
# ⭐ 关键：handoffs 字段！告诉它"你可以转交给这些 Agent"

triage_agent = Agent(
    name="triage_agent",
    instructions=(
        "你是电商客服的分诊台，第一时间接收用户问题。"
        "你的任务：判断用户的问题属于哪类，然后【转交】给对应专员：\n"
        "  - 退款相关 → 转给 refund_agent\n"
        "  - 产品技术/bug/使用问题 → 转给 tech_agent\n"
        "  - 快递/物流/发货问题 → 转给 logistics_agent\n"
        "如果问题不清楚，礼貌地问用户更多细节。\n"
        "记住：你只负责分诊，不要自己回答专业问题。"
    ),
    model=MODEL,
    handoffs=[refund_agent, tech_agent, logistics_agent],  # ⭐ 可以转给这 3 个
)


# ===== 3. 测试 =====
async def test(question: str):
    print("\n" + "=" * 60)
    print(f"👤 用户: {question}")
    print("-" * 60)

    result = await Runner.run(triage_agent, question)

    # ⭐ result.last_agent 告诉我们：最后是哪个 Agent 在回答
    print(f"🎯 最终响应的 Agent: {result.last_agent.name}")
    print(f"🤖 回答: {result.final_output}")


async def main():
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("❌ 请先设置 DEEPSEEK_API_KEY")
        return

    # 测试 1：明显的退款问题
    await test("我上周买的鞋子不合脚，怎么退款？")

    # 测试 2：明显的技术问题
    await test("App 老是闪退，怎么办？")

    # 测试 3：明显的物流问题
    await test("我的快递三天了还没动，怎么回事？")

    # 测试 4：模糊问题（看分诊台怎么处理）
    await test("我的订单有点问题")


if __name__ == "__main__":
    asyncio.run(main())
