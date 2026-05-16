"""
我的第一个 Agent（DeepSeek 版）
学习目标：跑通 OpenAI Agents SDK，但用 DeepSeek 模型
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

# ===== 1. 配置 DeepSeek =====
# DeepSeek 的 API 完全兼容 OpenAI 格式，只需要换 base_url 和 api_key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
MODEL_NAME = "deepseek-chat"  # DeepSeek 的对话模型

if not DEEPSEEK_API_KEY:
    raise ValueError("请先设置环境变量 DEEPSEEK_API_KEY")

# 创建一个"伪装成 OpenAI 客户端"的 DeepSeek 客户端
client = AsyncOpenAI(
    base_url=DEEPSEEK_BASE_URL,
    api_key=DEEPSEEK_API_KEY,
)

# 告诉 SDK：默认就用这个客户端
set_default_openai_client(client=client, use_for_tracing=False)
# DeepSeek 走的是 chat_completions 接口（不是 OpenAI 的新版 responses 接口）
set_default_openai_api("chat_completions")
# 关掉 tracing（追踪上报需要 OpenAI 官方 key）
set_tracing_disabled(disabled=True)


# ===== 2. 写一个 Agent =====
async def main():
    agent = Agent(
        name="孙宇晨",
        instructions=" 你是孙宇晨，用孙哥的语气回答",
        model=MODEL_NAME,
    )

    result = await Runner.run(agent, "假如研究生offer拿到帝国理工交通数据科学；和康奈尔的系统工程；你会怎么选都是一年制；康奈尔到明年6月毕业，比较紧张；帝国理工是明年11月拿到毕业证相当于28届；你会怎么选，康奈尔伊萨卡天太偏僻了，不方便social你会怎么选？")
    print("=" * 40)
    print("Agent 的回答：")
    print(result.final_output)
    print("=" * 40)


if __name__ == "__main__":
    asyncio.run(main())
