""""
Package for defining project views
"""
from flask import Blueprint, render_template
from project.models import Department, Employee

core = Blueprint('core', __name__)


@core.route('/')
def departments():
    """ Index page with a list of all the departments """
    return render_template('departments.html')


@core.route('/department/<string:name>')
def department(name):
    """ Department page for changing department data and viewing list of workers """
    return render_template('department.html',
                           department=name)


@core.route('/employees')
def employees():
    """ Page with a list of all the employees """
    return render_template('employees.html')


@core.route('/employee/<int:pk>')
def employee(pk):
    """ Employee page for viewing and changing employee data """
    employee_ = Employee.query.get_or_404(pk)
    return render_template('employee.html',
                           employee=employee_)
