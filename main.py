from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, placements

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Placement Tracker", version="1.0")

app.include_router(auth.router)
app.include_router(placements.router)

@app.get("/")
def root():
    return {"message": "Placement Tracker API is running!"}