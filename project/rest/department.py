"""
Module for creating endpoints for the '/department' part of rest api
"""
from typing import Tuple
from flask_restful import Resource, reqparse
from project import db
from project.models import Department, Employee


class AllDepartmentsAPI(Resource):
    """
    Endpoint for restoring all departments data

    Route
    -----
        /api/department/

    Allowed Methods
    ---------------
        - GET - returns a list of all departments
    """

    def get(self) -> Tuple[dict, int]:
        """ returns a list of all departments """
        depts = {'departments': []}

        for dept in Department.query.all():
            depts['departments'].append(dept.json())

        return depts, 200


class DepartmentAPI(Resource):
    """
    Endpoint for working with department data

    Route
    -----
        /api/department/<string:name>

    Allowed Methods
    ---------------
        - GET - returns data about department from db
        - POST - creates new department
        - PUT - changes data related to an existing
                department or creates a new one
        - DELETE - removes department from db
    """

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='New Name of the Department.')

    def get(self, name: str) -> Tuple[dict, int]:
        """ returns data about department from db """
        dept = Department.query.filter_by(name=name).first()

        if dept:
            return dept.json(), 200

        return {'message': 'department with name \'{}\' does not exist'.format(name)}, 404

    def post(self, name: str) -> Tuple[dict, int]:
        """ creates new department """
        if Department.query.filter_by(name=name).first():
            return {'message': 'department with name \'{}\' already exists'.format(name)}, 400

        dept = Department(name=name)
        db.session.add(dept)
        db.session.commit()

        return dept.json(), 201

    def put(self, name: str) -> Tuple[dict, int]:
        """ changes data related to an existing department or creates a new one """
        dept = Department.query.filter_by(name=name).first()

        if not dept:
            return self.post(name)

        data = DepartmentAPI.parser.parse_args()
        if Department.query.filter_by(name=data['name']).first():
            return {'message': 'department with name \'{}\''
                               'already exists'.format(data['name'])}, 400

        dept.name = data['name']
        db.session.commit()
        return dept.json(), 200

    def delete(self, name: str) -> Tuple[dict, int]:
        """ removes department from db """
        dept = Department.query.filter_by(name=name).first()

        if not dept:
            return {'message': 'department with name \'{}\' does not exist'.format(name)}, 404

        db.session.delete(dept)
        db.session.commit()
        return {'message': 'department \'{}\' successfully removed'.format(name)}, 200


class DepartmentEmployeesAPI(Resource):
    """
    Endpoint for getting list of employees of department

    Route
    -----
        /api/department/<string:name>/employees

    Allowed Methods
    ---------------
        - GET - returns a list of employees of department
    """

    def get(self, name: str) -> Tuple[dict, int]:
        """ returns a list of employees of department """
        dept = Department.query.filter_by(name=name).first()

        if not dept:
            return {'message': 'department with name \'{}\' does not exist'.format(name)}, 404

        employees = Employee.query.filter_by(department_id=dept.id)
        return {'department': dept.json(),
                'employees': [empl.json() for empl in employees]}, 200

