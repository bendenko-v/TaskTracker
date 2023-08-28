from fastapi import HTTPException

from src.models import EmployeeModel, StatusEnum, TasksModel
from src.schemas import TaskImportantScheme, TaskScheme


async def get_important_tasks_service(
    important_tasks: list[TasksModel | None],
    employees: list[tuple[EmployeeModel, ...] | None],
) -> list[TaskImportantScheme | None]:
    if not important_tasks:
        raise HTTPException(status_code=404, detail='Tasks not found')

    if not employees:
        raise HTTPException(status_code=404, detail='Employees not found')

    tasks_data = {t.parent_id: t.id for t in important_tasks}
    emp_data = {
        emp.id: {
            'employee': emp,
            'tasks': [t.id for t in emp.tasks if t.status == StatusEnum.doing],
            'active_tasks': active_tasks,
        }
        for emp, active_tasks in employees
    }

    employments_list = list(emp_data.values())
    potential_employees = {}

    for task_id in tasks_data:
        employments_list.sort(key=lambda emp: emp['active_tasks'])
        min_tasks = employments_list[0]['active_tasks']
        for employee_entry in employments_list:
            emp_id = employee_entry['employee'].id
            """
            If an employee has a parent task with a task_id that matches the given task,
            and the employee has no more than 2 additional active tasks compared to the
            least busy employee, then we add this employee to the list of potential_employees
            """
            if task_id in emp_data[emp_id]['tasks'] and emp_data[emp_id]['active_tasks'] - min_tasks <= 2:
                potential_employees[tasks_data[task_id]] = emp_data[emp_id]['employee']
                employee_entry['active_tasks'] += 1
                break
        """ If the employee hasn't been assigned, then we assign the least busy employee to this task. """
        if not potential_employees.get(tasks_data[task_id]) and employments_list:
            least_busy_employee = employments_list[0]['employee']
            potential_employees[tasks_data[task_id]] = least_busy_employee
            employments_list[0]['active_tasks'] += 1

    return [
        TaskImportantScheme(
            task=TaskScheme(**task.__dict__),
            deadline=task.deadline,
            employees=[potential_employees.get(task.id)],
        )
        for task in important_tasks
    ]
