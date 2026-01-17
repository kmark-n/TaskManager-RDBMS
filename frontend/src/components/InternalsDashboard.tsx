import type { EngineEvent, ASTNode } from "../types";

export default function InternalsDashboard({ query, events }: { query: string, ast: ASTNode | null, events: EngineEvent[] }) {
  return (
    <div className="panel right">
      <h2>🧠 Internals Dashboard</h2>
      
      <div className="terminal-section">
        <label>LAST EXECUTED SQL</label>
        <pre className="query-display">{query || "Waiting for query..."}</pre>
      </div>

      <div className="terminal-section">
        <label>ENGINE EVENT LOG</label>
        <div className="event-log">
          {events.map((e, i) => (
            <div key={i} className="event-item">
              <span className="event-type">[{e.type}]</span> {e.message}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
