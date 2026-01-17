import { useState } from "react";
import type { TaskStatus, Project } from "../types";

interface AddTaskFormProps {
  onExecute: (sql: string) => void;
  onCancel: () => void;
  projects: Project[];
}

export default function AddTaskForm({ onExecute, onCancel, projects }: AddTaskFormProps) {
  const [title, setTitle] = useState("");
  const [status, setStatus] = useState<TaskStatus>("Open");
  
  // Initialize with an empty string
  const [selectedProjectId, setSelectedProjectId] = useState("");

  // DERIVED STATE:
  // If no project is selected yet, but projects are available, 
  // we use the first one as the effective ID.
  const effectiveProjectId = selectedProjectId || (projects.length > 0 ? projects[0].id.toString() : "");

  console.log("DEBUG - AddTaskForm projects prop:", projects);
  console.log("DEBUG - effectiveProjectId:", effectiveProjectId);

  const handleSubmit = () => {
    // Use the effective ID here so the form works even if the user didn't click the dropdown
    if (!title.trim() || !effectiveProjectId) return;

    const sql = `INSERT INTO tasks VALUES (0, "${title.trim()}", "${status}", ${Number(effectiveProjectId)})`;
    
    console.log("EXECUTING SQL:", sql);
    onExecute(sql);
    onCancel();
  };

  const inputStyle = { color: "black", backgroundColor: "white" };

  return (
    <div className="form-container">
      <h3><span>📝</span> New Database Task</h3>

      <div className="field-group">
        <label htmlFor="taskTitle">Task Title</label>
        <input
          id="taskTitle"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="e.g., Implement B-Tree Indexing"
          style={inputStyle}
        />
      </div>

      <div className="field-group">
        <label htmlFor="projectSelect">Relational Project (Foreign Key)</label>
        <select
          id="projectSelect"
          // Use the effectiveProjectId to ensure the UI shows the first project as selected
          value={effectiveProjectId}
          onChange={(e) => setSelectedProjectId(e.target.value)}
          style={inputStyle}
        >
          {projects.length === 0 ? (
            <option value="">No projects available...</option>
          ) : (
            projects.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} (ID: {p.id})
              </option>
            ))
          )}
        </select>
      </div>

      <div className="field-group">
        <label htmlFor="statusSelect">Initial Status</label>
        <select
          id="statusSelect"
          value={status}
          onChange={(e) => setStatus(e.target.value as TaskStatus)}
          style={inputStyle}
        >
          <option value="Open">Open</option>
          <option value="In Progress">In Progress</option>
          <option value="Done">Done</option>
        </select>
      </div>

      <div className="form-actions">
        <button type="button" className="btn-cancel" onClick={onCancel}>Discard</button>
        <button
          type="button"
          className="btn-submit"
          onClick={handleSubmit}
          // Button is enabled if we have a title and an effective project ID
          disabled={!title.trim() || !effectiveProjectId}
        >
          Execute INSERT
        </button>
      </div>
    </div>
  );
}
