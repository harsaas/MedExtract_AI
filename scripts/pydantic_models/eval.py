from pydantic import BaseModel, Field

class Metrics(BaseModel):
    accuracy: float = Field(
        description="Score 0.0-1.0: Does the extracted data match the facts in the source?",
        ge=0, le=1
    )
    faithfulness: float = Field(
        description="Score 0.0-1.0: Is the data grounded ONLY in the source (no hallucinations)?",
        ge=0, le=1
    )
    reasoning: str = Field(
        description="Detailed explanation of why these specific scores were given"
    )