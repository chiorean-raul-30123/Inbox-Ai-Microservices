import { useMemo, useState } from "react";
import { ChevronLeft, ChevronRight, Clock } from "lucide-react";

import { MailSidebar } from "../components/mail/MailSidebar";
import { UserProfileMenu } from "../components/UserProfileMenu";
import { getTodos } from "../utils/todoStorage";
import { useAuth } from "../auth/AuthContext";

const hours = Array.from({ length: 14 }, (_, index) => `${7 + index}:00`);

function getStartOfWeek(date: Date) {
  const result = new Date(date);
  const day = result.getDay();
  const diff = result.getDate() - day + (day === 0 ? -6 : 1);

  result.setDate(diff);
  result.setHours(0, 0, 0, 0);

  return result;
}

function addDays(date: Date, days: number) {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

function toDateInputValue(date: Date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}

function formatDateLabel(date: Date) {
  return date.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
}

function formatFullDate(date: Date) {
  return date.toLocaleDateString(undefined, {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

function buildEventKey(date: Date, hour: string) {
  return `${toDateInputValue(date)}-${hour}`;
}

const eventTemplates = [
  {
    dayOffset: 0,
    hour: "10:00",
    title: "HR document review",
    department: "HR",
    completed: false,
  },
  {
    dayOffset: 2,
    hour: "13:00",
    title: "Finance batch check",
    department: "Finance",
    completed: false,
  },
  {
    dayOffset: 4,
    hour: "11:00",
    title: "Legal contract validation",
    department: "Legal",
    completed: false,
  },
];

export function CalendarPage() {
  const { user } = useAuth();
  const [selectedDate, setSelectedDate] = useState(new Date());

  const weekStart = useMemo(() => getStartOfWeek(selectedDate), [selectedDate]);

  const weekDays = useMemo(() => {
    return Array.from({ length: 7 }, (_, index) => addDays(weekStart, index));
  }, [weekStart]);

  const todos = useMemo(() => {
    if (!user) return [];
    return getTodos(user.id);
  }, [selectedDate, user?.id])

  const events = useMemo(() => {
    const templateEvents = eventTemplates.map((event) => {
      const date = addDays(weekStart, event.dayOffset);

      return {
        key: buildEventKey(date, event.hour),
        title: event.title,
        department: event.department,
        completed: event.completed,
      };
    });

    const todoEvents = todos.map((todo) => ({
      key: `${todo.dueDate}-${todo.dueTime}`,
      title: todo.title,
      completed: todo.completed,
    }));

    return [...templateEvents, ...todoEvents];
  }, [weekStart, todos]);

  function getEvent(date: Date, hour: string) {
    const key = buildEventKey(date, hour);
    return events.find((event) => event.key === key);
  }

  function goToPreviousWeek() {
    setSelectedDate((current) => addDays(current, -7));
  }

  function goToNextWeek() {
    setSelectedDate((current) => addDays(current, 7));
  }

  function goToToday() {
    setSelectedDate(new Date());
  }

  return (
    <div className="flex h-screen overflow-hidden bg-[#f3f6fb]">
      <MailSidebar activeSection="calendar" />

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
          <div>
            <h1 className="text-lg font-bold text-slate-950">Calendar</h1>
            <p className="text-sm text-slate-500">
              {formatFullDate(weekStart)} - {formatFullDate(addDays(weekStart, 6))}
            </p>
          </div>

          <UserProfileMenu />
        </header>

        <main className="flex min-h-0 flex-1 flex-col p-6">
          <div className="mb-5 flex flex-wrap items-center justify-between gap-4">
            <div>
              <h2 className="text-2xl font-bold text-slate-950">
                Weekly schedule
              </h2>
              <p className="text-sm text-slate-500">
                Select any date to jump to that week. To Do tasks appear here automatically.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={goToPreviousWeek}
                className="rounded-xl border border-slate-200 bg-white p-2 hover:bg-slate-50"
              >
                <ChevronLeft size={18} />
              </button>

              <button
                onClick={goToToday}
                className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              >
                Today
              </button>

              <input
                type="date"
                value={toDateInputValue(selectedDate)}
                onChange={(event) => {
                  const [year, month, day] = event.target.value.split("-").map(Number);
                  setSelectedDate(new Date(year, month - 1, day));
                }}
                className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 outline-none"
              />

              <button
                onClick={goToNextWeek}
                className="rounded-xl border border-slate-200 bg-white p-2 hover:bg-slate-50"
              >
                <ChevronRight size={18} />
              </button>
            </div>
          </div>

          <div className="min-h-0 flex-1 overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
            <div className="grid grid-cols-[90px_repeat(7,minmax(150px,1fr))] border-b border-slate-200 bg-slate-50">
              <div className="p-4 text-xs font-semibold uppercase text-slate-400">
                Time
              </div>

              {weekDays.map((date) => {
                const isToday = toDateInputValue(date) === toDateInputValue(new Date());

                return (
                  <div
                    key={date.toISOString()}
                    className="border-l border-slate-200 p-4"
                  >
                    <p className="text-sm font-bold text-slate-800">
                      {date.toLocaleDateString(undefined, { weekday: "short" })}
                    </p>
                    <p
                      className={`mt-1 inline-flex rounded-full px-2 py-1 text-xs font-semibold ${
                        isToday
                          ? "bg-blue-600 text-white"
                          : "bg-white text-slate-500"
                      }`}
                    >
                      {formatDateLabel(date)}
                    </p>
                  </div>
                );
              })}
            </div>

            <div className="h-full overflow-auto">
              {hours.map((hour) => (
                <div
                  key={hour}
                  className="grid min-h-[92px] grid-cols-[90px_repeat(7,minmax(150px,1fr))] border-b border-slate-100 last:border-b-0"
                >
                  <div className="sticky left-0 z-10 flex items-start gap-2 bg-white p-4 text-xs font-medium text-slate-400">
                    <Clock size={14} />
                    {hour}
                  </div>

                  {weekDays.map((date) => {
                    const event = getEvent(date, hour);

                    return (
                      <div
                        key={`${date.toISOString()}-${hour}`}
                        className="border-l border-slate-100 p-3"
                      >
                        {event && (
                          <div
                            className={`rounded-2xl border p-3 shadow-sm ${
                              event.completed
                                ? "border-slate-200 bg-slate-50"
                                : "border-blue-100 bg-blue-50"
                            }`}
                          >
                            <p
                              className={`text-sm font-bold ${
                                event.completed
                                  ? "text-slate-400 line-through"
                                  : "text-blue-900"
                              }`}
                            >
                              {event.title}
                            </p>
                            
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}