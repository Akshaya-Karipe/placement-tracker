from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Placement(Base):
    __tablename__ = "placements"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    package_lpa = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))