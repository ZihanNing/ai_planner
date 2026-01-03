from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.state_io import load_state, save_state
from backend.schemas import ProjectUpdate, NewProject, WeeklyReviewRequest

# for API: step 2, to generate the state_preprocessed.json via API
from backend.analyzer import analyze_projects_stub

# plan my week: reserve for API (final generation/plan)
from backend.planner import plan_week_stub

# related to React (to interact with the frontend)
from pathlib import Path

# to read the todos (and to show on the frontend - react)
from fastapi import Body
import json



app = FastAPI(
    title="AI Planner Backend",
    version="0.2.0",
    description="Backend service for project state management and weekly planning"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# ---------------------------------------------------------------------
# CORS (for local frontend development)
# ---------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # local development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------
# Basic health checks
# ---------------------------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "AI Planner backend is running"}


@app.get("/health")
def health():
    return {"health": "green"}

# ---------------------------------------------------------------------
# Project state APIs (state.json as SSOT)
# ---------------------------------------------------------------------
@app.get("/projects")
def get_projects():
    """
    Get all projects from state.json
    """
    state = load_state()
    return state.get("projects", [])


@app.patch("/projects/{project_id}")
def update_project(project_id: str, update: ProjectUpdate):
    """
    Update an existing project (human-editable fields only)
    """
    state = load_state()
    projects = state.get("projects", [])

    for proj in projects:
        if proj.get("id") == project_id:
            updates = update.dict(exclude_unset=True)
            for key, value in updates.items():
                proj[key] = value

            save_state(state)
            return {"success": True, "project": proj}

    raise HTTPException(status_code=404, detail="Project not found")


@app.post("/projects")
def add_project(new_project: NewProject):
    """
    Add a new project to state.json
    """
    state = load_state()
    projects = state.get("projects", [])

    if any(p.get("id") == new_project.id for p in projects):
        raise HTTPException(status_code=400, detail="Project id already exists")

    projects.append(new_project.dict())
    save_state(state)

    return {"success": True, "project": new_project}

@app.delete("/projects/{project_id}")
def delete_project(project_id: str):
    """
    Delete a project from state.json
    """
    state = load_state()
    projects = state.get("projects", [])

    new_projects = [p for p in projects if p.get("id") != project_id]

    if len(new_projects) == len(projects):
        raise HTTPException(status_code=404, detail="Project not found")

    state["projects"] = new_projects
    save_state(state)

    return {"success": True, "deleted_project": project_id}

# ---------------------------------------------------------------------
# Project state APIs (to generate state_preprocessed.json)
# ---------------------------------------------------------------------
@app.post("/analyze-projects")
def analyze_projects():
    """
    Analyze projects based on state.json and status_preprocessing_prompt.

    Current implementation:
    - DOES NOT call AI
    - Assumes state_preprocessed.json is manually generated
    - Only validates and loads the preprocessed result
    """
    try:
        summary = analyze_projects_stub()
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "success": True,
        "message": "State preprocessing completed (manual)",
        "summary": summary
    }

# ---------------------------------------------------------------------
# Project state APIs (final plan the week: API outputs)
# ---------------------------------------------------------------------
@app.post("/plan-week")
def plan_week():
    """
    Generate weekly plan based on preprocessed state and calendar.

    Current implementation:
    - No AI
    - Reads manually prepared weekly_plan.md and weekly_todos.json
    """
    try:
        summary = plan_week_stub()
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "success": True,
        "message": "Weekly plan generated (manual)",
        "summary": summary
    }

# ---------------------------------------------------------------------
# Read weekly_plan.md to frontend
# ---------------------------------------------------------------------
@app.get("/api/final-plan/plan")
def get_weekly_plan():
    plan_path = DATA_DIR / "weekly_plan.md"

    if not plan_path.exists():
        return {"error": "weekly_plan.md not found"}

    content = plan_path.read_text(encoding="utf-8")
    return {"content": content}

# ---------------------------------------------------------------------
# Read weekly_todos.md to frontend/React
# ---------------------------------------------------------------------
@app.get("/api/final-plan/todos")
def get_weekly_todos():
    todos_path = DATA_DIR / "weekly_todos.json"

    if not todos_path.exists():
        return {"error": "weekly_todos.json not found"}

    return json.loads(todos_path.read_text(encoding="utf-8"))

# ---------------------------------------------------------------------
# POST todos
# ---------------------------------------------------------------------
@app.post("/api/final-plan/todos")
def update_weekly_todos(payload: dict = Body(...)):
    todos_path = DATA_DIR / "weekly_todos.json"

    todos_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return {"status": "ok"}

