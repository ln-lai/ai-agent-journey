"""
阶段 1 练习：Streaming Agent（流式输出）

学习目标：
  1. 理解 Runner.run 和 Runner.run_streamed 的区别
  2. 看到 Agent 的回答如何一小段一小段打印出来
  3. 知道 stream_events() 里最常用的文字事件是什么

跑法（在 openai-agents-python 目录下）：
  DEEPSEEK_API_KEY="你的key" uv run python 我的练习/01_single_agent/streaming_agent.py
"""

import asyncio
import os

from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent

from agents import (
    Agent,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)


# ===== 1. 配置 DeepSeek =====
# DeepSeek 兼容 OpenAI Chat Completions API，所以这里沿用前面练习的配置。
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
MODEL_NAME = "deepseek-chat"

client = AsyncOpenAI(
    base_url=DEEPSEEK_BASE_URL,
    api_key=DEEPSEEK_API_KEY,
)

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)


# ===== 2. 创建一个普通 Agent =====
agent = Agent(
    name="流式讲解助手",
    instructions=(
        "你是一个 Agent 学习教练。"
        "回答要用中文，语言简单直接。"
        "先给一句话结论，再用一个生活类比，最后给一个小例子。"
    ),
    model=MODEL_NAME,
)


# ===== 3. 普通输出：等完整答案生成后，一次性打印 =====
async def run_normal(question: str) -> None:
    print("\n" + "=" * 70)
    print("普通输出：等 Agent 全部答完，再一次性显示")
    print("=" * 70)

    result = await Runner.run(agent, question)
    print(result.final_output)


# ===== 4. 流式输出：边生成边打印 =====
async def run_streaming(question: str) -> None:
    print("\n" + "=" * 70)
    print("流式输出：Agent 每生成一点，就立刻显示一点")
    print("=" * 70)

    result = Runner.run_streamed(agent, input=question)

    async for event in result.stream_events():
        # raw_response_event 是模型最底层吐出来的事件。
        # ResponseTextDeltaEvent 表示“刚刚新增的一小段文字”。
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    print("\n" + "-" * 70)
    print(f"流式运行是否完成: {result.is_complete}")


async def main() -> None:
    if not DEEPSEEK_API_KEY:
        print("请先设置 DEEPSEEK_API_KEY 环境变量")
        return

    question = "请用大白话解释：Agent 和普通聊天机器人的区别是什么？"

    # 你可以先只跑 run_streaming，感受最明显。
    # await run_normal(question)
    await run_streaming(question)


if __name__ == "__main__":
    asyncio.run(main())
