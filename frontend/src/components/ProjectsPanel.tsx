import { useState } from "react";
import type { Project } from "../types";

interface ProjectsPanelProps {
  onExecute: (sql: string) => void;
  onClose: () => void;
  projects: Project[];
}

export default function ProjectsPanel({ onExecute, onClose, projects }: ProjectsPanelProps) {
  const [name, setName] = useState("");

  const handleAddProject = () => {
    if (!name.trim()) return;

    const sql = `INSERT INTO projects VALUES ("${name.trim()}")`;
    onExecute(sql);
    setName("");
  };

  return (
    <div className="form-container">
      <h3>
        <span style={{ marginRight: "10px" }}>📁</span> 
        Manage Projects
      </h3>

      {/* Input Section */}
      <div className="field-group">
        <label htmlFor="projectName">New Project Name</label>
        <div style={{ display: "flex", gap: "8px" }}>
          <input
            id="projectName"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g., Backend Engine"
            onKeyDown={(e) => e.key === "Enter" && handleAddProject()}
          />
          <button className="btn-submit" onClick={handleAddProject}>
            Create
          </button>
        </div>
      </div>

      {/* List Section */}
      <div style={{ marginTop: "24px" }}>
        <label className="list-label">EXISTING PROJECTS</label>
        <ul className="project-list">
          {projects.length === 0 ? (
            <li className="project-item empty">No projects in database</li>
          ) : (
            projects.map((p) => (
              <li key={p.id} className="project-item">
                <span className="project-name">{p.name}</span>
                <code className="project-id">ID: {p.id}</code>
              </li>
            ))
          )}
        </ul>
      </div>

      {/* Footer Section */}
      <div className="form-actions" style={{ marginTop: "20px" }}>
        <button className="btn-cancel" onClick={onClose} style={{ width: "100%" }}>
          Back to Task Manager
        </button>
      </div>
    </div>
  );
}
