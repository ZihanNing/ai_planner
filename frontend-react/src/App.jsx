import { useState } from "react";

function App() {
  // -----------------------
  // State
  // -----------------------
  const [showFinalPlan, setShowFinalPlan] = useState(false);
  const [weeklyPlan, setWeeklyPlan] = useState("");
  const [weeklyTodos, setWeeklyTodos] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // -----------------------
  // Load weekly plan + todos
  // -----------------------
  async function loadFinalPlan() {
  console.log("Final Plan button clicked");

  // ⬅️ 必须放在最前面
  setShowFinalPlan(true);

  setLoading(true);
  setError(null);

  try {
    const planRes = await fetch(
      "http://127.0.0.1:8000/api/final-plan/plan"
    );

    console.log("planRes ok:", planRes.ok);

    const planData = await planRes.json();
    console.log("planData:", planData);

    setWeeklyPlan(planData.content);

    const todosRes = await fetch(
      "http://127.0.0.1:8000/api/final-plan/todos"
    );

    console.log("todosRes ok:", todosRes.ok);

    const todosData = await todosRes.json();
    console.log("todosData:", todosData);

    setWeeklyTodos(todosData);
  } catch (err) {
    console.error("loadFinalPlan error:", err);
    setError(err.message);
  } finally {
    setLoading(false);
  }
}



  // -----------------------
  // Update todo status
  // -----------------------
  async function updateTodoStatus(dayIndex, todoId, newStatus) {
    if (!weeklyTodos) return;

    const updated = {
      ...weeklyTodos,
      days: weeklyTodos.days.map((day, dIdx) => {
        if (dIdx !== dayIndex) return day;

        return {
          ...day,
          todos: day.todos.map((todo) =>
            todo.id === todoId
              ? { ...todo, status: newStatus }
              : todo
          ),
        };
      }),
    };

    // optimistic UI update
    setWeeklyTodos(updated);

    // persist to backend
    await fetch("http://127.0.0.1:8000/api/final-plan/todos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated),
    });
  }

  // -----------------------
  // Render
  // -----------------------
  return (
    <div style={{ padding: "24px", fontFamily: "sans-serif" }}>
      <h1>AI Weekly Planner</h1>

      <button
        onClick={loadFinalPlan}
        style={{
          padding: "10px 16px",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        Final Plan
      </button>

      {showFinalPlan && (
        <div
          style={{
            marginTop: "24px",
            padding: "16px",
            border: "1px solid #ccc",
          }}
        >
          <p style={{ color: "blue" }}>
            showFinalPlan = {String(showFinalPlan)}
          </p>
          
          <h2>Final Plan</h2>

          {loading && <p>Loading weekly plan...</p>}

          {error && <p style={{ color: "red" }}>{error}</p>}

          {!loading && !error && weeklyPlan && (
            <pre
              style={{
                whiteSpace: "pre-wrap",
                background: "#f7f7f7",
                padding: "12px",
              }}
            >
              {weeklyPlan}
            </pre>
          )}

          {/* -----------------------
              Weekly Todos
             ----------------------- */}
          {weeklyTodos && (
            <div style={{ marginTop: "24px" }}>
              <h2>Weekly Todos</h2>

              {weeklyTodos.days.map((day, dayIndex) => (
                <div
                  key={day.date}
                  style={{
                    marginBottom: "16px",
                    paddingBottom: "8px",
                    borderBottom: "1px solid #eee",
                  }}
                >
                  <h3>{day.date}</h3>

                  {day.todos.length === 0 && (
                    <p style={{ color: "#888" }}>No todos</p>
                  )}

                  {day.todos.map((todo) => (
                    <div
                      key={todo.id}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                        marginBottom: "6px",
                      }}
                    >
                      <span
                        style={{
                          flex: 1,
                          textDecoration:
                            todo.status === "done"
                              ? "line-through"
                              : "none",
                          color:
                            todo.status === "done"
                              ? "#999"
                              : "inherit",
                        }}
                      >
                        {todo.task}
                      </span>

                      <button
                        onClick={() =>
                          updateTodoStatus(
                            dayIndex,
                            todo.id,
                            "done"
                          )
                        }
                      >
                        ✅
                      </button>
                      <button
                        onClick={() =>
                          updateTodoStatus(
                            dayIndex,
                            todo.id,
                            "partial"
                          )
                        }
                      >
                        ½
                      </button>
                      <button
                        onClick={() =>
                          updateTodoStatus(
                            dayIndex,
                            todo.id,
                            "postponed"
                          )
                        }
                      >
                        🔜
                      </button>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
