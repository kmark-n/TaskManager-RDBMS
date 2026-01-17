# 🛡️ Custom RDBMS & Database Internals Visualizer

A from-scratch implementation of a relational database management system (RDBMS)
featuring a custom SQL parser, execution engine, indexing subsystem, JOIN support,
and a real-time database internals visualization dashboard.

The project focuses on **how SQL queries are executed internally**, not just
the final results — exposing scans, index lookups, inserts, and JOIN execution
through a live UI.

---

## 🎯 Challenge Fulfillment Mapping

| Requirement | Implementation |
|------------|----------------|
| **Declaring Tables** | Custom schemas for `tasks` and `projects` (`db/setup.py`). |
| **CRUD Operations** | SQL-driven `INSERT`, `SELECT`, `UPDATE`, `DELETE`. |
| **Primary & Unique Keys** | Enforced primary keys with auto-increment logic. |
| **Indexing** | Custom hash-based indexing engine (`HashIndex`). |
| **JOIN Support** | Nested-loop JOIN execution with explicit ON-clause handling. |
| **Interactive REPL** | CLI-based SQL REPL (`repl.py`). |
| **Web App Demo** | React application with real-time WebSocket event streaming. |
| **Execution Visualization** | Live TABLE_SCAN, INDEX_LOOKUP, ROW_INSERTED, JOIN events. |

---

## 🏗️ Architecture Overview
![Architecture Diagram](./docs/architecture.png)


### Core Components
- **Parser**: EBNF-based SQL grammar using Lark to generate ASTs  
- **Executor**: Interprets AST nodes to perform relational operations  
- **Storage Engine**: In-memory table storage with primary key enforcement  
- **Indexing Engine**: Hash-based indexes for fast lookups  
- **Event System**: Pub/Sub engine emitting execution events in real time  

---

## 🖥️ Web Application UI



### Task Manager (Left Panel)
- Create, update, delete tasks
- Assign tasks to projects (foreign keys)
- Filter tasks by status
- Toggle between:
  - Tasks only
  - Tasks joined with projects

### Internals Dashboard (Right Panel)
- Displays executed SQL
- Visualizes the generated AST
- Streams live execution events via WebSockets
- Shows JOIN execution and index usage in real time

---

## 🚀 Running the Project

### Backend
```bash
python main.py

### SQL REPL
python repl.py

### Frontend
cd frontend
npm install
npm run dev

⚠️ Design Notes

The database engine is intentionally in-memory to emphasize execution logic.

Restarting the backend resets all data.

The SQL grammar is minimal by design and easily extensible.

📜 Credits & Attribution

Database engine, execution logic, indexing, and visualization
Implemented by the repository author.

AI Assistance
Architectural guidance and debugging support provided by Gemini (AI).

SQL Parsing
Powered by the Lark parsing library.



