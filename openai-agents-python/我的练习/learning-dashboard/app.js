function getStatusLabel(status) {
  const labels = {
    done: "完成",
    in_progress: "进行中",
    started: "已启动",
    todo: "未开始",
  };
  return labels[status] || status;
}

function getOverallProgress(phases) {
  const taskGroups = phases.flatMap((phase) => phase.tasks);
  const done = taskGroups.filter((task) => task.status === "done").length;
  return Math.round((done / taskGroups.length) * 100);
}

function findCurrentTask(data) {
  const phase = data.phases.find((item) => item.id === data.currentFocus.phaseId);
  const task = phase?.tasks.find((item) => item.id === data.currentFocus.taskId);
  return { phase, task };
}

function getTaskCounts(phases) {
  const tasks = phases.flatMap((phase) => phase.tasks);
  return {
    done: tasks.filter((task) => task.status === "done").length,
    total: tasks.length,
  };
}

function renderMetrics(data, overallProgress) {
  const counts = getTaskCounts(data.phases);
  const metrics = data.milestones.map((item) => {
    let value = item.value;
    if (item.label === "整体进度") value = `${overallProgress}%`;
    if (item.label === "已完成") value = `${counts.done}/${counts.total}`;

    return `
      <article class="metric">
        <strong>${value}</strong>
        <span>${item.label} · ${item.caption}</span>
      </article>
    `;
  });

  document.querySelector("#metrics").innerHTML = metrics.join("");
}

function renderNextTask(data) {
  const { phase, task } = findCurrentTask(data);
  document.querySelector("#next-task").innerHTML = `
    <div class="task-focus">
      <h3>${task?.title || data.currentFocus.title}</h3>
      <p>${data.currentFocus.summary}</p>
      <div class="artifact">${task?.artifact || "待创建练习文件"}</div>
      <p class="muted">${phase?.title || "当前阶段"} · ${phase?.name || ""}</p>
    </div>
  `;
}

function renderSprint(data) {
  if (!data.sprint || !data.tomorrowPlan) return;

  document.querySelector("#sprint-title").textContent = data.sprint.title;
  document.querySelector("#sprint-meta").textContent = `${data.sprint.targetDate} · ${data.sprint.pace}`;
  document.querySelector("#sprint-summary").textContent = data.sprint.summary;

  const items = data.tomorrowPlan.map((item) => {
    return `
      <article class="plan-item">
        <span class="plan-time">${item.time}</span>
        <h3>${item.title}</h3>
        <p>${item.goal}</p>
        <span class="plan-output">产出：${item.output}</span>
      </article>
    `;
  });

  document.querySelector("#tomorrow-plan").innerHTML = items.join("");
}

function renderPhases(data) {
  const currentPhaseId = data.currentFocus.phaseId;
  const currentTaskId = data.currentFocus.taskId;

  const phases = data.phases.map((phase) => {
    const tasks = phase.tasks
      .map((task) => {
        const isCurrent = task.id === currentTaskId ? " · 当前" : "";
        return `
          <div class="task ${task.status}">
            <mark aria-hidden="true"></mark>
            <div>
              <span class="task-title">${task.title}</span>
              <span class="task-artifact">${getStatusLabel(task.status)}${isCurrent} · ${task.artifact}</span>
            </div>
          </div>
        `;
      })
      .join("");

    const currentClass = phase.id === currentPhaseId ? " is-current" : "";

    return `
      <article class="phase${currentClass}">
        <div class="phase-head">
          <div>
            <p class="phase-kicker">${phase.title} · ${getStatusLabel(phase.status)}</p>
            <h3>${phase.name}</h3>
            <p class="phase-goal">${phase.goal}</p>
          </div>
          <div class="phase-percent">${phase.progress}%</div>
        </div>
        <div class="bar" aria-label="${phase.name} 进度 ${phase.progress}%">
          <span style="width: ${phase.progress}%"></span>
        </div>
        <div class="tasks">${tasks}</div>
      </article>
    `;
  });

  document.querySelector("#phase-list").innerHTML = phases.join("");
}

function renderLog(data) {
  const log = data.recentLog.map((item) => {
    return `
      <article class="log-item">
        <time>${item.date}</time>
        <h3>${item.title}</h3>
        <p>${item.note}</p>
      </article>
    `;
  });

  document.querySelector("#recent-log").innerHTML = log.join("");
}

function renderDashboard(data) {
  const overallProgress = getOverallProgress(data.phases);

  document.documentElement.style.setProperty("--overall-progress", overallProgress);
  document.querySelector("#current-summary").textContent = data.currentFocus.summary;
  document.querySelector("#current-title").textContent = data.currentFocus.title;
  document.querySelector("#updated-at").textContent = `更新于 ${data.updatedAt}`;
  document.querySelector("#overall-percent").textContent = `${overallProgress}%`;
  document.querySelector(".ring").style.setProperty("--percent", overallProgress);

  renderMetrics(data, overallProgress);
  renderSprint(data);
  renderNextTask(data);
  renderPhases(data);
  renderLog(data);
}

renderDashboard(learningProgress);
