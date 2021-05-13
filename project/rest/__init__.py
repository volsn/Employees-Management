"""
Package for creating endpoints for the rest api
"""
from .department import AllDepartmentsAPI, DepartmentAPI, DepartmentEmployeesAPI
from .employee import AllEmployeesAPI, EmployeeAPI


__all__ = [AllDepartmentsAPI, DepartmentAPI, DepartmentEmployeesAPI,
           AllEmployeesAPI, EmployeeAPI]
