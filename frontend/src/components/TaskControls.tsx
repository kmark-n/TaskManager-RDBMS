import type { StatusFilter, ViewMode } from "../types";

interface Props {
  status: StatusFilter;
  view: ViewMode;
  onStatusChange: (status: StatusFilter) => void; 
  onViewChange: (view: ViewMode) => void;
  onExecute: (sql: string) => void;
  onAddTask: () => void;
  onProjects: () => void;
}

export default function TaskControls({ 
  status, 
  view, 
  onStatusChange, // Changed from setStatus
  onViewChange,   // Changed from setView
  onExecute, 
  onAddTask, 
  onProjects 
}: Props) {

  const handleStatusChange = (newStatus: StatusFilter) => {
    onStatusChange(newStatus);
    if (newStatus === "ALL") {
      onExecute("SELECT * FROM tasks");
    } else {
      onExecute(`SELECT * FROM tasks WHERE status = '${newStatus}'`);
    }
  };

  const handleViewChange = (newView: ViewMode) => {
    onViewChange(newView);
    if (newView === "TASKS_PROJECTS") {
      onExecute("SELECT tasks.id, tasks.title, tasks.status, projects.name FROM tasks JOIN projects ON tasks.project_id = projects.id");
    } else {
      onExecute("SELECT * FROM tasks");
    }
  };

  return (
    <div className="controls">
      <button onClick={onAddTask}>Add Task</button>
      <button onClick={onProjects}>Projects</button>

      <select value={status} onChange={e => handleStatusChange(e.target.value as StatusFilter)}>
        <option value="ALL">All Status</option>
        <option value="Open">Open</option>
        <option value="In Progress">In Progress</option>
        <option value="Done">Done</option>
      </select>

      <select value={view} onChange={e => handleViewChange(e.target.value as ViewMode)}>
        <option value="TASKS_ONLY">Tasks Only</option>
        <option value="TASKS_PROJECTS">Tasks + Projects (JOIN)</option>
      </select>
    </div>
  );
}
