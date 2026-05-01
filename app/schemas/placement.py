from pydantic import BaseModel
from typing import Optional

class PlacementCreate(BaseModel):
    student_name: str
    company: str
    role: str
    package_lpa: float
    status: str
    year: int

class PlacementUpdate(BaseModel):
    student_name: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    package_lpa: Optional[float] = None
    status: Optional[str] = None
    year: Optional[int] = None

class PlacementOut(BaseModel):
    id: int
    student_name: str
    company: str
    role: str
    package_lpa: float
    status: str
    year: int
    owner_id: int

    class Config:
        from_attributes = True