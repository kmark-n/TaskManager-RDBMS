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
        // onExecute={onExecute} <--- ADD THIS if TaskControls requires it
      />

      {/* CONDITIONAL PANELS */}
      {panel === "ADD_TASK" && (
        <AddTaskForm
          projects={projects}
          onExecute={onExecute}
          onCancel={() => setPanel("TASKS")}
        />
      )}

      {panel === "PROJECTS" && (
        <ProjectsPanel
          projects={projects}
          onExecute={onExecute}
          onClose={() => setPanel("TASKS")}
        />
      )}

      {/* ONLY RENDER TABLE IF IN TASKS MODE */}
      {panel === "TASKS" && (
        <TaskTable
          tasks={visibleTasks}
          showProject={view === "TASKS_PROJECTS"}
          onDelete={handleDelete}
          onUpdate={handleUpdate}
        />
      )}
    </div>
  );