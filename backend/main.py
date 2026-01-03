from fastapi import FastAPI
from backend.schemas import WeeklyReviewRequest
from backend.loader import load_weekly_todos

app = FastAPI(title="AI Planner Backend", version="0.1.0")


@app.get("/")
def root():
    return {"status": "ok", "message": "AI Planner backend is running"}


@app.get("/health")
def health():
    return {"health": "green"}


@app.post("/weekly-review")
def weekly_review(payload: WeeklyReviewRequest):
    """
    Weekly review endpoint.
    Todos are automatically loaded from data/weekly_todos.json.
    """
    todos = load_weekly_todos()

    completed = sum(1 for t in todos if t.get("checked") is True)

    return {
        "capacity": payload.capacity,
        "total_todos": len(todos),
        "completed_todos": completed,
        "todos": todos
    }
