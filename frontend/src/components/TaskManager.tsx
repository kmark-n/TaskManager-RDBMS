import { useState } from "react";
import TaskControls from "./TaskControls";
import TaskTable from "./TaskTable";
import AddTaskForm from "./AddTaskForm";
import ProjectsPanel from "./ProjectsPanel";
import type { StatusFilter, ViewMode, Task, Project } from "../types";

type PanelMode = "TASKS" | "ADD_TASK" | "PROJECTS";

interface Props {
  tasks: Task[];       // Received from App.tsx
  projects: Project[]; // Received from App.tsx
  onExecute: (sql: string) => Promise<void>;
}

export default function TaskManager({ tasks, projects, onExecute }: Props) {
  // --- UI State ---
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("ALL");
  const [view, setView] = useState<ViewMode>("TASKS_ONLY");
  const [panel, setPanel] = useState<PanelMode>("TASKS");

  const handleDelete = (id: number) => {
    if (confirm("Delete this task?")) {
        onExecute(`DELETE FROM tasks WHERE id = ${id}`);
    }
  };

  const handleUpdate = (id: number, title: string, status: string) => {
    const sql = `UPDATE tasks SET title = "${title}", status = "${status}" WHERE id = ${id}`;
    onExecute(sql);
  };

  
  const visibleTasks =
    statusFilter === "ALL"
      ? tasks
      : tasks.filter(t => t.status === statusFilter);

  
  return (
    <div className="task-manager">
      <h2>✏️ Task Manager</h2>

      <TaskControls
        status={statusFilter}
        view={view}
        onStatusChange={setStatusFilter}
        onViewChange={setView}
        onAddTask={() => setPanel("ADD_TASK")}
        onProjects={() => setPanel("PROJECTS")}
        onExecute={onExecute}
      />

      {/* ADD TASK FORM */}
      {panel === "ADD_TASK" && (
        <AddTaskForm
          projects={projects}
          onExecute={onExecute} // App.tsx handles the refresh logic
          onCancel={() => setPanel("TASKS")}
        />
      )}

      {/* PROJECTS MANAGEMENT */}
      {panel === "PROJECTS" && (
        <ProjectsPanel
          projects={projects}
          onExecute={onExecute} // App.tsx handles the refresh logic
          onClose={() => setPanel("TASKS")}
        />
      )}

      {/* TASK DATA TABLE */}
      {panel === "TASKS" && (
        <TaskTable
          tasks={visibleTasks}
          showProject={view === "TASKS_PROJECTS"}
          onDelete={handleDelete}
          onUpdate={handleUpdate
          }
        />
      )}
    </div>
  );
}
