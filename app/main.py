from fastapi import FastAPI
from app.api.routers import syllabus, manim

app = FastAPI(title="BaseLife Pipeline API")

# routers
app.include_router(syllabus.router, prefix="/syllabus", tags=["Syllabus"])
app.include_router(manim.router, prefix="/manim", tags=["Manim"])
