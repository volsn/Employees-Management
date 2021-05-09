import os
import random
import logging
import argparse
from faker import Faker

from project import db, basedir
from project.models import Department, Employee


def drop_data():
    try:
        db.session.query(Department).delete()
        db.session.query(Employee).delete()
        db.session.commit()
    except:
        logging.error('Couldn\'t delete Data from the Database.')
        db.session.rollback()


def populate_departments(limit=14):
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


def populate_employees(max_limit_per_department=10):
    logging.info('Populating Employees Database')
    faker = Faker()
    departments = Department.query.all()
    for department in departments:
        for _ in range(random.randint(1, max_limit_per_department)):
            employee = Employee(
                department_id=department.id,
                name=faker.name(),
                birthdate=faker.date_between(start_date='-50y', end_date='-18y'),
                salary=random.randint(700, 2000)
            )
            db.session.add(employee)
    db.session.commit()
    logging.info('Successfully populated Employees Database')


if __name__ == '__main__':
    populate_departments()
    populate_employees()
