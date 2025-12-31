import React from "react";

type Task = {
  id: number;
  title: string;
  description: string;
  task_date: string;
  completed: boolean;
};

type Props = {
  tasks: Task[];
};

const TaskList: React.FC<Props> = ({ tasks }) => {
  return (
    <div>
      <h2>Tareas</h2>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <strong>{task.title}</strong> - {task.description} - {task.task_date}{" "}
            [{task.completed ? "✔️" : "❌"}]
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TaskList;
