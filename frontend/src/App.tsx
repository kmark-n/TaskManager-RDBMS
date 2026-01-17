import { useState, useEffect, useCallback } from "react";
import TaskManager from "./components/TaskManager";
import InternalsDashboard from "./components/InternalsDashboard";
import type { Task, Project, EngineEvent, ASTNode } from "./types";
import "./styles.css";

export default function App() {
  // 1. DATA STATE (The Single Source of Truth)
  const [tasks, setTasks] = useState<Task[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  
  // 2. INTERNALS STATE
  const [lastQuery, setLastQuery] = useState("");
  const [ast, setAst] = useState<ASTNode | null>(null);
  const [events, setEvents] = useState<EngineEvent[]>([]);

  /* -----------------------------
      DATA FETCHING LOGIC
  ------------------------------*/
  const fetchData = useCallback(async () => {
    try {
      // We fetch both tables using our custom SQL console endpoint
      const [projRes, taskRes] = await Promise.all([
        fetch("http://localhost:8000/api/query", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ sql: "SELECT * FROM projects" }),
        }),
        fetch("http://localhost:8000/api/query", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ sql: "SELECT * FROM tasks" }),
        })
      ]);

      const projData = await projRes.json();
      const taskData = await taskRes.json();

      // routes.py wraps results in a .result property
      if (projData.result) setProjects(projData.result);
      if (taskData.result) setTasks(taskData.result);
      
    } catch (err) {
      console.error("Fetch Error:", err);
    }
  }, []);

  // Initial load when the app starts
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  /* -----------------------------
      SQL EXECUTION
  ------------------------------*/
  const runSQL = async (sql: string) => {
  try {
    const res = await fetch("http://localhost:8000/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sql }),
    });

    const data = await res.json();
    if (res.status === 400 || data.detail) {
        console.error("SQL Error:", data.detail);
        alert("Parser Error: " + data.detail); 
        return data; // Stop here if there was an error
      }

    setLastQuery(sql);
    setAst(data.ast ?? null);

    // If the query was a SELECT, update the specific state immediately
    const cleanSQL = sql.trim().toUpperCase();

    if (cleanSQL.startsWith("SELECT")) {
      // Direct update for SELECTs
      if (cleanSQL.includes("FROM TASKS")) {
        setTasks(data.result || []);
      } else if (cleanSQL.includes("FROM PROJECTS")) {
        setProjects(data.result || []);
      }
    } else {
      // It's an INSERT, DELETE, or UPDATE.
      // We MUST wait for the database to finish, then pull fresh data.
      console.log("Write operation detected. Refreshing data...");
      await fetchData();
    }
    
    return data;
  } catch (err) {
    console.error("SQL Execution Error:", err);
  }
};

  /* -----------------------------
      WEBSOCKET: ENGINE EVENTS
  ------------------------------*/
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/events");
    socket.onmessage = (event) => {
      const engineEvent: EngineEvent = JSON.parse(event.data);
      setEvents((prev) => [engineEvent, ...prev]);
    };
    return () => socket.close();
  }, []);

  return (
    <div className="app">
      <div className="panel left">
        <TaskManager 
          tasks={tasks} 
          projects={projects} 
          onExecute={runSQL} 
        />
      </div>

      <div className="panel right">
        <InternalsDashboard
          query={lastQuery}
          ast={ast}
          events={events}
        />
      </div>
    </div>
  );
}
