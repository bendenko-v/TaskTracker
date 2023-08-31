# TaskTrackerAPI

TaskTracker API is a FastAPI-based REST API for managing tasks and employees within a task tracking system.
It leverages SQLAlchemy for database operations and Pydantic for data validation.

## Project Structure

- `src/main.py`: Main FastAPI application file where the app is created and routers are connected.
- `src/database.py`: Configuration of connection to the database (PostgreSQL).
- `src/congig.py`: Congiguration of the application and database settings.
- `src/api/`: API endpoints
- `src/crud/`: CRUD operations
- `src/models/`: Data models
- `src/schemas/`: Pydantic schemas
- `src/services/`: Business logic

## Installation

1. Clone the repository: `git clone git@github.com:bendenko-v/TaskTracker.git`
2. Navigate to the project directory: `cd TaskTracker`
3. Install dependencies using Poetry: `poetry install`

## Usage

1. Create `.env` file: Copy the contents of `.env_example` to a new `.env` file in the project root directory. Adjust
   the variables according to your environment settings.

    ```bash
    cp .env_example .env
    ```
2. Run Postgres database with the following command:
    ```bash
    docker-compose up -d
   ```
3. Make migrations: Apply database migrations using Alembic to set up the database schema. Run the following
   command:
    ```bash
    alembic upgrade head
    ```
4. Run the FastAPI application:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

## Endpoints

- `/employee`, `/employee/{employee_id}`: Create/Read/Update Employees
- `/tasks`, `/tasks/{task_id}`: Create/Read/Update Tasks
- `/employee/busiest`: Busiest Employees
- `/tasks/important`: Important tasks and employees who can take them (less busy employee or employee who have a parent
  task and no more than 2 tasks than a less busy employee)

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Poetry](https://python-poetry.org/)
