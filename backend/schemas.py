from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal


# ---------------------------------------------------------------------
# Project-related schemas (state.json human-editable layer)
# ---------------------------------------------------------------------

class ProjectUpdate(BaseModel):
    """
    Fields that are allowed to be updated by human / frontend.
    All fields are optional to support PATCH semantics.
    """
    status: Optional[str] = Field(
        None, description="Project status, e.g. active / inactive / done"
    )
    status_reason: Optional[str] = Field(
        None, description="Short reason explaining current status"
    )
    notes: Optional[str] = Field(
        None, description="Free-form human notes"
    )
    narrative_input: Optional[Dict[str, Any]] = Field(
        None, description="Human narrative input for AI understanding"
    )


class NewProject(BaseModel):
    """
    Schema for creating a new project.
    Must provide all essential human-defined fields.
    """
    id: str = Field(
        ..., description="Unique project identifier (used as primary key)"
    )
    narrative_input: Dict[str, Any] = Field(
        ..., description="Human narrative description of the project"
    )
    user_confirmed: Dict[str, Any] = Field(
        ..., description="Explicit user confirmations / constraints"
    )
    status: str = Field(
        ..., description="Initial project status"
    )
    status_reason: Optional[str] = Field(
        None, description="Reason for initial status"
    )
    notes: Optional[str] = Field(
        None, description="Optional free-form notes"
    )


# ---------------------------------------------------------------------
# Weekly review / capacity input (temporary, transitional)
# ---------------------------------------------------------------------

class WeeklyReviewRequest(BaseModel):
    """
    Minimal input for weekly review.
    Todos are loaded internally from weekly_todos.json.
    """
    capacity: Literal["low", "medium", "high"] = Field(
        ..., description="Overall weekly capacity"
    )
