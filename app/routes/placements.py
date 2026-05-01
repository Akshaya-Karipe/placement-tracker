from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.placement import Placement
from app.schemas.placement import PlacementCreate, PlacementUpdate, PlacementOut
from app.auth import get_current_user
from app.models.user import User
import csv, io

router = APIRouter(prefix="/placements", tags=["Placements"])

@router.post("/", response_model=PlacementOut)
def create_placement(data: PlacementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    placement = Placement(**data.dict(), owner_id=current_user.id)
    db.add(placement)
    db.commit()
    db.refresh(placement)
    return placement

@router.get("/", response_model=List[PlacementOut])
def get_placements(
    company: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Placement).filter(Placement.owner_id == current_user.id)
    if company:
        query = query.filter(Placement.company.ilike(f"%{company}%"))
    if status:
        query = query.filter(Placement.status == status)
    return query.all()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    placements = db.query(Placement).filter(Placement.owner_id == current_user.id).all()
    total = len(placements)
    offered = sum(1 for p in placements if p.status == "Offered")
    avg_package = round(sum(p.package_lpa for p in placements) / total, 2) if total else 0
    return {"total": total, "offered": offered, "avg_package_lpa": avg_package}

@router.put("/{placement_id}", response_model=PlacementOut)
def update_placement(placement_id: int, data: PlacementUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    placement = db.query(Placement).filter(Placement.id == placement_id, Placement.owner_id == current_user.id).first()
    if not placement:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(placement, key, value)
    db.commit()
    db.refresh(placement)
    return placement

@router.delete("/{placement_id}")
def delete_placement(placement_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    placement = db.query(Placement).filter(Placement.id == placement_id, Placement.owner_id == current_user.id).first()
    if not placement:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(placement)
    db.commit()
    return {"message": "Deleted successfully"}

@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    placements = db.query(Placement).filter(Placement.owner_id == current_user.id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Student Name", "Company", "Role", "Package (LPA)", "Status", "Year"])
    for p in placements:
        writer.writerow([p.id, p.student_name, p.company, p.role, p.package_lpa, p.status, p.year])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=placements.csv"})