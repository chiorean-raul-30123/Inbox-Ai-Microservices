import { useEffect, useState } from "react";
import { CalendarPlus, CheckCircle2, Plus, Trash2 } from "lucide-react";

import { MailSidebar } from "../components/mail/MailSidebar";
import { UserProfileMenu } from "../components/UserProfileMenu";
import {
  addTodo,
  deleteTodo,
  getTodos,
  updateTodo,
  type TodoItem,
} from "../utils/todoStorage";
import { useAuth } from "../auth/AuthContext";

export function ToDoPage() {
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [dueDate, setDueDate] = useState(new Date().toISOString().slice(0, 10));
  const [dueTime, setDueTime] = useState("10:00");
  const { user } = useAuth();

  function loadTodos() {
    if (!user) return;
    setTodos(getTodos(user.id));
    }

  useEffect(() => {
    loadTodos();
  }, []);

  function handleAddTodo() {
    if (!title.trim()) return;

    const todo: TodoItem = {
      id: crypto.randomUUID(),
      title: title.trim(),
      description: description.trim() || undefined,
      dueDate,
      dueTime,
      completed: false,
    };

    if (!user) return;
    addTodo(user.id, todo);
    loadTodos();

    setTitle("");
    setDescription("");
  }

  function toggleTodo(todo: TodoItem) {
    if (!user) return;

    updateTodo(user.id, {
    ...todo,
    completed: !todo.completed,
    });

    loadTodos();
  }

  function handleDelete(todoId: string) {
    if (!user) return;

    deleteTodo(user.id, todoId);
    loadTodos();
  }
  useEffect(() => {
    loadTodos();
    }, [user?.id]);

  return (
    <div className="flex h-screen overflow-hidden bg-[#f3f6fb]">
      <MailSidebar activeSection="todo" />

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
          <div>
            <h1 className="text-lg font-bold text-slate-950">To Do</h1>
            <p className="text-sm text-slate-500">
              Tasks connected to your calendar schedule
            </p>
          </div>

          <UserProfileMenu />
        </header>

        <main className="min-h-0 flex-1 overflow-y-auto p-6">
          <div className="grid gap-6 lg:grid-cols-[420px_1fr]">
            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="mb-5 flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-blue-50 text-blue-600">
                  <CalendarPlus size={22} />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-slate-950">New task</h2>
                  <p className="text-sm text-slate-500">
                    Add a task with a date and time.
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                <input
                  value={title}
                  onChange={(event) => setTitle(event.target.value)}
                  placeholder="Task title"
                  className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
                />

                <textarea
                  value={description}
                  onChange={(event) => setDescription(event.target.value)}
                  placeholder="Description optional"
                  rows={4}
                  className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
                />

                <div className="grid grid-cols-2 gap-3">
                  <input
                    type="date"
                    value={dueDate}
                    onChange={(event) => setDueDate(event.target.value)}
                    className="rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
                  />

                  <input
                    type="time"
                    value={dueTime}
                    onChange={(event) => setDueTime(event.target.value)}
                    className="rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
                  />
                </div>


                <button
                  onClick={handleAddTodo}
                  className="flex w-full items-center justify-center gap-2 rounded-2xl bg-blue-600 px-5 py-3 text-sm font-bold text-white hover:bg-blue-700"
                >
                  <Plus size={18} />
                  Add to calendar
                </button>
              </div>
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white shadow-sm">
              <div className="border-b border-slate-200 px-6 py-5">
                <h2 className="text-xl font-bold text-slate-950">Task list</h2>
                <p className="mt-1 text-sm text-slate-500">
                  {todos.length} task{todos.length === 1 ? "" : "s"} scheduled
                </p>
              </div>

              <div className="divide-y divide-slate-100">
                {todos.length === 0 ? (
                  <div className="p-8 text-sm text-slate-500">
                    No tasks yet. Create one from the form.
                  </div>
                ) : (
                  todos.map((todo) => (
                    <div
                      key={todo.id}
                      className="flex items-start justify-between gap-4 p-5 hover:bg-slate-50"
                    >
                      <div className="flex gap-3">
                        <button
                          onClick={() => toggleTodo(todo)}
                          className={`mt-1 rounded-full ${
                            todo.completed ? "text-emerald-600" : "text-slate-300"
                          }`}
                        >
                          <CheckCircle2 size={22} />
                        </button>

                        <div>
                          <p
                            className={`font-semibold ${
                              todo.completed
                                ? "text-slate-400 line-through"
                                : "text-slate-950"
                            }`}
                          >
                            {todo.title}
                          </p>

                          {todo.description && (
                            <p className="mt-1 text-sm text-slate-500">
                              {todo.description}
                            </p>
                          )}

                          <div className="mt-3 flex flex-wrap gap-2 text-xs font-semibold">
                            <span className="rounded-full bg-blue-50 px-3 py-1 text-blue-700">
                              {todo.dueDate} at {todo.dueTime}
                            </span>
                            
                          </div>
                        </div>
                      </div>

                      <button
                        onClick={() => handleDelete(todo.id)}
                        className="rounded-xl p-2 text-slate-400 hover:bg-red-50 hover:text-red-600"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}