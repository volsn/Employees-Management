"""
Package for creating and populating the database using SQLAlchemy ORM
"""
from datetime import datetime
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

    def __init__(self, department_id: int,  name: str, birthdate: datetime.date, salary: int) -> None:
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
        self.birthdate = birthdate
        self.salary = salary

    def __repr__(self):
        """
        Magic representation method of a class.

        Returns
        -------
            name : str
                name of the employee
        """
        return self.name
