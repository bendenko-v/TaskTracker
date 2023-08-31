from src.models import EmployeeModel


def test_get_employee_by_id(client, get_test_session):
    employee = EmployeeModel(
        name='John',
        job='engineer',
    )
    get_test_session.add(employee)
    get_test_session.commit()
    response = client.get('/employee/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'John', 'job': 'engineer'}
