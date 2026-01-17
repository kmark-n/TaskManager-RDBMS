import type { Task } from "../types";

interface JoinedTask extends Task {
  name?: string; // This comes from the projects table during a JOIN
}

interface Props {
  tasks: JoinedTask[];
  showProject: boolean;
  onDelete: (id: number) => void;
}

export default function TaskTable({ tasks, showProject, onDelete }: Props) {
  console.log("TASKTABLE RECEIVED:", tasks);
  if (!tasks || !Array.isArray(tasks)) {
    return <div style={{color: "red"}}>Error: Tasks is not an array!</div>;
  }

  if (tasks.length === 0) {
    return <div style={{padding: "20px", color: "gray"}}>No tasks found in database.</div>;
  }
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Status</th>
          {showProject && <th>Project</th>}
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {tasks.map((t, index) => (
          <tr key={t.id || index}>
            <td>{t.id}</td>
            <td>{t.title}</td>
            <td>{t.status}</td>
            
            {/* CHANGE IS HERE: Handle both JOIN results (name) and FK results (project_id) */}
            {showProject && (
              <td>{t.name || (t.project_id !== 0 ? `ID: ${t.project_id}` : "-")}</td>
            )}

            <td>
              <button 
                onClick={() => onDelete(t.id)} 
                style={{ cursor: "pointer", border: "none", background: "none" }}
              >
                🗑
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
