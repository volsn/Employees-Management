""" Unittests for models module """
import unittest
from project.tests import UnittestSetup
from project.models import Department, Employee
from project.models.populate import drop_data


class ModelsTest(UnittestSetup, unittest.TestCase):
    """ Unittests for the models module """

    def test_departments_created(self):
        """ Verify that 'department' table has been populated """
        self.assertEqual(len(Department.query.all()), 14)

    def test_employees_created(self):
        """ Verify that 'employee' table has been populated """
        self.assertNotEqual(len(Employee.query.all()), 0)

    def test_drop_data(self):
        """ Test that drop_data function drops all tables' data """
        drop_data()
        self.assertEqual(len(Department.query.all()), 0)
        self.assertEqual(len(Employee.query.all()), 0)
