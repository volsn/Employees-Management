import os
import re
from datetime import datetime
from typing import Tuple
from flask import request
from flask_restful import Resource, reqparse
from project import db
from project.models import Department, Employee


class AllDepartmentsAPI(Resource):
    def get(self) -> Tuple[dict, int]:
        depts = {'departments': []}

        for dept in Department.query.all():
            depts['departments'].append(dept.json())

        return depts, 200


class DepartmentAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='New Name of the Department.')

    def get(self, name: str) -> Tuple[dict, int]:
        dept = Department.query.filter_by(name=name).first()

        if dept:
            return dept.json(), 200

        return {'message': 'department with name \'{}\' does not exist'.format(name)}, 404

    def post(self, name: str) -> Tuple[dict, int]:
        if Department.query.filter_by(name=name).first():
            return {'message': 'department with name \'{}\' already exists'.format(name)}, 400

        dept = Department(name=name)
        db.session.add(dept)
        db.session.commit()

        return dept.json(), 201

    def put(self, name: str) -> Tuple[dict, int]:
        dept = Department.query.filter_by(name=name).first()

        if not dept:
            return self.post(name)

        data = DepartmentAPI.parser.parse_args()
        if Department.query.filter_by(name=data['name']).first():
            return {'message': 'department with name \'{}\' already exists'.format(data['name'])}, 400

        dept.name = data['name']
        db.session.commit()
        return dept.json(), 200

    def delete(self, name: str) -> Tuple[dict, int]:
        dept = Department.query.filter_by(name=name).first()

        if not dept:
            return {'message': 'department with name \'{}\' does not exist'.format(name)}, 404

        db.session.delete(dept)
        db.session.commit()
        return {'message': 'department \'{}\' successfully removed'.format(name)}, 200


class DepartmentEmployeesAPI(Resource):

    def get(self, name: str) -> Tuple[dict, int]:
        dept = Department.query.filter_by(name=name).first()

        if not dept:
            return {'message': 'department with name \'{}\' does not exist'.format(name)}, 404

        employees = Employee.query.filter_by(department_id=dept.id)
        return {'department': dept.json(),
                'employees': [empl.json() for empl in employees]}, 200


class AllEmployeesAPI(Resource):

    def get(self) -> Tuple[dict, int]:
        employees = [employee.json() for employee in Employee.query.all()]
        return {'employees': employees}, 200

    def post(self) -> Tuple[dict, int]:
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
        return data, 201


class EmployeeAPI(Resource):

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
        if 'birthdate' in data.keys():
            try:
                datetime.strptime(data['birthdate'], '%m.%d.%Y')
            except ValueError:
                return "time data '{}' does not match format '%m.%d.%Y'".format(data['birthdate']), 400

        if 'department' in data.keys() and not Department.query.filter_by(name=data['department']).first():
            return 'department with name \'{}\' does not exist'.format(data['department']), 400

        return '', 200

    def get(self, pk: int) -> Tuple[dict, int]:
        employee = Employee.query.filter_by(id=pk).first()

        if employee:
            return employee.json(), 200

        return {'message': 'employee with id {} not found'.format(pk)}, 404

    def put(self, pk: int) -> Tuple[dict, int]:
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
            return employee.first().json(), 200
        else:
            return {'message': 'employee with id {} not found'.format(pk)}, 404

        """
        else:
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
            return data, 201
        """

    def delete(self, pk: int) -> Tuple[dict, int]:
        employee = Employee.query.filter_by(id=pk).first()
        if not employee:
            return {'message': 'employee with id {} does not exist'.format(pk)}, 404

        db.session.delete(employee)
        db.session.commit()
        return {'message': 'employee with id {} successfully removed'.format(pk)}, 200
