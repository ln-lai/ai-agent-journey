# 我的 Agent 学习区

这里放你自己的练习，不直接改官方 examples。

## 先看这 3 个文件

1. `学习路线.md`：总路线。
2. `学习执行框架.md`：每天怎么推进、怎么问 GPT、怎么验收。
3. 当前练习代码：
   - `my_hello_deepseek.py`
   - `my_tools_agent.py`
   - `my_routing_agent.py`

## 当前进度

你已经完成：

- 单 Agent 基础。
- 双人格 Agent。
- Streaming Agent：理解 `run_streamed`、`stream_events`、`event`、`item`、工具调用事件。
- SDK 工具调用。
- 多工具组合调用。
- handoff / routing 初版。
- 手写过一次底层 tools loop 和 memory。

下一步从这里开始：

1. `02_tools/tool_error_agent.py`
2. `02_tools/real_api_tool_agent.py`
3. `03_patterns/agents_as_tools_research_agent.py`
4. `03_patterns/judge_code_review_agent.py`

## 文件夹说明

```text
00_notes/        每阶段复盘
01_single_agent/ 单 Agent、动态 instructions、streaming
02_tools/        tools、错误处理、真实 API 或本地文件工具
03_patterns/     routing、agents-as-tools、judge、guardrails、parallelization
04_multi_agent/  handoff、memory、多 Agent 协作
05_project/      最终简历项目
```

## 每个练习必须交付

- 一个可运行 Python 文件。
- 三到五条测试输入。
- 一段复盘：我学到了什么、这个模式解决什么问题、哪里还不稳。
