from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
from pathlib import Path
import tempfile
import os

from solver.solver import build_and_solve

app = FastAPI(title="Timetable Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Student(BaseModel):
    id: str
    name: str
    enrolled: List[str]

class Faculty(BaseModel):
    id: str
    name: str
    unavailable: Optional[List[int]] = []
    preferred: Optional[List[int]] = []
    max_hours: Optional[int] = None

class Course(BaseModel):
    id: str
    name: str
    faculty: str
    sessions_per_week: int

class TimetableRequest(BaseModel):
    students: List[Student]
    faculty: List[Faculty]
    courses: List[Course]
    days: List[str]
    periods_per_day: int

@app.get("/")
async def root():
    return {"message": "Timetable Generator API"}

@app.post("/generate")
async def generate_timetable(request: TimetableRequest):
    try:
        # Convert pydantic models to dict format expected by solver
        data = {
            "days": request.days,
            "periods_per_day": request.periods_per_day,
            "courses": [course.dict() for course in request.courses],
            "faculty": [fac.dict() for fac in request.faculty],
            "students": [student.dict() for student in request.students]
        }

        # Call the solver
        result = build_and_solve(data, time_limit_seconds=15)

        if result is None:
            raise HTTPException(status_code=400, detail="No feasible timetable could be generated")

        return {"success": True, "timetable": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating timetable: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)