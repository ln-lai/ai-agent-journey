from openai import OpenAI
from dotenv import load_dotenv
import os

# 从 .env 文件读取 API Key
load_dotenv()

# 创建客户端，指向 DeepSeek 的 API 地址
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 对话历史（Agent 的"记忆"）
messages = [
    {"role": "system", "content": "你是一个有帮助的 AI 助手。"}
]

print("Agent 启动！输入 'quit' 退出\n")

while True:
    user_input = input("你: ")

    if user_input.lower() == "quit":
        print("再见！")
        break

    # 把用户输入加入对话历史
    messages.append({"role": "user", "content": user_input})

    # 调用 LLM
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    # 取出回复
    reply = response.choices[0].message.content

    # 把 AI 回复也加入历史（这样 AI 记得上文）
    messages.append({"role": "assistant", "content": reply})

    print(f"\nAgent: {reply}\n")
