const BASE_URL = "http://127.0.0.1:8000";

export const fetchTasks = async () => {
  const res = await fetch(`${BASE_URL}/tasks`);
  if (!res.ok) throw new Error("Error fetching tasks");
  return res.json();
};

export const createTask = async (task: {
  title: string;
  description: string;
  date: string;
}) => {
  const res = await fetch(`${BASE_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task),
  });
  if (!res.ok) throw new Error("Error creating task");
  return res.json();
};
