import json
from pathlib import Path
from typing import Dict, Any

STATE_PATH = Path("data/state.json")


def load_state() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        raise FileNotFoundError("state.json not found")

    with STATE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: Dict[str, Any]) -> None:
    # basic safety check
    if "projects" not in state:
        raise ValueError("Invalid state format: missing 'projects'")

    with STATE_PATH.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
