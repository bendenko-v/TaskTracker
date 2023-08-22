from fastapi import FastAPI

from src.config import settings
from src.tasks.router import tasks_router, important_tasks_router
from src.employee.router import employees_router, special_router

app = FastAPI(
    title=settings.title,
    description=settings.project_description,
    version=settings.project_version,
)

app.include_router(tasks_router)
app.include_router(employees_router)
app.include_router(special_router)
app.include_router(important_tasks_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
