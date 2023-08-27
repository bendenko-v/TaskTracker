from fastapi import FastAPI

from src.api.api_v1.api import api_router
from src.config import settings

app = FastAPI(
    title=settings.title,
    description=settings.project_description,
    version=settings.project_version,
)

app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
