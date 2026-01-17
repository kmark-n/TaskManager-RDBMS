export type TaskStatus = "Open" | "In Progress" | "Done";

/**
 * Used by the Status dropdown
 */
export type StatusFilter = TaskStatus | "ALL";

/**
 * Controls JOIN behavior
 */
export type ViewMode = "TASKS_ONLY" | "TASKS_PROJECTS";

export interface Task {
  id: number;
  title: string;
  status: TaskStatus;
  project_id?: number;
  project?: string;
}

export interface Project {
  id: number;
  name: string;
}

export interface EngineEvent {
  type: string;
  message: string;
}

export interface ASTNode {
  node: string;
  children?: (ASTNode | string)[];
}

