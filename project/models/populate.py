"""
Populate App Database

Functions:

    drop_data() -> None
    populate_departments(limit: int = 14) -> None
    populate_departments(limit: int = 14) -> None
    main() -> None
"""
import random
import logging
import argparse

logging.basicConfig(level=logging.DEBUG, filename='app.log', format='%(name)s:%(levelname)s:%(message)s')

from faker import Faker

from project import db
from project.models import Department, Employee


def drop_data() -> None:
    """
    Drop Data from the Tables.

    Raises:
        SQLAlchemy Exception : May raise when error occurs while working with the DB.
    """
    try:
        Department.query.delete()
        Employee.query.delete()
        db.session.commit()

    except Exception as err:
        logging.error('Couldn\'t delete Data from the Database: {}'.format(str(err)))
        db.session.rollback()


def populate_departments(limit: int = 14) -> None:
    """
    Populates 'Department' Table

    Parameters:
        limit (int): Max number of departments

    Returns:
        None
    """
    logging.info('Populating Departments Database')

    department_names = ['General Management', 'Marketing', 'Operations',
                        'Finance', 'Sales', 'Human Resource', 'Purchase',
                        'Training', 'Development', 'Test Team', 'Architecture',
                        'Customer Support', 'Public relations', 'Research']

    for name in department_names[:limit]:
        department = Department(name=name)
        db.session.add(department)
    db.session.commit()

    logging.info('Successfully populated Departments Database')


def populate_employees(limit: int = 10) -> None:
    """
    Populates 'Employees' Table

    Parameters:
        limit (int): Max number of employees per department

    Returns:
        None
    """
    logging.info('Populating Employees Database')

    Faker.seed(42)
    faker = Faker()

    departments = Department.query.all()
    for department in departments:
        for _ in range(random.randint(1, limit)):
            employee = Employee(
                department_id=department.id,
                name=faker.name(),
                birthdate=faker.date_between(start_date='-50y', end_date='-18y').strftime('%m.%d.%Y'),
                salary=random.randint(700, 2000)
            )
            db.session.add(employee)
    db.session.commit()

    logging.info('Successfully populated Employees Database')


def main() -> None:
    """ Main function that runs when the Script is called from the Console """
    parser = argparse.ArgumentParser(description='A Script to populate App '
                                                 'Database with the test Data.')
    parser.add_argument('-d', '--drop', help='Drop Data from the Tables.',
                        action='store_true')
    parser.add_argument('-ld', '--limit-departments', default=14,
                        help='Limit Number of Departments', type=int)
    parser.add_argument('-le', '--limit-employees', default=10,
                        help='Limit Number of Employees per Department', type=int)
    args = parser.parse_args()

    if args.drop:
        drop_data()

    populate_departments(args.limit_departments)
    populate_employees(args.limit_employees)


if __name__ == '__main__':
    main()
