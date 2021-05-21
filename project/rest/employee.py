"""
Module for creating endpoints for the '/employee' part of rest api
"""
from datetime import datetime
from typing import Tuple
from flask import request
from flask_restful import Resource, reqparse
from project import db, logger
from project.models import Department, Employee


class AllEmployeesAPI(Resource):
    """
    Endpoint for getting list of existing employees or creating a new one

    Route
    -----
        /api/employee/

    Allowed Methods
    ---------------
        - GET - returns a list of existing employees
        - POST - create new user
    """

    def get(self) -> Tuple[dict, int]:
        """ returns a list of existing employees """
        employees = [employee.json() for employee in Employee.query.order_by(Employee.id.desc()).all()]
        logger.debug('Returning the list of all Employees')
        return {'employees': employees}, 200

    def post(self) -> Tuple[dict, int]:
        """ create new user """
        data = EmployeeAPI.parser.parse_args()
        message, status_code = EmployeeAPI.validate_args(data)
        if status_code != 200:
            return {'message': message}, status_code

        department = Department.query.filter_by(name=data['department']).first()
        employee = Employee(department_id=department.id,
                            name=data['name'],
                            birthdate=data['birthdate'],
                            salary=data['salary'])
        db.session.add(employee)
        db.session.commit()

        data['id'] = employee.id
        logger.debug('New Employee created')
        return data, 201


class EmployeeAPI(Resource):
    """
    Endpoint for working with employee data

    Route
    -----
        /api/employee/<int:id>

    Allowed Methods
    ---------------
        - GET - returns data about employee from db
        - PUT - changes data related to an existing user
        - DELETE - removes employee from db
    """

    parser = reqparse.RequestParser()
    parser.add_argument('department',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')
    parser.add_argument('name',
                        type=str,
                        required=True)
    parser.add_argument('birthdate',
                        type=str,
                        required=True)
    parser.add_argument('salary',
                        type=int,
                        required=True)

    @staticmethod
    def validate_args(data) -> Tuple[str, int]:
        """ Static method for validating input data """

        if 'salary' in data.keys():
            if not isinstance(data['salary'], int) and not data['salary'].isnumeric():
                return 'salary has to be a number', 400

        if 'birthdate' in data.keys():
            try:
                datetime.strptime(data['birthdate'], '%m.%d.%Y')
            except ValueError:
                return "time data '{}' does not match format " \
                       "'%m.%d.%Y'".format(data['birthdate']), 400

        if 'department' in data.keys() and not Department.query.filter_by(name=data['department']).first():
            return 'department with name \'{}\' does not exist'.format(data['department']), 400

        return '', 200

    def get(self, pk: int) -> Tuple[dict, int]:
        """ returns data about employee from db """
        employee = Employee.query.filter_by(id=pk).first()

        if employee:
            logger.debug('Returning Employee Data')
            return employee.json(), 200

        return {'message': 'employee with id {} not found'.format(pk)}, 404

    def put(self, pk: int) -> Tuple[dict, int]:
        """ changes data related to an existing user """
        data = request.get_json()

        if Employee.query.filter_by(id=pk).first():
            message, status_code = EmployeeAPI.validate_args(data)
            if status_code != 200:
                return {'message': message}, status_code

            if 'department' in data.keys():
                department = Department.query.filter_by(name=data['department']).first()
                data['department_id'] = department.id
                data.pop('department', None)

            employee = Employee.query.filter_by(id=pk)
            employee.update(data)
            db.session.commit()
            logger.debug('Updated Employee Data')
            return employee.first().json(), 200

        return {'message': 'employee with id {} not found'.format(pk)}, 404

    def delete(self, pk: int) -> Tuple[dict, int]:
        """ removes employee from db """
        employee = Employee.query.filter_by(id=pk).first()
        if not employee:
            return {'message': 'employee with id {} does not exist'.format(pk)}, 404

        db.session.delete(employee)
        db.session.commit()
        logger.debug('Employee removed')
        return {'message': 'employee with id {} successfully removed'.format(pk)}, 200
