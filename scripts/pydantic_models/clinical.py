from pydantic import BaseModel, Field
from typing import List


class Medication(BaseModel):
    name: str = Field(..., description="Name of the prescribed medication")
    dosage: str = Field(..., description="Dosage (e.g., 500mg)")
    frequency: str = Field(..., description="Frequency (e.g., twice daily)")


class ClinicalDiagnosis(BaseModel):
    condition: str = Field(..., description="The diagnosed medical condition")
    status: str = Field(..., description="Status (e.g., acute, chronic, resolved)")


class PatientEncounter(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier")
    summary: str = Field(..., description="Brief summary of the clinical encounter")
    diagnoses: List[ClinicalDiagnosis] = Field(default_factory=list)
    medications: List[Medication] = Field(default_factory=list)
    follow_up_needed: bool = Field(default=False)
