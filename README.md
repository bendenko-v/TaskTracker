# TaskTrackerAPI

TaskTracker API is a FastAPI-based REST API for managing tasks and employees within a task tracking system.
It leverages SQLAlchemy for database operations and Pydantic for data validation.

## Project Structure ![Status](https://img.shields.io/badge/Status-InProgress-yellow)

- `src/main.py`: Main FastAPI application file where the app is created and routers are connected.
- `src/database.py`: Configuration of connection to the database (PostgreSQL).
- `src/congig.py`: Congiguration of the application and database settings.
- `src/tasks/...`: *files related to "Tasks"*
    - `crud.py`: Defines DAO for CRUD operations.
    - `models.py`: Defines data models.
    - `schemas.py`: Defines pydantic schemas.
    - `router.py`: Defines routes and implementation of endpoints.
- `src/employee/...`: *files related to "Employee"*
    - `crud.py`: Defines DAO for CRUD operations.
    - `models.py`: Defines data models.
    - `schemas.py`: Defines pydantic schemas.
    - `router.py`: Defines routes and implementation of endpoints.


## Installation

1. Clone the repository: `git clone git@github.com:bendenko-v/TaskTracker.git`
2. Navigate to the project directory: `cd TaskTracker`
3. Install dependencies using Poetry: `poetry install`


## Usage

1. Make sure you have PostgreSQL installed and running (`docker-compose up -d` to run db in my example)
2. Configure the database connection in `database.py` and required variables in `.env`.
3. Run the FastAPI application: `poetry run uvicorn app:app --host 0.0.0.0 --port 8000`


## Endpoints 


- CRUD Employees: `/employee`, `/employee/{employee_id}`
- CRUD Tasks: `/tasks`, `/tasks/{task_id}`
- Busy Employees: `/busiest-employee`
- Important Tasks: `/important-tasks` ![Status](https://img.shields.io/badge/Status-InProgress-yellow)


## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) 
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Poetry](https://python-poetry.org/)


