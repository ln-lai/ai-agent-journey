# OpenAI Agents SDK 学习笔记：Streaming Agent、Event、Item、Tool Call

日期：2026-06-15

## 1. 这段代码在学什么？

这段代码主要在学习：

> 使用 `Runner.run_streamed()` 流式运行 Agent，并通过 `result.stream_events()` 观察 Agent 运行过程中发生的事件。

它不是单纯看“模型一字一句输出了什么”，而是看 Agent 的完整执行过程，比如：

```text
Agent updated: Joker
-- Tool was called: how_many_jokes
-- Tool output: 3
-- Message output:
 1. ...
 2. ...
 3. ...
```

也就是说，这段代码重点看的是：

```text
哪个 Agent 在运行
调用了哪个工具
工具返回了什么
最后 Agent 输出了什么消息
```

## 2. Runner.run 和 Runner.run_streamed 的区别

### 2.1 Runner.run

```python
result = await Runner.run(agent, input="Hello")
print(result.final_output)
```

意思是：

```text
等 Agent 全部运行完
拿到最终答案
一次性打印最终结果
```

像是：

```text
等饭全部做好，再一次性端上来
```

### 2.2 Runner.run_streamed

```python
result = Runner.run_streamed(agent, input="Hello")

async for event in result.stream_events():
    ...
```

意思是：

```text
Agent 一边运行
一边产生事件
我们可以边运行边观察过程
```

像是：

```text
厨房做菜时，你可以不断看到：
厨师开始做了
用了什么工具
菜做好一部分了
最终菜上桌了
```

注意：

> `run_streamed` 不代表你一定会看到文字一个字一个字输出。
> 你能看到什么，取决于你处理了哪些 event。

## 3. stream_events 是什么？

```python
async for event in result.stream_events():
```

这句的意思是：

> 不断监听 Agent 运行过程中产生的事件。

这里的 `event` 可以理解为：

```text
Agent 运行过程中发生的一件事
```

比如：

```text
Agent 更新了
模型开始生成文字
工具被调用了
工具返回了结果
最终消息生成好了
```

所以：

```text
event = 发生了什么事
```

## 4. event 和 item 的区别

这是最容易混的地方。

简单记：

```text
event = 发生了一件事
item = 这件事里面产生的具体东西
```

用外卖举例：

```text
event：骑手已取餐
item：具体这份外卖订单

event：订单已送达
item：送达的那份餐
```

放到 Agent 里：

```text
event：发生了一次工具调用事件
item：具体调用的是 how_many_jokes 这个工具

event：发生了一次工具输出事件
item：工具返回的结果，比如 3

event：发生了一次消息输出事件
item：最终生成的那条消息
```

所以：

```text
event 是“通知”
item 是“通知里携带的具体内容”
```

## 5. 常见 event 类型

### 5.1 raw_response_event

```python
if event.type == "raw_response_event":
    continue
```

`raw_response_event` 是模型底层的原始输出事件。

它通常表示：

```text
模型正在一小段一小段生成文字
```

比如模型最终想说：

```text
Here are three jokes.
```

流式过程中可能拆成：

```text
Here
 are
 three
 jokes
.
```

这些小片段就属于 `raw_response_event`。

如果想做“打字机效果”，就要处理它。

### 5.2 agent_updated_stream_event

```python
elif event.type == "agent_updated_stream_event":
    print(f"Agent updated: {event.new_agent.name}")
```

意思是：

```text
当前正在运行的 Agent 更新了
```

简单单 Agent 场景里，可能就是：

```text
Agent updated: Joker
```

复杂多 Agent 场景里，可能会从一个 Agent 切到另一个 Agent。

比如：

```text
客服 Agent -> 退款 Agent
```

### 5.3 run_item_stream_event

```python
elif event.type == "run_item_stream_event":
```

这是比较高层的 Agent 运行事件。

它表示：

```text
Agent 运行过程中产生了一个具体 item
```

这个 item 可能是：

```text
工具调用
工具输出
最终消息
handoff
其他运行过程中的对象
```

## 6. 常见 item 类型

### 6.1 tool_call_item

```python
if event.item.type == "tool_call_item":
    print(f"-- Tool was called: {getattr(event.item.raw_item, 'name', 'Unknown Tool')}")
```

意思是：

```text
Agent 决定调用一个工具
```

比如输出：

```text
-- Tool was called: how_many_jokes
```

人话解释：

```text
Agent 按了一下 how_many_jokes 这个按钮
```

### 6.2 tool_call_output_item

```python
elif event.item.type == "tool_call_output_item":
    print(f"-- Tool output: {event.item.output}")
```

意思是：

```text
工具执行完了，并返回了结果
```

比如：

```text
-- Tool output: 3
```

人话解释：

```text
how_many_jokes 工具告诉 Agent：你要讲 3 个笑话
```

这里的：

```python
event.item.output
```

就是工具真正返回的值。

### 6.3 message_output_item

```python
elif event.item.type == "message_output_item":
    print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
```

意思是：

```text
Agent 最终生成了一条完整消息
```

比如：

```text
-- Message output:
 1. Why did the scarecrow win an award? Because he was outstanding in his field.
 2. Why don't skeletons fight each other? They don't have the guts.
 3. Why did the computer go to the doctor? Because it had a virus.
```

注意：

> `message_output_item` 通常是完整消息生成好了之后，再一次性打印出来。
> 它不是逐字输出。

## 7. raw_response_event 和 message_output_item 的区别

最重要的一句话：

```text
raw_response_event = 模型正在一点点吐字
message_output_item = 一条完整消息已经生成好了
```

所以：

### 如果你打印 raw_response_event

