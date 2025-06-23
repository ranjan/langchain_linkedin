from pydantic import BaseModel, Field
from typing import List

class Summary(BaseModel):
    summary: str = Field(description="summary about the person")
    facts: List[str] = Field(description="interesting facts about them")
