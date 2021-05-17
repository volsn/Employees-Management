"""
Package for creating and populating the database using SQLAlchemy ORM
"""
from datetime import datetime
from sqlalchemy.sql import func
from project import db


class Department(db.Model):
    """
    A class for ORM to create 'Department' Table

    Attributes
    ----------
    name : str
        name of the department

    Methods
    -------
        __init__(self, name: str) -> None:
            Constructor with all the necessary attributes of the object.
        __repr__(self) -> str:
            Magic representation method of a class.
    """

    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='department', passive_deletes=True)

    def __init__(self, name: str) -> None:
        """
        Constructor with all the necessary attributes of the object.

        Parameters
        ----------
            name : str
                name of the department. Has to be unique
        """
        self.name = name

    def json(self) -> dict:
        """
        Method that returns json representation of the object

        Returns
        -------
            json : dict
                department object data
        """
        return {'id': self.id, 'name': self.name,
                'num_employees': Employee.query.filter_by(department_id=self.id).count(),
                'avg_salary': int(Employee.query.with_entities(func.avg(Employee.salary))
                                  .filter_by(department_id=self.id)[0][0])}

    def __repr__(self) -> str:
        """
        Magic representation method of a class.

        Returns
        -------
            name : str
                name of the department
        """
        return self.name


class Employee(db.Model):
    """
    A class for ORM to create 'Department' Table

    Attributes
    ----------
    name : str
        name of the department

    Methods
    -------
    __init__(self, name: str) -> None:
        Constructor with all the necessary attributes of the object.
    __repr__(self) -> str:
        Magic representation method of a class.
    """

    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    birthdate = db.Column(db.DateTime)
    salary = db.Column(db.Integer)

    def __init__(self, department_id: int,  name: str, birthdate: str, salary: int) -> None:
        """
        Constructor with all the necessary attributes of the object.

        Parameters
        ----------
            department_id : int
                id of a department, where employee works. Used as a foreign key
            name : str
                name of the department. Has to be unique
            birthdate : datetime.date
                employee's date of birth
            salary : int
                employee's salary
        """
        self.department_id = department_id
        self.name = name
        self.birthdate = datetime.strptime(birthdate, '%m.%d.%Y')
        self.salary = salary

    def json(self) -> dict:
        """
        Method that returns json representation of the object

        Returns
        -------
            json : dict
                employee object data
        """
        department = Department.query.get(self.department_id)
        return {'id': self.id, 'name': self.name, 'department': department.name,
                'birthdate': self.birthdate.strftime('%m.%d.%Y'), 'salary': self.salary}

    def __repr__(self):
        """
        Magic representation method of a class.

        Returns
        -------
            name : str
                name of the employee
        """
        return self.name
