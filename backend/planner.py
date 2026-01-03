import json
from pathlib import Path
from typing import Dict, Any

STATE_PREPROCESSED = Path("data/state_preprocessed.json")
CALENDAR = Path("data/calendar.json")
PLAN_PROMPT = Path("weekly_planner_prompt.md")

WEEKLY_PLAN_MD = Path("data/weekly_plan.md")
WEEKLY_TODOS = Path("data/weekly_todos.json")


def plan_week_stub() -> Dict[str, Any]:
    """
    Stub implementation:
    - No AI call
    - Assumes weekly_plan.md and weekly_todos.json
      are manually generated
    """

    for p in [STATE_PREPROCESSED, CALENDAR, PLAN_PROMPT]:
        if not p.exists():
            raise FileNotFoundError(f"Missing required input: {p}")

    for p in [WEEKLY_PLAN_MD, WEEKLY_TODOS]:
        if not p.exists():
            raise FileNotFoundError(f"Missing output file: {p}")

    with WEEKLY_TODOS.open("r", encoding="utf-8") as f:
        todos = json.load(f)

    return {
        "days": len(todos.get("days", [])),
        "projects": list(todos.get("projects", {}).keys())
    }
