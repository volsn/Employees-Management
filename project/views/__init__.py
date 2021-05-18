from flask import Blueprint, render_template
from project.models import Department, Employee

core = Blueprint('core', __name__)


@core.route('/')
def departments():
    return render_template('departments.html')


@core.route('/department/<string:name>')
def department(name):
    return render_template('department.html',
                           department=name)


@core.route('/employees')
def employees():
    return render_template('employees.html')


@core.route('/employee/<int:pk>')
def employee(pk):
    employee_ = Employee.query.get_or_404(pk)
    return render_template('employee.html',
                           employee=employee_)
