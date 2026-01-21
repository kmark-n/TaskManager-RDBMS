import { useState } from "react";
import type { Task } from "../types";

interface JoinedTask extends Task {
  name?: string; 
}

interface Props {
  tasks: JoinedTask[];
  showProject: boolean;
  onDelete: (id: number) => void;
  onUpdate: (id: number, title: string, status: string) => void;
}

export default function TaskTable({ tasks, showProject, onDelete, onUpdate }: Props) {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editStatus, setEditStatus] = useState("");

  const startEdit = (t: JoinedTask) => {
    setEditingId(t.id);
    setEditTitle(t.title);
    setEditStatus(t.status);
  };

  const cancelEdit = () => {
    setEditingId(null);
  };

  const handleSave = (id: number) => {
    onUpdate(id, editTitle, editStatus);
    setEditingId(null);
  };

  if (!tasks || !Array.isArray(tasks)) {
    return <div style={{ color: "red" }}>Error: Tasks is not an array!</div>;
  }

  if (tasks.length === 0) {
    return <div style={{ padding: "20px", color: "gray" }}>No tasks found in database.</div>;
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
        {tasks.map((t, index) => {
          const isEditing = editingId === t.id;
          return (
            <tr key={t.id || index}>
              <td>{t.id}</td>

              {/* TITLE CELL */}
              <td>
                {isEditing ? (
                  <input
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    autoFocus
                  />
                ) : (
                  t.title
                )}
              </td>

              {/* STATUS CELL */}
              <td>
                {isEditing ? (
                  <select value={editStatus} onChange={(e) => setEditStatus(e.target.value)}>
                    <option value="Open">Open</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Done">Done</option>
                  </select>
                ) : (
                  <span className={`status-badge ${t.status.toLowerCase().replace(" ", "-")}`}>
                    {t.status}
                  </span>
                )}
              </td>

              {showProject && (
                <td>{t.name || (t.project_id !== 0 ? `ID: ${t.project_id}` : "-")}</td>
              )}

              {/* ACTIONS CELL */}
              <td>
                {isEditing ? (
                  <div className="action-buttons">
                    <button onClick={() => handleSave(t.id)} title="Save" style={{ background: 'none', border: 'none', cursor: 'pointer' }}>💾</button>
                    <button onClick={cancelEdit} title="Cancel" style={{ background: 'none', border: 'none', cursor: 'pointer' }}>❌</button>
                  </div>
                ) : (
                  <div className="action-buttons">
                    <button
                      onClick={() => startEdit(t)}
                      style={{ cursor: "pointer", marginRight: "8px", background: 'none', border: 'none' }}
                      title="Edit"
                    >
                      ✏️
                    </button>
                    <button
                      onClick={() => onDelete(t.id)}
                      style={{ cursor: "pointer", color: "red", background: 'none', border: 'none' }}
                      title="Delete"
                    >
                      🗑
                    </button>
                  </div>
                )}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
