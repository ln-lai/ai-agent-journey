import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import TOOLS, TOOL_MAP

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

messages = [
    {"role": "system", "content": "你是一个有帮助的 AI 助手，可以查天气和做计算。"}
]

print("Agent 启动！输入 'quit' 退出\n")

while True:
    user_input = input("你: ")
    if user_input.lower() == "quit":
        break

    messages.append({"role": "user", "content": user_input})

    # ── Agent 内部循环：思考 → 用工具 → 再思考 ──────────
    while True:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=TOOLS           # 把工具列表告诉 AI
        )

        msg = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        # 情况1：AI 决定调用工具
        if finish_reason == "tool_calls":
            messages.append(msg)  # 把 AI 的"我要用工具"记录进历史

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"\n[Agent 正在使用工具: {name}({args})]")

                # 执行真正的 Python 函数
                result = TOOL_MAP[name](**args)

                # 把工具结果加入历史
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # 工具执行完，继续循环让 AI 根据结果给出最终回答

        # 情况2：AI 直接回答（不需要工具，或工具用完了）
        else:
            reply = msg.content
            messages.append({"role": "assistant", "content": reply})
            print(f"\nAgent: {reply}\n")
            break  # 跳出内部循环，等待下一轮用户输入