你会看到打字机效果：

```text
1.
 Why
 did
 the
 scarecrow
...
```

### 如果你忽略 raw_response_event，只打印 message_output_item

你会看到最终完整消息：

```text
1. Why did the scarecrow win an award? Because he was outstanding in his field.
2. Why don't skeletons fight each other? They don't have the guts.
3. Why did the computer go to the doctor? Because it had a virus.
```

## 8. 为什么代码里忽略 raw_response_event？

代码：

```python
if event.type == "raw_response_event":
    continue
```

意思是：

```text
如果遇到底层文字碎片事件，我不打印它，直接看下一个事件
```

这不是阻止 Agent 输出。

它只是：

```text
这类事件我不处理
这类事件我不展示
Agent 继续正常运行
```

`continue` 的意思是：

```text
跳过本轮循环，继续下一轮循环
```

所以 Agent 还是会继续：

```text
调用工具
拿到工具结果
生成最终消息
输出 message_output_item
```

## 9. 这段代码的真实运行顺序

以这个输出为例：

```text
=== Run starting ===
Agent updated: Joker
-- Tool was called: how_many_jokes
-- Tool output: 3
-- Message output:
 1. Why did the scarecrow win an award? Because he was outstanding in his field.
 2. Why don't skeletons fight each other? They don't have the guts.
 3. Why did the computer go to the doctor? Because it had a virus.
```

真实过程大概是：

```text
1. 程序开始运行
2. 当前 Agent 是 Joker
3. 模型根据 instructions 判断：我要先调用 how_many_jokes 工具
4. 产生工具调用 item：tool_call_item
5. 工具 how_many_jokes 被调用
6. 工具返回 3
7. 产生工具输出 item：tool_call_output_item
8. 模型根据工具结果，开始生成 3 个笑话
9. 生成过程中可能有很多 raw_response_event，但代码忽略了
10. 最终完整消息生成完成
11. 产生 message_output_item
12. 代码一次性打印完整消息
```

## 10. ItemHelpers 是什么？

```python
ItemHelpers.text_message_output(event.item)
```

`ItemHelpers` 可以理解成：

```text
SDK 提供的拆包工具
```

因为 `event.item` 本身不是普通字符串，而是一个复杂对象。

里面可能有：

```text
消息内容
角色信息
结构化字段
原始 API 数据
其他元信息
```

如果自己拆，会很麻烦。

所以 SDK 提供了：

```python
ItemHelpers.text_message_output(event.item)
```

它的作用是：

```text
从复杂的 message_output_item 里，把真正的文本内容拿出来
```

人话：

```text
event.item 是一个复杂包裹
ItemHelpers.text_message_output 是帮你从包裹里只拿出文本
```

## 11. raw_item 是什么？

```python
event.item.raw_item
```

`raw_item` 里的 `raw` 是“原始”的意思。

简单说：

```text
item = SDK 包装过、比较好理解的对象
raw_item = 底层 API 返回的原始对象
```

你平时优先看：

```python
event.item.type
event.item.output
```

就够了。

只有当你需要拿更底层的信息，比如工具名字时，才可能用到：

```python
event.item.raw_item
```

## 12. getattr 是什么？

代码：

```python
getattr(event.item.raw_item, 'name', 'Unknown Tool')
```

意思是：

```text
尝试从 event.item.raw_item 里面拿 name 属性
如果拿得到，就返回 name
如果拿不到，就返回 Unknown Tool
```

它比直接写下面这样更安全：

```python
event.item.raw_item.name
```

因为如果 `raw_item` 没有 `name`，直接取会报错。

而 `getattr` 可以设置默认值：

```python
getattr(对象, "属性名", "默认值")
```

所以这句可以理解为：

```text
尽量拿工具名字
拿不到就显示 Unknown Tool
```

## 13. 最简单的记忆表

| 名词 | 人话解释 |
| --- | --- |
| `Runner.run` | 等 Agent 全部跑完，一次性拿最终结果 |
| `Runner.run_streamed` | Agent 边跑边产生事件，可以边看过程 |
| `stream_events()` | 监听 Agent 运行过程中的事件流 |
| `event` | 发生了一件事 |
| `item` | 这件事里面产生的具体对象 |
| `raw_response_event` | 模型正在一点点吐字的底层事件 |
| `agent_updated_stream_event` | 当前运行的 Agent 更新了 |
| `run_item_stream_event` | Agent 运行中产生了一个高层对象 |
| `tool_call_item` | Agent 决定调用工具 |
| `tool_call_output_item` | 工具返回了结果 |
| `message_output_item` | 最终完整消息生成好了 |
| `ItemHelpers` | 帮你从复杂 item 里提取信息的工具 |
| `raw_item` | 底层 API 原始对象 |
| `getattr` | 安全地从对象里取属性 |
| `continue` | 跳过当前这轮循环，继续看下一个事件 |

## 14. 我自己的理解总结

这段代码可以理解为一个：

```text
Agent 运行日志打印器
```

它不是重点展示“模型一个字一个字说了什么”，而是展示：

```text
谁在运行
调用了什么工具
工具返回了什么
最终输出了什么
```

如果想看文字逐字输出，就处理：

```python
raw_response_event
```

如果想看 Agent 的关键执行步骤，就忽略：

```python
raw_response_event
```

然后重点看：

```python
run_item_stream_event
```

里面的：

```python
tool_call_item
tool_call_output_item
message_output_item
```

最终记住一句话：

> `event` 是“发生了什么事”，`item` 是“这件事里产生的具体东西”。
> `raw_response_event` 是模型正在一点点吐字；`message_output_item` 是完整消息已经生成好了。
