from pydantic import BaseModel, Field


class TaskSummary(BaseModel):
    title: str = Field(description="Short title for the user's task")
    summary: str = Field(description="One or two sentence summary")
    priority: str = Field(description="One of: low, medium, high")
    next_steps: list[str] = Field(default_factory=list)
