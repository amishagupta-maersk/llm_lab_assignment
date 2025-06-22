from pydantic import BaseModel, Field
from typing import List, Optional

class ResumeChecklist(BaseModel):
    first_name: str = Field(..., description="Candidate's first name")
    second_name: str = Field(..., description="Candidate's second name or family name")
    skills: List[str] = Field(..., description="Technical or professional skills listed")
    experience_years: int = Field(..., description="Total number of years of professional experience")
    education_level: str = Field(..., description="Highest education level attained (e.g. Bachelor's, Master's, PhD)")
    last_job_role: str = Field(..., description="Most recent or current job title mentioned in resume")
    salary_expectation: Optional[int] = Field(None, description="Salary expectation if explicitly mentioned (annual, USD)")
    projects_count: Optional[int] = Field(None, description="Number of distinct projects mentioned or led in resume")
