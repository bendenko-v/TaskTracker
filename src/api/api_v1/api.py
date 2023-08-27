from fastapi import APIRouter

from src.api.api_v1.endpoints import employee, task

api_router = APIRouter()
api_router.include_router(employee.router, prefix='/employee', tags=['employee'])
api_router.include_router(task.router, prefix='/tasks', tags=['tasks'])
