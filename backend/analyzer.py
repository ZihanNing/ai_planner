import json
from pathlib import Path
from typing import Dict, Any

STATE_PATH = Path("data/state.json")
PREPROCESSED_PATH = Path("data/state_preprocessed.json")


def load_state() -> Dict[str, Any]:
    with STATE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_preprocessed_state() -> Dict[str, Any]:
    if not PREPROCESSED_PATH.exists():
        raise FileNotFoundError("state_preprocessed.json not found")

    with PREPROCESSED_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def analyze_projects_stub() -> Dict[str, Any]:
    """
    Temporary stub:
    - No API call
    - Simply checks that state_preprocessed.json exists and is readable
    """
    state = load_state()
    preprocessed = load_preprocessed_state()

    return {
        "project_count": len(state.get("projects", [])),
        "preprocessed_keys": list(preprocessed.keys()),
    }
