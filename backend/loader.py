import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_weekly_todos(filename: str = "weekly_todos.json"):
    """
    Safely load weekly todos from data directory.
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Weekly todos file not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in {file_path}: {e}")

    if "todos" not in data or not isinstance(data["todos"], list):
        raise ValueError("weekly_todos.json must contain a list field: 'todos'")

    return data["todos"]