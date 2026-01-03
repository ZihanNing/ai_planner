from pydantic import BaseModel
from typing import Literal


class WeeklyReviewRequest(BaseModel):
    capacity: Literal["low", "medium", "high"]
