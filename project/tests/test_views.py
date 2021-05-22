""" Unittests for views api module """
import unittest
from project.tests import UnittestSetup


class ViewsTest(UnittestSetup, unittest.TestCase):

    def test_departments(self):
        """ Test that index page is returned correctly """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_department(self):
        """ Test that department page is returned correctly """
        response = self.client.get('/department/Marketing')
        self.assertEqual(response.status_code, 200)

    def test_employees(self):
        """ Test that employees page is returned correctly """
        response = self.client.get('/employees')
        self.assertEqual(response.status_code, 200)

    def test_employee(self):
        """ Test that employee page is returned correctly """
        response = self.client.get('/employee/1')
        self.assertEqual(response.status_code, 200)

    def test_404(self):
        """ Test that 404 error is raised and custom error page is returned"""
        response = self.client.get('/department/Does not exist')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page not found', str(response.data))
