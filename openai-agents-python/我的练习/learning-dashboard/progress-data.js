const learningProgress = {
  updatedAt: "2026-06-15",
  currentFocus: {
    phaseId: "phase-2",
    taskId: "tool-errors",
    title: "Tool Error Agent",
    summary: "Streaming Agent 已完成。下一步练工具错误处理：工具报错时，Agent 如何接住错误并给用户一个稳的回答。",
    status: "in_progress",
  },
  milestones: [
    {
      label: "已完成",
      value: "6/15",
      caption: "核心练习",
    },
    {
      label: "当前阶段",
      value: "2",
      caption: "工具与多轮",
    },
    {
      label: "整体进度",
      value: "40%",
      caption: "第一轮学习地图",
    },
  ],
  phases: [
    {
      id: "phase-1",
      title: "阶段 1",
      name: "单 Agent 基础",
      goal: "理解 Agent 和一次普通模型调用的区别。",
      status: "done",
      progress: 100,
      tasks: [
        {
          id: "hello-deepseek",
          title: "跑通最小 Agent",
          status: "done",
          artifact: "my_hello_deepseek.py",
        },
        {
          id: "dual-persona",
          title: "双人格 Agent",
          status: "done",
          artifact: "已做过，后续可补归档文件",
        },
        {
          id: "streaming-agent",
          title: "流式输出 Agent",
          status: "done",
          artifact: "01_single_agent/streaming_agent.py",
        },
      ],
    },
    {
      id: "phase-2",
      title: "阶段 2",
      name: "工具与多轮",
      goal: "理解工具调用的本质，以及模型如何决定调用工具。",
      status: "in_progress",
      progress: 50,
      tasks: [
        {
          id: "sdk-tools",
          title: "SDK 工具调用",
          status: "done",
          artifact: "my_tools_agent.py",
        },
        {
          id: "multi-tool",
          title: "多工具组合调用",
          status: "done",
          artifact: "天气 + 算数 + 时间",
        },
        {
          id: "tool-errors",
          title: "工具错误处理",
          status: "in_progress",
          artifact: "02_tools/tool_error_agent.py",
        },
        {
          id: "real-tool",
          title: "真实 API 或本地文件工具",
          status: "todo",
          artifact: "02_tools/real_api_tool_agent.py",
        },
      ],
    },
    {
      id: "phase-3",
      title: "阶段 3",
      name: "Agent 设计模式",
      goal: "掌握 routing、judge、guardrails、agents-as-tools 等面试核心模式。",
      status: "started",
      progress: 18,
      tasks: [
        {
          id: "routing-handoff",
          title: "routing / handoff 初版",
          status: "done",
          artifact: "my_routing_agent.py",
        },
        {
          id: "ecommerce-routing",
          title: "全能客服路由升级",
          status: "todo",
          artifact: "03_patterns/ecommerce_routing_agent.py",
        },
        {
          id: "agents-as-tools",
          title: "Agents as tools 研究经理",
          status: "todo",
          artifact: "03_patterns/agents_as_tools_research_agent.py",
        },
        {
          id: "judge-guardrails",
          title: "Judge + Guardrails",
          status: "todo",
          artifact: "03_patterns/judge_code_review_agent.py",
        },
      ],
    },
    {
      id: "phase-4",
      title: "阶段 4",
      name: "多 Agent 协作",
      goal: "理解多个 Agent 如何交接任务、共享状态和避免循环。",
      status: "todo",
      progress: 0,
      tasks: [
        {
          id: "hospital-handoff",
          title: "医院导诊 handoff",
          status: "todo",
          artifact: "04_multi_agent/hospital_handoff_agent.py",
        },
        {
          id: "memory-agent",
          title: "长期记忆 Agent",
          status: "todo",
          artifact: "04_multi_agent/memory_agent.py",
        },
      ],
    },
    {
      id: "phase-5",
      title: "阶段 5",
      name: "简历项目",
      goal: "把工具、路由、并行、judge、记忆串成一个可展示项目。",
      status: "todo",
      progress: 0,
      tasks: [
        {
          id: "project-scope",
          title: "项目立项",
          status: "todo",
          artifact: "05_project/README.md",
        },
        {
          id: "content-intel-agent",
          title: "内容研究 / 情报 Agent",
          status: "todo",
          artifact: "05_project/app.py",
        },
      ],
    },
  ],
  recentLog: [
    {
      date: "2026-06-15",
      title: "完成 Streaming Agent",
      note: "已学习 run_streamed、stream_events、raw_response_event、run_item_stream_event、event/item、tool_call_item、tool_call_output_item 和 message_output_item。",
    },
    {
      date: "2026-06-15",
      title: "归档学习笔记",
      note: "已加入 00_notes/2026-06-15_streaming_agent_event_item_tool_call.md。",
    },
    {
      date: "2026-06-14",
      title: "创建 Streaming Agent 练习",
      note: "已补上 01_single_agent/streaming_agent.py，用 run_streamed 和 stream_events 展示流式输出。",
    },
    {
      date: "2026-06-14",
      title: "确认当前位置",
      note: "双人格 Agent 你认为已经做过，当前继续 Streaming Agent。",
    },
    {
      date: "2026-06-14",
      title: "建立学习地图网页",
      note: "以后问进度时，优先更新 progress-data.js，让网页同步显示。",
    },
  ],
};
