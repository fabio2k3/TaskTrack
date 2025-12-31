import { useEffect, useState } from "react";
import "./App.css";

interface Task {
  id: number;
  title: string;
  description: string;
  date: string;
  completed: boolean;
  created_at: string;
}

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);

  // Función para cargar tareas desde el backend
  const loadTasks = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/tasks");
      const data: Task[] = await res.json();
      setTasks(data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      await loadTasks();
    };
    fetchData();
  }, []);

  return (
    <div className="App">
      <h1>TaskTrack Frontend</h1>
      {loading && <p>Cargando tareas...</p>}
      {!loading && tasks.length === 0 && <p>No hay tareas.</p>}
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <strong>{task.title}</strong> - {task.description} | Fecha: {task.date} |{" "}
            {task.completed ? "Completada" : "Pendiente"}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
