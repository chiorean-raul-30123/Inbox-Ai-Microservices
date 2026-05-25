export type TodoItem = {
  id: string;
  title: string;
  description?: string;
  dueDate: string;
  dueTime: string;
  completed: boolean;
};

function getTodoKey(userId: string) {
  return `inboxAiTodos:${userId}`;
}

export function getTodos(userId: string): TodoItem[] {
  const raw = localStorage.getItem(getTodoKey(userId));
  if (!raw) return [];

  try {
    return JSON.parse(raw) as TodoItem[];
  } catch {
    return [];
  }
}

export function saveTodos(userId: string, todos: TodoItem[]) {
  localStorage.setItem(getTodoKey(userId), JSON.stringify(todos));
}

export function addTodo(userId: string, todo: TodoItem) {
  const todos = getTodos(userId);
  saveTodos(userId, [todo, ...todos]);
}

export function updateTodo(userId: string, todo: TodoItem) {
  const todos = getTodos(userId).map((item) =>
    item.id === todo.id ? todo : item
  );

  saveTodos(userId, todos);
}

export function deleteTodo(userId: string, todoId: string) {
  const todos = getTodos(userId).filter((item) => item.id !== todoId);
  saveTodos(userId, todos);
}